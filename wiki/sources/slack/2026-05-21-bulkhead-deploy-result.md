---
type: source
of: raw/slack/2026-05-21-bulkhead-deploy-result.md
source_hash: e5d152bcc98e0c00c7fd5aaeb19559a40496048b
tags: [source, slack]
---

## Summary
워커풀 분리(bulkhead) 배포 결과 — PG 타임아웃 0건. 웹훅 폭주가 결제 승인을 굶기던 구조의 해소 확인. 타임아웃 10s 단축+재시도 1회는 멱등키 덕에 안전.

## Concepts
- 비동기 결제 승인
- 멱등성
