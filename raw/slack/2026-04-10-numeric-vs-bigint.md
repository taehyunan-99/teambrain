---
created: 2026-04-10
tags: [slack, raw-dump, database, payment]
channel: pay-dev
---

# slack #pay-dev 2026-04-10

**16:42 이준호**: 그제 회의에서 금액 NUMERIC으로 정했는데, 어차피 KRW만 쓸 거면 BIGINT 원 단위가 더 빠르고 단순하지 않아요?
**16:47 김도현**: 수수료 계산에서 소수점 중간값이 나와요. 3.3% 떼면 원 단위로 안 떨어짐
**16:49 이준호**: 그건 계산만 NUMERIC으로 하고 저장은 BIGINT로 해도...
**16:52 김도현**: 저장이랑 계산 타입이 다르면 변환 버그 납니다. NUMERIC 유지하되 KRW는 scale 0으로 시작하죠
**16:54 이준호**: 넵 ㅇㅋ
