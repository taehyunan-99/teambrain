---
title: 인프라 베이스라인과 관측성 (Infra Baseline & Observability)
tags: [infra, baseline, sre, monitoring, observability]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2024-07-22-decision-infra-baseline.md
  - raw/infra/slack/2024-07-15-single-server-status.md
  - raw/infra/slack/2025-12-03-observability-dashboard.md
source_hashes:
  - a41d85d6f37df9b6878e8603b654459f81d88c44
  - 963dca2a25124ef8f3bf23e2fb9236eb925b8b2a
  - 82883938ac4a9d75bcd4f0393d911ba73f375296
---

<!-- llmwiki:auto -->

## Summary
결제 API와 MySQL이 단일 EC2 1대에 함께 올라간 단일 장애점(SPOF)·무모니터링·무백업 상태에서, 가장 큰 리스크(데이터 유실·무가시성)부터 제거하는 단계적 인프라 베이스라인 원칙을 세웠다. 모니터링/알람 최소셋과 MySQL 자동 백업을 즉시 도입하고, 이후 관측성 대시보드를 latency/Redis/MySQL 세 그룹으로 정비해 알람을 연동했다.

## Details
### 출발점 — 단일 서버 현황 (2024-07-15)
SRE로 합류한 정유진이 첫 주 현황을 #infra에 공유했다. 당시 구조의 문제는 세 가지였다.
- 결제 API와 MySQL이 EC2급 인스턴스 단 1대에 함께 떠 있어, 이 한 대가 죽으면 결제와 DB가 동시에 날아가는 단일 장애점(SPOF).
- 배포는 SSH 접속 후 `git pull` + 수동 프로세스 재시작 — 누가 언제 무엇을 올렸는지 추적 불가.
- 모니터링/알람이 사실상 없어 장애를 가맹점 문의로만 인지. CPU/메모리 그래프도 없었다.

또한 API와 DB가 같은 인스턴스를 공유해 트래픽이 조금만 튀어도 DB가 함께 느려지는 리소스 경합도 관측됐다. 우선순위는 (1) DB 분리, (2) 배포 자동화/문서화, (3) 모니터링 도입으로 메모됐고, 다음 주 합류하는 강민석과 함께 디테일을 잡기로 했다.

### 베이스라인 원칙 결정 (2024-07-22)
정유진이 결정자로서, 단일 서버를 임시 체제로 간주하되 리스크 큰 항목부터 제거하기로 했다. 검토한 대안은 (1) 즉시 컨테이너+멀티 인스턴스 전면 전환(인력상 비현실적), (2) DB 즉시 물리 분리(백업 없는 상태 분리는 위험), (3) 단일 서버 유지 + 최소셋 안전장치 도입이었고 (3)을 채택했다.

결정 내용:
1. 단일 서버는 임시. Q4까지 컨테이너 기반(이미지 빌드 → 배포)으로 전환한다.
2. 모니터링/알람 최소셋 3종을 먼저 도입: 헬스체크(API 응답), 디스크 사용률, CPU 사용률.
3. DB 물리 분리는 보류하되 MySQL 자동 백업 스케줄(일 1회 덤프 + 보관)을 즉시 건다.
4. 수동 SSH 배포는 Q4 컨테이너 전환과 함께 폐기 대상으로 둔다.

근거는 "데이터 유실은 복구 불가능한 사고이므로 백업이 비용 대비 효과가 가장 큰 첫 조치", "작게 시작해 검증된 것만 늘린다"였다. 알려진 잔존 리스크로 SPOF(Q4 전환 전까지 수용), DB 리소스 경합, 그리고 "백업은 떠도 복구 절차를 검증하지 않으면 무의미"하므로 복구 리허설을 별도 과제로 등록할 필요를 명시했다.

### 관측성 대시보드 1차 정비 (2025-12-03)
정유진이 관측성 대시보드 1차 정비를 마쳤다. 그동안 메트릭은 쌓이는데 보는 사람이 없던 상태에서, 세 그룹으로 묶었다.
1. API latency (p50/p95/p99)
2. Redis (command latency + used_memory + 연결 수)
3. MySQL (active connections / connection pool 사용률)

알람을 alert-bot 채널에 연동했고, 임계치를 보수적으로 잡았다: API p99 > 2s(5분 지속), Redis command latency > 50ms, Redis used_memory > 80%(초안 75%였으나 평소 60% 수준이라 배치 시 오탐 우려로 한 칸 상향), MySQL connection 사용률 > 80%. 강민석은 "임계치를 너무 타이트하게 잡으면 알람 피로가 와서 결국 다들 무시한다"고 우려했고, 정유진은 "처음엔 보수적으로 빡세게 걸고 2주 데이터를 보며 튜닝"하기로 절충해 2주 뒤 임계치 리뷰를 잡았다.

## Related
이 베이스라인은 후속 인프라 결정의 출발점이다. SPOF·수동 배포 폐기는 [[kubernetes-migration]]으로, MySQL 백업·복구 가능성 확보는 [[mysql-ha-failover]]로, 캐시/세션 표준화는 [[redis-introduction]]으로 이어졌다. 관측성 대시보드의 Redis/MySQL 알람은 이후 [[redis-eviction-policy]] 메모리 경보와 [[promo-capacity-planning]]의 실시간 모니터링 기반이 됐다. 알람 임계치·피로 절충 논의는 온콜/알람 운영(oncall-and-alerting) 주제와 맞닿는다.
