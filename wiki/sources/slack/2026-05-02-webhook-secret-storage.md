---
type: source
of: raw/slack/2026-05-02-webhook-secret-storage.md
source_hash: 84dd3cddac86193967eec8758a0ea5ce561eb01e
tags: [source, slack]
---

## Summary
**슬랙에서만 내려진 결정** — webhook_secret 보관은 vault 대신 DB 암호화 컬럼(pgcrypto), KMS는 다음 분기 검토. 시크릿 회전 API도 함께 지시.

## Concepts
- 웹훅 전송
- PostgreSQL 선택
