---
created: 2025-08-12
channel: infra
tags: [redis, maxmemory, eviction, oom, alert, 멱등성, 결제팀협의]
---

# slack #infra 2025-08-12

**14:32 alert-bot**: 🚨 [WARN] redis-prod-01 used_memory 90.2% of maxmemory (5.4GB / 6GB)
threshold: 90% / duration: 5m
→ runbook: wiki/infra/redis-memory

**14:33 강민석**: 어 이거 계속 차오르네요
어제 85%였는데

**14:34 정유진**: 지금 추세면 저녁쯤 maxmemory 칠 듯
근데 우리 maxmemory-policy 뭐였죠

**14:35 강민석**: noeviction이요
설정 안 건드렸으면 디폴트일걸요

**14:36 강민석**:
```
config get maxmemory-policy
1) "maxmemory-policy"
2) "noeviction"
```
넵 noeviction 맞네요

**14:37 정유진**: 아 그럼 maxmemory 닿는 순간 write 다 거부됨
OOM command not allowed 떨어지면서 SET 막힘
이거 결제까지 영향 가요

**14:38 강민석**: ㅇㅇ 사실상 장애죠
읽기는 되는데 쓰기가 안 되니까

**14:39 정유진**: 일단 급한대로 allkeys-lru로 바꾸면 오래된 키부터 evict해서 OOM은 피하긴 하는데

**14:40 강민석**: 그쵸 그게 제일 간단한 처방이긴 한데

**14:41 정유진**: 잠깐
allkeys면 TTL 안 끝난 키도 LRU로 그냥 날려버리잖아요
우리 Redis에 TTL 내에 절대 유실되면 안 되는 키 있지 않나
결제팀 멱등성 키 그거 여기 들어가 있을 텐데

**14:42 강민석**: 아... 맞다
멱등성 키 TTL 24h짜리 그거요
그게 evict되면 같은 Idempotency-Key 들어와도 캐시 미스 나서

**14:43 정유진**: 중복 처리 위험 생기죠
allkeys-lru는 그래서 좀 위험할 듯
멱등키가 LRU상 오래됐다고 막 날아가면 안 됨

**14:44 강민석**: volatile-lru는 어때요
TTL 걸린 키 중에서만 evict
근데 멱등키도 TTL 걸려있어서 결국 대상에 들어가는 건 똑같지 않나요

**14:45 정유진**: 음 그러네
정책만으로는 멱등키만 콕 집어 살릴 수가 없네
어떤 키가 진짜 못 죽는 건지를 우리가 모름

**14:46 강민석**: 세션 키도 여기 있고 웹훅 재시도 큐 비슷한 것도 있고
뭐가 evict돼도 되고 안 되는지 결제팀이 알지 우린 모르죠

**14:47 정유진**: 그러니까 정책 바꾸기 전에 결제팀한테 먼저 물어봐야 함
지금 메모리 어디에 뭐가 얼마나 쌓여 있는지부터 좀 봐야겠다
강민석님 키 패턴별로 메모리 점유 좀 뽑아줄 수 있어요
`redis-cli --bigkeys` 돌리거나 키 프리픽스별로

**14:48 강민석**: 넵 돌려볼게요
idem: / sess: / 이런 프리픽스 기준으로 집계해서 올릴게요

**14:49 정유진**: 일단 급한 불은 maxmemory를 임시로 8GB로 올려서 시간 벌고
그 사이에 정책 결정합시다
6GB→8GB는 인스턴스 스펙상 여유 있죠

**14:50 강민석**: 있어요 메모리 16짜리라
지금 올릴게요

**14:51 정유진**: ㅇㅋ
그리고 #pay-dev에 핑 날릴게요
"Redis maxmemory 한계 임박, eviction 정책 검토 중인데 멱등성 키처럼 TTL 안에 절대 유실되면 안 되는 키 있는지 / 어떤 프리픽스가 그런지 알려달라" 이렇게

**14:52 강민석**: 👍 maxmemory 8GB 적용했어요
```
config set maxmemory 8gb
OK
```
used_memory 5.4GB / 8GB = 67%로 일단 떨어짐

**14:53 정유진**: 굿 한숨 돌렸다
근데 이거 임시방편이라 메모리 계속 차면 또 닿음
근본적으로 뭘 evict할 거냐를 정해야 함

**14:54 강민석**: 넵 bigkeys 결과 나오면 바로 공유할게요
결제팀 답변 오면 정책 같이 정하시죠

**14:55 정유진**: ㅇㅋ 결제팀 핑 보냈음 🙏
