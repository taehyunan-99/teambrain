---
title: PostgreSQL 선택 (PostgreSQL Choice)
tags: [database, architecture, decision]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/slack/2024-10-30-db-connection-exhaustion.md
  - raw/2025-05-19-decision-mysql-failover-policy.md
  - raw/slack/2025-05-20-pay-dev-failover-inflight-tx.md
  - raw/transcripts/2026-02-10-tech-debt-review-transcript.md
  - raw/slack/2026-02-12-q1-replatform-mood.md
  - raw/slack/2026-04-02-for-update-deadlock.md
  - raw/2026-04-08-meeting-db-choice.md
  - raw/slack/2026-04-10-numeric-vs-bigint.md
  - raw/2026-04-29-decision-idempotency-db-unique.md
  - raw/pr/pr-136-db-migration-numeric.md
source_hashes:
  - f348851af70dee20c13f91de174abd2257c18c3e
  - 5101edd2700a6bb141f5bca216e2bed3321eecd2
  - 7b64c06674fbe8c9528e2c11f9cb72274bd378cf
  - d6d8c22b5750815970dcd4df162c266acc30c7e1
  - 7b756b1b7bbaf15f082f2cf8c5c1745f676ee78c
  - da31e98dc78383000cd0b059d948f68bf899c605
  - 61b549d07de5f05cb4d6ec5d25ba416a3cad1050
  - 9be4b50722a253612cfb6cb2c7b98029367b1e84
  - ffc1d104e7f604383e6dd36eced7eec0706f140b
  - 1086f41b308ff9f193e95949fce76cbe5d91b6e8
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 결제·정산 저장소로 PostgreSQL을 채택했다(2026-04-08). 이는 신규 그린필드 선택이 아니라 **기존 MySQL에서 Postgres로의 이주 결정**이다 — v1(2024)부터 MySQL을 주 트랜잭션 저장소로 써왔으나, 멱등성을 DB 레벨로 받치기 어려운 유니크/트랜잭션 한계가 누적돼 2026-Q1 기술부채 점검에서 리플랫폼 동기로 명시됐고(아래 "이주 결정의 경위"), 4/8 회의에서 Postgres로 결론냈다. 선택 근거는 강한 트랜잭션·유니크 제약·`ON CONFLICT` upsert가 멱등 처리에 핵심이고, 윈도우 함수·CTE가 정산 집계에 유리하기 때문이다.

## Details
- 후보 중 MongoDB는 약한 트랜잭션으로 탈락(개발 속도 이점보다 금액 필드 보호·유니크 제약이 결제에 필수 — 회의 전 슬랙 사전 논쟁 포함), MySQL도 가능했으나 Postgres의 `SELECT ... FOR UPDATE`·부분 인덱스·`ON CONFLICT`가 멱등 처리에 더 유리해 채택.
- 멱등성 유니크 제약과 `ON CONFLICT DO NOTHING`으로 중복 결제·중복 송금을 가드한다. ([[idempotency]])
- **금액 타입 `NUMERIC(19,4)`** (부동소수점 금지). 회의 후 BIGINT 원 단위 이견이 있었으나(4/10 슬랙) "수수료 3.3% 중간계산의 소수점 + 저장/계산 타입 분리 시 변환 버그 위험"으로 NUMERIC 유지 — KRW는 scale 0 운용, scale 4는 계산 여유분 + scale 변경 마이그레이션이 더 비싸다는 판단 (PR-136). ([[fee-calculation]])
- **운영 노하우:** `FOR UPDATE` 데드락은 락 획득 순서를 payment → ledger로 통일해 해결 (4/2). `pgcrypto`는 웹훅 시크릿 암호화 보관에도 사용. ([[webhook-delivery]])
- 이 선택은 멱등성 2중화 결정(DB 유니크가 최종 방어선)과 직접 맞물린다.

### 이주 결정의 경위 — MySQL 한계가 어떻게 Postgres 결정으로 이어졌나 (2026-Q1)
이 채택은 무에서 고른 게 아니라 **MySQL의 한계가 누적돼 갈아탄 이주**다. 인과 사슬:

