# llmwiki — 개념 카탈로그

> 이 파일은 `wiki-build` 스킬이 자동 갱신한다. `<!-- llmwiki:auto:start -->` ~ `<!-- llmwiki:auto:end -->` 영역만 덮어쓴다.

<!-- llmwiki:auto:start -->

## 결제 (Payment)

- [[idempotency]] — 같은 요청을 여러 번 보내도 한 번처럼 처리하는 핵심 신뢰성 원칙 (Redis SETNX v1 기원 → Redis+DB 2중화, TTL 48h 승인)
- [[async-payment-approval]] — API는 PENDING 즉시 반환, 워커가 PG 승인 처리하는 비동기 구조 (폴링 워커·bulkhead, JS SDK v1 래핑)
- [[payment-gateway-abstraction]] — 토스/나이스를 PaymentGateway 인터페이스로 추상화 (추상화 보류 전사 → adapter 패턴, 멀티 PG 라우팅 Q3 착수)
- [[webhook-delivery]] — 결제 결과 가맹점 전송: fire-and-forget v1 → 지수 백오프+jitter 재시도, HMAC 서명, 시크릿 관리
- [[refund-flow]] — 부분 환불 설계 (Q3 메인 과제, 미착수)

## 정산 (Settlement)

- [[settlement-batch]] — 수기 엑셀 → D+1 일배치 진화사, (merchant_id, settlement_date) 복합 유니크, 송금 가드 + 분산 락
- [[fee-calculation]] — 수수료 3.3% 원 단위 미만 절사 (2025-02 분쟁 → 약관 5조 2항 확정)

## 인프라 (Infrastructure)

- [[infra-baseline]] — 단일 서버 SPOF·무모니터링·무백업에서 출발한 단계적 인프라 베이스라인 원칙 + 관측성 대시보드
- [[kubernetes-migration]] — 수동 배포 사고를 계기로 컨테이너화·CI 도입 후 관리형 K8s로 무중단 컷오버
- [[redis-introduction]] — 팀별 제각각이던 캐시·세션을 관리형 Redis 사내 표준으로 통합 (TTL 필수, 키 네이밍 컨벤션)
- [[redis-eviction-policy]] — noeviction 쓰기 거부(결제 실패) 위험으로 volatile-lru 전환 (멱등키 등 보호 데이터 보존)
- [[autoscaling-hpa]] — 고정 replica 수동 스케일을 대체한 결제 API HPA (CPU 70% 타깃, max replica는 다운스트림 커넥션 역산)
- [[mysql-ha-failover]] — 단일 MySQL을 관리형 HA로 분리 (자동 백업+PITR, 다중 AZ 페일오버, ProxySQL 풀)
- [[promo-capacity-planning]] — 결제 3배 트래픽 프로모션 대비 앞단(HPA)+후단(Redis/ProxySQL) 동시 증설 + 온콜 강화

## 원칙·운영 (Principles & Operations)

- [[postgresql-choice]] — 트랜잭션·유니크 제약·ON CONFLICT가 멱등 처리에 핵심이라 채택, NUMERIC(19,4), MySQL 페일오버 정책 전사
- [[fail-closed-principle]] — 외부 의존 실패 시 통과 아닌 거부를 택하는 결제 경로 안전 기본값 (도메인 의존 개념 포함)
- [[oncall-and-alerting]] — 인프라 모니터링 출발점 → 3인 온콜 로테이션 + "오래 걸림/죽음"을 구분하는 배치 알람 3단계

<!-- llmwiki:auto:end -->
