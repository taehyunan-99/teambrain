---
type: source
of: raw/pr/pr-112-idempotency-middleware.md
source_hash: 2a8633743676e379d02abb3aa0bda19c3795e3b6
tags: [source, pr-review]
---

## Summary
**INC-204의 기원이 된 PR** — redis 타임아웃 처리를 두고 서연이 고민을 표했으나 도현이 '결제 못 받는 손실이 더 크다'며 fail-open(통과)을 결정. 준호의 중복 결제 우려에 'redis 가용성 높으니 일단'으로 머지. 한 달 뒤 INC-204로 이 판단이 뒤집힘.

## Concepts
- 멱등성
- fail-closed 원칙
