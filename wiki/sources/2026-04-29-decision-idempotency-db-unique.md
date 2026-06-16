---
type: source
of: raw/2026-04-29-decision-idempotency-db-unique.md
source_hash: ffc1d104e7f604383e6dd36eced7eec0706f140b
tags: [source, decision]
---

## Summary
멱등성 키 결정 수정(2026-04-29) — INC-204 장애 후속. 3/11의 Redis 단독 저장을 Redis 캐시 + `payment_idempotency` 테이블 UNIQUE 제약 2계층으로 변경. Redis 조회 실패 시 fail-closed. 클라이언트가 Idempotency-Key를 보내는 방식 자체는 유지.

## Concepts
- 멱등성
- PostgreSQL 선택
- fail-closed 원칙
