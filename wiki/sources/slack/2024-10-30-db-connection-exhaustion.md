---
type: source
of: raw/slack/2024-10-30-db-connection-exhaustion.md
source_hash: f348851af70dee20c13f91de174abd2257c18c3e
tags: [source]
---

## Summary
온보딩 트래픽이 5~6배로 늘자 HikariPool 커넥션 풀이 고갈되어 승인 요청이 30초 타임아웃을 냈다. maximumPoolSize 30, connectionTimeout 5초, maxLifetime 30분으로 임시 튜닝해 복구했으나, 동기 승인의 커넥션 점유 패턴과 모니터링·알람 부재가 근본 문제로 남았다.

## Concepts
- DB 커넥션 고갈
- 비동기 결제 승인
