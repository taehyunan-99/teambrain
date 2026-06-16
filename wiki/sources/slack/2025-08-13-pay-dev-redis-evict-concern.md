---
type: source
of: raw/slack/2025-08-13-pay-dev-redis-evict-concern.md
source_hash: 259b43a21642b8f1f4e4c7524a5dced816ea7912
tags: [source]
---

## Summary
결제팀(#pay-dev)에서 박서연·이준호·김도현이 인프라의 Redis allkeys-lru 전환 공지가 멱등키에 미칠 영향을 논의했다. idem:{key}(TTL 24h)가 Redis 단독 의존(백업·DB 가드 없음)이라 메모리 압박 시 만료 전 evict되면 재시도가 신규 결제로 통과돼 중복 결제가 발생함을 확인하고, 멱등키만 별도 정책으로 보호 가능한지 인프라와 함께 봐야 한다는 결론으로 #infra 스레드를 파기로 했다.

## Concepts
- Redis eviction 정책
- Redis 도입
- 단일 장애점(SPOF)
