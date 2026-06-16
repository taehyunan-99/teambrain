---
title: 멱등성 (Idempotency)
tags: [payment, idempotency, reliability]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/pr/pr-061-idempotency-redis-setnx.md
  - raw/slack/2025-05-12-idempotency-v1-redis-plan.md
  - raw/2026-03-11-decision-idempotency-key-client.md
  - raw/2026-04-22-incident-duplicate-charge.md
  - raw/2026-04-29-decision-idempotency-db-unique.md
  - raw/2026-05-13-incident-settlement-double-payout.md
  - raw/2026-05-20-troubleshooting-pg-timeout.md
  - raw/pr/pr-112-idempotency-middleware.md
  - raw/pr/pr-140-hotfix-fail-closed.md
  - raw/pr/pr-142-payment-idempotency-unique.md
  - raw/pr/pr-145-sdk-key-enforcement.md
  - raw/slack/2026-03-13-redis-ttl-question.md
  - raw/slack/2026-04-21-inc204-realtime.md
  - raw/slack/2026-06-10-idem-ttl-48h-proposal.md
  - raw/slack/2026-06-15-idem-ttl-48h-approved.md
  - raw/transcripts/2026-04-23-inc204-postmortem-transcript.md
  - raw/transcripts/2026-04-29-idempotency-v2-transcript.md
source_hashes:
  - 8c4814e1eb0d4e1c89e9ac126a65412f5c282576
  - a13bff40cec9f498295c7258f4e2f860c09fd87d
  - 10620d1cdbf895c572754fa29a133e775f28c033
  - 35908695e477a83f6de25a0ad09d4e912124c790
  - ffc1d104e7f604383e6dd36eced7eec0706f140b
  - 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
  - d45b1fae55627009672630ea4c604a6160ed16e5
  - 2a8633743676e379d02abb3aa0bda19c3795e3b6
  - b3d613157e3e5d9c29dd3344369aaa8994dca927
  - 16cbf59d8f572e214f286677eff606ca6e1c6fbc
  - cb1e4a147cf3b376e15047f536cad94648e6e95b
  - 7d9842ac8c25cc21f9432751bc666b07dec8f01e
  - 920892c2c84ba0acec607e1fa41e4b83b71a184b
  - df185ec85e8e0476de45ef8e3d883520718c6309
  - 08a7fe48f87d1bcf33c3066ece5743e377619268
  - 749625389b82f5c1ba0b090b2946c3f0c73cef07
  - c706699307b03bd1ff3983fcb47e4e53faa102a3
---

<!-- llmwiki:auto -->

## Summary
멱등성은 같은 요청을 여러 번 보내도 결과가 한 번 보낸 것과 같도록 보장하는 성질이며, Nimbus Pay 결제 백엔드의 가장 핵심적인 신뢰성 원칙이다. 클라이언트가 `Idempotency-Key`(UUID)를 보내고 서버가 중복을 가드한다. 저장 방식은 처음엔 Redis 단독이었으나 중복 결제 장애를 거치며 **Redis 캐시 + DB 유니크 제약 2중화**로 진화했다.

## Details

### 현재 설계 (2026-04-29 기준)
- 클라이언트가 `Idempotency-Key` 헤더로 UUID를 전송한다. SDK가 키 생성을 강제한다.
- 서버는 2계층으로 중복을 가드한다:
  1. **Redis 캐시**(`idem:{key}`, TTL 24h) — 빠른 경로, 응답 재생용.
  2. **DB UNIQUE 제약**(`payment_idempotency.idempotency_key`) — 최종 방어선. INSERT가 유니크 위반이면 중복으로 보고 기존 응답을 반환한다.
- Redis 조회 실패 시 **fail-closed**(거부 후 클라 재시도). 결제 경로에서 통과시키지 않는다. ([[fail-closed-principle]])

