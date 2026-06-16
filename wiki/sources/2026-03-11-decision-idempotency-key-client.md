---
type: source
of: raw/2026-03-11-decision-idempotency-key-client.md
source_hash: 10620d1cdbf895c572754fa29a133e775f28c033
tags: [source, decision]
---

## Summary
멱등성 키 설계 결정(2026-03-11). 클라이언트가 `Idempotency-Key` 헤더로 UUID를 보내고 서버는 Redis에 응답을 24h 저장하는 방식 채택. 서버 생성·자연 키 방식은 정당한 재결제를 구분 못 해 탈락. (이후 4/29에 DB 유니크 2중화로 수정됨.)

## Concepts
- 멱등성
