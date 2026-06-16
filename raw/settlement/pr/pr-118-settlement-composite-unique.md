---
created: 2025-10-29
tags: [pr-review, raw-dump, settlement, database]
pr: 118
---

# PR #118 — feat: settlement 테이블 (merchant_id, settlement_date) 복합 유니크 + upsert

> 작성: 오세훈 / 리뷰: 한지우, 박서연(결제팀 자문) / 머지: 2025-10-29

**한지우 (migration/0034_settlement_unique.sql:5)**: 9월에 배치 두 번 도는 바람에 같은 (가맹점, 날짜) 행이 두 개 생긴 케이스 있었잖아요. 이 마이그레이션 돌리기 전에 기존 중복부터 정리해야 제약이 걸릴 텐데
**오세훈**: 같은 파일 위에 정리 스크립트 먼저 넣었어요. (merchant_id, settlement_date) 그룹으로 묶어서 가장 최신 updated_at 한 행만 남기고 나머지 DELETE → 그다음 ADD CONSTRAINT 순서요
**한지우**: 그 "최신 한 행만 남긴다" 기준이 위험할 수 있어요. 중복 두 행 중 하나가 이미 송금 완료(PAID)면 그 행을 살려야지 updated_at만 보고 지우면 안 돼요
**오세훈**: 아 맞네요. PAID 행이 있으면 그걸 우선 보존하도록 정렬 기준에 status 우선순위 넣을게요. PAID > 그 외, 동순위면 updated_at 최신
**박서연 (settlement_repo.go:88)**: upsert 쪽도 같은 맥락이에요. ON CONFLICT (merchant_id, settlement_date) DO UPDATE 하는데, 이미 PAID인 행을 재실행이 덮어쓰면 안 돼요. 돈 나간 기록을 배치가 다시 계산한 값으로 갈아엎으면 정합성 깨져요
**오세훈**: 그럼 DO UPDATE에 `WHERE settlement.status <> 'PAID'` 붙일게요. PAID 행은 충돌 나도 그대로 두고, PENDING/계산중인 행만 갱신
**박서연**: 네 그 WHERE가 핵심이에요. ON CONFLICT는 충돌만 잡지 어떤 행을 보호할지는 안 정해주니까 — PAID 가드는 명시적으로 걸어야 해요
**오세훈**: 반영했어요. 정리 스크립트 status 우선순위 + upsert WHERE status<>'PAID' 둘 다 커밋했습니다
**한지우**: 스테이징 데이터로 중복 정리 검산했어요. 정리 전 1,204건 중복 → 정리 후 0건, PAID 행 손실 없음 확인. 재실행 두 번 돌려봤는데 PAID 행 안 건드리고 PENDING만 갱신되네요. approve 👍
**박서연**: WHERE 조건 확인했습니다. approve
