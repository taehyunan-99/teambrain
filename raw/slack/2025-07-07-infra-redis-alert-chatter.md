---
created: 2025-07-07
tags: [slack, raw-dump, redis, infra, ops]
channel: infra
---

# slack #infra 2025-07-07

**09:48 강민석**: 새벽 3시쯤 redis connected_clients 알람 한번 울렸었네요
잠깐 튀고 바로 내려왔어요
**09:50 정유진**: 그거 배치 도는 시간이랑 겹쳤을걸요 일시적인거
**09:51 강민석**: 네 임계치를 좀 빡빡하게 잡아놨나봐요. 알람 thresh 살짝 올릴게요
**09:52 이준호**: 멱등키 쪽은 멀쩡하죠? idem: prefix 키들
**09:53 강민석**: 네 그쪽은 used_memory도 평소랑 똑같아요 문제없음
**09:53 이준호**: 굿 👍
