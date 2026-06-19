---
created: 2024-11-03
tags: [slack, raw-dump, ops, disk, trend]
channel: infra
---

# slack #infra 2024-11-03

**08:05 infra-bot**: [weekly disk report] 2024-11-03 기준
- log-server-01: 41% used (전주 -1%)
- app-server-01: 29% used
- app-server-02: 32% used
**08:20 강민석**: 로그 서버 계속 감소 추세네요. 60일 retention으로 늘렸는데도 오히려 줄고 있어요
**08:22 정유진**: compress 효과가 retention 증가분보다 더 큰 것 같아요. 좋은 트렌드예요
**08:23 강민석**: 디스크 cleanup 자동화한 보람이 있네요 ㅎ