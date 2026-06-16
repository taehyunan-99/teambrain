---
type: source
of: raw/onboarding-payment-team.md
source_hash: 2392cdc90b371b2eef6b7a42da533335418be864
tags: [source, onboarding]
---

## Summary
결제 백엔드 팀 온보딩 가이드. Nimbus Pay의 핵심 결정(비동기 승인, 멱등성 2중화, PostgreSQL, D+1 정산, 웹훅 재시도+서명)과 반복 원칙(돈 나가는 지점 직전 유니크 가드, 결제 경로 fail-closed, 조용한 실패 금지)을 신입에게 압축 안내한다.

## Concepts
- 비동기 결제 승인
- 멱등성
- PostgreSQL 선택
- 정산 배치
- 웹훅 전송
- fail-closed 원칙
