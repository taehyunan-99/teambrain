---
type: source
of: raw/pr/pr-156-bulkhead-worker-pools.md
source_hash: 5cbd1fc330ed2e503c804520ef7c150c066c7f16
tags: [source, pr-review]
---

## Summary
워커풀 분리 PR — 결제 32(피크 TPS×PG 0.8s=26+여유)/웹훅 16 산정식 기록. 웹훅은 큐 대기+디스크 백업 큐로 유실 방지. '결제는 빠르게, 웹훅은 반드시.'

## Concepts
- 비동기 결제 승인
