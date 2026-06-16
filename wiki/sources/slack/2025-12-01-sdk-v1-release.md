---
type: source
of: raw/slack/2025-12-01-sdk-v1-release.md
source_hash: 28d4d2bc531f8276c93fba0d8d508be16d8efa6e
tags: [source]
---

## Summary
가맹점의 헤더·파라미터 실수를 줄이려 결제 요청과 결과 폴링을 감싼 JS SDK v1(@nimbuspay/sdk 1.0.0)을 배포했다. SDK가 Idempotency-Key용 UUID를 자동 생성해 붙여주며, 강제 대신 권장으로 깔고 채택률을 본 뒤 판단하기로 했다.

## Concepts
- SDK v1
- 멱등성
