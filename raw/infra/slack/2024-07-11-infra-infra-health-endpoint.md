---
created: 2024-07-11
tags: [slack, raw-dump, ops, healthcheck, monitoring]
channel: infra
---

# slack #infra 2024-07-11

**09:00 강민석**: `/healthz` 엔드포인트 추가하는 PR 머지됐어요. 헬스체크 알람 Slack 연동 설정할게요

**09:02 정유진**: timeout 임계치는 얼마로 잡았어요?

**09:03 강민석**: 우선 4초로 잡았어요. 오탐 빈도 보면서 조정할 예정이에요

**09:04 정유진**: 새벽에 응답이 좀 느린 서비스들은 따로 체크가 필요해요. 모니터링 알람 잘 오나 이번 주 확인해요
