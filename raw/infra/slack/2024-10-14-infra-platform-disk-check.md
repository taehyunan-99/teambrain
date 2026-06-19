---
created: 2024-10-14
tags: [slack, raw-dump, ops, disk, platform]
channel: infra
---

# slack #infra 2024-10-14

**11:05 강민석**: 플랫폼 서버들 디스크 현황 같이 공유합니다
- k8s-worker-01: 36%
- k8s-worker-02: 39%
- log-server-01: 43%
- db-server-01: 22%
**11:07 정유진**: 전반적으로 여유롭네요. k8s 노드들이 40% 안 넘게 유지되고 있어요
**11:08 강민석**: 로그 서버만 좀 높은 편인데 cleanup + compress 적용하면 내려올 것 같아요
**11:09 정유진**: df 결과 주간 공유하는 거 좋은 것 같으니까 계속해요