---
type: source
of: raw/settlement/slack/2025-10-30-composite-key-deployed.md
source_hash: bb746b80c1a7f3cac60519aac7ae98c020cf9440
tags: [source]
---

## Summary
(merchant_id, settlement_date) 복합 유니크가 무중단 마이그레이션으로 운영 반영됐다는 보고 슬랙. 이제 행 중복은 DB가 막고 재실행 시 두 번째 INSERT는 upsert로 떨어진다. 다만 같은 행을 실제 송금 두 번 쏘는 것은 여전히 payout 상태 체크에만 의존하며, 분산 락은 다음 스코프로 남겼다.

## Concepts
- 정산 복합 유니크 키
- DB 제약 기반 정합성
- 송금 중복 방지
- 배치 분산 락
