---
created: 2024-09-04
tags: [slack, raw-dump, ops, redis, monitoring]
channel: infra
---

# slack #infra 2024-09-04

**13:10 강민석**: Redis Sentinel 헬스체크 timeout 알람이 새벽에 한 번 울렸어요

**13:12 정유진**: 오탐인가요 실제 문제인가요

**13:13 강민석**: 오탐이에요. Sentinel이 리더 선출 하는 동안 잠깐 응답이 늦어진 건데 임계치 안에 걸린 거예요

**13:14 정유진**: 모니터링에서 Sentinel 선출 이벤트 제외하는 필터 설정 가능해요?

**13:15 강민석**: Prometheus에서 레이블 필터로 제외하면 될 것 같아요. 오탐 줄이는 방향으로 임계치도 같이 검토할게요
