---
type: source
of: raw/slack/2024-07-12-v1-launch-prep.md
source_hash: 4462dc8b370682cd0774e46208280840507b65e2
tags: [source]
---

## Summary
v1 출시 막판 점검에서 토스 SDK approve()를 동기 호출해 MySQL에 결제 레코드를 바로 insert하는 단순 구조로 가기로 했다. PG 추상화, 멱등성, 재시도/웹훅은 첫 가맹점 한 곳뿐이라 일단 백로그로 미루고 출시를 우선했다.

## Concepts
- 비동기 결제 승인
- PG 게이트웨이 추상화
- 멱등성
- 웹훅 발송
