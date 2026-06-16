---
title: PostgreSQL 선택 (PostgreSQL Choice)
tags: [database, architecture, decision]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/2026-04-08-meeting-db-choice.md
  - raw/2026-04-29-decision-idempotency-db-unique.md
  - raw/pr/pr-136-db-migration-numeric.md
  - raw/slack/2026-04-02-for-update-deadlock.md
  - raw/slack/2026-04-10-numeric-vs-bigint.md
source_hashes:
  - 61b549d07de5f05cb4d6ec5d25ba416a3cad1050
  - ffc1d104e7f604383e6dd36eced7eec0706f140b
  - 1086f41b308ff9f193e95949fce76cbe5d91b6e8
  - da31e98dc78383000cd0b059d948f68bf899c605
  - 9be4b50722a253612cfb6cb2c7b98029367b1e84
---

<!-- llmwiki:auto -->

## Summary
Nimbus Pay는 결제·정산 저장소로 PostgreSQL을 채택했다(2026-04-08). 강한 트랜잭션·유니크 제약·`ON CONFLICT` upsert가 멱등 처리에 핵심이고, 윈도우 함수·CTE가 정산 집계에 유리하기 때문이다.

## Details
- 후보 중 MongoDB는 약한 트랜잭션으로 탈락(개발 속도 이점보다 금액 필드 보호·유니크 제약이 결제에 필수 — 회의 전 슬랙 사전 논쟁 포함), MySQL도 가능했으나 Postgres의 `SELECT ... FOR UPDATE`·부분 인덱스·`ON CONFLICT`가 멱등 처리에 더 유리해 채택.
- 멱등성 유니크 제약과 `ON CONFLICT DO NOTHING`으로 중복 결제·중복 송금을 가드한다. ([[idempotency]])
- **금액 타입 `NUMERIC(19,4)`** (부동소수점 금지). 회의 후 BIGINT 원 단위 이견이 있었으나(4/10 슬랙) "수수료 3.3% 중간계산의 소수점 + 저장/계산 타입 분리 시 변환 버그 위험"으로 NUMERIC 유지 — KRW는 scale 0 운용, scale 4는 계산 여유분 + scale 변경 마이그레이션이 더 비싸다는 판단 (PR-136). ([[fee-calculation]])
- **운영 노하우:** `FOR UPDATE` 데드락은 락 획득 순서를 payment → ledger로 통일해 해결 (4/2). `pgcrypto`는 웹훅 시크릿 암호화 보관에도 사용. ([[webhook-delivery]])
- 이 선택은 멱등성 2중화 결정(DB 유니크가 최종 방어선)과 직접 맞물린다.

## Related
- [[idempotency]] — DB 유니크 제약을 최종 방어선으로 쓰는 멱등성
- [[settlement-batch]] — 윈도우 함수·CTE로 처리하는 정산 집계
- [[fee-calculation]] — NUMERIC 유지의 근거가 된 수수료 소수점 계산
- [[webhook-delivery]] — pgcrypto 시크릿 보관
