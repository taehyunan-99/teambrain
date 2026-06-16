---
created: 2026-04-02
tags: [slack, raw-dump, database]
channel: pay-dev
---

# slack #pay-dev 2026-04-02

**14:30 이준호**: 결제 상태 갱신할 때 SELECT FOR UPDATE 두 군데서 잡으니까 로컬에서 데드락 나는데요
**14:34 박서연**: 락 잡는 순서가 달라서 그래요. payment → ledger 순서로 통일하면 돼요
**14:36 이준호**: 아 순서 문제구나. 근데 이런 거 mongo였으면 신경도 안 썼을 텐데 ㅋㅋ
**14:38 박서연**: 대신 mongo면 트랜잭션 자체가 고통이에요. 다음주에 DB 정식으로 정하죠
**14:40 김도현**: ㅇㅇ 다음주 회의 안건
