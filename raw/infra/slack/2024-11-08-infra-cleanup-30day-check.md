---
created: 2024-11-08
tags: [slack, raw-dump, ops, cleanup, disk]
channel: infra
---

# slack #infra 2024-11-08

**10:10 infra-bot**: [log-cleanup] 실행 결과 (02:00 KST)
- 오늘 삭제 대상 없음 (30일 이상 파일 없음)
- df -h: log-server-01 42% used
**10:20 강민석**: 오늘은 삭제 파일 없네요. cleanup이 제때제때 돌아서 30일 된 게 쌓이지를 않아요
**10:22 정유진**: 그래도 cron 자체는 정상 실행되고 있으니까 ok. 0건도 정상 결과예요