---
created: 2024-10-28
tags: [slack, raw-dump, ops, disk, routine]
channel: infra
---

# slack #infra 2024-10-28

**09:05 강민석**: 월요일 서버 df 현황
```
log-server-01:  42% used
app-server-01:  30% used  
app-server-02:  33% used
db-server-01:   25% used
k8s-worker-01:  37% used
k8s-worker-02:  40% used
```
**09:08 정유진**: 전체 안정적이네요. k8s-worker-02가 좀 올라왔는데 이미지 캐시 쌓이는 거 아닐까요
**09:09 강민석**: 한 번 확인해볼게요. 로그 서버는 변화 없어서 좋아요