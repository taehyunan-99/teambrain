---
created: 2026-04-08
tags: [meeting, database, architecture]
---

# 회의: 결제 DB 선택

- 일시: 2026-04-08
- 참석: 김도현, 박서연, 이준호

## 안건
결제·정산 데이터 저장소 결정.

## 논의
- 후보: PostgreSQL vs MySQL vs MongoDB.
- 박서연: 결제는 강한 일관성·트랜잭션·유니크 제약이 생명(멱등성 DB 제약 떠올려라). MongoDB는 트랜잭션이 약해 탈락.
- 이준호: MySQL도 되지만 PostgreSQL이 `SELECT ... FOR UPDATE`, 부분 인덱스, `ON CONFLICT`(upsert) 등 멱등 처리에 유리.
- 김도현: 정산 집계 쿼리가 복잡해질 텐데 Postgres의 윈도우 함수·CTE가 강력.

## 결정
- **PostgreSQL 채택.**
- 멱등성 유니크 제약, `ON CONFLICT DO NOTHING`으로 중복 결제/송금 가드 구현.
- 금액은 `NUMERIC`(부동소수점 금지).

## 근거
- 결제 도메인의 핵심 요구(트랜잭션·유니크·정확한 금액)에 Postgres가 가장 부합.
- 멱등성 2중화 결정(DB 유니크)과 직접 맞물림.
