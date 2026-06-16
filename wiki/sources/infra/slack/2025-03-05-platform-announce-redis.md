---
type: source
of: raw/infra/slack/2025-03-05-platform-announce-redis.md
source_hash: 249b6f294f56db84914178d888fcd61d6aebea28
tags: [source]
---

## Summary
정유진이 #platform-announce에 공용 Redis 캐시/세션 인프라 오픈을 전사 공지했다. 내부 엔드포인트·팀별 prefix·vault 접근 정보를 안내하고, 모든 키 TTL 필수, 현재 maxmemory 정책은 `noeviction`(메모리 차면 쓰기 실패)이라 TTL이 선택이 아닌 필수임, 대용량 키는 사전 협의를 당부했다. 결제·정산팀에 멱등성/세션 도입 검토 시 함께 보겠다고 안내했다.

## Concepts
- Redis 도입
- Redis eviction 정책
