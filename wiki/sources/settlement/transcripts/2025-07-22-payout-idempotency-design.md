---
type: source
of: raw/settlement/transcripts/2025-07-22-payout-idempotency-design.md
source_hash: 3e1f7c167c047b4890e0513d2dbb620cfd14ca6b
tags: [source]
---

## Summary
송금 자동화 설계 회의 전사. 정산 키를 (merchant_id, settlement_date)로 잡고 송금 직전 상태 체크로 완료면 스킵하는 방안에 대해, 결제팀 박서연이 체크-송금 사이 경쟁 조건을 경고했다. 단일 인스턴스 하루 1회 실행 전제에선 락 없이 트랜잭션+상태 체크로 충분하나, 동시 실행이 생기면 락/유니크 가드가 필요하다고 정리했다.

## Concepts
- 자동 지급(payout)
- 정산 멱등성
- 경쟁 조건 / 분산 락(보류)
- 정산 복합 유니크 키
