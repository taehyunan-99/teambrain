---
type: source
of: raw/settlement/pr/pr-096-auto-payout-status-guard.md
source_hash: c979da2aed1ab50990ff44c109f3f3c241652cf8
tags: [source]
---

## Summary
정산 송금 자동화 PR로, 송금 전 settlement.status가 PAID면 스킵하는 상태 체크 가드를 도입했다. SELECT-송금-UPDATE 사이의 비원자성으로 동시 실행 시 경쟁 조건이 있으나, 단일 인스턴스 하루 1회 실행 전제이므로 락 없이 가드만으로 충분하다고 합의했고 payout 이력 로그를 남긴다.

## Concepts
- 자동 지급(payout)
- 상태 체크 가드
- 정산 멱등성
- 경쟁 조건 / 분산 락(보류)
