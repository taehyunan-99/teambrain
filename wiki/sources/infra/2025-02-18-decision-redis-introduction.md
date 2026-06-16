---
type: source
of: raw/infra/2025-02-18-decision-redis-introduction.md
source_hash: c49d8ba41ab6cdec6ed582f5c5527c06f88eb6a5
tags: [source]
---

## Summary
팀마다 제각각이던 캐시·세션 저장소를 표준화하기 위해 관리형 Redis를 사내 표준으로 도입하기로 결정했다(memcached·DB 세션 테이블 대안 탈락). 단일 인스턴스로 시작하고 maxmemory는 넉넉히, eviction 정책은 데이터 유실 방지를 위해 `noeviction`으로 두며, 키 네이밍 컨벤션과 용도별 TTL 명시를 규칙으로 정했다.

## Concepts
- Redis 도입
- Kubernetes 마이그레이션
- 단일 장애점(SPOF)
