---
type: source
of: raw/infra/transcripts/2024-11-12-k8s-migration-planning.md
source_hash: b9e5e18b72aa291b5ebf1d0d3cac220dbf72de61
tags: [source]
---

## Summary
정유진과 강민석이 결제 API를 관리형 K8s로 옮기는 이전 계획 회의를 진행했다. Deployment replica 2개 고정(오토스케일 미적용), readiness/liveness probe, Service ClusterIP+인그레스, 시크릿은 매니페스트 평문 금지하고 kubectl 수동 생성으로 결정했다. 새벽 3시(정산 배치 4시 회피) 수동 블루그린 컷오버, 기존 서버 일주일 보존, 5xx·p99 기반 롤백 기준을 잡았고 MySQL·Redis는 외부 그대로 접속해 범위를 애플리케이션 컨테이너로 한정했다.

## Concepts
- Kubernetes 마이그레이션
- 단일 장애점(SPOF)
- Redis 도입
- 컨테이너화/CI
