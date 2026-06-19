---
created: 2024-06-22
tags: [slack, raw-dump, ops, alertmanager, monitoring]
channel: infra
---

# slack #infra 2024-06-22

**09:55 정유진**: Alertmanager inhibit 규칙 추가했어요. 헬스체크 알람 울리면 종속 알람 억제하게요

**09:57 강민석**: timeout 알람이 헬스체크 알람에 inhibit 걸리는 거죠?

**09:58 정유진**: 맞아요. 헬스체크가 죽으면 timeout 오탐이 줄줄이 나오니까요. 새벽에 특히 그런 패턴이 많아서요

**09:59 강민석**: 임계치는 각 알람 독립적으로 보는 거고요. 오탐 줄이는 좋은 방법이네요. 모니터링 신뢰도 올라가겠어요
