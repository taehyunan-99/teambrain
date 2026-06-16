---
type: source
of: raw/settlement/slack/2025-09-25-duplicate-settlement-row.md
source_hash: 54114f72d07c609b9f52775d7137bc1a952b6f32
tags: [source]
---

## Summary
아침 검산에서 한 가맹점 정산액이 평소 2배로 잡힌 사고 슬랙. 원인은 중간에 멈춘 배치를 재실행할 때 기존 행을 지우지 않고 또 INSERT해 같은 (가맹점, 정산일) 행이 둘 생긴 것이었다. 코드 수정이 아니라 DB 차원에서 중복을 막는 방향을 찾기로 했다.

## Concepts
- 정산 복합 유니크 키
- 정산 멱등성
- 중복 정산 행 사고
- DB 제약 기반 정합성
