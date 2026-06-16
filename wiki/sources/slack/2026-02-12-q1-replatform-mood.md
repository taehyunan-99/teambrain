---
type: source
of: raw/slack/2026-02-12-q1-replatform-mood.md
source_hash: 7b756b1b7bbaf15f082f2cf8c5c1745f676ee78c
tags: [source]
---

## Summary
회의 후 리플랫폼 착수 분위기 속에서, 멱등성을 Redis 단독에 의존하는 불안(TTL 만료·Redis 장애 시 뚫림)과 MySQL 유니크 제약·트랜잭션 보장, 웹훅 재시도 부재를 우선 갚을 기술부채로 꼽았다. 가맹점 영향 최소화를 위해 스키마 변경도 무중단으로 설계하기로 했다.

## Concepts
- 리플랫폼
- 기술부채
- 멱등성
- 웹훅 발송
