---
type: source
of: raw/slack/2026-06-10-idem-ttl-48h-proposal.md
source_hash: df185ec85e8e0476de45ef8e3d883520718c6309
tags: [source, slack]
---

## Summary
TTL 24h 만료 후 재시도 실측 7건(가맹점 배치 재처리 패턴) — 3/13에 보류한 엣지가 실재함을 확인. DB 유니크가 막아 사고는 아니나 캐시 미스로 409 혼란 발생, TTL 48h 제안. redis 메모리 추산 후 결정 예정(검토중).

## Concepts
- 멱등성
