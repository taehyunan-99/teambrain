---
title: 정산 배치 (Settlement Batch)
tags: [settlement, batch, architecture]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/2026-03-25-decision-settlement-batch.md
  - raw/2026-05-13-incident-settlement-double-payout.md
  - raw/pr/pr-125-settlement-aggregation.md
  - raw/pr/pr-151-payout-unique-guard.md
  - raw/pr/pr-153-batch-distributed-lock.md
  - raw/slack/2026-03-27-settlement-key-naming.md
  - raw/slack/2026-05-12-inc231-realtime.md
  - raw/slack/2026-05-14-batch-lock-discussion.md
source_hashes:
  - 26bd99230c53aada841f8841fdde795f2baccaca
  - 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
  - 74220c848aa8e3ad5425c32830ffdfb8497d3629
  - ceab4af77a6076f99b265157aaad25f1410da74b
  - e6d5eb68853d4d9dd2880838258540717688588b
  - 84f0a1fd3cb7dc0ae9230e72d51d9fddd626e5ad
  - f2f89b652ed42550c47398d57584ebf635e9c56a
  - 39a6ecd6afe3081fa4baac662fe1a01ea23049df
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 가맹점 매출을 D+1 일배치로 정산한다. 매일 04:00에 전날 승인 거래를 가맹점별 집계 → 수수료 차감 → 송금한다. 정산 멱등 키는 가맹점ID+정산일이며, 이중 송금 장애를 거쳐 송금 단계에도 유니크 가드와 분산 락이 추가됐다.

## Details

### 설계 (2026-03-25)
- 일배치(D+1): 매일 04:00 KST 크론. 전일 00:00~23:59:59 `APPROVED` 거래 기준 — 구현은 `approved_at >= D AND < D+1` 반개구간으로 경계 중복/누락 없음 (PR-125, 120만 건 4.2초 실측).
- 단계: 집계 → 수수료 계산([[fee-calculation]]) → 정산명세서 생성 → 송금 요청 → 결과 기록.
- **정산 멱등 키 (2026-03-27 슬랙 결정 — 정식 문서 없음):** 별도 키 컬럼 없이 `(merchant_id, settlement_date)` 복합 유니크. 재실행 판정도 같은 컬럼 사용.
- 부분 재실행 지원(실패한 가맹점만 재처리).
- 실시간 정산은 환불 정정 복잡성·송금 수수료로 탈락. D+1 충분 여부는 가맹점·영업 사전 확인(경쟁사 동일).

### 이중 송금 장애와 보강 (INC-231, 2026-05-13)
배치 지연을 "멈춤"으로 오판해 수동 재실행했고(슬랙 실시간 스레드에 04:41 재실행 결정 순간이 기록돼 있음 — 송금 API 지연으로 로그만 멈춘 상태였음), 정산 멱등성이 **명세서 생성 단계까지만** 적용돼 송금 단계엔 가드가 없어 이중 송금이 발생했다(가맹점 3곳·1,840만원, 당일 전액 회수). 보강:
- **송금 유니크 가드 (PR-151):** 송금 호출 *전* `payout_log`에 (가맹점ID, 정산일) INSERT(status=initiated) → 유니크 충돌이면 송금 자체를 스킵. initiated 고아 행(INSERT 후 송금 실패)은 1시간 후 수동 확인 큐로 — **자동 재송금은 위험해서 금지**, "돈 나가는 건 모호하면 사람이 본다." ([[idempotency]])
- **분산 락 (PR-153):** Redis lock TTL 2h + 30분 heartbeat 연장(진짜 죽으면 연장이 멈춰 자동 해제). pg advisory lock 안과 논쟁 끝에 "락 실패 = 실행 안 함이라 Redis가 죽어도 안전한 실패"라는 fail-closed 논리로 Redis 채택 (5/14 슬랙).
- **알람 단계화:** "오래 걸림"과 "죽음"을 구분하는 3단계 알람 도입. ([[oncall-and-alerting]])
- 교훈: 멱등성은 돈이 실제 나가는 지점에 걸어야 한다(결제 INC-204와 동일).

### 진행 중 (2026-06)
- 정산명세서 CSV 내보내기 (가맹점 C 요구 → 대시보드 공통 기능으로 확장, PR-162 draft).

## Related
- [[idempotency]] — 정산 송금의 멱등 가드와 공통 교훈
- [[postgresql-choice]] — 정산 집계 쿼리와 유니크 제약을 지원하는 DB
- [[fail-closed-principle]] — 배치 동시 실행을 막는 안전 기본값
- [[fee-calculation]] — 정산 파이프라인의 수수료 절사 정책
- [[oncall-and-alerting]] — INC-231 이후의 배치 알람 단계화
- [[refund-flow]] — 기정산 거래 차감이 얽힐 Q3 과제
