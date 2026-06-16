---
title: 온콜과 알람 체계 (On-call & Alerting)
tags: [operations, monitoring, incident]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/slack/2026-05-23-oncall-rotation.md
  - raw/slack/2026-05-28-batch-alert-tuning.md
  - raw/pr/pr-164-alert-tuning.md
  - raw/transcripts/2026-05-13-inc231-postmortem-transcript.md
source_hashes:
  - a6e99babda0a6333ad29f5499ee9d5287675f526
  - 40b690ff70884b7e21f6fa15275c836d2917ba94
  - e915db5af4016318e704caf52c0f80dc35181033
  - 9e9b10b297b26b1474f22fed86f1639bc43bcb22
---

<!-- llmwiki:auto -->

## Summary
새벽 장애 2건(INC-204, INC-231)을 겪은 후 확립된 운영 체계. 온콜은 주단위 3인 로테이션(도현 상시 백업)이며, 배치 알람은 "오래 걸림"과 "죽음"을 구분하는 3단계로 설계됐다. 알람 메시지에 "재실행 금지. 락 확인 먼저"를 박아 INC-231형 오판을 방지한다.

## Details

### 온콜 로테이션 (2026-05-23, 슬랙 결정 — 정식 문서 없음)
- 주단위 로테이션: 서연 → 준호 → 민지, 도현은 상시 백업.
- PM(민지)도 포함 — 1차는 탐지/판단/에스컬레이션, 기술 대응은 백업 콜.
- 04시 정산 배치 알람은 온콜 폰으로 라우팅.

### 배치 알람 단계화 (2026-05-28, PR-164)
INC-231의 시작이 "30분 초과 = 알람"을 보고 죽음으로 오판한 것이었으므로, 알람이 그 둘을 구분하게 재설계:
1. **60분 초과** → 경고만 (근거: 최근 60일 배치 소요 p99 = 52분, 분기마다 재점검)
2. **송금 API 무응답 10분** → 긴급
3. **락은 있는데 프로세스 없음** → 긴급 (진짜 죽은 케이스만 정밀 탐지)

알람 메시지에 "재실행 금지. 락 확인 먼저" 명시 — 새벽에 졸린 사람의 실수 방지.

### 배경 교훈 (INC-231 포스트모템)
"사람이 새벽 4시에 죽었는지 느린지 구분할 정보가 없었다"가 근본 원인 중 하나로 지목됨. ([[settlement-batch]], [[fail-closed-principle]])

## Related
- [[settlement-batch]] — 알람 대상인 정산 배치와 INC-231
- [[fail-closed-principle]] — 불확실하면 실행하지 않는다는 같은 정신
