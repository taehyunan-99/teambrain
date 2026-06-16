---
type: source
of: raw/slack/2025-08-14-infra-paydev-redis-policy-resolution.md
source_hash: 5d3c8174d11fbab2b18a3b489419581cfd9b8a6b
tags: [source]
---

## Summary
정유진과 결제팀(박서연·김도현)이 #infra에서 멱등키 evict 우려를 정리했다. volatile-lru로 가도 TTL 있는 멱등키는 후보가 되는 한계를 보완하기 위해, 멱등키용 Redis를 메모리 여유 있는 별도 인스턴스로 분리(volatile-lru 병행)하기로 합의했다. 캐시 계층에 정합성 책임을 100% 지우는 찜찜함은 운영하며 보기로 하고, idem 인스턴스 메모리 80% 알람을 별도로 걸기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 단일 장애점(SPOF)
- 관측성 대시보드
