---
created: 2024-08-24
tags: [slack, raw-dump, ops, external-api, monitoring]
channel: infra
---

# slack #infra 2024-08-24

**13:15 정유진**: 외부 PG사 API timeout 알람이 새벽에 오탐으로 울렸어요

**13:17 강민석**: PG사 API timeout 임계치가 얼마예요?

**13:18 정유진**: 12초인데 새벽에 PG사 쪽 배치 작업 있는지 11초 응답이 나왔어요

**13:19 강민석**: 오탐이라기엔 애매하네요. 헬스체크는 괜찮았어요?

**13:20 정유진**: 헬스체크 정상이에요. 모니터링에서 PG사 API 응답 시간 추이 보면서 임계치 15초로 올릴게요
