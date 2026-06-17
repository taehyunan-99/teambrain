---
created: 2025-06-09
channel: infra
tags: [slack, raw-dump, infra, redis, monitoring, ops-chatter]
---

# slack #infra 2025-06-09

**16:40 강민석**: redis exporter에 메트릭 몇 개 더 붙였어요. used_memory랑 connected_clients만 있었는데 keyspace hits/misses랑 evicted_keys도 긁어오게 했어요
**16:42 정유진**: 오 evicted_keys 좋네요. allkeys-lru라 메모리 차면 알아서 밀어내는데 그게 얼마나 도는지 눈으로 보고 싶었어요
**16:43 강민석**: 지금은 거의 0이에요. 세션이랑 캐시 정도라 메모리 한참 여유 있고
**16:44 정유진**: ㅇㅇ 지금이야 한가하죠. 나중에 키 많이 쌓이는 용도 붙으면 그때 evict 추이 봐야 할 거예요
**16:45 강민석**: 넵 일단 수집은 해두는 걸로. 보는 화면은 나중에 정리하죠
**16:46 정유진**: 👍 raw 메트릭이라도 있는 게 어디예요
