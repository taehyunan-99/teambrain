---
created: 2026-04-28
tags: [slack, raw-dump, idempotency, database]
channel: pay-dev
---

# slack #pay-dev 2026-04-28

**15:00 박서연**: 내일 결정 회의 전에 payment_idempotency 테이블 DDL 초안 공유해요
```
CREATE TABLE payment_idempotency (
  idempotency_key UUID PRIMARY KEY,
  request_hash    TEXT NOT NULL,
  response_snapshot JSONB,
  created_at      TIMESTAMPTZ DEFAULT now()
);
```
**15:05 이준호**: PK가 곧 유니크 제약이니 깔끔하네요. request_hash는 왜 있어요?
**15:08 박서연**: 같은 키인데 바디가 다른 요청 잡아내려고요. 그건 클라 버그라 409로 거부
**15:10 김도현**: 좋네요. 내일 이 안으로 확정합시다
