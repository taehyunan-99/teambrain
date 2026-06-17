---
created: 2024-11-22
tags: [pr-review, raw-dump, payment, webhook]
---

# PR 리뷰 한담 2024-11-22

> 작성: 이준호 / 리뷰: 김도현

**김도현 (webhook_sender.go:71)**: 웹훅 실패할 때 로그에 가맹점 ID랑 이벤트 타입은 찍히는데 재시도 횟수는 안 보이네요. 디버깅할 때 그게 제일 궁금할 듯
**이준호**: 아 맞네요. retry count 같이 찍을게요
**김도현 (webhook_sender.go:90)**: 그리고 응답 바디 통째로 로그 찍으면 나중에 PII 섞일 수 있으니 status code만 남기는 게 안전해요
**이준호**: ㅇㅋ 바디는 빼고 status랑 retry count만 남기겠습니다
**김도현**: 그렇게 하고 머지하죠 👍