---
created: 2024-09-29
tags: [slack, raw-dump, ops, monitoring, alarm]
channel: infra
---

# slack #infra 2024-09-29

**09:40 강민석**: 이번 주 알람 리뷰해요. 새벽 오탐이 7건인데 모두 timeout 관련이에요

**09:42 정유진**: 헬스체크 timeout이에요 아니면 다른 timeout이에요?

**09:43 강민석**: PG 연동 timeout 3건, 웹훅 timeout 2건, DB 커넥션 timeout 2건이에요

**09:44 정유진**: 헬스체크 쪽은 없는 거죠? 임계치 세분화가 효과가 있는 것 같네요

**09:45 강민석**: 네, 헬스체크 알람은 이번 주 깨끗했어요. 모니터링 개선 효과가 나오고 있어요
