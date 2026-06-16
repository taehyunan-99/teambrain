---
type: source
of: raw/slack/2026-05-13-settlement-recovery-followup.md
source_hash: 7c9e2e1e80e81f648eb796732a8282e8e92ca4c2
tags: [source]
---

## Summary
이중 송금 1,840만원(3곳·6건)을 1원 단위 대사로 전액 회수 완료하고, 명세서는 손대지 않은 채 "송금 오류 회수" 항목으로 내부 원장에 양변 기표해 정합성을 지켰다. 재발 방지로 payout_log에 송금 직전 유니크 가드와 배치 중복 실행을 막는 분산 락을 결제팀과 함께 도입하기로 했다.

## Concepts
- 정산 자동화
- 멱등성
- 중복 결제
- 페일오버 정책
