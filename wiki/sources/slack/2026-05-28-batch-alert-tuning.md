---
type: source
of: raw/slack/2026-05-28-batch-alert-tuning.md
source_hash: 40b690ff70884b7e21f6fa15275c836d2917ba94
tags: [source, slack]
---

## Summary
배치 알람 단계화 — INC-231 오판의 시작점이던 '30분 초과=알람'을 3단계로 분리: 60분 경고 / 송금 무응답 10분 긴급 / 락 있는데 프로세스 없음 긴급. 알람 문구에 '재실행 금지. 락 확인 먼저' 명시.

## Concepts
- 온콜·알람
- 정산 배치
