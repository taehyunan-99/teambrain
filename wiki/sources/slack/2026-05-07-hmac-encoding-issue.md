---
type: source
of: raw/slack/2026-05-07-hmac-encoding-issue.md
source_hash: c986fcdf9329e6add09d9fc8bf7bb9f1c2700675
tags: [source, slack]
---

## Summary
HMAC 간헐 검증 실패 원인 — json 재직렬화로 키 순서가 바뀌어 서명 불일치. '전송 직전 raw bytes로 서명'으로 수정, 가맹점 가이드에 '받은 바디 그대로 검증' 명시.

## Concepts
- 웹훅 전송
