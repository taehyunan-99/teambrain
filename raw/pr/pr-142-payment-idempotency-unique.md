---
created: 2026-04-30
tags: [pr-review, raw-dump, idempotency, database]
pr: 142
---

# PR #142 — feat: payment_idempotency 테이블 + DB 유니크 가드

> 작성: 박서연 / 리뷰: 김도현, 이준호 / 머지: 2026-05-01

**김도현 (idempotency_store.go:55)**: INSERT ... ON CONFLICT DO NOTHING 후에 영향 행 수가 0이면 중복으로 판단하는 거죠? 23505를 직접 잡는 게 아니라
**박서연**: 네 ON CONFLICT DO NOTHING + RETURNING으로 처리해요. 23505 예외 핸들링보다 깔끔하고 postgres 관용구라서
**이준호 (idempotency_store.go:80)**: 중복이면 기존 응답 스냅샷을 돌려주는데, 1차 요청이 "아직 처리 중"이라 스냅샷이 비어있으면요?
**박서연**: 그 경우 409 + "processing"으로 응답해요. 클라는 잠시 후 재시도. 동시 도착한 같은 키의 둘째 요청이 여기 떨어져요
**김도현**: redis는 이제 순수 캐시 역할이고 진실은 DB라는 거 — 주석으로 계층 역할 명시해주세요. 다음 사람이 redis를 다시 진실로 착각하면 안 되니
**박서연**: 추가했어요. "redis = 응답 재생 캐시, DB UNIQUE = 멱등성의 진실"
**김도현**: approve / **이준호**: approve
