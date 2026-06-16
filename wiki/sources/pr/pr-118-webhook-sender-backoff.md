---
type: source
of: raw/pr/pr-118-webhook-sender-backoff.md
source_hash: a8bf7e8890923a168b5fb72de14b412d778f1148
tags: [source, pr-review]
---

## Summary
웹훅 전송기 PR — 백오프에 ±20% jitter 추가(thundering herd 방지), 'at-least-once + 수신측 event_id 멱등'을 공식 전달 모델로 명문화.

## Concepts
- 웹훅 전송
