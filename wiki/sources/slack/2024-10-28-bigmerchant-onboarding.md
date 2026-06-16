---
type: source
of: raw/slack/2024-10-28-bigmerchant-onboarding.md
source_hash: c21496615e11f8c89bec1d38ce2541e6ace3d8f8
tags: [source]
---

## Summary
첫 대형 가맹점(마켓플로우) 온보딩으로 평소 2~3배 트래픽이 예상되면서, 동기 승인 구조에서 PG 응답 대기 중 스레드·DB 커넥션이 묶여 병목이 우려됐다. 구조 변경 시간이 없어 앱 스케일아웃과 DB 커넥션 풀 조정으로 막되, DB max connection 한계 때문에 인프라팀과 함께 점검하기로 했다.

## Concepts
- 비동기 결제 승인
- DB 커넥션 고갈
- PG 게이트웨이 추상화
