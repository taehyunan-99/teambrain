---
type: source
of: raw/infra/transcripts/2025-05-28-failover-drill.md
source_hash: 908d149536e222ffcf3eb0a775266374abcab5ae
tags: [source]
---

## Summary
정유진과 강민석이 MySQL standby 강제 승격 페일오버 드릴을 진행했다(정산 배치 04시 회피해 오전 10~11시 수행). 승격 자체는 2초 안쪽이나 ProxySQL이 죽은 커넥션을 인지하는 지연으로 앱 재연결까지 약 8초가 걸렸고, monitor 주기·connect_timeout 튜닝으로 3~4초까지 단축 가능함을 확인했다. 프로모션 3배 트래픽 대비 백엔드 풀 20→30+여유 5 상향과 다음 드릴의 강제 노드 다운 시나리오를 합의했다.

## Concepts
- MySQL HA/백업
- 프로모션 용량 계획
- 관측성 대시보드
