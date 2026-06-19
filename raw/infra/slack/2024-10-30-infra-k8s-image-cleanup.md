---
created: 2024-10-30
tags: [slack, raw-dump, ops, k8s, cleanup]
channel: infra
---

# slack #infra 2024-10-30

**14:15 강민석**: k8s-worker-02 디스크 확인해봤어요. 컨테이너 이미지 캐시가 18GB 쌓여있었어요
**14:16 강민석**: `docker image prune -a --filter until=168h` 로 정리했더니 40% → 33%로 내려갔네요
**14:18 정유진**: 이미지 cleanup은 주기적으로 해줘야 하는데 자동화 안 되어 있었나요?
**14:19 강민석**: 로그 서버 cleanup은 자동인데 k8s 쪽은 cron 안 걸어놨었어요
**14:21 정유진**: 이번 주에 k8s 노드도 이미지 정리 cron 추가합시다. 용량 관리는 서버마다 일관되게 가야 해요