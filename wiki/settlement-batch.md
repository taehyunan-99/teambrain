---
title: 정산 배치 (Settlement Batch)
tags: [settlement, batch, architecture]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/2026-03-25-decision-settlement-batch.md
  - raw/2026-05-13-incident-settlement-double-payout.md
  - raw/pr/pr-125-settlement-aggregation.md
  - raw/pr/pr-151-payout-unique-guard.md
  - raw/pr/pr-153-batch-distributed-lock.md
  - raw/slack/2026-03-27-settlement-key-naming.md
  - raw/slack/2026-05-12-inc231-realtime.md
  - raw/slack/2026-05-14-batch-lock-discussion.md
  - raw/settlement/2024-08-14-decision-settlement-v1-manual.md
  - raw/settlement/slack/2024-08-12-manual-excel-settlement.md
  - raw/settlement/2024-11-15-decision-daily-batch-v1.md
  - raw/settlement/pr/pr-031-daily-aggregation-batch.md
  - raw/settlement/slack/2024-11-19-batch-first-run.md
  - raw/settlement/slack/2025-07-18-auto-payout-fear.md
  - raw/settlement/slack/2025-08-14-auto-payout-live.md
  - raw/settlement/pr/pr-096-auto-payout-status-guard.md
  - raw/settlement/2025-10-27-decision-composite-unique-key.md
  - raw/settlement/pr/pr-118-settlement-composite-unique.md
  - raw/settlement/slack/2025-09-25-duplicate-settlement-row.md
  - raw/settlement/slack/2025-10-30-composite-key-deployed.md
  - raw/settlement/pr/pr-082-settlement-statement-pdf.md
  - raw/settlement/slack/2025-05-09-statement-pdf-request.md
  - raw/settlement/pr/pr-129-statement-refund-line.md
  - raw/settlement/slack/2025-07-21-cross-idempotency-ask-paydev.md
  - raw/settlement/transcripts/2026-01-22-settlement-quarter-retro.md
  - raw/settlement/transcripts/2025-12-04-year-end-reconciliation.md
source_hashes:
  - 26bd99230c53aada841f8841fdde795f2baccaca
  - 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
  - 74220c848aa8e3ad5425c32830ffdfb8497d3629
  - ceab4af77a6076f99b265157aaad25f1410da74b
  - e6d5eb68853d4d9dd2880838258540717688588b
  - 84f0a1fd3cb7dc0ae9230e72d51d9fddd626e5ad
  - f2f89b652ed42550c47398d57584ebf635e9c56a
  - 39a6ecd6afe3081fa4baac662fe1a01ea23049df
  - a09bc63a587ba07d34a0ab8b3a22d677f858df2e
  - e39971cc4928beabad2808e047214f91ec97c075
  - eda0196e5d3402c6ca2740d0adb0181771249aee
  - 5b1bb44f3674ad7981ab676dcb9a2ef64e1590ee
  - 7777ffcdf93af90465febd4674a733624a3db6bc
  - 6fd6501d1f16b6c24a37cb348585fd5cd8f480ee
  - 67fec951ff8821c01ac27cf31f6324c9a423ce33
  - c979da2aed1ab50990ff44c109f3f3c241652cf8
  - be915ee19dfd2671f7a53e7745b2e7e0bb0ea11d
  - 8de73ef280d8cb438be3e2324ca2577666f7ab82
  - 54114f72d07c609b9f52775d7137bc1a952b6f32
  - bb746b80c1a7f3cac60519aac7ae98c020cf9440
  - c48e9ba3e93a63c0b860abd55dd0a298bfd25c4e
  - f496ca141b7bd318358034dee1eef2899f154b77
  - 54522db560aa48f883565ff734af818b24f81cf4
  - 93595e2851a81c18d0633a5109d68e0c23a75a93
  - e474087ec8d143b57a685954b652c0fec93b70e1
  - a933148c97762e9b4cce3936332b530563b861e4
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 가맹점 매출을 D+1 일배치로 정산한다. 매일 04:00에 전날 승인 거래를 가맹점별 집계 → 수수료 차감 → 송금한다. 정산 멱등 키는 가맹점ID+정산일이며, 이중 송금 장애를 거쳐 송금 단계에도 유니크 가드와 분산 락이 추가됐다.

## Details

### 진화사 (2024~2025)
2026년의 D+1 배치·INC-231 보강은 1년 반에 걸친 점진적 진화의 마지막 단계다. 정산 시스템은 가맹점 수가 늘 때마다 한 단계씩 자동화·가드를 더해 왔다.

