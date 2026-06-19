---
created: 2024-07-02
tags: [slack, raw-dump, ops, k8s, monitoring]
channel: infra
---

# slack #infra 2024-07-02

**14:00 정유진**: k8s liveness probe 설정 리뷰해줄 수 있어요? 헬스체크 관련인데요

**14:02 강민석**: `timeoutSeconds`가 1초로 돼 있는데 오탐 나오지 않아요?

**14:03 정유진**: 새벽에 간헐적으로 pod 재시작이 생겨서요. liveness probe timeout이 너무 짧아서 오탐으로 죽이는 것 같아요

**14:04 강민석**: 3초로 늘리세요. 알람 모니터링에서도 이 패턴 잡히게 해두면 좋겠어요. 임계치 설정도 같이요

**14:05 정유진**: liveness probe `timeoutSeconds: 3`으로 바꾸고 알람 추가할게요
