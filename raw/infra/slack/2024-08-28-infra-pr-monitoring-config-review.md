---
created: 2024-08-28
tags: [pr, raw-dump, code-review, monitoring, infra]
---

# PR #14 monitoring: 알람 임계값 설정 정리

작성: 강민석 / 리뷰: 정유진

## 변경
- 흩어져 있던 알람 임계값(CPU/디스크/헬스체크)을 `alerts.yaml` 한 파일로 모음
- cron 백업 스케줄 주석에 설명 추가

## 리뷰 코멘트

**정유진**: `cpu_threshold_pct` 이름 좋네요. 근데 `disk_thresh`만 줄임말이라 `disk_threshold_pct`로 통일해주세요 (nit)
**강민석**: 앗 넵 통일할게요
**정유진**: 5분 평균 조건 주석에 "백업 cron 스파이크 오탐 방지"라고 한 줄 적어두면 나중에 왜 이렇게 했는지 알기 좋을 듯
**강민석**: 추가했어요
**정유진**: 굿. 나머지 lgtm 👍 머지하세요
