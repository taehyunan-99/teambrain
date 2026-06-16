---
type: source
of: raw/settlement/2025-10-27-decision-composite-unique-key.md
source_hash: be915ee19dfd2671f7a53e7745b2e7e0bb0ea11d
tags: [source]
---

## Summary
배치 부분 재실행으로 같은 가맹점·정산일 행이 중복 생성된 사고를 계기로, 정산 테이블에 `UNIQUE(merchant_id, settlement_date)` 복합 유니크 제약과 upsert(ON DUPLICATE KEY UPDATE)를 도입해 정합성 보증을 코드가 아닌 DB 제약이 지게 한 결정. 이미 PAID인 행은 덮어쓰지 않도록 PAID 보호 가드를 함께 둔다.

## Concepts
- 정산 복합 유니크 키
- 정산 멱등성
- DB 제약 기반 정합성
- PAID 보호 가드(upsert)
