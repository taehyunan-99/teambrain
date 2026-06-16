---
created: 2026-05-15
tags: [pr-review, raw-dump, settlement, batch]
pr: 153
---

# PR #153 — fix: 정산 배치 분산 락 (INC-231)

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-05-16

**이준호 (batch_lock.go:20)**: lock TTL 2시간 — 배치가 2시간 넘게 걸리면 락이 풀려서 INC-231이 재현될 수 있는 거 아닌가요?
**박서연**: 배치 진행 중 30분마다 TTL 연장(heartbeat)해요. 프로세스가 진짜 죽으면 연장이 멈춰서 락이 풀리고, 살아있으면 계속 잡고 있고
**이준호 (batch_lock.go:45)**: 락 획득 실패 시 동작은요?
**박서연**: 즉시 종료 + "이미 실행 중" 로그. 실행 안 하는 게 기본값(fail-closed). 슬랙에서 정한 그대로요
**이준호**: heartbeat 좋네요. approve 👍
