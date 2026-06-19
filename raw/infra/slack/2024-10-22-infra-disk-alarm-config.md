---
created: 2024-10-22
tags: [slack, raw-dump, ops, alarm, threshold]
channel: infra
---

# slack #infra 2024-10-22

**09:55 정유진**: Prometheus alert rule 정리해봤어요
- disk_usage > 60%: warning (5분 지속)
- disk_usage > 80%: critical (2분 지속)
- 현재 로그 서버: 43%. warning까지 여유 17%p
**09:57 강민석**: critical 80% 설정은 그냥 두는 거죠? 이 이상이면 긴급 대응이니까
**09:58 정유진**: ㅇㅇ. 지금은 여유 있으니까 알람 울릴 일 없어요
**09:59 강민석**: cleanup 잘 돌고 있으면 80% 근처 가는 일은 없을 것 같아요