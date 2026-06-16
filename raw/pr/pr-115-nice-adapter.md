---
created: 2026-03-19
tags: [pr-review, raw-dump, payment, gateway]
pr: 115
---

# PR #115 — feat: 나이스페이 어댑터

> 작성: 이준호 / 리뷰: 박서연 / 머지: 2026-03-19

**박서연 (nice_adapter.go:30)**: 나이스는 응답이 EUC-KR로 올 때가 있다던데 인코딩 처리 있어요?
**이준호**: 헤더 보고 EUC-KR이면 UTF-8 변환해요. 테스트 케이스도 있어요 (nice_adapter_test.go:120)
**박서연 (nice_adapter.go:55)**: 토스 어댑터랑 에러 매핑 상수 파일 공유하는 구조 좋네요. unknown → 비재시도 규칙도 동일하게 적용됐고
**이준호**: 네 PR-108에서 정한 규칙 그대로요
**박서연**: approve 👍
