---
type: source
of: raw/infra/2024-07-22-decision-infra-baseline.md
source_hash: a41d85d6f37df9b6878e8603b654459f81d88c44
tags: [source]
---

## Summary
결제 API와 MySQL이 단일 EC2 1대에 함께 올라간 단일 장애점(SPOF)·무모니터링·무백업 상태에서, 정유진이 단일 서버를 임시로 유지하되 리스크가 큰 항목부터 제거하기로 결정했다. 모니터링/알람 최소셋 3종(헬스체크·디스크·CPU)과 MySQL 일 1회 자동 백업을 즉시 도입하고, Q4까지 컨테이너 기반 전환으로 수동 SSH 배포를 폐기하는 단계적 인프라 베이스라인 원칙을 세웠다.

## Concepts
- 인프라 베이스라인
- 단일 장애점(SPOF)
- 관측성 대시보드
- 컨테이너화/CI
- MySQL HA/백업
