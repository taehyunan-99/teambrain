---
type: source
of: raw/settlement/pr/pr-082-settlement-statement-pdf.md
source_hash: c48e9ba3e93a63c0b860abd55dd0a298bfd25c4e
tags: [source]
---

## Summary
정산 명세서 PDF 생성 PR. StatementData를 builder가 만들고 렌더러는 포맷만 그리는 구조이며, 라인 합과 합계 행 일치를 검증해 불일치 시 명세서를 아예 생성하지 않는다. 금액은 원 단위 절사 함수를 거치며 '라인 절사 후 합산' 순서로 footer와 일치시킨다.

## Concepts
- 정산 명세서 PDF
- 합계 일치 검증
- builder/렌더러 분리
- 수수료 원 단위 절사
