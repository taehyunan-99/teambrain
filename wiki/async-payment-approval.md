---
title: 비동기 결제 승인 (Async Payment Approval)
tags: [payment, architecture, async]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/2025-12-03-decision-sdk-v1-scope.md
  - raw/2026-03-04-meeting-payment-arch-kickoff.md
  - raw/2026-05-20-troubleshooting-pg-timeout.md
  - raw/slack/2024-07-12-v1-launch-prep.md
  - raw/slack/2025-12-01-sdk-v1-release.md
  - raw/pr/pr-133-polling-worker.md
  - raw/pr/pr-156-bulkhead-worker-pools.md
  - raw/transcripts/2026-03-04-kickoff-transcript.md
source_hashes:
  - 1fd8c16543e547f1bef940c1feaa0b3a518a4955
  - 8e1412ee09e88672e56cea0b25198cd3cf5ead1e
  - d45b1fae55627009672630ea4c604a6160ed16e5
  - 4462dc8b370682cd0774e46208280840507b65e2
  - 28d4d2bc531f8276c93fba0d8d508be16d8efa6e
  - 4551b34533dfd21264009b16a502efa6b6b7ffe4
  - 5cbd1fc330ed2e503c804520ef7c150c066c7f16
  - d46f73f32dfdf8b92fa81f9a9ec12e8eb6ae5e9d
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 결제 승인을 비동기로 처리한다. API는 즉시 `PENDING`을 반환하고 워커가 PG 승인을 거쳐 상태(`APPROVED`/`FAILED`)를 갱신한다. PG 외부 지연(p99 3s)에 우리 API가 인질로 잡히지 않게 하기 위한 2026-03-04 킥오프 결정이다.

## Details
- API는 결제 요청을 받으면 즉시 `PENDING` 상태로 응답한다. 실제 PG 승인은 워커가 비동기로 처리한다.
- 클라이언트는 결과를 **웹훅(서버간) + 폴링(클라)** 두 경로로 받는다. ([[webhook-delivery]])
- **결정 배경 (킥오프 transcript):** 도현의 전 회사에서 PG 직연동을 동기로 했다가 PG 점검일에 자사 API가 전부 같이 죽은 경험이 비동기 결정의 직접 동기. 정식 회의록에는 없는 맥락.

### 폴링 워커 (PR-133)
- PENDING 10분 초과 결제를 PG에 재조회해 동기화. **PG가 진실의 원천(source of truth)** — PG가 승인이면 APPROVED로 올리고 웹훅 발송.
- 폴링 1분 주기, 토스 조회 rate limit(분당 600건) 내에서 백프레셔로 조절.

### 클라이언트 경험 — v1 런칭과 SDK가 폴링을 감싼 과정
- **2024-07-12 최초 v1 런칭:** 출시 막판엔 비동기조차 없었다. 토스 SDK `approve()`를 **동기 호출**해 MySQL에 결제 레코드를 바로 insert하는 단순 구조로 갔고, PG 추상화·멱등성·재시도/웹훅은 첫 가맹점 한 곳뿐이라 백로그로 미루고 출시를 우선했다. 비동기 PENDING 모델은 이후의 진화다. ([[payment-gateway-abstraction]])
- **2025-12-03 SDK v1 스코프 확정:** 비동기 모델이 자리잡자 가맹점이 직접 다뤄야 하는 폴링 부담이 문제로 떠올랐다. 가맹점 연동 부담을 줄이려 결제 SDK v1을 **JS SDK로 한정**하고, **결제 호출 + 결과 폴링을 래핑**하기로 확정. 멱등 키 자동생성은 기본 on(권장)이되 강제는 아니며, SDK를 우회한 직접 API 호출 경로는 막지 않기로 했다.
- **2025-12-01 SDK v1 배포:** 가맹점의 헤더·파라미터 실수를 줄이려 결제 요청과 결과 폴링을 감싼 `@nimbuspay/sdk` 1.0.0을 배포. SDK가 `Idempotency-Key`용 UUID를 자동 생성해 붙여주며, 강제 대신 권장으로 깔고 채택률을 본 뒤 강제 여부를 판단하기로 했다(이후 2026 멱등성 정비에서 SDK 키 강제로 이어짐). ([[idempotency]])

### 워커 격리 (2026-05-20 트러블슈팅 → PR-156)
결제 승인 워커와 웹훅 재전송 워커가 같은 스레드풀을 공유하면, 웹훅 폭주 시 결제 승인이 굶는다(INC 수준 지연). 해결책으로 두 워커풀을 **분리(bulkhead 패턴)**하고 결제 승인에 우선순위를 줬다.
- 풀 사이즈 산정식: 결제 32 (피크 TPS 프로모션 3배 기준 × PG 평균 응답 0.8s = 26 + 여유분), 웹훅 16 (지연 허용이라 절반).
- 웹훅 풀 포화 시 큐 대기 → 디스크 백업 큐로 유실 방지. 철학: **"결제는 빠르게, 웹훅은 반드시."**
- PG 호출 타임아웃을 10s로 단축하고 1회 재시도를 넣었는데, 이게 안전한 이유는 [[idempotency]] 키가 중복 승인을 막기 때문이다.

## Related
- [[payment-gateway-abstraction]] — 비동기 워커가 호출하는 PG 어댑터 계층
- [[webhook-delivery]] — 비동기 승인 결과를 가맹점에 전달하는 경로
- [[idempotency]] — PG 재시도를 안전하게 만드는 멱등성 키
