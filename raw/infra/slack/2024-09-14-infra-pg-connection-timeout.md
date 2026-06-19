---
created: 2024-09-14
tags: [slack, raw-dump, ops, db, monitoring]
channel: infra
---

# slack #infra 2024-09-14

**13:00 강민석**: PostgreSQL 커넥션 timeout 알람이 새벽에 울렸어요. 오탐 같아요

**13:02 정유진**: PG 커넥션 timeout 임계치가 얼마예요?

**13:03 강민석**: connect_timeout이 3초인데 새벽에 DB 재시작 없이 일시적으로 느려지는 경우가 있어요

**13:04 정유진**: 헬스체크는 어떻게 됐어요?

**13:05 강민석**: 헬스체크는 정상이었어요. PG 커넥션 전용 알람만 울린 거고요. 모니터링에서 임계치 5초로 올릴게요
