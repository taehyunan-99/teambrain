---
title: Kubernetes 마이그레이션 (Kubernetes Migration)
tags: [infra, kubernetes, k8s, containerization, ci, deployment]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2024-09-16-decision-containerize-ci.md
  - raw/infra/slack/2024-09-10-manual-deploy-mistake.md
  - raw/infra/transcripts/2024-11-12-k8s-migration-planning.md
  - raw/infra/pr/pr-infra-12-k8s-manifests.md
  - raw/infra/slack/2024-11-22-k8s-cutover-done.md
source_hashes:
  - 5dc2ac374d4b60a24e7d3bbf82939ccab37d365c
  - 747e90490fcfb9349a19378f0d5a8f8827e9c7b2
  - b9e5e18b72aa291b5ebf1d0d3cac220dbf72de61
  - 1c02407aaaad90aac2c6f696d4f06ef3febfb030
  - e6a2491ca3c3bc71a1683723070369bef32a8dd2
---

<!-- llmwiki:auto -->

## Summary
수동 SSH 배포 사고를 계기로 결제 API를 컨테이너화하고 CI 파이프라인을 도입한 뒤, 단계적으로 관리형 Kubernetes로 오케스트레이션을 전환했다. K8s는 컨테이너화/CI를 1단계로 안정화한 다음 후행했으며, replica 2개 고정·readiness/liveness probe·새벽 수동 블루그린 컷오버로 무중단 이전을 완료했다.

## Details
### 계기 — 수동 배포 사고 (2024-09-10)
정유진이 SSH 수동 배포 중 의도와 다른 브랜치(`feature/webhook-retry`)를 prod에 올려 결제 approve 엔드포인트가 약 5분간 5xx를 냈고, 직전 정상 빌드로 즉시 롤백했다. 원인은 사람이 브랜치 선택·빌드·기동을 수기로 수행하는 구조(서버에서 `git pull` 후 systemd/pm2 재기동, 빌드가 서버 상태에 의존해 재현성 낮음)였다. 정유진·강민석은 "사람이 브랜치를 손으로 고르는 한 또 터진다"는 데 동의하고, Docker 이미지 빌드 + CI(이미지 태그 기반 배포/롤백)를 도입하기로 했다.

### 결정 — 컨테이너화/CI 먼저, 오케스트레이션 후행 (2024-09-16)
강민석이 결정자로서 단계적 접근(대안 C)을 채택했다. 검토한 대안은 A(systemd+배포스크립트 보완, 재현성 미확보로 탈락), B(바로 K8s 직행, 도입 표면적이 넓어 단기 안정성 리스크 큼), C(컨테이너화+CI 먼저, K8s는 Q4 후행)였다.

1단계 도입 내용:
- 결제 API를 Docker 멀티스테이지 이미지로 빌드(런타임 이미지 경량화).
- CI에서 build → test(실패 시 머지 차단) → image push(main 머지 시 커밋 SHA + 환경 태그로 레지스트리 푸시) 자동화.
- 배포는 서버 직접 `git pull`/빌드 흐름을 제거하고 푸시된 이미지를 기동하는 방식으로 전환.

근거는 "컨테이너화는 어차피 K8s의 선행 작업이므로 이미지/CI를 먼저 안정화한 뒤 오케스트레이션으로 넘어가는 단계적 접근이 리스크 대비 효율이 높다"였다.

### 이전 계획 회의 (2024-11-12)
정유진·강민석이 결제 API를 관리형 K8s로 옮기는 계획을 잡았다.
- **워크로드**: Deployment 1 + Service 1. 기존에 이미 프로세스 2개로 운영 중이었으므로 replica 2개 고정으로 시작하고, 오토스케일은 이번 범위에서 제외("처음부터 오토스케일까지 같이 넣으면 뭐가 문제인지 구분이 안 된다"). 안정화 후 HPA를 별도로 얹기로 했다.
- **probe**: readiness/liveness 둘 다 필수. 기존 `/healthz`는 200만 던져 DB 연결을 보지 않으므로, readiness용으로 DB·Redis 핑까지 보는 엔드포인트를 결제팀(이준호)과 조율하기로 했다.
- **네트워크/시크릿**: Service는 ClusterIP + 인그레스. 시크릿은 매니페스트 평문 금지, `kubectl` 수동 생성.
- **컷오버**: 자동화 없이 수동 블루그린. 클러스터에 미리 띄워 헬스체크를 통과시킨 뒤 트래픽을 넘기되, LB 가중치로 조금씩 흘리는 방식을 시도하고 안 되면 한 번에 스위치하되 구 서버를 죽이지 않고 띄워둔다. 시점은 트래픽 최저인 새벽 3~4시, 단 정산 배치(04시)와 겹치지 않게. 롤백 기준은 5xx·p99.
- **범위 한정**: MySQL·Redis는 외부에 그대로 두고 접속만 유지해, 이번 전환 범위를 애플리케이션 컨테이너로 한정했다.

### PR #12 리뷰 — K8s 매니페스트 (2024-11-12)
강민석이 올린 Deployment/Service/ConfigMap PR을 정유진이 리뷰하며 세 가지를 지적해 모두 반영했다.
- **readinessProbe 누락**: liveness만 있어 파드가 뜨자마자 Service 엔드포인트에 등록돼 PG 커넥션 풀·설정 로딩이 끝나기 전에 트래픽을 받는 문제. `/healthz`(liveness, 프로세스 생존)와 `/readyz`(readiness, PG 핑+설정 로딩+토스 어댑터 핑까지)를 분리. initialDelay 5s / period 10s.
- **resources requests/limits 누락**: 미설정 시 한 파드가 노드 메모리를 다 먹어 같은 노드의 다른 파드를 OOM으로 끌고 갈 위험(컷오버 중 구·신 파드 동거 시 특히 위험). 시작값 memory requests 512Mi / limits 1Gi, cpu requests 250m / limits 1. (참고: 이후 [[autoscaling-hpa]] PR #31에서 cpu requests를 250m로, memory를 256Mi/512Mi로 재조정.)
- **ConfigMap 시크릿 분리**: PG 시크릿은 Secret으로 분리, ConfigMap엔 엔드포인트 URL·타임아웃 등 비밀 아닌 설정만.

컷오버는 매니페스트 머지 → 신 클러스터 기동 → 구 서버 병행 → readiness green 확인 후 LB 가중치 이동 순으로 합의했다.

### 컷오버 완료 (2024-11-22)
강민석이 K8s 컷오버 완료를 공유했다. 신 클러스터로 트래픽을 모두 넘겼고 Deployment replica 2개가 Running, readiness/liveness 통과, `/healthz` 200, 테스트 결제 정상, 에러레이트도 안정적이었다. 정유진이 무중단 전환과 에러레이트 안정을 확인했고("단일 서버 시대 끝"). 기존 단일 서버는 트래픽만 끊고 일주일 관찰 후 내리기로 했으며, 다음 작업으로 pod 단위 메트릭·알람 강화를 잡았다.

## Related
이 마이그레이션은 [[infra-baseline]]에서 정한 "단일 서버 임시·Q4 컨테이너 전환·수동 SSH 배포 폐기" 원칙의 실행이다. replica 고정으로 시작해 나중에 얹기로 한 오토스케일은 [[autoscaling-hpa]]에서 HPA로 구현됐고, 외부에 둔 데이터 계층은 [[mysql-ha-failover]]와 [[redis-introduction]]에서 별도 표준화됐다. pod 메트릭/알람 강화는 [[infra-baseline]]의 관측성 대시보드로 이어진다.
