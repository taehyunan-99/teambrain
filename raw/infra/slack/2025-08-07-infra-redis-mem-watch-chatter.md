---
created: 2025-08-07
tags: [slack, raw-dump, redis, infra, ops]
channel: infra
---

# slack #infra 2025-08-07

**15:05 정유진**: prod-redis 메모리 어제도 피크에 88% 찍었네요. 점점 빡빡해지는 중
**15:06 강민석**: grafana에 used_memory 추이 보면 일주일째 우상향이에요. 평일 낮 트래픽이랑 같이 올라감
**15:08 정유진**: maxmemory 정책 noeviction이라 계속 이러면 한계 닿을 때 write 거부 떨어질 텐데. 정책 손볼지 한 번 봐야겠어요
**15:09 강민석**: prefix별로 뭐가 제일 먹는지 뽑아볼까요. 막연히 늘었다보다 어떤 키가 범인인지 보고 가는 게
**15:10 정유진**: 굿 그거 먼저 뽑아주세요. 결정은 데이터 보고
**15:11 강민석**: 넵 오늘 중에 prefix별 점유 정리해서 올릴게요
