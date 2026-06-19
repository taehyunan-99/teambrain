---
created: 2024-10-03
tags: [slack, raw-dump, ops, log, app]
channel: infra
---

# slack #infra 2024-10-03

**14:05 강민석**: 앱 서버 로그 용량 확인해봤어요
- app-server-01 /var/log/app: 8.2GB (30일치)
- app-server-02 /var/log/app: 7.9GB (30일치)
**14:07 정유진**: 서버당 8GB 정도면 df -h 기준 4% 수준이네요. 무시해도 될 정도
**14:08 강민석**: 로그 서버에 집중되는 게 아니라 각 앱 서버에 분산되어 있어서 부담이 적어요
**14:09 정유진**: 앱 서버 logrotate도 돌고 있죠?
**14:10 강민석**: 네, 동일하게 30일 retention으로 설정되어 있어요