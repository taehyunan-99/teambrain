---
created: 2025-07-07
channel: infra
tags:
  - slack
  - raw-dump
  - infra
  - ops
  - redis
---

# slack #infra 2025-07-07

**09:48 정유진**: 주말 redis used_memory 슬쩍 봤는데 안정적이네요. TTL 24h라 쌓였다 빠졌다 잘 함
**09:50 강민석**: 네 패널상 피크가 평일 낮인데 그래도 인스턴스 메모리 대비 여유 많아요
**09:51 정유진**: 굿. 지금 정책 allkeys-lru로 잡아둔 거라 꽉 차도 알아서 밀어내긴 하는데, 아직 그럴 규모는 아님
**09:53 강민석**: connected_clients도 평탄하고요. 일단 지켜보는 걸로
**09:54 정유진**: ㅇㅇ 임계치 알람은 추이 좀 더 보고 잡읍시다
