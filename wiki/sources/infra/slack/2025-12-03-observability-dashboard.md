---
type: source
of: raw/infra/slack/2025-12-03-observability-dashboard.md
source_hash: 82883938ac4a9d75bcd4f0393d911ba73f375296
tags: [source]
---

## Summary
정유진이 관측성 대시보드 1차 정비 완료를 #infra에 공유했다. API latency(p50/p95/p99), Redis(command latency·used_memory·연결 수), MySQL(active connections·풀 사용률) 세 그룹으로 묶고 alert-bot 채널에 알람을 연동했다. 임계치(API p99>2s, Redis latency>50ms, used_memory 75→80% 조정, MySQL 커넥션>80%)를 두고 강민석과 알람 피로 vs 조기 감지를 논의하며 2주 뒤 튜닝 리뷰를 잡았다.

## Concepts
- 관측성 대시보드
- Redis 도입
- MySQL HA/백업
