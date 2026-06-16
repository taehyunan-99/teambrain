---
type: source
of: raw/settlement/pr/pr-058-fee-truncation.md
source_hash: a4a1a5f576b6dc7009f978401800cea15aa9585b
tags: [source]
---

## Summary
가맹점 1원 클레임을 계기로 수수료 계산을 반올림에서 원 단위 절사(표준약관 5조 2항)로 바꾼 PR. float 부동소수점 오차를 피해 decimal/정수 연산으로 강제하고, 33.0/33.4/33.9 경계값 회귀 테스트를 추가했다.

## Concepts
- 수수료 계산/반올림
- 수수료 원 단위 절사
- 부동소수점 오차 방지
- 경계값 회귀 테스트
