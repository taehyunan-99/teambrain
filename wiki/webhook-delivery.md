---
title: 웹훅 전송 (Webhook Delivery)
tags: [payment, webhook, integration]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/2026-03-18-decision-webhook-retry-policy.md
  - raw/2026-05-06-decision-webhook-hmac-signature.md
  - raw/pr/pr-118-webhook-sender-backoff.md
  - raw/pr/pr-121-dead-letter-table.md
  - raw/pr/pr-148-hmac-signature.md
  - raw/pr/pr-159-secret-rotation-api.md
  - raw/slack/2026-05-02-webhook-secret-storage.md
  - raw/slack/2026-05-07-hmac-encoding-issue.md
source_hashes:
  - 90bb7e15214edf042b29cb6be352e42339118591
  - a6282a95f50214930b843f44ad1b6f1689a8f2b5
  - a8bf7e8890923a168b5fb72de14b412d778f1148
  - df6c04ab3240dc98977102bd5b59aa813e1eff33
  - b34ad27caa64ec7e7f16b2686fbdba8555ceea8a
  - 64ce65e552813c17418e9a9d1714ec7fc396eb08
  - 84dd3cddac86193967eec8758a0ea5ce561eb01e
  - c986fcdf9329e6add09d9fc8bf7bb9f1c2700675
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 결제 결과를 가맹점 서버로 웹훅 전송한다. 가맹점 인프라 불안정에 대비해 지수 백오프 재시도(최대 6회)와 dead letter를 두고, 위조 방지를 위해 HMAC-SHA256 서명을 붙인다.

## Details

### 재시도 정책 (2026-03-18, 구현 PR-118)
- 지수 백오프: 즉시 → 1m → 5m → 30m → 2h → 6h (최대 6회) + **각 간격 ±20% jitter** (가맹점 복구 직후 재시도 폭주 = thundering herd 방지).
- 가맹점 응답 2xx만 성공. 그 외(타임아웃 포함)는 실패로 재시도.
- 6회 모두 실패 → `webhook_dead_letter` 이동 + 가맹점 이메일 알림(조용한 실패 금지). 이메일은 best-effort — "기록은 보장, 알림은 노력". 90일 보관 후 아카이브는 백로그.
- 페이로드에 `event_id`(멱등) 포함 → 가맹점이 중복 수신을 거를 수 있게. ([[idempotency]])
- 공식 전달 모델: **"at-least-once + 수신측 event_id 멱등"**. 계기는 3/17 가맹점 A의 웹훅 유실(서버 500, 재시도 부재).

### 서명 (2026-05-06, 구현 PR-148)
3/18에 미결로 남았던 위조 방지를 해소한 결정이다.
- 모든 웹훅에 `X-Nimbus-Signature` = `HMAC-SHA256(secret, raw_body)` 헤더 추가.
- **서명 대상은 전송 직전의 raw bytes** — json 재직렬화 시 키 순서가 바뀌어 간헐 검증 실패하는 버그를 구현 중 발견·수정. 가맹점 가이드에도 "받은 바디 그대로 검증" 명시 (재직렬화 후 검증이 단골 문의 예상 1순위).
- payload `timestamp` 5분 초과 시 가맹점이 거부(리플레이 방지). 5분의 근거: 가맹점 서버 시계 오차 + 재시도 지연, Stripe 기본값과 동일. 2026-07-01부터 검증 필수화 — 언어별(node/python/java) 검증 샘플 제공.

### 시크릿 관리 (2026-05-02 슬랙 결정 — 정식 문서 없음)
- `webhook_secret` 보관: vault 대신 **DB 암호화 컬럼(pgcrypto)**. vault는 운영 부담으로 기각, KMS 연동은 다음 분기 검토. ([[postgresql-choice]])
- **시크릿 회전 API (PR-159): 리뷰 보류 중** — 구 시크릿 유예기간(24h 고정 vs 가맹점 선택 vs 72h 고정) 미결, 작성자 휴가로 6월 중 재개 예정.

## Related
- [[async-payment-approval]] — 웹훅으로 전달되는 비동기 승인 결과 (웹훅/결제 워커풀 분리 포함)
- [[idempotency]] — event_id 기반 웹훅 수신 중복 제거
- [[postgresql-choice]] — 시크릿 보관에 쓰이는 pgcrypto
