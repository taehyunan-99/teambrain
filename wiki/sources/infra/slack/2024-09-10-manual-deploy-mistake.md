---
type: source
of: raw/infra/slack/2024-09-10-manual-deploy-mistake.md
source_hash: 747e90490fcfb9349a19378f0d5a8f8827e9c7b2
tags: [source]
---

## Summary
정유진이 수동 SSH 배포 중 잘못된 브랜치(feature/webhook-retry)를 prod에 올려 결제 API가 약 5분간 5xx를 낸 사고를 공유하고 즉시 롤백했다. 사람이 브랜치를 손으로 고르는 구조가 사고를 부른다는 데 동의해, 강민석과 Docker 이미지 빌드+CI 파이프라인(이미지 태그 기반 배포/롤백) 도입을 단계적으로 추진하기로 했다.

## Concepts
- 컨테이너화/CI
- Kubernetes 마이그레이션
- 인프라 베이스라인
