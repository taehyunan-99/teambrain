---
created: 2024-11-12
tags: [pr-review, raw-dump, infra, kubernetes, deployment]
pr: 12
---

# PR #12 — feat: 결제 API K8s 매니페스트 (Deployment/Service/ConfigMap)

> 작성: 강민석 / 리뷰: 정유진 / 머지: 2024-11-12

**정유진 (deployment.yaml:34)**: livenessProbe만 있고 readinessProbe가 없네요. 이러면 파드가 뜨자마자 Service 엔드포인트에 등록돼서 아직 PG 커넥션 풀이나 설정 로딩이 안 끝났는데도 트래픽을 받아요. 결제 API라 컷오버 중에 이게 터지면 승인 요청 떨굽니다. readiness 꼭 넣어주세요
**강민석**: 아 맞다 liveness만 보고 readiness를 빼먹었네요. /healthz는 liveness(프로세스 살아있나)용으로 두고 /readyz를 따로 만들어서 PG 핑 + 설정 로딩 완료 체크하게 분리할게요
**정유진**: 네 그게 맞아요. /readyz는 외부 의존성(토스 어댑터 핑) 확인까지만 하고 너무 무겁게 만들진 마세요. readiness가 죽으면 트래픽만 끊기면 되는 거지 파드 재시작될 필요는 없으니까
**강민석**: ㅇㅋ readinessProbe 추가하고 initialDelay 5s, period 10s로 잡았어요
**정유진 (deployment.yaml:50)**: resources에 limit/request가 아예 없어요. 이거 안 잡으면 한 파드가 노드 메모리 다 먹어서 같은 노드의 다른 파드까지 OOM으로 끌고 갈 수 있어요. 무중단 컷오버 중에 옛날 파드랑 새 파드가 같은 노드에 뜰 텐데 더 위험하구요
**강민석**: requests/limits 둘 다 넣을게요. 현재 단일 서버 기준으로 평소 메모리 300MB 안쪽이라 requests 512Mi / limits 1Gi, cpu requests 250m / limits 1 정도로 시작하면 될까요
**정유진**: 시작값은 그 정도면 됨. 컷오버 끝나고 실측 보고 조정하죠. limit은 너무 빡빡하게 잡으면 throttle 걸리니 일단 여유 두는 게 나아요
**강민석**: 반영했습니다. readinessProbe + resources requests/limits 둘 다 들어갔어요
**정유진 (configmap.yaml:8)**: ConfigMap에 PG 시크릿 키 들어있는 거 아니죠?
**강민석**: 넵 그건 Secret으로 따로 뺐고 ConfigMap엔 엔드포인트 URL이랑 타임아웃 값 같은 비밀 아닌 설정만 있어요
**정유진**: 좋아요. 컷오버는 매니페스트 머지하고 새 클러스터에 띄운 다음, 구 서버랑 병행 띄워놓고 트래픽 수동으로 넘기는 순서로 가죠. readiness 정상 확인되면 그때 LB 가중치 옮길게요
**강민석**: ㅇㅋ 새 파드 readyz 다 green 뜨는 거 확인하고 넘기겠습니다
**정유진**: approve 👍
