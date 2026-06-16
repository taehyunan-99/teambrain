---
type: source
of: raw/slack/2025-05-20-pay-dev-failover-inflight-tx.md
source_hash: 7b64c06674fbe8c9528e2c11f9cb72274bd378cf
tags: [source]
---

## Summary
MySQL HA 페일오버 윈도우 동안 PG 승인 후 DB 기록이 막히면 돈만 나가고 흔적이 없는 미아 트랜잭션이 우려됐다. (1) PENDING INSERT → (2) PG approve → (3) APPROVED UPDATE 순서를 보장하면, 윈도우에 걸린 건은 PENDING으로 적체됐다가 폴링 워커가 PG status 재조회로 보정해 미아를 막을 수 있다는 결론에 도달했다.

## Concepts
- 페일오버 정책
- 비동기 결제 승인
- 멱등성
- 중복 결제
