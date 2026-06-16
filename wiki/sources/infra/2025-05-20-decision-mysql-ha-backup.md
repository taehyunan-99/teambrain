---
type: source
of: raw/infra/2025-05-20-decision-mysql-ha-backup.md
source_hash: c29d5b28d32ee23aa844c746cf39ce97186cca35
tags: [source]
---

## Summary
K8s 내부 단일 인스턴스로 PITR 불가·비정기 수동 백업 상태였던 MySQL을 외부 관리형 HA 구성으로 분리·표준화하기로 결정했다. 자동 일일 백업+PITR(보존 14일), 다중 AZ primary/standby 자동 페일오버, 앱-DB 사이 ProxySQL 커넥션 풀을 도입하고 결제/정산 접속을 ProxySQL 엔드포인트로 표준화했다.

## Concepts
- MySQL HA/백업
- Kubernetes 마이그레이션
- 단일 장애점(SPOF)