- **수기 엑셀 정산 (2024-08):** 가맹점 5곳 규모, 정산 절차 자체가 없던 시절. 매주 금요일 CSV 추출 → 엑셀 피벗 합산 → 수수료 3.3% 차감 → 은행 앱 수기 이체로 정산 v1을 시작했다(엑셀 템플릿 표준화, 수수료는 임시 반올림). 첫 마감에서 이미 가맹점 1원 차이 문의가 들어와 수수료 처리의 모호함이 드러났다 — 이후 [[fee-calculation]] 절사 정책 분쟁의 씨앗.
- **D+1 일배치 v1 (2024-11):** 가맹점 20곳을 넘으며 수기가 한계에 달해, 매일 04:00 전날 거래를 가맹점별로 SUM하는 1세대 자동화를 도입했다(PR-031). 단 **집계만 자동화하고 송금은 사람이 리포트 검토 후 수기 이체** — 락·멱등 가드 없이 실패 시 전체 재실행하는 단순 운영을 전제했다. 첫 정상 가동(11/19)에서 가맹점 C 80원 차이가 났고, 원인은 자정 직후 환불 건의 날짜 경계 귀속 모호성이었다(케이스를 더 모아 정하기로 보류, 당장은 수기 보정). 경계 귀속 문제는 2026 설계에서 반개구간으로 정식 해결된다.
- **자동 지급(payout) 도입 (2025-07~08):** 가맹점 40곳을 넘으며 수동 이체가 한계. 가장 큰 우려는 "배치 중복 실행 시 같은 가맹점에 송금이 두 번 나가면 롤백 불가"였다. ★ 이때 정산팀이 결제팀(#pay-dev)에 중복 방지 방식을 직접 문의한 것이 교차 협업의 시작이다(7/21) — 결제는 Idempotency-Key(UUID)를 Redis TTL 24h로 저장해 재요청 시 기존 결과만 반환하지만, 송금은 별도 키 없이 `(가맹점, 정산일)` 조합이 자연 유니크하니 그 단위로 한 번만 송금되게 하라는 조언을 받았다([[idempotency]]). 설계 회의(7/22)에서 결제팀 박서연이 "체크-송금 사이 경쟁 조건"을 경고했으나, **단일 인스턴스 하루 1회 실행 전제**에선 락 없이 트랜잭션+상태 체크로 충분하다고 정리했다(동시 실행이 생기면 락/유니크 가드 필요 — 이 미결이 2026 INC-231로 실현된다). 8/14 배치가 집계→송금까지 수동 개입 0번으로 첫 자동 완주(송금 직전 status가 confirmed/PAID 아니면 스킵하는 상태 체크 가드, PR-096). 자동화 후에도 매일 아침 송금 결과 수기 검산을 안전망으로 유지.
- **복합 유니크 키 정식화 (2025-09~10):** 9/25 아침 검산에서 한 가맹점 정산액이 2배로 잡힌 사고 — 중간에 멈춘 배치 재실행 시 기존 행을 지우지 않고 또 INSERT해 같은 `(가맹점, 정산일)` 행이 둘 생긴 것. "코드가 아니라 DB가 막자"는 방향으로, `UNIQUE(merchant_id, settlement_date)` 복합 유니크 + upsert(`ON DUPLICATE KEY UPDATE`)를 도입했다(2025-10-27 결정, PR-118). 제약 추가 전 중복 행 정리 시 PAID 행을 우선 보존하도록 정렬했고, upsert의 `DO UPDATE`에 `WHERE status <> 'PAID'`를 걸어 송금 완료 행을 보호(스테이징 1,204건 중복 → 0건, PAID 손실 없음 검증). 10/30 무중단 마이그레이션으로 운영 반영. **다만 행 중복은 DB가 막게 됐어도, 같은 행을 실제 송금 두 번 쏘는 것은 여전히 payout 상태 체크에만 의존했고 분산 락은 다음 스코프로 남겼다** — 이 잔존 갭이 2026 INC-231의 직접 원인.
- **정산 명세서 PDF (2025-05~):** 세무 신고용 PDF 요청이 늘어 수기 캡처 발송을 자동 생성으로 전환(5/9 항목 확정 → PR-082). builder가 StatementData를 만들고 렌더러는 포맷만 그리는 구조이며, **라인 합과 합계 행이 1원이라도 틀리면 명세서를 아예 생성하지 않는다**. 금액은 원 단위 절사 함수를 거치되 '라인 절사 후 합산' 순서로 footer와 일치시킨다([[fee-calculation]]). 이후 명세서에 환불 차감 항목을 별도 행으로 추가하고 `정산액 = 승인합계 − 수수료 − 환불차감`으로 재정의(PR-129) — 환불차감은 원금 + 수수료 비례 환원분을 포함하고 절사는 거래 단위로 통일, 마감 후 환불은 다음 정산일 귀속, 음수 정산액은 0 처리 후 미정산 잔액으로 이월.
- **연말 정합성 점검 (2025-12-04):** 1년치 정산 정합성 점검에서 회차 경계를 넘은 환불의 수수료 환원이 명세서엔 차감 표기되지만 합계 재계산엔 누락돼 회사가 더 가져간 차이를 발견 → 소급 정정 입금 + 환불 차감 항목 분리 + 합계 재계산에 회차 경계 환불 물리기 + 절사 거래 단위 통일을 액션으로 확정(PR-129로 이어짐).
- **분기 회고 (2026-01-22):** 1년 반의 흐름(수기 → D+1 배치 → 자동 송금 → 복합 유니크 → 명세서 자동화)을 정리하고, 송금 중복 방지가 복합 유니크와 상태 체크에만 의존해 **동시 실행 시 분산 락 부재가 찜찜하다**는 점을 백로그(우선순위 낮음)로, 정산 CSV export를 우선순위 있게 남겼다. 이 "낮은 우선순위"였던 분산 락은 넉 달 뒤 INC-231로 우선순위가 강제 상향된다.

### 설계 (2026-03-25)
- 일배치(D+1): 매일 04:00 KST 크론. 전일 00:00~23:59:59 `APPROVED` 거래 기준 — 구현은 `approved_at >= D AND < D+1` 반개구간으로 경계 중복/누락 없음 (PR-125, 120만 건 4.2초 실측).
- 단계: 집계 → 수수료 계산([[fee-calculation]]) → 정산명세서 생성 → 송금 요청 → 결과 기록.
- **정산 멱등 키 (2026-03-27 슬랙 결정 — 정식 문서 없음):** 별도 키 컬럼 없이 `(merchant_id, settlement_date)` 복합 유니크. 재실행 판정도 같은 컬럼 사용.
- 부분 재실행 지원(실패한 가맹점만 재처리).
- 실시간 정산은 환불 정정 복잡성·송금 수수료로 탈락. D+1 충분 여부는 가맹점·영업 사전 확인(경쟁사 동일).

### 이중 송금 장애와 보강 (INC-231, 2026-05-13)
배치 지연을 "멈춤"으로 오판해 수동 재실행했고(슬랙 실시간 스레드에 04:41 재실행 결정 순간이 기록돼 있음 — 송금 API 지연으로 로그만 멈춘 상태였음), 정산 멱등성이 **명세서 생성 단계까지만** 적용돼 송금 단계엔 가드가 없어 이중 송금이 발생했다(가맹점 3곳·1,840만원, 당일 전액 회수). 보강:
- **송금 유니크 가드 (PR-151):** 송금 호출 *전* `payout_log`에 (가맹점ID, 정산일) INSERT(status=initiated) → 유니크 충돌이면 송금 자체를 스킵. initiated 고아 행(INSERT 후 송금 실패)은 1시간 후 수동 확인 큐로 — **자동 재송금은 위험해서 금지**, "돈 나가는 건 모호하면 사람이 본다." ([[idempotency]])
- **분산 락 (PR-153):** Redis lock TTL 2h + 30분 heartbeat 연장(진짜 죽으면 연장이 멈춰 자동 해제). pg advisory lock 안과 논쟁 끝에 "락 실패 = 실행 안 함이라 Redis가 죽어도 안전한 실패"라는 fail-closed 논리로 Redis 채택 (5/14 슬랙).
- **알람 단계화:** "오래 걸림"과 "죽음"을 구분하는 3단계 알람 도입. ([[oncall-and-alerting]])
- 교훈: 멱등성은 돈이 실제 나가는 지점에 걸어야 한다(결제 INC-204와 동일).

### 진행 중 (2026-06)
- 정산명세서 CSV 내보내기 (가맹점 C 요구 → 대시보드 공통 기능으로 확장, PR-162 draft).

## Related
- [[idempotency]] — 정산 송금의 멱등 가드와 공통 교훈
- [[postgresql-choice]] — 정산 집계 쿼리와 유니크 제약을 지원하는 DB
- [[fail-closed-principle]] — 배치 동시 실행을 막는 안전 기본값
- [[fee-calculation]] — 정산 파이프라인의 수수료 절사 정책
- [[oncall-and-alerting]] — INC-231 이후의 배치 알람 단계화
- [[refund-flow]] — 기정산 거래 차감이 얽힐 Q3 과제
