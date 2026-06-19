---
created: 2024-06-24
tags: [slack, raw-dump, ops, prometheus, monitoring]
channel: infra
---

# slack #infra 2024-06-24

**11:10 강민석**: Prometheus alert rule에 헬스체크 오탐 방지 로직 추가했어요. `for: 2m` 조건 넣어서 순간 timeout은 알람 안 가게요

**11:12 정유진**: 좋은데요. 새벽에 잠깐 timeout 걸리는 것들이 알람으로 오지 않게 되는 거죠?

**11:13 강민석**: 맞아요. 2분 지속되어야 알람 가게 되니까 오탐이 줄어요

**11:14 정유진**: 임계치는 그대로인 거죠? alert rule `for` 조건만 추가한 거죠?

**11:15 강민석**: 맞아요. 임계치는 그대로이고 지속시간 조건만 추가했어요. 모니터링 오탐 잡는 표준 패턴이에요
