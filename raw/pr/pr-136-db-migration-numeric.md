---
created: 2026-04-09
tags: [pr-review, raw-dump, database]
pr: 136
---

# PR #136 — feat: 결제 테이블 마이그레이션 (postgres)

> 작성: 박서연 / 리뷰: 이준호, 김도현 / 머지: 2026-04-09

**이준호 (migration/0012.sql:8)**: amount NUMERIC(19,4)인데 scale 4는 왜요? KRW는 소수점 없잖아요
**박서연**: 어제 회의에서 NUMERIC 결정 났고, scale은 수수료 중간 계산(3.3%) 손실 방지 + 나중에 외화 결제 대비로 4 잡았어요
**김도현**: 외화는 아직 계획에 없으니 over-engineering 같기도 한데... 근데 scale 바꾸는 마이그레이션이 더 비싸니 4로 두는 데 동의
**이준호**: ㅇㅋ. 저장은 어차피 원 단위 정수값이고 계산 여유분이라고 이해할게요
**김도현**: approve / **이준호**: approve
