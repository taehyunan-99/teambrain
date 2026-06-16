---
type: source
of: raw/slack/2026-02-12-q1-replatform-mood.md
source_hash: 7b756b1b7bbaf15f082f2cf8c5c1745f676ee78c
tags: [source]
---

## Summary
기술부채 점검 회의(2026-02-10) 직후 #pay-dev 잡담. "드디어 갈아엎느냐"는 들뜬 분위기 속에서, 박서연이 "갈아엎는다기보단 빚 갚는 것 — 순서를 정하고 가야 한다"며 **멱등성과 DB부터** 보고 싶다고 우선순위를 제시했다. Redis 단독 멱등이 불안하고(TTL 만료·Redis 흔들림 시 뚫림), **MySQL도 "유니크 제약·트랜잭션 보장을 제대로 걸 수 있는 쪽으로"** 함께 봐야 한다고 — Postgres 이주 방향을 사실상 가리킴. 김도현은 v1 때 본인의 "빨리 출시" 푸시가 빚을 키웠음을 인정하고 이번엔 제대로 하자고 했고, 최민지는 "멱등성/DB는 결제 흐름 한복판이니 가맹점 영향 최소화·무중단"을 조건으로 달았다(박서연이 무중단 스키마 전환 약속). 구체 일정은 미정, 이번 주 내 우선순위·범위 정리 공유로 마무리.

## Concepts
- PostgreSQL 선택 (PostgreSQL Choice) — "유니크/트랜잭션 제대로 거는 DB"로 이주 방향
- 멱등성 (Idempotency) — DB부터 보자는 우선순위
- 비동기 결제 승인 (Async Payment Approval) — 동기 직연동 탈피
