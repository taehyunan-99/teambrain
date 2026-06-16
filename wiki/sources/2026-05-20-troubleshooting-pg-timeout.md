---
type: source
of: raw/2026-05-20-troubleshooting-pg-timeout.md
source_hash: d45b1fae55627009672630ea4c604a6160ed16e5
tags: [source, troubleshooting]
---

## Summary
PG 승인 간헐적 타임아웃 트러블슈팅(2026-05-20). 결제 승인 워커와 웹훅 재전송 워커가 같은 스레드풀을 공유해, 웹훅 폭주 시 결제 승인이 굶는 게 원인. 해결로 워커풀 분리(bulkhead) + 결제 우선순위 + 타임아웃 단축·재시도(멱등성 키 덕분에 안전).

## Concepts
- 비동기 결제 승인
- PG 추상화
- 멱등성
