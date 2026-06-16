---
type: source
of: raw/slack/2025-08-18-webhook-v1-design.md
source_hash: 972b6ee514ad67988a2a0fd1bd7db2897d371f72
tags: [source]
---

## Summary
가맹점의 폴링 부담을 줄이려 결제 승인/취소 확정 시 등록 URL로 POST 1회를 쏘는 웹훅 v1을 설계했다. 재시도·dead letter·서명은 MVP라 생략(fire and forget)하되, 폴링은 절대 죽이지 않고 안내에 "참고용, getStatus 검증 필수"를 명시하는 두 가지를 전제로 삼았다.

## Concepts
- 웹훅 발송
- 비동기 결제 승인
