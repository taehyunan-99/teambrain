---
created: 2025-01-17
tags: [slack, raw-dump, ops-chatter, infra, ci, branch]
channel: #infra
---

# slack #infra 2025-01-17

**15:00 강민석**: CI 파이프라인 브랜치 전략 논의해요
**15:01 강민석**: 지금은 모든 브랜치에 full build 돌리는데, main/release 브랜치에만 full 하고 feature에는 lint+test만 하는 게 어때요?
**15:03 정유진**: 빌드 시간 줄이는 거죠. 빌드 자체는 main 머지 때만?
**15:04 강민석**: 맞아요. 도커 이미지 빌드는 배포 대상 브랜치에서만
**15:05 이준호**: 그럼 feature PR에서는 테스트 통과 확인만 하고 머지하는 거죠?
**15:06 강민석**: 네. 그게 실용적일 것 같아요. 어떻게 생각해요?
**15:07 정유진**: 한번 해보죠. 문제 생기면 롤백하면 되고