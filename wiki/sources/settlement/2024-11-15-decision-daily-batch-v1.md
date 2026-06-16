---
type: source
of: raw/settlement/2024-11-15-decision-daily-batch-v1.md
source_hash: eda0196e5d3402c6ca2740d0adb0181771249aee
tags: [source]
---

## Summary
가맹점 20곳을 넘으며 수기 정산이 한계에 달해, 매일 새벽 04:00에 전날 거래를 가맹점별로 집계하는 D+1 일배치를 도입한 1세대 자동화 결정. 송금은 배치가 하지 않고 사람이 리포트 검토 후 수기 이체하며, 락·멱등 가드 없이 단순하게 시작했다.

## Concepts
- 정산 배치
- D+1 일배치 집계
- 집계와 송금 분리
- 정산 멱등성 부재(초기)
