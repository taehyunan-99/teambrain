---
created: 2026-05-14
tags: [pr-review, raw-dump, settlement, idempotency]
pr: 151
---

# PR #151 — fix: 송금 직전 payout_log 유니크 가드 (INC-231)

> 작성: 이준호 / 리뷰: 박서연, 김도현 / 머지: 2026-05-15

**박서연 (payout.go:62)**: 순서가 중요해요 — payout_log INSERT가 송금 API 호출 *전*인가요 *후*인가요?
**이준호**: 전이요. INSERT(status=initiated) 성공 → 송금 호출 → status=completed 갱신. INSERT가 유니크 충돌하면 송금 자체를 안 해요
**박서연**: 그럼 INSERT 성공 후 송금 호출이 실패하면 initiated 행이 남는데, 재실행 시 그 가맹점은 유니크 충돌로 스킵돼서 영영 송금이 안 되지 않아요?
**이준호**: 좋은 지적... initiated 상태로 1시간 넘은 행은 송금 API에 결과 조회 후 수동 확인 큐로 보내는 보정 로직 추가할게요. 자동 재송금은 위험해서 안 하고요
**김도현**: "자동 재송금 안 함" 동의해요. 돈 나가는 건 모호하면 사람이 봐야죠. INC-231 직후라 더더욱
**박서연**: 보정 로직 확인. approve
**김도현**: approve
