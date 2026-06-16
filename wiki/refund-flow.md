---
title: 환불 플로우 (Refund Flow) — 설계 예정
tags: [payment, refund, planning]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/slack/2026-06-02-refund-flow-open.md
  - raw/transcripts/2026-06-08-q3-planning-transcript.md
source_hashes:
  - d7e8884fdeb137e1dcb972262599d388000a6d0d
  - b75e48cea4af53b493bfb30ea1f91989f6a38a3a
---

<!-- llmwiki:auto -->

## Summary
**Q3 메인 과제로 확정된 미착수 설계.** 현재는 전액 환불만 지원하며, 부분 환불은 가맹점 요구 1순위(문의 증가 추세)다. 기정산 거래의 차감 정산, 환불 멱등성 등 설계 이슈가 커서 2026 Q3에 착수한다.

## Details

### 현재 상태 (2026-06 기준)
- 전액 환불만 지원. 부분 환불 요구 가맹점에는 "다음 분기" 안내(민지).

### 식별된 설계 이슈
1. **기정산 거래의 부분 환불:** 이미 정산이 나간 거래를 환불하면 차감을 다음 정산에서 처리해야 함. ([[settlement-batch]])
2. **환불 멱등성:** 같은 환불 요청이 두 번 오는 경우의 가드 필요. ([[idempotency]])
3. **적용할 기존 패턴:** 환불도 돈이 나가는 외부 부수효과이므로 payout 가드와 같은 패턴(부수효과 직전 유니크 가드) 적용 — 두 장애(INC-204·231)에서 배운 패턴이 그대로 적용되는 도메인이라는 것이 Q3 계획 회의의 평가. ([[fail-closed-principle]])

### 일정
- 2026 Q3 메인 과제 (6/8 계획 회의 확정). 상세 설계는 미작성.

## Related
- [[idempotency]] — 환불에 그대로 적용될 멱등 가드 패턴
- [[settlement-batch]] — 환불-정산 차감 연동 지점
- [[fail-closed-principle]] — 돈 나가는 경로의 안전 기본값
