---
type: source
of: raw/infra/2025-08-15-decision-redis-eviction-policy.md
source_hash: 2323210237275ca98d43476e0e08cffb2b4a32c1
tags: [source]
---

## Summary
운영 Redis 메모리가 maxmemory 한계에 근접해 `noeviction`상 쓰기 거부(OOM)가 결제 실패로 이어질 위험이 커지자, eviction 정책을 `noeviction → volatile-lru`로 변경하기로 결정했다(allkeys-lru는 TTL 없는 보호 데이터까지 제거되어 탈락). 변경 후 TTL 있는 키 중에서만 LRU로 제거되며 TTL 없는 키는 보존되고, 보호 데이터는 TTL 없이 두거나 충분히 길게 설정하라는 전사 원칙을 공지했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 프로모션 용량 계획
