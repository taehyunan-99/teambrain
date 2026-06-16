---
type: source
of: raw/infra/slack/2024-07-15-single-server-status.md
source_hash: 963dca2a25124ef8f3bf23e2fb9236eb925b8b2a
tags: [source]
---

## Summary
SRE로 합류한 정유진이 첫 주 현황 파악 결과를 #infra에 공유했다. 결제 API와 MySQL이 단일 인스턴스 1대에 함께 떠 있는 단일 장애점(SPOF), 추적 불가한 수동 SSH 배포, 사실상 없는 모니터링/알람을 문제로 지적하고, DB 분리·배포 자동화·모니터링 도입을 우선순위로 메모하며 다음 주 합류할 강민석과 함께 디테일을 잡기로 했다.

## Concepts
- 단일 장애점(SPOF)
- 인프라 베이스라인
- 관측성 대시보드
