---
created: 2024-12-30
tags: [slack, raw-dump, ops-chatter, infra, ci, build]
channel: #infra
---

# slack #infra 2024-12-30

**09:20 이준호**: CI 빌드 깨졌어요. 확인 부탁드려요
**09:22 강민석**: 보고 있어요. 에러 메시지가 뭐예요?
**09:23 이준호**: `incompatible dependency version: expected 2.3.x, got 2.4.0` 이거요
**09:25 강민석**: 아 lodash 하위 의존성 버전이 자동 업그레이드된 거네요. lockfile 고정이 안 됐어요
**09:27 강민석**: lockfile 업데이트하고 재빌드 했어요. 파이프라인 다시 돌려봐요
**09:35 이준호**: 그린 떴어요! 감사합니다
**09:36 강민석**: 의존성 pinning 관련해서 다음 스프린트 때 정책 논의 한 번 해야겠네요