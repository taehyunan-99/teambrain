---
title: fail-closed 원칙 (Fail-Closed Principle)
tags: [reliability, principle, payment]
created: 2026-06-12
updated: 2026-06-16
sources:
  - raw/2026-04-22-incident-duplicate-charge.md
  - raw/2026-04-29-decision-idempotency-db-unique.md
  - raw/2026-05-13-incident-settlement-double-payout.md
  - raw/pr/pr-112-idempotency-middleware.md
  - raw/slack/2026-04-23-failopen-debate.md
  - raw/transcripts/2026-04-23-inc204-postmortem-transcript.md
  - raw/slack/2025-05-21-settlement-failover-batch-safety.md
  - raw/settlement/transcripts/2025-07-22-payout-idempotency-design.md
source_hashes:
  - 35908695e477a83f6de25a0ad09d4e912124c790
  - ffc1d104e7f604383e6dd36eced7eec0706f140b
  - 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
  - 2a8633743676e379d02abb3aa0bda19c3795e3b6
  - 53bfbe6b11ef39b4e48179110dbf80cab06c42bb
  - 749625389b82f5c1ba0b090b2946c3f0c73cef07
  - 684d0e34022df0784480575e404b7c129e12f639
  - 3e1f7c167c047b4890e0513d2dbb620cfd14ca6b
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

### 선례 — 원칙 확립 이전의 정산·인프라 사례 (2025)
INC-204(2026-04)에서 명문화되기 전부터 정산·인프라 영역에 같은 정신의 판단이 선행했다.
- **자동 지급 멱등 설계 (2025-07-22):** 송금 자동화 설계 회의에서 "모호하면 사람이 본다"의 원형이 나왔다 — 단일 인스턴스 하루 1회 실행 전제에선 트랜잭션+상태 체크로 충분하나, 동시 실행 같은 불확실성이 생기면 락/유니크 가드 없이는 자동 송금을 보장하지 못한다고 정리했다. 이 보류된 안전 판단이 2026 정산 송금 가드("자동 재송금 금지, 모호하면 사람이 본다")로 이어진다. ([[settlement-batch]])
- **페일오버 중 배치 안전성 (2025-05-21):** MySQL HA 페일오버가 04:00 정산 배치 중 발생하면 배치가 부분 처리되는데, 재실행 시 이미 확정된 명세서를 다시 만들면 회계 정합성이 깨진다 → "불확실하면 안 돌린다"는 판단으로 DB 레벨 복합 유니크 가드 보완과 배치 재실행 절차 문서화를 인프라 합의에 포함하기로 했다. 페일오버 윈도우 동안 쓰기를 거부하는 DB 정책([[postgresql-choice]])과 같은 결의 보수적 안전 기본값.

## Related
- [[idempotency]] — fail-closed가 적용되는 멱등성 조회
- [[settlement-batch]] — 배치 동시 실행을 막는 fail-closed 락
- [[payment-gateway-abstraction]] — 미지의 에러를 비재시도로 분류하는 보수성
- [[oncall-and-alerting]] — "재실행 금지, 락 확인 먼저"의 같은 정신
- [[postgresql-choice]] — 페일오버 윈도우 쓰기 거부의 DB 운영 적용
