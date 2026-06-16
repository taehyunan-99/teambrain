---
created: 2026-05-02
tags: [slack, raw-dump, webhook, security]
channel: pay-dev
---

# slack #pay-dev 2026-05-02

**13:30 이준호**: 웹훅 서명 구현하려는데 가맹점별 webhook_secret을 어디 보관하죠? vault 같은 거 도입해요?
**13:34 박서연**: vault 운영 부담이 커요. DB 암호화 컬럼으로 시작하는 게 낫지 않나
**13:37 김도현**: ㅇㅇ DB 암호화 컬럼(pgcrypto)으로 가고, KMS 연동은 다음 분기에 검토. 지금 vault까지 가면 과해요
**13:39 이준호**: 넵 pgcrypto로 구현할게요
**13:40 김도현**: 시크릿 회전 API도 같이 — 대시보드에서 가맹점이 직접 돌릴 수 있게
