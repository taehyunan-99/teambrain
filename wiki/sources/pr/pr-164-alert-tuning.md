---
type: source
of: raw/pr/pr-164-alert-tuning.md
source_hash: e915db5af4016318e704caf52c0f80dc35181033
tags: [source, pr-review]
---

## Summary
배치 알람 단계화 PR — 60분 경고 기준은 최근 60일 p99(52분) 실측 기반, 분기마다 재점검. '락 있는데 프로세스 없음'으로 죽음만 정밀 탐지. 알람 메시지에 '재실행 금지. 락 확인 먼저.'

## Concepts
- 온콜·알람
- 정산 배치
