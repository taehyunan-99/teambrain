---
created: 2026-04-27
tags:
  - pr
  - raw-dump
  - infra
  - monitoring
  - code-review
pr: 34
---

# PR #34 — chore: 알람 룰 정리 + Redis 메모리 알람 임계 분리

> 작성: 강민석 / 리뷰: 정유진 / 머지: 2026-04-28

**정유진 (alerts/redis.yaml:9)**: WARN 90% / CRIT 95% 두 단계로 나눈 거 좋네요. 근데 duration이 둘 다 5m이면 WARN 뜨고 거의 동시에 CRIT 뜰 텐데, CRIT은 좀 더 길게 잡아서 진짜 닿을 때만 울리게 하는 게 나을 듯
**강민석**: 아 맞네요. WARN 5m / CRIT 10m으로 벌려둘게요. WARN으로 먼저 인지하고 CRIT은 진짜 지속될 때만
**정유진**: 넵 그게 알람 피로 덜 쌓여요

**정유진 (alerts/redis.yaml:21)**: 알람 이름 `redis_mem_high` 이거 인스턴스 안 들어가서 어느 노드인지 메시지만 봐선 모름. 라벨에 instance 붙어있긴 한데 summary 문구에 {{ $labels.instance }} 한번 박아주세요
**강민석**: 오 그거 좋네요. summary에 인스턴스랑 현재 사용률 같이 찍히게 했어요. 한밤에 알람 오면 노드부터 보이는 게 편하긴 하죠

**정유진 (alerts/batch.yaml:14)**: 정산 배치 디스크 알람은 그대로 두는 거죠? 이번 PR 범위 아닌 거 맞고
**강민석**: 네 이번엔 Redis 알람만 손봤어요. 배치 디스크는 따로

**정유진**: ㅇㅋ duration 분리 + summary 인스턴스만 반영해주면 approve. 알람 자체 로직은 단순해서 부담 없네요 👍
**강민석**: 넵 둘 다 반영하고 머지할게요. 룰 변경은 에이전트 다음 배포 때 같이 나갑니다
