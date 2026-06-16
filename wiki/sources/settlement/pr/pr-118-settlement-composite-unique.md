---
type: source
of: raw/settlement/pr/pr-118-settlement-composite-unique.md
source_hash: 8de73ef280d8cb438be3e2324ca2577666f7ab82
tags: [source]
---

## Summary
settlement 테이블에 (merchant_id, settlement_date) 복합 유니크 제약과 upsert를 적용한 PR. 제약 추가 전 중복 행 정리 시 PAID 행을 우선 보존하도록 정렬했고, upsert의 DO UPDATE에 `WHERE status <> 'PAID'`를 걸어 송금 완료 행을 보호했다. 스테이징에서 1,204건 중복을 0건으로 정리하고 PAID 손실 없음을 검증했다.

## Concepts
- 정산 복합 유니크 키
- 정산 멱등성
- PAID 보호 가드(upsert)
- 중복 행 정리 마이그레이션
