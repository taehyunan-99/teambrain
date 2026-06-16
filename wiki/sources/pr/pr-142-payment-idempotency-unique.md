---
type: source
of: raw/pr/pr-142-payment-idempotency-unique.md
source_hash: 16cbf59d8f572e214f286677eff606ca6e1c6fbc
tags: [source, pr-review]
---

## Summary
DB 유니크 가드 구현 PR — ON CONFLICT DO NOTHING + RETURNING 관용구, 동시 도착 둘째 요청은 409 'processing'. 'redis=응답 재생 캐시, DB UNIQUE=멱등성의 진실' 계층 역할을 주석으로 명문화.

## Concepts
- 멱등성
- PostgreSQL 선택
