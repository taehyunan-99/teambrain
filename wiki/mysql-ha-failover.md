---
title: MySQL HA·페일오버·백업 (MySQL HA / Failover / Backup)
tags: [infra, mysql, ha, failover, backup, proxysql, pitr]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2025-05-20-decision-mysql-ha-backup.md
  - raw/infra/transcripts/2025-05-28-failover-drill.md
source_hashes:
  - c29d5b28d32ee23aa844c746cf39ce97186cca35
  - 908d149536e222ffcf3eb0a775266374abcab5ae
---

<!-- llmwiki:auto -->

## Summary
K8s 내부 단일 인스턴스로 PITR 불가·비정기 수동 백업 상태였던 MySQL을, 인프라/SRE 관점에서 외부 관리형 HA 구성으로 분리·표준화했다. 자동 일일 백업+PITR(보존 14일), 다중 AZ primary/standby 자동 페일오버, 앱-DB 사이 ProxySQL 커넥션 풀을 도입하고, 페일오버 드릴로 재연결 지연(약 8초, 대부분 ProxySQL의 죽은 커넥션 인지 지연)을 측정·튜닝했다.

## Details
### 결정 — MySQL 운영 표준화 (2025-05-20, 결정자 정유진)
당시 MySQL은 K8s 클러스터 내부 단일 인스턴스(StatefulSet 1개)로, 백업은 수동 mysqldump 비정기 수행이었다. 결제 승인/취소·멱등성 키·정산 payout 데이터가 모두 이 단일 노드에 집적돼 복구 절차가 없었고, PITR 불가로 사고 시 마지막 수동 덤프 시점까지만 되돌릴 수 있어 유실 구간이 컸다. 결제/정산은 금액(DECIMAL)을 다루므로 정합성·복구 가능성이 인프라 차원의 전제 조건이었다.

검토한 대안: A(K8s 내부 self-managed 복제 HA — 통제권·비용 이점이나 페일오버 자동화·binlog 아카이빙·백업 검증을 전부 인프라팀이 직접 운영, split-brain 등 자체 부담), B(외부 관리형 RDS급 — 백업/PITR/페일오버를 매니지드 위임, 비용↑·외부 종속). **대안 B 채택.**

구성 요소:
1. 자동 일일 백업 + PITR 활성, 백업 보존 14일.
2. primary/standby 다중 AZ 복제, 자동 페일오버(standby 승격).
3. 앱-DB 사이 ProxySQL 커넥션 풀(커넥션 수렴 + 페일오버 시 재연결 완충).
- 결제/정산의 DB 접속은 모두 ProxySQL 엔드포인트 경유로 표준화.

근거: 금액 데이터 신뢰성 확보 최우선, PITR로 유실 구간을 분 단위로 축소, 페일오버/백업 검증을 매니지드에 위임해 제한된 SRE 인력을 모니터링·연결 관리에 집중, ProxySQL로 다수 파드 커넥션 폭증 제어 및 엔드포인트 전환 충격 흡수. 리스크: 페일오버 시 짧은 커넥션 끊김(수 초~수십 초, 인플라이트 쿼리 실패 가능 → 앱단 재시도 필요), 비동기 복제 특성상 미전파 binlog 유실 가능(동기성 수준 별도 검토), 외부 종속 비용/레이턴시, **백업/PITR 복구 절차는 정기 복구 리허설로 실효성 검증 필요**.

> 범위 메모: 결제팀 관점의 페일오버 정책(멱등키 기반 안전 재시도 등)은 별도 주제(postgresql-choice)에서 다루며, 본 문서는 인프라팀의 HA/백업/페일오버 운영 관점에 한정한다.

> 이주 메모: 여기서 표준화한 MySQL은 Nimbus Pay의 **당시 주 트랜잭션 저장소**다. 이후 멱등/트랜잭션 한계가 누적돼 2026-Q1 리플랫폼 동기로 이어지고 2026-04 PostgreSQL로 **이주**한다([[postgresql-choice]] "이주 결정의 경위"). 따라서 본 문서의 HA/백업/페일오버 운영은 이주 이전 시기의 인프라 정합성 기반에 해당한다.

### 페일오버 드릴 (2025-05-28)
정유진·강민석이 standby 강제 승격 페일오버 드릴을 수행했다. 시간대는 **정산 D+1 배치(04시 KST)를 피해 트래픽 낮은 오전 10~11시** — 배치 중 페일오버가 터지면 머천트별 정산 데이터의 기록 지점이 애매해지기 때문.

- 구성: primary 1 / standby 1 비동기 복제, replication lag ≈ 0초. 앱은 ProxySQL(VIP 물림)만 알고 뒤의 primary/standby는 모름.
- 측정: standby promote(복제 끊고 read_only 해제) 후 새 primary가 read/write를 받기 시작. 앱 쪽에서 약 **8~9초간 커넥션 에러** 후 재연결.
- 원인 분석: **승격 자체는 2초 안쪽이고, 나머지 대부분은 ProxySQL이 옛 primary로 가던 죽은 커넥션을 끌어안고 있다가 인지하는 지연**. monitor 체크 주기·connect_timeout이 길게 잡혀 죽은 커넥션 정리가 늦음. 튜닝하면 3~4초까지 단축 가능하나, 너무 짧게 잡으면 평소 멀쩡한 커넥션도 자꾸 끊었다 다시 맺어 오버헤드 발생 → 밸런스 필요.
- 풀 사이즈: 백엔드 max_connections 20, 프론트 max_connections 1000. 결제 워커 동시성이 낮아 평소 20도 넉넉하나, **프로모션 3배 트래픽 대비 백엔드 풀 20 → 30 + 여유(free) 커넥션 5, 대기 타임아웃 3초**로 상향하기로 합의(다음 드릴 때 재측정).
- 추가 관찰: 백엔드 커넥션 멀티플렉싱이 prepared statement·세션 변수와 안 맞을 때가 있어 앱 드라이버 설정(결제팀 이준호 커넥션 풀과 엮임)을 별도 점검. 다음 드릴은 graceful 승격이 아닌 **강제 노드 다운 시나리오**를 동일하게 10시대(새벽 배치 회피)에 잡기로 했다.

## Related
이 표준화는 [[infra-baseline]]에서 미룬 "DB 물리 분리"의 후속이며, MySQL을 외부로 분리해 [[kubernetes-migration]] 범위 밖에 둔 데이터 계층을 정식화한다. ProxySQL 백엔드 풀·MySQL max_connections는 [[autoscaling-hpa]]의 maxReplicas 역산과 [[promo-capacity-planning]]의 커넥션 산정에 직접 연동된다. 페일오버 시 인플라이트 쿼리 재시도는 [[idempotency]] 기반 안전 재시도와 맞닿는다. 드릴 시간대(정산 04시 배치 회피)는 [[settlement-batch]]와 관련된다.
