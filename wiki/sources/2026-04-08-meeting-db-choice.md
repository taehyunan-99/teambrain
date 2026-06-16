---
type: source
of: raw/2026-04-08-meeting-db-choice.md
source_hash: 61b549d07de5f05cb4d6ec5d25ba416a3cad1050
tags: [source, meeting]
---

## Summary
결제 DB 선택 회의(2026-04-08). PostgreSQL 채택 — 트랜잭션·유니크 제약·`ON CONFLICT` upsert가 멱등 처리에 핵심이고, 윈도우 함수·CTE가 정산 집계에 유리. MongoDB는 약한 트랜잭션으로 탈락. 금액은 NUMERIC 사용(부동소수점 금지).

## Concepts
- PostgreSQL 선택
- 멱등성
