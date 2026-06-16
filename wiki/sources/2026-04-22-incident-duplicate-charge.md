---
type: source
of: raw/2026-04-22-incident-duplicate-charge.md
source_hash: 35908695e477a83f6de25a0ad09d4e912124c790
tags: [source, incident]
---

## Summary
중복 결제 장애 회고 INC-204(2026-04-21, 87건 중복 청구). Redis 응답 지연으로 멱등성 키 조회가 타임아웃나자 fail-open(통과)으로 신규 결제 처리. 근본 원인은 멱등성의 Redis 단일 의존 + 결제 경로 fail-open. 조치로 fail-closed 전환 및 DB 유니크 2중화(4/29 결정으로 이어짐).

## Concepts
- 멱등성
- fail-closed 원칙
