---
type: source
of: raw/pr/pr-074-webhook-sender-v1.md
source_hash: 37caabde6274c792e260aab378b7fe2749b885ff
tags: [source]
---

## Summary
결제 approve/cancel 직후 가맹점 endpoint로 단일 HTTP POST 1회를 보내는 fire-and-forget 웹훅 발송기 v1을 머지했다. 재시도·dead letter·서명은 범위에서 제외(TODO 주석으로 표시)하고, non-2xx 시 merchant_id/endpoint/status code 로깅과 connect/read 각 5초 타임아웃만 갖춘 MVP다.

## Concepts
- 웹훅 발송
- fire-and-forget 발송
- 웹훅 재시도 부재 (dead letter 미구현)
- 웹훅 타임아웃 설정
