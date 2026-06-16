---
created: 2026-04-22
tags: [pr-review, raw-dump, incident, idempotency]
pr: 140
---

# PR #140 — hotfix: 멱등성 조회 타임아웃 시 fail-closed

> 작성: 이준호 / 리뷰: 김도현, 박서연 / 머지: 2026-04-21 22:05 (긴급)

**이준호**: [긴급] INC-204 핫픽스. redis 타임아웃/에러 시 503 반환 + Retry-After 헤더. 통과시키던 기존 동작 제거
**김도현**: diff 확인. 이게 PR-112에서 제가 fail-open으로 가자고 한 그 지점이네요. 제 판단이 틀렸습니다. approve
**박서연 (idempotency.go:48)**: 503에 Retry-After 3s 박혀있는데 클라 SDK가 이 헤더 읽고 자동 재시도하나요?
**이준호**: SDK는 지수 백오프 자체 재시도라 헤더는 힌트용이에요. 직접 호출 가맹점을 위해 넣었어요
**박서연**: ㅇㅋ approve. 상세 리뷰는 내일 후속 PR에서 — 지금은 멈추는 게 우선
