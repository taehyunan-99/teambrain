---
created: 2026-03-05
tags: [slack, raw-dump, payment]
channel: pay-dev
---

# slack #pay-dev 2026-03-05

**10:12 이준호**: 어제 킥오프에서 얘기한 PG 인터페이스 초안 잡는 중인데, 이름 PaymentGateway vs PgClient 뭐가 나아요?
**10:14 김도현**: PaymentGateway. PgClient는 postgres랑 헷갈림 ㅋㅋ
**10:15 박서연**: ㅋㅋㅋ 그건 좀
**10:17 이준호**: 메서드는 approve / cancel / getStatus 세 개로 시작할게요
**10:20 김도현**: ㅇㅋ 토스 어댑터부터. 나이스는 다음주
**10:21 이준호**: 넵 PR 올리면 리뷰 부탁드려요
