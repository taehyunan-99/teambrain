---
type: source
of: raw/slack/2026-06-15-idem-ttl-48h-approved.md
source_hash: 08a7fe48f87d1bcf33c3066ece5743e377619268
tags: [source]
---

## Summary
멱등키 Redis TTL을 24h→48h로 늘리는 건이 승인됐다. 박서연의 메모리 추산 결과 일평균 약 32만 개 키 기준 피크 메모리 +12%로 여유분 내 감당 가능하며, 김도현이 승인했다. DB 유니크는 영구 최종 방어선이라 그대로 두고 Redis(응답 재생 캐시)만 48h로 늘려 가맹점 다음날 배치 재처리 시 409가 안 뜨게 한다. `idem:{key}` TTL 상수 한 줄 변경이며 다음 배포에 포함.

## Concepts
- 멱등성 (Idempotency)
