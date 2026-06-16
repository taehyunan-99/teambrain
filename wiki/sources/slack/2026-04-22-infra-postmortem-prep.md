---
type: source
of: raw/slack/2026-04-22-infra-postmortem-prep.md
source_hash: 959c05e406caed3a84f5b4bf0d5c51db5087c68d
tags: [source]
---

## Summary
프로모션 새벽 Redis P99가 800ms까지 튀었으나 eviction 0건으로 데이터 유실은 없었고, 결제팀의 중복 결제는 호출 측 타임아웃 처리 로직(늦게 받은 응답을 못 받은 것으로 간주해 재요청)이 원인일 수 있다는 추측이 나왔다. 인프라팀은 원인 단정을 미루고 포스트모템에 P99·커넥션 풀·eviction 지표를 사실 그대로 공유하기로 했다.

## Concepts
- 중복 결제
- 멱등성
- 페일오버 정책
