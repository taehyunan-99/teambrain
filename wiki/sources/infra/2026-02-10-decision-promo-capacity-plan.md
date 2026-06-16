---
type: source
of: raw/infra/2026-02-10-decision-promo-capacity-plan.md
source_hash: 816bc6dbfd8874ee56974aedc819dcc5b99c849f
tags: [source]
---

## Summary
대형 가맹점 프로모션(평시 대비 약 3배 트래픽) 대비 인프라 용량 계획으로, 앞단(HPA)만 늘리면 다운스트림이 병목으로 남기 때문에 정유진이 전 구간 동시 증설+온콜 강화를 결정했다. HPA maxReplicas 10→20, Redis 메모리 1.5배 증설 및 지연 알람 강화, ProxySQL 커넥션 풀 상향, 프로모션 기간 인프라/결제 교차 온콜을 채택했다.

## Concepts
- 프로모션 용량 계획
- 오토스케일링 HPA
- Redis 도입
- MySQL HA/백업
