---
type: source
of: raw/slack/2026-04-02-for-update-deadlock.md
source_hash: da31e98dc78383000cd0b059d948f68bf899c605
tags: [source, slack]
---

## Summary
SELECT FOR UPDATE 데드락 — 락 획득 순서를 payment→ledger로 통일해 해결. DB 선택 회의(4/8) 직전의 postgres 운영 경험.

## Concepts
- PostgreSQL 선택
