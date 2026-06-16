---
type: source
of: raw/infra/slack/2025-08-20-platform-announce-eviction.md
source_hash: 3fa0c52408d69e74800f4e9b1cea3379c83e333b
tags: [source]
---

## Summary
강민석이 #platform-announce에 공용 Redis eviction 정책 변경(8/26 점검 시 `noeviction → volatile-lru`)을 전사 공지했다. volatile-lru는 TTL 있는 키만 제거 대상이나 보호 목적 키도 메모리 부족 시 만료 전 evict될 수 있음을 경고하며, 각 팀에 TTL 충분히 길게 설정 또는 DB 이중화(UNIQUE 등)를 권고했다. 결제팀(박서연)은 멱등키 24h TTL과 DB 가드 부재를 재검토하기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
