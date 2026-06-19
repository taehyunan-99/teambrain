---
created: 2024-09-30
tags: [slack, raw-dump, ops, logrotate, cron]
channel: infra
---

# slack #infra 2024-09-30

**13:15 강민석**: logrotate cron 잘 돌고 있는지 확인했어요. /etc/cron.daily/logrotate 타임스탬프 정상
**13:17 정유진**: 서버 로그 /var/log/syslog rotate 됐고, 오래된 .gz 파일들 용량 보니까 총 1.2GB 정도
**13:18 강민석**: 디스크 전체 용량이 200GB니까 그 정도면 무시해도 되는 수준이네요
**13:20 정유진**: 그렇죠. 당분간 cleanup 스크립트 없어도 괜찮을 것 같아요. 여유 있으니까