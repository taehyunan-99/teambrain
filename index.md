# llmwiki — 개념 카탈로그

> 이 파일은 `wiki-build` 스킬이 자동 갱신한다. `<!-- llmwiki:auto:start -->` ~ `<!-- llmwiki:auto:end -->` 영역만 덮어쓴다.

<!-- llmwiki:auto:start -->

## 결제 (Payment)

- [[idempotency]] — 같은 요청을 여러 번 보내도 한 번처럼 처리하는 핵심 신뢰성 원칙 (Redis+DB 2중화, Redis TTL 48h 승인)
- [[async-payment-approval]] — API는 PENDING 즉시 반환, 워커가 PG 승인 처리하는 비동기 구조 (폴링 워커·bulkhead 포함)
- [[payment-gateway-abstraction]] — 토스/나이스를 PaymentGateway 인터페이스로 추상화 (adapter 패턴, 멀티 PG 라우팅 Q3 착수 결정)
- [[webhook-delivery]] — 결제 결과 가맹점 전송: 지수 백오프+jitter 재시도, HMAC 서명, 시크릿 관리
- [[refund-flow]] — 부분 환불 설계 (Q3 메인 과제, 미착수)

## 정산 (Settlement)

- [[settlement-batch]] — D+1 일배치 정산, (merchant_id, settlement_date) 복합 유니크, 송금 가드 + 분산 락
- [[fee-calculation]] — 수수료 3.3% 원 단위 미만 절사 (약관 5조 2항)

## 인프라·원칙 (Infra & Principles)

- [[postgresql-choice]] — 트랜잭션·유니크 제약·ON CONFLICT가 멱등 처리에 핵심이라 채택, NUMERIC(19,4)
- [[fail-closed-principle]] — 외부 의존 실패 시 통과 아닌 거부를 택하는 결제 경로 안전 기본값 (도메인 의존 개념 포함)
- [[oncall-and-alerting]] — 3인 온콜 로테이션 + "오래 걸림/죽음"을 구분하는 배치 알람 3단계

<!-- llmwiki:auto:end -->
