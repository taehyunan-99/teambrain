---
type: source
of: raw/infra/transcripts/2026-02-04-promo-readiness-review.md
source_hash: 964c943c38be09ec5a8dd3098743139db29990c9
tags: [source]
---

## Summary
정유진·강민석이 결제팀 최민지가 공유한 2/21 대형 가맹점 프로모션(결제 승인 약 3배) 대비 사전 점검 회의를 했다. HPA max 10→20~25 상향+당일 min 임시 상향(워밍업), Redis 멱등키 메모리 헤드룸 정확 계산(noeviction 유지하되 인스턴스 4GB→8GB 검토), ProxySQL 백엔드 풀과 MySQL max_connections(100) 역산, PG사(토스/나이스) rate limit 확인 요청을 정리했다. Redis 지연 알람·p99 패널을 행사 전 미리 세팅하기로 했다.

## Concepts
- 프로모션 용량 계획
- 오토스케일링 HPA
- Redis 도입
- MySQL HA/백업
- 관측성 대시보드
