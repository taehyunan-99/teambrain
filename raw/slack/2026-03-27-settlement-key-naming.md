---
created: 2026-03-27
tags: [slack, raw-dump, settlement, idempotency]
channel: pay-dev
---

# slack #pay-dev 2026-03-27

**15:10 이준호**: 정산 멱등키 컬럼 이름 뭐로 하죠. settlement_key? merchant_date_key?
**15:12 박서연**: 그냥 (merchant_id, settlement_date) 복합 유니크로 하고 별도 키 컬럼 안 만들어도 되지 않나
**15:15 이준호**: 오 그게 낫네요. 재실행 판정도 그 두 컬럼으로 하면 되고
**15:17 김도현**: ㅇㅋ 복합 유니크로 갑시다. 결정문서까진 필요 없고 이 스레드 참조
**15:18 이준호**: 넵
