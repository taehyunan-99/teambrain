---
type: source
of: raw/slack/2026-04-28-idem-table-ddl.md
source_hash: 69c1a1b4acb21b2227259e75381a43353ba1d6c6
tags: [source, slack]
---

## Summary
payment_idempotency 테이블 DDL 초안 — 키를 PK로(유니크 제약 겸용), request_hash로 같은 키·다른 바디(클라 버그)를 409 거부. 4/29 결정 회의의 기술 초안.

## Concepts
- 멱등성
- PostgreSQL 선택
