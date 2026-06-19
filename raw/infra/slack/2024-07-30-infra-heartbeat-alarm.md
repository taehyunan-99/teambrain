---
created: 2024-07-30
tags: [slack, raw-dump, ops, monitoring, alarm]
channel: infra
---

# slack #infra 2024-07-30

**10:00 정유진**: Heartbeat 알람이 새벽에 한 번 울렸어요. 오탐인 것 같아요

**10:02 강민석**: Heartbeat timeout 임계치가 얼마예요?

**10:03 정유진**: 30초인데 모니터링 에이전트가 잠깐 네트워크 이슈로 60초 침묵한 거예요

**10:04 강민석**: 헬스체크랑 다른 알람이에요. Heartbeat 임계치는 좀 넉넉하게 잡아야 해요

**10:05 정유진**: 60초로 늘릴게요. 오탐 없애는 게 우선이니까요
