---
created: 2025-01-16
tags: [slack, raw-dump, ops-chatter, infra, ci, build]
channel: #infra
---

# slack #infra 2025-01-16

**09:10 이준호**: CI 빌드가 깨졌어요. 환경변수 못 찾는다고
**09:12 강민석**: 어떤 변수요?
**09:13 이준호**: `PAYMENT_GATEWAY_SECRET_KEY` 이거요. 스테이징 환경 설정에서 빠진 것 같아요
**09:15 강민석**: 아 CI secrets 설정에서 누락됐네요. 추가할게요
**09:20 강민석**: 추가했어요. 파이프라인 재시작해봐요
**09:28 이준호**: 그린 떴어요! 테스트도 전부 패스
**09:29 강민석**: 새 변수 추가할 때 CI secrets 체크리스트 공유해둘게요