---
created: 2024-10-18
tags: [slack, raw-dump, ops, monitoring, alarm]
channel: infra
---

# slack #infra 2024-10-18

**14:20 정유진**: Prometheus 디스크 알람 조건 다시 확인해봤어요
- log-server-01: 43%, 경고 기준 60% → 여유 17%p
- 알람 울리려면 한참 더 차야 해요
**14:22 강민석**: compress 이후로 로그 서버 증가 속도가 많이 줄었어요. df 트렌드 보면 주당 0.5%p 이하
**14:23 정유진**: 좋네요. 이 속도면 60% 경고 임계치 도달하는 게 몇 달은 걸리겠다
**14:24 강민석**: 당분간 신경 끄고 있어도 될 것 같아요. cleanup 스크립트도 잘 돌고 있으니까