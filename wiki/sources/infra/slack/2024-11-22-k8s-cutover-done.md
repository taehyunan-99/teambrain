---
type: source
of: raw/infra/slack/2024-11-22-k8s-cutover-done.md
source_hash: e6a2491ca3c3bc71a1683723070369bef32a8dd2
tags: [source]
---

## Summary
강민석이 결제 API의 K8s 컷오버 완료를 #infra에 공유했다. 신규 클러스터로 트래픽을 모두 넘겼고 Deployment replica 2개가 Running, readiness/liveness 통과, 테스트 결제 정상이며 에러레이트도 안정적이었다. 기존 단일 서버는 트래픽만 끊고 일주일 관찰 후 내리기로 했고, 다음 작업으로 pod 단위 메트릭·알람 강화를 잡았다.

## Concepts
- Kubernetes 마이그레이션
- 단일 장애점(SPOF)
- 관측성 대시보드
