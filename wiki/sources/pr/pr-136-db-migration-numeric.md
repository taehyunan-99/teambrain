---
type: source
of: raw/pr/pr-136-db-migration-numeric.md
source_hash: 1086f41b308ff9f193e95949fce76cbe5d91b6e8
tags: [source, pr-review]
---

## Summary
결제 테이블 마이그레이션 PR — NUMERIC(19,4) 채택 근거: 수수료 중간계산 손실 방지 + scale 변경 마이그레이션이 더 비쌈. over-engineering 이견 있었으나 수용.

## Concepts
- PostgreSQL 선택
