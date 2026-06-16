---
type: source
of: raw/infra/slack/2025-08-13-redis-eviction-crossteam.md
source_hash: dc5d97df60936545aa39120d3e29d1b026d58b1a
tags: [source]
---

## Summary
정유진이 결제팀 박서연과 #infra에서 Redis eviction 정책을 협의했다. allkeys-lru는 TTL 24h 멱등키가 메모리 압박(=트래픽·결제 최다 시점)에 evict돼 중복청구로 이어질 수 있어 폐기하고, TTL 없는 영구키를 보호하는 volatile-lru 채택+maxmemory 상향으로 평시 eviction 회피라는 두 트랙에 합의했다. 멱등키 TTL 재검토는 결제팀이 별도 진행하기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 프로모션 용량 계획
