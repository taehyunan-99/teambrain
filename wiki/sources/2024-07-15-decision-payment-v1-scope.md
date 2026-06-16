---
type: source
of: raw/2024-07-15-decision-payment-v1-scope.md
source_hash: 8ea7d23927fb5243b54f2e6a4f347ca649be328c
tags: [source]
---

## Summary
첫 가맹점 온보딩 데드라인에 맞춰 결제 서비스 v1 범위를 토스 단일 PG 직연동 + 동기 승인 + MySQL 저장으로 확정했다. PG 추상화, 멀티 PG, 비동기 승인, 멱등성, 자동 재시도는 출시 속도 우선으로 v1에서 제외했다.

## Concepts
- 결제 v1 스코프
- 토스 단일 PG 직연동
- 동기 승인
- PG 추상화 보류
- 단일 PG 종속 리스크
