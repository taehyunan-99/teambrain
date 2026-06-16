---
type: source
of: raw/slack/2026-05-14-batch-lock-discussion.md
source_hash: 39a6ecd6afe3081fa4baac662fe1a01ea23049df
tags: [source, slack]
---

## Summary
배치 락 기술 선택 논쟁 — pg advisory lock(의존성 無, 커넥션 해제 시 자동 풀림) vs redis lock. '락 실패=실행 안 함이라 redis가 죽어도 안전한 실패'라는 fail-closed 논리로 redis lock 채택, TTL 2h. 포스트모템엔 없는 선택 근거.

## Concepts
- 정산 배치
- fail-closed 원칙
