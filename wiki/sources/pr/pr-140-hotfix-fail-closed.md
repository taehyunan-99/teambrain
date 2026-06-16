---
type: source
of: raw/pr/pr-140-hotfix-fail-closed.md
source_hash: b3d613157e3e5d9c29dd3344369aaa8994dca927
tags: [source, pr-review]
---

## Summary
INC-204 긴급 핫픽스 PR(당일 22:05 머지) — redis 타임아웃 시 503+Retry-After로 fail-closed 전환. 도현이 'PR-112에서 제가 fail-open으로 가자고 한 그 지점, 제 판단이 틀렸다'고 리뷰에 기록.

## Concepts
- 멱등성
- fail-closed 원칙
