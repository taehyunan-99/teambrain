---
created: 2025-10-08
tags: [pr-review, raw-dump, infra, autoscaling, k8s]
pr: 31
---

# PR #31 — feat: 결제 API HPA(오토스케일) 도입 + resource requests/limits 조정

> 작성: 강민석 / 리뷰: 정유진 / 머지: 2025-10-09

**정유진 (k8s/payment-api/hpa.yaml:12)**: maxReplicas 10인데 — 파드 하나당 DB 커넥션을 몇 개씩 잡죠? 10개로 스케일아웃되면 ProxySQL 풀이랑 MySQL max_connections 그만큼 감당되나요. 같이 계산해야 해요. 트래픽 받겠다고 스케일했는데 DB 커넥션 고갈로 다 같이 죽는 게 최악
**강민석**: 파드당 풀 20개로 잡고 있어요. 10×20=200인데 ProxySQL이 앞에서 멀티플렉싱하니까 실제 백엔드 커넥션은 그보다 훨씬 적고... 아 근데 maxReplicas만 보고 산정 안 했네요. ProxySQL max_connections랑 MySQL max_connections 기준으로 역산해서 maxReplicas 다시 잡을게요
**정유진**: 넵. ProxySQL 백엔드 풀이 지금 얼마인지 확인하고, max 파드 × 파드당 풀 ≤ ProxySQL 수용량이 되도록. 안 되면 maxReplicas 낮추거나 ProxySQL부터 올리고요
**강민석**: ProxySQL 백엔드 풀 25, MySQL max_connections 100이에요. 파드당 풀을 20→10으로 줄이고 maxReplicas는 8로 낮췄어요. 8×10=80 < 100. ProxySQL이 앞단에서 멀티플렉싱하니 실제 백엔드는 더 여유 있고요. 산정식 hpa.yaml 주석에 적어둠

**정유진 (k8s/payment-api/hpa.yaml:28)**: scaleDown stabilizationWindowSeconds가 0이네요. 이러면 CPU 잠깐 떨어질 때마다 바로 축소돼서 플래핑 나요. 트래픽 출렁이면 파드가 늘었다 줄었다 반복하다가 콜드스타트 비용만 계속 나가요
**강민석**: 아 맞다. scaleDown은 300초(5분)로 두고 scaleUp은 빠르게(0초)로 비대칭 설정할게요. 늘릴 땐 즉시, 줄일 땐 천천히
**정유진**: 그게 맞아요. 결제는 늦게 줄여서 생기는 약간의 비용 < 모자라서 생기는 장애. scaleUp policy도 한번에 너무 공격적으로 안 늘게 percent/pods 정책 확인해주세요
**강민석**: scaleUp은 60초마다 최대 100%(2배)까지, scaleDown은 300초 윈도우에 최대 50%로 제한 걸었어요

**정유진 (k8s/payment-api/deployment.yaml:40)**: requests.cpu 100m / limits.cpu 500m — HPA가 averageUtilization 기준이면 requests 값이 분모예요. 100m 너무 낮게 잡으면 살짝만 받아도 utilization 폭등해서 과하게 스케일됨. 실측 idle/peak 보고 잡았어요?
**강민석**: 스테이징 부하테스트 기준 평상시 한 파드가 200~250m 정도 써요. requests를 250m로 올리고 limits 500m 유지. targetCPUUtilization 70%로 잡았어요
**정유진**: 넵 그 정도면 합리적. memory도 requests/limits 같이 잡혀있는지만 확인
**강민석**: memory requests 256Mi / limits 512Mi 들어가 있어요

**정유진**: 좋네요. maxReplicas DB 커넥션 역산 + scaleDown 윈도우 둘 다 반영됐고 requests 실측 기반이라 괜찮아요. 배포는 트래픽 적은 시간대에 하고, 일주일은 HPA 동작이랑 ProxySQL 커넥션 알람 같이 보죠. approve 👍
**강민석**: 넵 머지하고 알람 대시보드 링크 공유할게요
