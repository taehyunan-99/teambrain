---
type: source
of: raw/pr/pr-061-idempotency-redis-setnx.md
source_hash: 8c4814e1eb0d4e1c89e9ac126a65412f5c282576
tags: [source]
---

## Summary
Redis SETNX(SET NX EX 600) 기반 멱등성 미들웨어 1차를 머지했다. 키는 클라이언트 X-Idempotency-Key 헤더 우선, 없으면 `order:` prefix를 붙인 order_id로 폴백하며, Redis 에러/타임아웃 시에는 결제 손실을 막기 위해 fail-open(통과)하고 `idem_redis_error_total` 메트릭으로 통과 빈도를 관측한다.

## Concepts
- 멱등성 (Redis SETNX)
- 멱등성 미들웨어
- Idempotency-Key 헤더
- 멱등 키 폴백 (order_id)
- fail-open 트레이드오프
- 멱등 TTL
