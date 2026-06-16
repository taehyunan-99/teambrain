---
type: source
of: raw/pr/pr-151-payout-unique-guard.md
source_hash: ceab4af77a6076f99b265157aaad25f1410da74b
tags: [source, pr-review]
---

## Summary
송금 유니크 가드 PR(INC-231 후속) — INSERT(initiated)가 송금 호출보다 먼저, 유니크 충돌 시 송금 자체를 스킵. initiated 고아 행은 1시간 후 수동 확인 큐로(자동 재송금은 위험해서 금지). '돈 나가는 건 모호하면 사람이 본다.'

## Concepts
- 정산 배치
- 멱등성
