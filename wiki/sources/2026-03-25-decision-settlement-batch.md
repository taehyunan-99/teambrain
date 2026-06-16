---
type: source
of: raw/2026-03-25-decision-settlement-batch.md
source_hash: 26bd99230c53aada841f8841fdde795f2baccaca
tags: [source, decision]
---

## Summary
정산 배치 아키텍처 결정(2026-03-25). 일배치(D+1) 정산 채택 — 매일 04:00 전날 승인 거래를 가맹점별 집계 후 송금. 정산 멱등 키는 가맹점ID+정산일, 부분 재실행 지원. 실시간 정산은 환불 정정 복잡성·수수료로 탈락.

## Concepts
- 정산 배치
- 멱등성
