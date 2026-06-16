---
created: 2026-03-23
tags: [pr-review, raw-dump, webhook]
pr: 121
---

# PR #121 — feat: webhook_dead_letter 테이블 + 알림

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-03-23

**이준호 (migration/0007.sql:5)**: dead letter 행을 지우는 정책이 없는데 무한히 쌓이나요?
**박서연**: 90일 보관 후 아카이브 배치로 정리하려고요. 이번 PR엔 없고 백로그에 적어뒀어요
**이준호 (notifier.go:33)**: 이메일 발송 실패하면요? dead letter의 dead letter ㅋㅋ
**박서연**: ㅋㅋ 이메일은 best-effort예요. 실패해도 dead letter 행 자체는 남아있으니 대시보드에서 보여요. "기록은 보장, 알림은 노력"
**이준호**: ㅇㅋ 그 한 줄 주석으로 박아주세요. approve
