---
type: source
of: raw/settlement/pr/pr-031-daily-aggregation-batch.md
source_hash: 5b1bb44f3674ad7981ab676dcb9a2ef64e1590ee
tags: [source]
---

## Summary
새벽 4시에 전날 거래를 가맹점별로 SUM하는 일별 정산 집계 배치 PR. 리뷰에서 자정 경계 거래 귀속 기준(created_at)은 일단 보류하고, 환불/취소 status를 집계에서 제외하도록 수정해 머지했으며, 멱등 가드 없이 실패 시 전체 재실행하는 단순 운영을 전제로 한다.

## Concepts
- 정산 배치
- D+1 일배치 집계
- 환불/취소 제외 집계
- 날짜 경계 귀속 기준
