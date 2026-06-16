---
title: 오토스케일링 HPA (Autoscaling with HPA)
tags: [infra, autoscaling, hpa, kubernetes, payment-api]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2025-10-08-decision-autoscaling-hpa.md
  - raw/infra/pr/pr-infra-31-hpa-config.md
source_hashes:
  - bec72f6e934b3f9b781f541d1f1acf190e496832
  - a33d23a3209d66520a8380d1dd369ee1f30318ff
---

<!-- llmwiki:auto -->

## Summary
고정 replica 수동 스케일로 운영하던 결제 API에, 프로모션/이벤트 트래픽 급증 대응을 위해 HPA(Horizontal Pod Autoscaler)를 도입했다. CPU 사용률 70% 타깃, replica min 2 / max 10으로 시작하고, RPS 커스텀 메트릭을 보조 신호로 검토하며, max replica는 Redis/MySQL 다운스트림 커넥션 한도와 연동해 산정한다.

## Details
### 결정 — HPA 도입 (2025-10-08, 결정자 강민석)
결제 API는 고정 replica 3개 수동 스케일로 운영 중이었고, 프로모션/이벤트 구간 급증 시 응답 지연·타임아웃 우려와 야간·주말 대응 공백·온콜 부담이 배경이었다. K8s 위에서 운영 중이라 표준 오토스케일 적용이 가능했다.

검토한 대안: (1) 수동 스케일 유지(급증 대응 지연·온콜 부담), (2) Cluster Autoscaler만 적용(replica 자체는 안 늘고 노드 증설도 수 분 단위로 느림), (3) **HPA 도입(채택)**.

결정 세부:
- 타깃 메트릭: CPU 사용률 70%.
- 추가 메트릭: RPS 커스텀 메트릭 기반 스케일 검토(메트릭 어댑터 구성·임계치 산정 후 단계 적용).
- replica 범위: min 2 / max 10. (min 2로 단일 pod 장애 시에도 가용성, max 10은 당시 클러스터 노드 용량 기준 상한.)
- Cluster Autoscaler와 병행 가능하나 이번 결정 범위는 HPA(pod 레벨)로 한정.

근거: 결제 API 부하는 CPU와 강한 상관이라 CPU가 1차 신호로 적합. 단 요청량 급증을 CPU가 후행 반영하는 경우가 있어 RPS를 보조 신호로 검토. 핵심 리스크는 **"pod를 늘려도 Redis/DB 커넥션이 병목이면 효과가 제한"**되며, 커넥션 풀 상한을 넘는 증설은 DB 커넥션 고갈로 오히려 장애를 키울 수 있어 **max replica를 다운스트림 커넥션 한도와 연동해 산정**해야 한다는 점이다. CPU만 보면 I/O 대기 위주 부하에서 과소 스케일 가능(RPS 검토 사유), 스케일 인 시 graceful shutdown·연결 드레이닝 점검 필요.

### PR #31 리뷰 — HPA 설정 + resource 조정 (2025-10-08, 머지 10-09)
강민석이 올린 HPA 도입 + resource 조정 PR을 정유진이 리뷰하며 세 가지를 지적해 반영했다.

1. **maxReplicas ↔ DB 커넥션 한도 역산**: maxReplicas 10에서 파드당 풀 20이면 10×20=200. 정유진이 "트래픽 받겠다고 스케일했는데 DB 커넥션 고갈로 다 같이 죽는 게 최악"이라며 역산을 요구. 강민석이 ProxySQL 백엔드 풀 25, MySQL max_connections 100 기준으로 **파드당 풀 20 → 10, maxReplicas 10 → 8**로 조정(8×10=80 < 100). ProxySQL이 앞단에서 멀티플렉싱하므로 실제 백엔드는 더 여유. 산정식은 hpa.yaml 주석에 기록.
2. **scaleDown stabilizationWindow 0초 → 플래핑 위험**: 0이면 CPU가 잠깐 떨어질 때마다 즉시 축소돼 파드가 늘었다 줄었다 반복(콜드스타트 비용). **scaleUp 즉시(0초) / scaleDown 300초(5분) 비대칭** 설정으로. 정유진: "결제는 늦게 줄여서 생기는 약간의 비용 < 모자라서 생기는 장애." scaleUp은 60초마다 최대 100%(2배), scaleDown은 300초 윈도우에 최대 50% 제한.
3. **HPA averageUtilization 분모 = requests.cpu**: requests.cpu 100m이 너무 낮으면 살짝만 받아도 utilization 폭등해 과스케일. 스테이징 부하테스트 실측(평상시 파드당 200~250m) 기준 **requests 250m로 상향, limits 500m 유지, targetCPUUtilization 70%**. memory는 requests 256Mi / limits 512Mi.

배포는 트래픽 적은 시간대에, 일주일은 HPA 동작과 ProxySQL 커넥션 알람을 함께 관찰하기로 했다.

> 메모: 결정문서의 max 10은 PR #31에서 DB 커넥션 역산으로 8로 낮춰졌고, 이후 [[promo-capacity-planning]]에서 프로모션 대비 10→20(공지)으로 상향됐다. 사전점검 회의(2026-02-04)에서는 당시 운영 기준이 min 3 / max 10으로 언급되며 20~25 상향 + 당일 min 임시 상향(워밍업)이 논의됐다.

## Related
HPA는 [[kubernetes-migration]]에서 replica 2개 고정으로 미뤄둔 오토스케일을 실현한 것이다. max replica 산정은 [[mysql-ha-failover]]의 ProxySQL 커넥션 풀·MySQL max_connections, 그리고 [[redis-introduction]]의 커넥션 한도와 연동된다. 프로모션 대비 maxReplicas 상향·당일 워밍업·다운스트림 동시 증설은 [[promo-capacity-planning]]에서 다룬다.
