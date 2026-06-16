---
type: source
of: raw/slack/2026-05-12-settlement-double-payout-realtime.md
source_hash: bd03168677029d27cbbcd45b77de4c0d8eee647a
tags: [source]
---

## Summary
새벽 정산 배치가 죽지 않았는데 재실행되어 동일 (merchant_id, settlement_date)로 송금이 두 번 나간 이중 송금 사고가 발생했다(3곳, 1,840만원). 명세서엔 복합 유니크가 있었으나 송금 호출 구간엔 가드가 없던 설계 구멍이 원인으로, 차액 회수와 함께 송금 시점 가드 도입을 정리하기로 했다.

## Concepts
- 정산 자동화
- 중복 결제
- 멱등성
- 페일오버 정책
