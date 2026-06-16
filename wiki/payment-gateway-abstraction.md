---
title: PG 추상화 (Payment Gateway Abstraction)
tags: [payment, architecture, gateway]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/2025-03-26-decision-pg-abstraction-defer.md
  - raw/2026-03-04-meeting-payment-arch-kickoff.md
  - raw/2026-05-20-troubleshooting-pg-timeout.md
  - raw/slack/2024-08-22-toss-maintenance-outage.md
  - raw/slack/2025-03-24-pg-vendor-lockin-risk.md
  - raw/2026-06-16-decision-multi-pg-routing.md
  - raw/pr/pr-101-payment-gateway-interface.md
  - raw/pr/pr-108-toss-adapter.md
  - raw/pr/pr-115-nice-adapter.md
  - raw/transcripts/2026-06-08-q3-planning-transcript.md
source_hashes:
  - 2246a76f21b72e4f7eeca31a419d69e3262c2cf0
  - 8e1412ee09e88672e56cea0b25198cd3cf5ead1e
  - d45b1fae55627009672630ea4c604a6160ed16e5
  - 9cf515eb42ab23b66571e0972348357792404a37
  - 8e6a7635aa97eecdbb2de6894e868b60fd16c472
  - 3e69d3386c865fa113e4b5b2cd476afbb80bcbf8
  - 8613c1747783fb6f7317d0fecfac6bfa13ca5998
  - da5cef41c4f9b61ccf78a6537279bcd1e1a8ae43
  - 9179ed1fbbb2667bc78a98f352dc623c8551b09c
  - b75e48cea4af53b493bfb30ea1f91989f6a38a3a
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 여러 PG사(토스페이먼츠, 나이스페이)를 `PaymentGateway` 인터페이스로 추상화하고 각 PG마다 adapter를 구현한다. 2026-03-04 킥오프에서 결정됐으며, PG 교체·추가를 상위 결제 로직 변경 없이 가능하게 한다.

## Details

### 추상화의 전사 — 왜 처음엔 안 했나 (2024~2025)
- **2024-08-22 단일 PG 리스크 실증:** 토스 정기점검(14~15시)과 겹쳐 approve 호출이 전부 타임아웃 났고, 동기 직연동 구조라 토스가 멈추자 결제 전체가 같이 멈췄다. 당장 끊을 방법이 없어 점검 종료까지 CS 안내로 버텼다 — 단일 PG 종속이 운영 리스크로 처음 드러난 사건. ([[async-payment-approval]])
- **2025-03-24 벤더 종속 리스크 부각:** 그 달 두 번째 토스 점검으로 결제가 또 전면 중단되며, 결제 로직이 토스 SDK에 직결돼 나이스 등 추가 PG를 붙이려면 호출부를 다 뜯어야 하는 상태가 드러났다. "단일 PG 종속 리스크"와 "추상화 한 겹 필요"를 공식 백로그로 올렸다.
- **2025-03-26 추상화 의도적 보류:** 그럼에도 이번 분기엔 추상화/다변화에 **착수하지 않기로 결정**했다. 인터페이스 추상화의 방향성과 리스크만 공식 기록으로 남기고 다음 분기 우선순위 후보로 재상정 — 의도적인 기술부채 인지였다. 약 1년 뒤 2026-03-04 킥오프에서 이 보류가 풀려 실제 착수로 이어진다.

- `PaymentGateway` 인터페이스를 정의하고 토스/나이스 각각 adapter로 구현(adapter 패턴). 메서드는 approve/cancel/getStatus 3개로 시작 (PgClient 명명안은 postgres와 혼동돼 기각).
- 상위 결제 승인 로직은 구체 PG를 모른 채 인터페이스로만 호출한다.
- **동기/비동기 경계 (PR-101):** 어댑터는 PG 호출을 동기로 감싸고, 비동기성은 워커 레벨이 담당. 어댑터에 비동기를 넣으면 PG마다 다른 콜백 방식 때문에 추상화가 깨진다. 부분취소는 시그니처 변경 없이 옵션 구조체로 확장 가능하게 유보.
- **에러 매핑 규칙 (PR-108/115):** PG 에러코드 → 내부 에러 매핑 테이블은 상수 파일로 분리해 어댑터 간 공유. **매핑 안 된 에러는 보수적으로 비재시도 분류** (무한 재시도 방지). 나이스는 EUC-KR 응답 변환 처리 포함.
- PG 호출은 [[async-payment-approval]] 워커에서 일어나며, 간헐적 타임아웃 대응으로 워커풀 분리·타임아웃 단축이 적용됐다(2026-05-20).
- **멀티 PG 라우팅 — Q3 착수 결정 (2026-06-16):** 토스가 7월부터 일부 카드사 수수료를 인상함에 따라 결제별로 더 유리한 PG를 고르는 라우팅 레이어를 Q3에 착수한다(김도현·이준호·박서연 결정). 나이스 어댑터는 이미 붙어 있으나 라우팅 없이 유휴 상태였다.
  - **구조:** 기존 어댑터 추상화 **위에** 라우터를 얹는다. 어댑터 인터페이스(approve/cancel/getStatus)는 건드리지 않는다 — 라우터가 인터페이스에만 의존하므로 PG 추가가 어댑터 + 룰 등록으로 끝난다(추상화를 미리 만든 것이 여기서 회수됨).
  - **라우팅 기준(1차):** 카드사 + 금액 구간별로 토스 vs 나이스 중 수수료가 낮은 쪽 선택. 룰은 설정으로 분리(하드코딩 금지).
  - **폴백:** 선택된 PG가 타임아웃/장애여도 다른 PG로 재시도하지 않는다(중복 결제 위험). 멱등키 정책 그대로 적용하고 실패는 fail-closed. ([[idempotency]], [[fail-closed-principle]])
  - **비목표:** 실시간 수수료 협상·동적 가중치 라우팅은 범위 밖(1차는 정적 룰 테이블). 3사 이상 확장은 인터페이스만 열어두고 이번엔 토스/나이스 2사만.

## Related
- [[async-payment-approval]] — PG 어댑터를 호출하는 비동기 워커
- [[idempotency]] — PG 재시도 안전성을 보장하는 멱등성 (라우팅 폴백 시에도 적용)
- [[fail-closed-principle]] — 라우팅 폴백을 막는 fail-closed 원칙
