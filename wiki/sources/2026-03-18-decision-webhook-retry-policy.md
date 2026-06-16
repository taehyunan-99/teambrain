---
type: source
of: raw/2026-03-18-decision-webhook-retry-policy.md
source_hash: 90bb7e15214edf042b29cb6be352e42339118591
tags: [source, decision]
---

## Summary
웹훅 재시도 정책 결정(2026-03-18). 지수 백오프로 최대 6회 재시도, 2xx만 성공 간주, 영구 실패는 dead letter + 이메일 알림. 페이로드에 event_id를 넣어 가맹점이 중복 수신을 거를 수 있게 함. 웹훅 위조 방지(서명)는 미결로 남김(이후 5/6 결정).

## Concepts
- 웹훅 전송
- 멱등성
