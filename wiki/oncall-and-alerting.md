---
title: 온콜과 알람 체계 (On-call & Alerting)
tags: [operations, monitoring, incident]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/slack/2026-05-23-oncall-rotation.md
  - raw/slack/2026-05-28-batch-alert-tuning.md
  - raw/pr/pr-164-alert-tuning.md
  - raw/transcripts/2026-05-13-inc231-postmortem-transcript.md
  - raw/infra/2024-07-22-decision-infra-baseline.md
  - raw/infra/slack/2024-09-10-manual-deploy-mistake.md
  - raw/infra/slack/2025-08-12-redis-maxmemory-alert.md
source_hashes:
  - a6e99babda0a6333ad29f5499ee9d5287675f526
  - 40b690ff70884b7e21f6fa15275c836d2917ba94
  - e915db5af4016318e704caf52c0f80dc35181033
  - 9e9b10b297b26b1474f22fed86f1639bc43bcb22
  - a41d85d6f37df9b6878e8603b654459f81d88c44
  - 747e90490fcfb9349a19378f0d5a8f8827e9c7b2
  - 5d3628971d753c3b66204aa64d4ce26d862ba6d9
---

<!-- llmwiki:auto -->

## Summary
새벽 장애 2건(INC-204, INC-231)을 겪은 후 확립된 운영 체계. 온콜은 주단위 3인 로테이션(도현 상시 백업)이며, 배치 알람은 "오래 걸림"과 "죽음"을 구분하는 3단계로 설계됐다. 알람 메시지에 "재실행 금지. 락 확인 먼저"를 박아 INC-231형 오판을 방지한다.

## Details

### 인프라 모니터링의 출발점 (2024~2025)
2026년의 정교한 배치 알람 단계화는 무(無)알람 상태에서 출발한 인프라 모니터링의 연장선이다.
- **모니터링/알람의 기원 (2024-07-22):** 결제 API와 MySQL이 단일 EC2 1대에 올라간 SPOF·무모니터링·무백업 상태에서, 장애를 가맹점 문의로만 인지하던 시절. 인프라 베이스라인 결정으로 **알람 최소셋 3종(헬스체크·디스크·CPU)**과 MySQL 일 1회 자동 백업을 즉시 도입했다 — Nimbus Pay 알람 체계의 진짜 0번째 단계. ([[infra-baseline]])
- **수동 배포 사고 (2024-09-10):** 정유진이 수동 SSH 배포 중 잘못된 브랜치를 prod에 올려 결제 API가 약 5분간 5xx를 낸 사고. "사람이 브랜치를 손으로 고르는 구조가 사고를 부른다"는 교훈으로 Docker 이미지+CI 파이프라인 도입을 추진했다. 새벽 배치 재실행 오판(INC-231)과 같은 계열의 "사람의 수동 개입이 사고를 만든다" 패턴.
- **Redis maxmemory 경보 (2025-08-12):** alert-bot이 redis-prod-01 메모리 90.2%(5.4GB/6GB) 경보를 띄운 사례. `noeviction`상 한계 도달 시 쓰기 거부가 결제에 영향을 주므로, maxmemory를 6GB→8GB로 임시 상향(67%로 하락)한 뒤 정책을 정하기로 했다 — 메모리 경보가 결제 영향으로 직결되는 알람의 실전 사례. ([[redis-eviction-policy]])

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
- [[infra-baseline]] — 알람 최소셋 3종이 시작된 인프라 모니터링의 출발점
- [[redis-eviction-policy]] — 결제 영향으로 직결되는 메모리 경보
