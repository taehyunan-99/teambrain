---
created: 2024-09-18
tags: [slack, raw-dump, ops, db, disk]
channel: infra
---

# slack #infra 2024-09-18

**13:40 강민석**: db-server-01 디스크 현황 공유해요
- /dev/sda1: 22% used (OS + 바이너리)
- /dev/sdb1: 35% used (MySQL 데이터)
**13:42 정유진**: DB 서버는 여유롭네요. 용량 걱정 없을 것 같아요
**13:43 강민석**: 데이터 보존 정책이 엄격해서 삭제가 거의 없어요. 증가 속도가 월 1~2% 수준이에요
**13:44 정유진**: 이 정도면 당분간 cleanup 같은 건 필요 없겠어요. 로그 서버랑 성격이 다르네요