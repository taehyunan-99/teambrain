---
title: 수수료 계산 (Fee Calculation)
tags: [settlement, payment, policy]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/pr/pr-127-fee-rounding.md
  - raw/slack/2026-04-10-numeric-vs-bigint.md
source_hashes:
  - 8c31349cd1a9b1a93b4f7c7cd8c1aeb84eedbf40
  - 9be4b50722a253612cfb6cb2c7b98029367b1e84
---

<!-- llmwiki:auto -->

## Summary
가맹점 수수료(3.3%)는 **원 단위 미만 절사**로 계산한다. 이 정책은 코드 리뷰(PR-127)에서 정책 부재가 발견되어 영업 약관 5조 2항으로 확정됐으며, 가맹점에 유리한 방향이다. 1원 차이도 정산 클레임이 될 수 있는 영역.

## Details
- **절사 정책의 출처:** PR-127 리뷰에서 "절사냐 반올림이냐"가 미정인 채 구현(반올림)된 것이 발견됨 → 민지(PM)가 영업 계약서 확인 → 표준 약관 5조 2항 "원 단위 미만 절사" → 코드 수정 + 약관 조항 번호를 주석으로 기록.
- **타입과의 관계:** 수수료 3.3%를 곱하면 원 단위로 떨어지지 않는 중간값이 나온다. 이것이 금액 타입을 `NUMERIC`으로 유지한 핵심 근거다(BIGINT 원 단위 제안은 저장/계산 타입 분리 위험으로 기각). ([[postgresql-choice]])
- **테스트:** 경계값(33.0원, 33.4원, 33.9원) 케이스 포함.
- 수수료 차감은 [[settlement-batch]]의 집계→수수료→명세서 단계에서 수행된다.

## Related
- [[settlement-batch]] — 수수료 계산이 실행되는 정산 파이프라인
- [[postgresql-choice]] — NUMERIC 타입 채택의 근거가 된 소수점 중간계산
