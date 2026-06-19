---
created: 2024-11-07
tags: [slack, raw-dump, ops, syslog, disk]
channel: infra
---

# slack #infra 2024-11-07

**14:33 강민석**: syslog 로테이션 상태 확인해봤어요. /var/log/syslog 현재 크기 45MB. 어제 rotate 됐고
**14:35 정유진**: 45MB면 정상이에요. syslog는 앱 로그보다 훨씬 작죠
**14:36 강민석**: 전체 /var/log 용량은 약 12GB. 서버 df -h 기준 6% 수준
**14:37 정유진**: 6%면 무시해도 될 정도. 정리 스케줄 그대로 유지합시다