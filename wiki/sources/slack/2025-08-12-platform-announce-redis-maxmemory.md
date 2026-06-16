---
type: source
of: raw/slack/2025-08-12-platform-announce-redis-maxmemory.md
source_hash: 3271f438ff40828fe4b07b8a8fe1aa69691ca2c9
tags: [source]
---

## Summary
정유진이 #platform-announce에 공용 Redis maxmemory-policy 변경(`noeviction → allkeys-lru`, 8/19 무중단 적용 예정)을 공지했다. 결제팀 박서연이 idem: 멱등키(TTL 24h)가 allkeys-lru에서 만료 전 evict돼 중복청구 위험이 있다고 제기했고, volatile-lru도 TTL 키라 후보가 되는 한계를 두고 멱등키용 별도 protected 인스턴스 분리를 검토했다. 결제팀 검토 완료까지 8/19 적용을 홀드하기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 관측성 대시보드
