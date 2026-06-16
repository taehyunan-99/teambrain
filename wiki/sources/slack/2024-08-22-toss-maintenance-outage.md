---
type: source
of: raw/slack/2024-08-22-toss-maintenance-outage.md
source_hash: 9cf515eb42ab23b66571e0972348357792404a37
tags: [source]
---

## Summary
토스 정기점검(14~15시)과 겹쳐 approve 호출이 전부 타임아웃 났고, 동기 직연동 구조라 토스가 멈추자 결제 전체가 같이 멈췄다. 당장 끊을 방법이 없어 점검 종료까지 CS 안내로 버티고, 다음부터 점검 일정을 캘린더에 미리 반영하기로 했다.

## Concepts
- 비동기 결제 승인
- PG 게이트웨이 추상화
- 페일오버 정책
