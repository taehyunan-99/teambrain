---
created: 2025-03-11
tags: [pr-review, raw-dump, settlement, csv]
pr: 61
---

# PR #61 — chore: 일배치 리포트 CSV 컬럼 정리

> 작성: 오세훈 / 리뷰: 한지우 / 머지: 2025-03-12

**한지우 (report_csv.go:24)**: 헤더에 `merchant_id`랑 `merchant_name` 둘 다 들어가니까 보기 좋네요. 검산할 때 이름으로 눈에 들어와서 편함 👍
**한지우 (report_csv.go:31)**: nit — 금액 컬럼 헤더가 `amount`인데 이게 거래총액인지 정산액인지 헷갈려요. `settle_amount`처럼 명확하게 가죠
**오세훈**: 아 맞아요 그게 수수료 떼고 난 정산액이라 `settle_amount`로 바꿨습니다. 거래총액 컬럼은 `gross_amount`로 같이 풀어뒀어요
**한지우 (report_csv.go:38)**: 좋아요. 그리고 가맹점 정렬은 지난번처럼 `merchant_id` 오름차순 고정 유지된 거 맞죠? 매일 순서 바뀌면 대조가 힘들어서
**오세훈**: 네 정렬 고정 그대로 뒀어요. 컬럼명만 손봤어요
**한지우**: 넵 approve. 수치 건드린 게 아니라 헤더만이라 가볍게 가도 될 듯
