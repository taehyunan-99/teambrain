---
type: source
of: raw/2026-06-16-decision-multi-pg-routing.md
source_hash: 3e69d3386c865fa113e4b5b2cd476afbb80bcbf8
tags: [source]
---

## Summary
멀티 PG 라우팅 레이어를 Q3에 착수하기로 결정했다(김도현·이준호·박서연). 토스의 7월 카드사 수수료 인상에 대응해, 기존 `PaymentGateway` 어댑터 추상화 위에 라우터를 얹어 카드사+금액 구간별로 수수료가 낮은 PG(토스/나이스)를 선택한다. 어댑터 인터페이스(approve/cancel/getStatus)는 건드리지 않고 룰은 설정으로 분리한다. PG 장애 시 다른 PG로 재시도하지 않고(중복 결제 위험) 멱등키 정책 그대로 fail-closed. 동적 가중치 라우팅·3사 이상 확장은 범위 밖(1차는 정적 룰 테이블, 2사).

## Concepts
- PG 추상화 (Payment Gateway Abstraction)
- 멱등성 (Idempotency)
- fail-closed 원칙
