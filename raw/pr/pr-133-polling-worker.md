---
created: 2026-04-03
tags: [pr-review, raw-dump, payment]
pr: 133
---

# PR #133 — feat: PENDING 상태 폴링 워커

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-04-04

**이준호 (polling_worker.go:40)**: PENDING 10분 넘은 결제를 PG에 재조회하는 거죠? 조회 결과 PG엔 승인인데 우리 DB가 PENDING이면요?
**박서연**: PG 기준으로 동기화해요. PG가 진실의 원천(source of truth). 승인이면 APPROVED로 올리고 웹훅 발송
**이준호 (polling_worker.go:72)**: 폴링 주기 1분인데 PG 조회 API에도 rate limit 있지 않아요?
**박서연**: 토스 조회는 분당 600건이라 여유 있어요. 초과 시 다음 주기로 밀리게 백프레셔 있고
**이준호**: approve 👍
