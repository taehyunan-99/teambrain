---
type: source
of: raw/infra/2024-09-16-decision-containerize-ci.md
source_hash: 5dc2ac374d4b60a24e7d3bbf82939ccab37d365c
tags: [source]
---

## Summary
2024-09-10 수동 배포 사고(잘못된 브랜치 기동으로 결제 approve 약 5분 응답 실패)를 계기로, 강민석이 결제 API 컨테이너화 및 CI 파이프라인 도입을 결정했다. 1단계로 Docker 멀티스테이지 이미지 빌드와 CI의 build/test/image push 자동화(테스트 실패 시 머지 차단)를 도입하고, 오케스트레이션(K8s)은 Q4에 후행하는 단계적 접근을 채택했다.

## Concepts
- 컨테이너화/CI
- Kubernetes 마이그레이션
- 인프라 베이스라인
