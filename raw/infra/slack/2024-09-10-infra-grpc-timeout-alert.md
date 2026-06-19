---
created: 2024-09-10
tags: [slack, raw-dump, ops, grpc, monitoring]
channel: infra
---

# slack #infra 2024-09-10

**15:20 강민석**: gRPC 통신 timeout 알람이 새벽에 오탐 떴어요

**15:22 정유진**: gRPC timeout 임계치가 얼마예요?

**15:23 강민석**: deadline이 3초인데 새벽 트래픽 낮을 때 서버 warm-up 시간이 걸려서요

**15:24 정유진**: 헬스체크는 정상이에요?

**15:25 강민석**: 헬스체크 별 이상 없었어요. gRPC 전용 알람만 울린 거예요. 모니터링에서 warm-up 필터 추가하거나 임계치 5초로 올릴게요
