---
type: source
of: raw/infra/pr/pr-infra-12-k8s-manifests.md
source_hash: 1c02407aaaad90aac2c6f696d4f06ef3febfb030
tags: [source]
---

## Summary
강민석이 올린 결제 API K8s 매니페스트(Deployment/Service/ConfigMap) PR #12를 정유진이 리뷰했다. readinessProbe 누락(PG 핑+설정 로딩 확인용 /readyz 분리), resources requests/limits 누락(노드 OOM 전파 방지), ConfigMap에 시크릿 분리 여부를 지적해 모두 반영하고, 구 서버 병행 운영 후 readiness 확인 시 LB 가중치를 옮기는 무중단 컷오버 방식에 합의했다.

## Concepts
- Kubernetes 마이그레이션
- 컨테이너화/CI
