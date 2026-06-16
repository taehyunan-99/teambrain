---
type: source
of: raw/settlement/slack/2025-02-18-fee-rounding-dispute.md
source_hash: d1aff1b02f3aa82d87393e31e4446772c7008ebb
tags: [source]
---

## Summary
가맹점 두 곳에서 정산 명세서 금액이 계약서와 1~2원 차이난다는 CS가 들어온 슬랙. 코드는 HALF_UP 반올림인데 약관 기준(절사 여부)이 확인 안 돼, 영업팀에 표준약관을 확인하고 반올림 vs 절사로 정산액이 달라지는 건수를 정산 시작 시점부터 누적 집계하기로 했다.

## Concepts
- 수수료 계산/반올림
- 1원 오차 클레임
- 약관 기준 확인
- 회계 정합성
