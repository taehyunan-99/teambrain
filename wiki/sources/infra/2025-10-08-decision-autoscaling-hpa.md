---
type: source
of: raw/infra/2025-10-08-decision-autoscaling-hpa.md
source_hash: bec72f6e934b3f9b781f541d1f1acf190e496832
tags: [source]
---

## Summary
고정 replica(3개) 수동 스케일로 운영하던 결제 API에, 프로모션/이벤트 트래픽 급증 대응을 위해 강민석이 HPA(Horizontal Pod Autoscaler) 도입을 결정했다. CPU 사용률 70% 타깃, replica 범위 min 2/max 10으로 설정하고, RPS 커스텀 메트릭을 보조 신호로 검토하며, Redis/MySQL 다운스트림 커넥션 한도와 연동해 max replica를 산정해야 한다는 점을 명시했다.

## Concepts
- 오토스케일링 HPA
- Kubernetes 마이그레이션
- Redis 도입
- MySQL HA/백업
