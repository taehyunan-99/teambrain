---
type: source
of: raw/slack/2026-03-13-redis-ttl-question.md
source_hash: 7d9842ac8c25cc21f9432751bc666b07dec8f01e
tags: [source, slack]
---

## Summary
멱등키 TTL 24h 만료 후 같은 키 재시도가 신규 결제로 처리되는 엣지 케이스 제기(준호) — '확률 낮으니 일단 24h' 보류로 종결. (6/10에 실측 7건으로 재부상하는 미결 사안.)

## Concepts
- 멱등성
