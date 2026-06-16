---
type: source
of: raw/infra/slack/2025-08-12-redis-maxmemory-alert.md
source_hash: 5d3628971d753c3b66204aa64d4ce26d862ba6d9
tags: [source]
---

## Summary
alert-bot이 redis-prod-01 메모리 90.2%(5.4GB/6GB) 경보를 띄우자, 정유진과 강민석이 `noeviction`상 한계 도달 시 쓰기 거부(결제 영향)를 우려해 대응을 논의했다. allkeys-lru는 멱등성 키까지 evict될 위험, volatile-lru도 TTL 있는 멱등키는 후보가 되는 한계를 확인하고, 우선 maxmemory를 6GB→8GB로 임시 상향(67%로 하락)한 뒤 키 프리픽스별 메모리 점유 분석과 결제팀 협의로 정책을 정하기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 관측성 대시보드
