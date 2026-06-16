---
type: source
of: raw/infra/slack/2025-02-25-redis-ready-announce.md
source_hash: 9e9e32ff41f41299cecde6dbd866fcc292e8dabc
tags: [source]
---

## Summary
강민석이 관리형 Redis 클러스터 준비 완료를 #infra에 알리며 엔드포인트(redis.internal.nimbuspay:6379, TLS), 커넥션 풀 권장 설정(max active 50/idle 10/min idle 2, timeout 2s, 앱 인스턴스당 풀 1개), 팀별 namespace prefix를 공유했다. 정유진은 모든 키에 TTL을 꼭 걸라 당부했고, maxmemory-policy는 일단 `allkeys-lru`로 잡아뒀다고 안내했다.

## Concepts
- Redis 도입
- Redis eviction 정책
- Kubernetes 마이그레이션
