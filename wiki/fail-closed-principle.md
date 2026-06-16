---
title: fail-closed 원칙 (Fail-Closed Principle)
tags: [reliability, principle, payment]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/2026-04-22-incident-duplicate-charge.md
  - raw/2026-04-29-decision-idempotency-db-unique.md
  - raw/2026-05-13-incident-settlement-double-payout.md
  - raw/pr/pr-112-idempotency-middleware.md
  - raw/slack/2026-04-23-failopen-debate.md
  - raw/transcripts/2026-04-23-inc204-postmortem-transcript.md
source_hashes:
  - 35908695e477a83f6de25a0ad09d4e912124c790
  - ffc1d104e7f604383e6dd36eced7eec0706f140b
  - 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
  - 2a8633743676e379d02abb3aa0bda19c3795e3b6
  - 53bfbe6b11ef39b4e48179110dbf80cab06c42bb
  - 749625389b82f5c1ba0b090b2946c3f0c73cef07
---

<!-- llmwiki:auto -->

## Summary
fail-closed는 의존 컴포넌트가 불확실하거나 실패할 때 "통과"가 아니라 "거부"를 택하는 안전 기본값이다. Nimbus Pay 결제 경로의 핵심 원칙으로, 중복 결제 장애(INC-204)에서 fail-open이 87건 중복 청구를 일으킨 교훈에서 확립됐다.

## Details
- 결제 경로의 외부 의존(Redis 멱등성 조회 등)이 타임아웃나면 **거부 후 클라 재시도**를 유도한다. 통과시키지 않는다.
- 근거: INC-204에서 Redis 타임아웃을 "키 없음=신규"로 fail-open 처리해 중복 결제가 발생했다. ([[idempotency]])

### 원칙이 확립된 과정
- **fail-open의 기원 (PR-112, 2026-03-15):** "redis 장애 = 결제 전면 장애"를 피하려고 테크리드가 가용성 우선(fail-open)을 선택. 당시에도 중복 결제 우려가 리뷰에 제기됐으나 "redis 가용성이 높다"로 수용.
- **INC-204 (4/21):** 그 트레이드오프가 실현됨 — 87건 중복 청구. 포스트모템에서 테크리드가 본인 결정임을 공식 인정(blameless).
- **개념 정리 (4/23 슬랙):** fail-open 자체가 틀린 건 아니다 — **도메인 의존**이다. 조회수 카운터라면 fail-open이 맞다. 결제는 "잘못 통과"(돈이 두 번 나감)의 비용이 "잘못 거부"(고객 재시도)보다 압도적이라 fail-closed가 기본.

### 적용 사례
- 멱등성 조회 실패 → 503 + Retry-After (PR-140 핫픽스, 4/29 정식 결정).
- 정산 배치 락 획득 실패 → 실행 안 함. 락 저장소(Redis)가 죽어도 "배치가 안 도는" 쪽으로 망하므로 안전한 실패 (5/14 락 기술 선택의 결정 논리). ([[settlement-batch]])
- PG 에러 매핑: 매핑 안 된 에러는 보수적으로 비재시도 분류. ([[payment-gateway-abstraction]])
- 반복 원칙: 돈이 나가는 외부 부수효과 앞에서는 보수적으로 거부하는 쪽이 안전하다.

## Related
- [[idempotency]] — fail-closed가 적용되는 멱등성 조회
- [[settlement-batch]] — 배치 동시 실행을 막는 fail-closed 락
- [[payment-gateway-abstraction]] — 미지의 에러를 비재시도로 분류하는 보수성
- [[oncall-and-alerting]] — "재실행 금지, 락 확인 먼저"의 같은 정신
