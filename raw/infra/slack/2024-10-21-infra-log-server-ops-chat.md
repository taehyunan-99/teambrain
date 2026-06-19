---
created: 2024-10-21
tags: [slack, raw-dump, ops, infra, chat]
channel: infra
---

# slack #infra 2024-10-21

**16:44 강민석**: 오늘 로그 서버 /var/log 용량 한 번 봤는데
- access.log.gz 파일들: 합산 2.1GB
- 앱 로그 .gz 파일들: 합산 1.8GB
- 합계 약 4GB. 서버 전체 200GB 대비 2% 수준
**16:46 정유진**: 생각보다 별로 없네요. compress 효과가 확실히 있어요
**16:47 강민석**: 정리 안 하면 어느 순간 확 늘어날 수 있으니까 cleanup 계속 돌리는 게 맞긴 하죠
**16:48 정유진**: ㅇㅇ. 지금은 여유 있으니까 모니터링만 계속하면 될 듯