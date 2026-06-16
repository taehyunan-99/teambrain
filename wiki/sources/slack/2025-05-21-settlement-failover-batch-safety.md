---
type: source
of: raw/slack/2025-05-21-settlement-failover-batch-safety.md
source_hash: 684d0e34022df0784480575e404b7c129e12f639
tags: [source]
---

## Summary
MySQL HA 페일오버가 04:00 정산 배치 중 발생하면 배치가 중단돼 정산이 부분 처리되는 문제를 논의했다. 재실행 시 이미 확정된 명세서를 다시 만들면 회계 정합성이 깨지므로, DB 레벨 복합 유니크 가드가 없는 현재 구조를 보완하고 인프라 합의에 배치 재실행 절차를 포함하기로 했다.

## Concepts
- 페일오버 정책
- 정산 자동화
- 멱등성
- 중복 결제
