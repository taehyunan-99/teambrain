---
type: source
of: raw/pr/pr-153-batch-distributed-lock.md
source_hash: e6d5eb68853d4d9dd2880838258540717688588b
tags: [source, pr-review]
---

## Summary
배치 분산 락 PR — redis lock TTL 2h + 30분 heartbeat 연장(진짜 죽으면 자동 해제). 락 획득 실패 시 즉시 종료(fail-closed).

## Concepts
- 정산 배치
- fail-closed 원칙
