---
created: 2024-09-07
tags: [slack, raw-dump, ops, http, monitoring]
channel: infra
---

# slack #infra 2024-09-07

**14:30 강민석**: HTTP 클라이언트 timeout 알람이 오탐으로 새벽에 세 번 울렸어요

**14:32 정유진**: HTTP timeout 임계치가 얼마예요?

**14:33 강민석**: read timeout이 5초인데 외부 API 호출이 4.8초 나오는 게 가끔 있어요

**14:34 정유진**: 오탐은 아닌 것 같은데요. 헬스체크랑 별개 알람이죠?

**14:35 강민석**: 헬스체크는 정상이에요. 외부 API 전용 모니터링에서만 나오는 거예요. timeout 임계치 7초로 올릴게요
