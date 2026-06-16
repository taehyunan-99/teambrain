---
type: source
of: raw/settlement/pr/pr-129-statement-refund-line.md
source_hash: 54522db560aa48f883565ff734af818b24f81cf4
tags: [source]
---

## Summary
명세서에 환불 차감 항목을 별도 행으로 추가하고 `정산액 = 승인합계 - 수수료 - 환불차감`으로 재정의한 PR. 환불차감은 원금과 수수료 비례 환원분을 포함하며 절사는 거래 단위로 통일한다. 마감 이후 환불은 다음 정산일로 귀속되고, 음수 정산액은 0 처리 후 미정산 잔액으로 이월한다.

## Concepts
- 정산 명세서 PDF
- 환불 차감 항목
- 수수료 비례 환원
- 미정산 잔액 이월
