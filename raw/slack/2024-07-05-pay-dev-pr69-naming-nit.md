---
created: 2024-07-05
tags: [pr-review, raw-dump, payment]
pr: 69
channel: pay-dev
---

# PR #69 — feat: 결제 승인 응답 매핑

> 작성: 이준호 / 리뷰: 박서연

**박서연 (payment.go:34)**: `res` 변수명 너무 막연해요. `tossApproveRes` 정도로 바꾸는 게 어때요
**이준호**: ㅇㅋ 바꿀게요. 손가락이 res만 치고 있었네 ㅋㅋ
**박서연 (payment.go:51)**: amount를 int로 받고 있는데 토스가 원 단위로 주니까 일단 괜찮긴 한데 타입 주석 한 줄만
**이준호**: 넵 // 원 단위, 부동소수 금지 라고 박아둘게요
**박서연**: 👍 approve
