---
type: source
of: raw/slack/2026-04-21-infra-redis-latency.md
source_hash: 340b6890313be6e4d298e7812dbec7cec0240e66
tags: [source]
---

## Summary
프로모션 트래픽 3배로 redis-prod p99 latency가 38ms까지 튀고 maxmemory 도달로 LRU eviction이 발생했다. maxmemory를 8G로 올려 p99를 14ms까지 낮췄으나 single-threaded CPU 한계가 남았고, 멱등키·세션이 같은 인스턴스를 쓰는 구조 분리를 후속 과제로 잡았다.

## Concepts
- DB 커넥션 고갈
- 멱등성
- 중복 결제
