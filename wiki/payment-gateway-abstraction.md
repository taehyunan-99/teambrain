---
title: PG 추상화 (Payment Gateway Abstraction)
tags: [payment, architecture, gateway]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/2026-03-04-meeting-payment-arch-kickoff.md
  - raw/2026-05-20-troubleshooting-pg-timeout.md
  - raw/pr/pr-101-payment-gateway-interface.md
  - raw/pr/pr-108-toss-adapter.md
  - raw/pr/pr-115-nice-adapter.md
  - raw/transcripts/2026-06-08-q3-planning-transcript.md
source_hashes:
  - 8e1412ee09e88672e56cea0b25198cd3cf5ead1e
  - d45b1fae55627009672630ea4c604a6160ed16e5
  - 8613c1747783fb6f7317d0fecfac6bfa13ca5998
  - da5cef41c4f9b61ccf78a6537279bcd1e1a8ae43
  - 9179ed1fbbb2667bc78a98f352dc623c8551b09c
  - b75e48cea4af53b493bfb30ea1f91989f6a38a3a
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 여러 PG사(토스페이먼츠, 나이스페이)를 `PaymentGateway` 인터페이스로 추상화하고 각 PG마다 adapter를 구현한다. 2026-03-04 킥오프에서 결정됐으며, PG 교체·추가를 상위 결제 로직 변경 없이 가능하게 한다.

## Details
- `PaymentGateway` 인터페이스를 정의하고 토스/나이스 각각 adapter로 구현(adapter 패턴). 메서드는 approve/cancel/getStatus 3개로 시작 (PgClient 명명안은 postgres와 혼동돼 기각).
- 상위 결제 승인 로직은 구체 PG를 모른 채 인터페이스로만 호출한다.
- **동기/비동기 경계 (PR-101):** 어댑터는 PG 호출을 동기로 감싸고, 비동기성은 워커 레벨이 담당. 어댑터에 비동기를 넣으면 PG마다 다른 콜백 방식 때문에 추상화가 깨진다. 부분취소는 시그니처 변경 없이 옵션 구조체로 확장 가능하게 유보.
- **에러 매핑 규칙 (PR-108/115):** PG 에러코드 → 내부 에러 매핑 테이블은 상수 파일로 분리해 어댑터 간 공유. **매핑 안 된 에러는 보수적으로 비재시도 분류** (무한 재시도 방지). 나이스는 EUC-KR 응답 변환 처리 포함.
- PG 호출은 [[async-payment-approval]] 워커에서 일어나며, 간헐적 타임아웃 대응으로 워커풀 분리·타임아웃 단축이 적용됐다(2026-05-20).
- **확장 계획 (Q3):** 토스 수수료 인상 대비 멀티 PG 라우팅(결제별 PG 선택)을 Q3 후반 설계 시작 — 어댑터 추상화 위에 라우팅 레이어만 얹는 구조.

## Related
- [[async-payment-approval]] — PG 어댑터를 호출하는 비동기 워커
- [[idempotency]] — PG 재시도 안전성을 보장하는 멱등성
