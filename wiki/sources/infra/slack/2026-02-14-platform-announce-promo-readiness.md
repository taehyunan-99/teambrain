---
type: source
of: raw/infra/slack/2026-02-14-platform-announce-promo-readiness.md
source_hash: d00e37fe562691258f83e8da30752e114072e272
tags: [source]
---

## Summary
강민석이 #platform-announce에 프로모션 기간 인프라 안정화 조치 완료와 협조사항을 전사 공지했다. HPA max replica 약 2배 상향, Redis 인스턴스 증설+메모리 여유 확보, 온콜 24/7 강화를 완료했고, 각 팀에 Redis/DB 호출의 타임아웃 시 동작(특히 결제 critical 경로, 정산 배치 재시도/중복) 점검을 요청했다. 정유진은 당일 Redis/DB 지표 실시간 모니터링을 안내했다.

## Concepts
- 프로모션 용량 계획
- 오토스케일링 HPA
- Redis 도입
- 관측성 대시보드
