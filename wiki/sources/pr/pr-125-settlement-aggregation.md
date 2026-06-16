---
type: source
of: raw/pr/pr-125-settlement-aggregation.md
source_hash: 74220c848aa8e3ad5425c32830ffdfb8497d3629
tags: [source, pr-review]
---

## Summary
정산 집계 쿼리 PR — CTE 4단, 120만 건 4.2초 실측. 집계 경계는 `approved_at >= D AND < D+1` 반개구간으로 회의 결정('전일 00:00~23:59:59')을 중복/누락 없이 구현.

## Concepts
- 정산 배치
- PostgreSQL 선택
