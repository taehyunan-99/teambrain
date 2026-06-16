---
type: source
of: raw/settlement/slack/2025-07-21-cross-idempotency-ask-paydev.md
source_hash: 93595e2851a81c18d0633a5109d68e0c23a75a93
tags: [source]
---

## Summary
결제팀(#pay-dev)에 중복 방지 방식을 물어본 교차팀 슬랙. 결제는 Idempotency-Key(UUID)를 Redis에 TTL 24h로 저장해 같은 키 재요청 시 기존 결과만 반환한다고 답했고, 정산 송금은 별도 키 없이 (가맹점, 정산일) 조합이 자연 유니크하므로 그 단위로 한 번만 송금되게 하라고 조언했다.

## Concepts
- 정산 멱등성
- Idempotency-Key
- 정산 복합 유니크 키
- 자동 지급(payout)
