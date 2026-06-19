---
created: 2024-11-13
tags: [slack, raw-dump, ops, routine, disk]
channel: infra
---

# slack #infra 2024-11-13

**11:50 강민석**: 목요일 점검 완료. 로그 서버 df -h
```
/dev/sda1   200G   83G  117G  41% /
```
**11:52 정유진**: 여유 117GB. 충분해요. 이 추세 계속 유지합시다
**11:53 강민석**: cleanup cron 이번 주도 매일 정상 실행 확인했어요. 문제없습니다