### 결정 히스토리 (왜 바뀌었나 — 신입 필독)
- **2025-05-12 기술적 기원 (Redis v1 계획):** 사실 멱등성의 첫 구현은 2026-03-11 결정보다 거의 1년 앞선다. 당시 클라가 보내기만 하고 활용 안 되던 `Idempotency-Key`를 살려, approve 진입부에서 키로 **Redis SETNX**를 시도해 신규면 정상 처리·기존 키면 409로 거절하는 v1을 빠르게 도입하기로 했다. TTL 6h, 키 포맷 `idem:{key}`, 결과 캐싱은 보류하고 중복 차단만 우선, 기존 Redis 인프라 재사용. ([[redis-introduction]])
- **2025-05 최초 구현 (PR-061):** `SET NX EX 600` 기반 미들웨어 1차를 머지. 키는 클라 `X-Idempotency-Key` 헤더 우선, 없으면 `order:` prefix를 붙인 order_id로 폴백. Redis 에러/타임아웃 시 결제 손실을 막으려 **fail-open(통과)**하고 `idem_redis_error_total` 메트릭으로 통과 빈도를 관측했다 — 이 fail-open이 2026 INC-204의 먼 뿌리다.
- **2026-03-11 재정비 결정:** 멱등성 = Redis 단독 저장(응답 24h 캐시)으로 정식화. 클라가 UUID 키를 보내는 방식을 공식 채택하고, 서버 생성 키·자연 키(주문ID+금액) 방식은 정당한 재결제를 구분 못 해 탈락했다. v1의 SETNX 차단 위에 응답 재생 캐싱을 더한 셈.
- **2026-03-15 fail-open의 기원 (PR-112):** 미들웨어 구현 리뷰에서 "Redis 타임아웃 시?"가 쟁점이 됐고, 도현(테크리드)이 "결제 못 받는 손실이 더 크다"며 **fail-open(통과)을 결정**했다. 서연의 고민 표명, 준호의 중복 결제 우려가 리뷰에 기록돼 있다 — 한 달 뒤 INC-204로 뒤집힌 판단의 원점.
- **2026-04-21 INC-204 장애:** 프로모션 트래픽(사전 경고 있었음)으로 Redis 지연 → 멱등성 조회 타임아웃 → fail-open으로 87건 중복 청구. 슬랙 실시간 스레드에서 서연이 fail-open 코드를 발견했고 도현이 본인 결정임을 즉석 인정, 당일 fail-closed 핫픽스(PR-140) 배포.
- **2026-04-23 포스트모템:** blameless 회고에서 도현이 PR-112 결정을 공식 인정. "결제 경로 외부 의존은 fail-closed 기본" 원칙과 DB 이중화 안이 확정됨.
- **2026-04-29 결정 수정:** 3/11 결정을 뒤집어 DB 유니크 2중화 + fail-closed로 변경. Redis는 "진실 → 응답 재생 캐시"로 역할 전환. 단, 클라가 키를 보내는 방식 자체는 옳았으므로 유지. 회의에서 "3/11을 수정하는 결정임을 기록하라"고 명시 — 히스토리 연결이 의도된 결정.

### 구현 디테일 (PR-142, PR-145)
- DB 가드는 `INSERT ... ON CONFLICT DO NOTHING + RETURNING` 관용구 (23505 예외 핸들링 대신). ([[postgresql-choice]])
- `request_hash` 컬럼: 같은 키인데 바디가 다른 요청(클라 버그)은 409 거부.
- 동시 도착한 같은 키의 둘째 요청은 1차 처리 중이면 409 "processing" → 잠시 후 재시도.
- SDK는 **"요청 객체 = 멱등성 단위"** 의미론: 같은 객체 재시도 = 같은 키, 새 객체 = 새 결제. 가맹점 개발자 혼동 1순위라 문서에 예제 명시. SDK 미사용 직접호출 가맹점 2곳은 2주 유예 후 키 없으면 400.

### TTL 24h → 48h (2026-06-15 승인)
- 3/13에 "확률 낮으니 보류"했던 'TTL 만료 후 같은 키 재시도' 케이스가 6/10 실측 7건(가맹점 배치 재처리 패턴)으로 재부상. DB 유니크가 막아 사고는 아니나 캐시 미스로 409 혼란 → TTL 48h 제안.
- **2026-06-15 승인:** Redis 메모리 추산 결과 일평균 약 32만 개 키 기준 피크 메모리 +12%로 여유분 내 감당 가능. 김도현 승인. `idem:{key}` TTL 상수 한 줄(24h→48h) 변경, 다음 배포 포함.
- **DB 유니크는 영구 그대로:** Redis는 응답 재생 캐시라 48h로 늘리지만, DB 유니크는 최종 방어선이라 손대지 않는다. 48h 연장의 목적은 가맹점 다음날 배치 재처리 시 캐시 미스로 인한 409를 없애는 것.

### 적용 지점
- 결제 승인: 클라 키 + Redis/DB 2중 가드.
- 정산 송금: INC-231 이후 송금 직전 `payout_log`에 (가맹점ID, 정산일) UNIQUE 체크. ([[settlement-batch]])
- PG 재시도: 멱등성 키가 있어 PG 호출 재시도가 안전하다. ([[async-payment-approval]])

### 팀이 반복하는 교훈
멱등성은 캐시(계산)가 아니라 **돈이 실제 나가는 외부 부수효과 직전의 영속 저장소 유니크 제약**이 최종 방어선이어야 한다. INC-204(결제)와 INC-231(정산) 두 장애가 같은 교훈을 가르쳤다.

## Related
- [[fail-closed-principle]] — 멱등성 조회 실패 시 거부하는 결제 경로 원칙 (PR-112 → INC-204에서 확립)
- [[settlement-batch]] — 정산 송금 단계의 멱등 가드
- [[async-payment-approval]] — 멱등성 키 덕분에 안전한 PG 재시도
- [[postgresql-choice]] — DB 유니크 제약이 멱등성의 최종 방어선인 이유
- [[webhook-delivery]] — event_id 기반 웹훅 수신 멱등성
- [[refund-flow]] — 같은 멱등 가드 패턴이 적용될 Q3 과제
- [[redis-introduction]] — 멱등성 v1 SETNX의 기반이 된 Redis 인프라
