---
type: source
of: raw/pr/pr-148-hmac-signature.md
source_hash: b34ad27caa64ec7e7f16b2686fbdba8555ceea8a
tags: [source, pr-review]
---

## Summary
HMAC 서명 PR — 재직렬화 json이 아닌 전송 버퍼 raw bytes로 서명(키 순서 버그 방지). timestamp 허용 오차 5분의 근거(시계 오차+재시도 지연, Stripe 동일) 기록. 회전 듀얼 키 검증은 PR-159로 분리.

## Concepts
- 웹훅 전송