- **2026-02-10 기술부채 점검:** 결제팀이 누적 부채를 한자리에 펼쳐 다섯을 식별했고(동기 직연동 / 멱등 Redis 단독 / **MySQL 한계** / 웹훅 재시도 부재 / 정산 수기), 그중 박서연이 "멱등을 DB 레벨로 한 번 더 받쳐주고 싶어도 지금 MySQL 구조로는 유니크 제약·트랜잭션 묶기가 깔끔하지 않고 금액 데이터 타입도 한계"라고 짚었다. 김도현이 "패치로 때우는 건 한계, 제대로 한 번 갈아엎는 그림이 필요"하다며 **다음 분기 아키텍처 재정비 공감대**를 확정(전원 동의). 이 자리에서 MySQL 한계가 리플랫폼 동기의 한 축으로 명시됐다.
- **2026-02-12 우선순위:** 회의 직후 잡담에서 박서연이 "갈아엎는다기보다 빚 갚는 것 — **멱등성과 DB부터**, 유니크 제약·트랜잭션 보장을 제대로 걸 수 있는 쪽으로"라고 방향을 못 박았다(Postgres를 사실상 가리킴). 최민지는 "결제 흐름 한복판이니 가맹점 영향 최소화·무중단"을 조건으로 달았다.
- **2026-04-08 결정:** 위 동기를 받아 후보 PostgreSQL/MySQL/MongoDB를 비교, "MySQL도 되지만 Postgres가 `FOR UPDATE`·부분 인덱스·`ON CONFLICT`로 멱등 처리에 더 유리"하다는 이유로 **Postgres 이주를 결론**(위 Details). 즉 4/8 회의의 "채택"은 2월에 합의된 이주 방향의 귀결이다.

### 전사(前史) — MySQL 시절의 결제 정합성 운영 (2024~2025)
이주 이전, Nimbus Pay의 주 트랜잭션 저장소는 MySQL이었다(결제·정산 모두, 금액 `DECIMAL`). 그 시기에 결제팀이 정한 운영 정책들은 DB 엔진이 바뀐 뒤에도 정합성 원칙으로 이어진다. (인프라팀 관점의 MySQL HA/백업/페일오버 운영은 [[mysql-ha-failover]]가 다루며, 여기서는 **결제 정합성 관점의 페일오버 정책(인플라이트 트랜잭션 처리)**에 한정한다.)

- **커넥션 고갈 사고 (2024-10-30):** 대형 가맹점 온보딩으로 트래픽이 5~6배 늘자 HikariPool 커넥션 풀이 고갈돼 승인 요청이 30초 타임아웃을 냈다. `maximumPoolSize 30 / connectionTimeout 5s / maxLifetime 30m`로 임시 튜닝해 복구. 근본 원인은 **동기 승인이 외부 PG 응답 대기 동안 커넥션을 점유하는 패턴** + 모니터링/알람 부재로 남았다(후자는 [[infra-baseline]]·[[oncall-and-alerting]]로, 전자는 비동기 승인 전환으로 이어짐). DB 운영 노하우의 출발점.
- **페일오버 정책 — 결제 정합성 관점 (2025-05-19):** 금전 트랜잭션 무손실을 위해 MySQL 프라이머리 자동 페일오버를 표준으로 정하되, **반동기 복제(semi-sync, RPO≈0)·헬스체크/펜싱·페일오버 윈도우 쓰기 거부**를 제약으로 두었다. 핵심은 "쓰기 실패 = 재시도 가능한 일시 오류로 간주, **클라이언트에 성공을 절대 반환하지 않는다**" — 불확실한 상태에서 쓰기를 받아 부분 커밋/모순을 만드느니 막는다는 [[fail-closed-principle]]의 DB 운영 적용이다.
- **인플라이트 트랜잭션 미아 방지 (2025-05-20):** 페일오버 윈도우에 PG 승인은 났는데 DB 기록이 막히면 "돈만 나가고 흔적 없는 미아 트랜잭션"이 생긴다. (1) `PENDING` INSERT → (2) PG approve → (3) `APPROVED` UPDATE 순서를 보장하면, 윈도우에 걸린 건은 PENDING으로 적체됐다가 **폴링 워커가 PG status 재조회로 보정**해 미아를 막는다. 이는 멱등성([[idempotency]]) 기반 안전 재시도와 직접 맞물린다.

## Related
- [[idempotency]] — DB 유니크 제약을 최종 방어선으로 쓰는 멱등성
- [[settlement-batch]] — 윈도우 함수·CTE로 처리하는 정산 집계
- [[fee-calculation]] — NUMERIC 유지의 근거가 된 수수료 소수점 계산
- [[webhook-delivery]] — pgcrypto 시크릿 보관
- [[mysql-ha-failover]] — 인프라 관점의 MySQL HA/백업/페일오버 운영(본 문서는 결제 정합성 관점)
- [[fail-closed-principle]] — 페일오버 윈도우 쓰기 거부의 안전 기본값
- [[infra-baseline]] — 커넥션 고갈을 드러낸 모니터링 부재의 출발점
