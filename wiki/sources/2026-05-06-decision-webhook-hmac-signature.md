---
type: source
of: raw/2026-05-06-decision-webhook-hmac-signature.md
source_hash: a6282a95f50214930b843f44ad1b6f1689a8f2b5
tags: [source, decision]
---

## Summary
웹훅 HMAC 서명 도입 결정(2026-05-06) — 3/18 웹훅 정책의 미결(위조 방지) 해소. 모든 웹훅에 `X-Nimbus-Signature`(HMAC-SHA256) 추가, 가맹점별 시크릿 발급·회전, timestamp로 리플레이 방지. 2026-07-01부터 서명 검증 필수화.

## Concepts
- 웹훅 전송
