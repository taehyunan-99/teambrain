---
type: source
of: raw/transcripts/2026-02-10-tech-debt-review-transcript.md
source_hash: d6d8c22b5750815970dcd4df162c266acc30c7e1
tags: [source]
---

## Summary
결제팀(김도현·박서연·이준호·최민지)이 누적 기술부채를 한자리에 펼친 점검 회의. 다섯 가지를 빚으로 식별했다: (1) 토스 동기 직연동(외부 PG가 느려지면 커넥션 풀이 잡혀 결제 전체 동반 지연), (2) 멱등성 Redis 단독 의존(Redis가 죽으면 멱등이 통째로 뚫림), (3) **MySQL의 유니크 제약·트랜잭션·금액 데이터 타입 한계**로 멱등을 DB 레벨로 받쳐주기가 깔끔하지 않음, (4) 웹훅 재시도 없음(한 번 실패 = 영구 유실), (5) 정산 수기. 박서연이 "이 문제들이 따로 노는 게 아니라 엮여 있다(멱등↔DB, 비동기↔웹훅)"고 짚었고, 김도현이 "패치로 때우는 건 한계, 제대로 한 번 갈아엎는 그림이 필요"하다고 결론. 당장 무엇을 바꿀지는 정하지 않고 **"다음 분기에 아키텍처를 제대로 재정비하자"는 공감대까지만** 합의(전원 동의). MySQL 한계 인지가 분기 리플랫폼 동기의 한 축으로 명시됐다.

## Concepts
- PostgreSQL 선택 (PostgreSQL Choice) — MySQL 한계 인지가 이주 동기
- 멱등성 (Idempotency) — Redis 단독 의존 + DB 미받침
- 비동기 결제 승인 (Async Payment Approval) — 동기 직연동 탈피 동기
- 웹훅 전송 (Webhook Delivery) — 재시도 부재
- 정산 배치 (Settlement Batch) — 수기 정산 한계
