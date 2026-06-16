---
type: source
of: raw/slack/2025-06-25-redis-provisioning.md
source_hash: d94cef24d7aa9fa5644e909b28cec001e161e2a2
tags: [source]
---

## Summary
결제팀 이준호가 #infra에 멱등성/세션 저장용 Redis 운영 인스턴스 프로비저닝을 요청했다(Idempotency-Key TTL 24h + 세션). 정유진은 무중단 HA 구성은 일정상 어려워 단일 인스턴스로 우선 띄우기로 했고(maxmemory 정책 allkeys-lru, vault redis/pay-prod), 박서연은 Redis가 멱등성 최후 방어선이라 단일이면 불안하다는 우려를 남기되 진행에 동의했다.

## Concepts
- Redis 도입
- Redis eviction 정책
- 단일 장애점(SPOF)
