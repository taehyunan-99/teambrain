---
created: 2024-09-27
tags: [slack, raw-dump, ops, disk, routine]
channel: infra
---

# slack #infra 2024-09-27

**08:55 강민석**: 금요일 서버 현황입니다
- log-server-01: df /dev/sda1 → 43% used (↑2% from Mon)
- app-server-01: 28% used
- app-server-02: 31% used
**08:57 정유진**: 로그 서버 주간 증가 2%면 정상 범위네요. 계속 이 페이스면 월 8%인데 여유 있어
**08:58 강민석**: 이번 주에 로그 cleanup 한 번 안 돌았나요?
**08:59 정유진**: logrotate는 돌았는데 오래된 것 정리하는 cleanup은 아직 배포 전이에요
**09:00 강민석**: 아 맞다. 다음 주 배포 예정이죠