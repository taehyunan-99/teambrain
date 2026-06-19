---
created: 2025-01-24
tags: [slack, raw-dump, ops-chatter, infra, ci, build]
channel: #infra
---

# slack #infra 2025-01-24

**14:05 이준호**: CI 빌드 깨졌어요. 권한 에러 같아요
**14:07 강민석**: 어떤 스텝이요?
**14:08 이준호**: build 단계에서 `permission denied: ./scripts/deploy.sh`
**14:10 강민석**: 아 실행 권한 없이 커밋됐네요. `chmod +x` 빠진 거예요
**14:11 강민석**: 파이프라인에서 스크립트 실행 전 권한 부여 스텝 추가했어요
**14:15 이준호**: 빌드 통과했어요. 테스트도 그린
**14:16 강민석**: 앞으로 스크립트 추가할 때 실행 권한 체크 README에 명시해둘게요