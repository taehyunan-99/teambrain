---
type: source
of: raw/slack/2025-05-12-idempotency-v1-redis-plan.md
source_hash: a13bff40cec9f498295c7258f4e2f860c09fd87d
tags: [source]
---

## Summary
이미 받기만 하던 Idempotency-Key를 활용해, approve 진입부에서 키로 Redis SETNX를 시도하고 성공하면 정상 처리, 기존 키면 409로 거절하는 멱등성 v1을 빠르게 도입하기로 했다. TTL은 6시간, 키 포맷은 idem:{key}, 결과 캐싱은 보류하고 중복 차단만 우선하며 기존 Redis 인프라를 재사용한다.

## Concepts
- 멱등성
- 중복 결제
