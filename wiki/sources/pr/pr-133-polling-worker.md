---
type: source
of: raw/pr/pr-133-polling-worker.md
source_hash: 4551b34533dfd21264009b16a502efa6b6b7ffe4
tags: [source, pr-review]
---

## Summary
PENDING 폴링 워커 PR — PG를 진실의 원천으로 삼아 10분 초과 PENDING을 재조회·동기화. 폴링 1분 주기, 토스 조회 rate limit(분당 600) 내 백프레셔.

## Concepts
- 비동기 결제 승인
