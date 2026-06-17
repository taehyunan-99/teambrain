---
created: 2024-12-03
tags: [slack, raw-dump, deploy]
channel: infra
---

# slack #infra 2024-12-03

**11:05 강민석**: 결제 API v0.9.7 배포합니다. 응답코드 매핑 몇 건 추가랑 로그 필드 보강이에요
**11:06 강민석**: 롤백은 이전 리비전으로 `kubectl rollout undo` 하면 바로 됩니다. K8s 넘어온 뒤로 이건 편하네요
**11:14 강민석**: 배포 완료. replica 2개 다 Running, /healthz 200, 테스트 결제 한 건 정상
**11:15 정유진**: 에러레이트 안 튐 확인. 수고요
**11:16 강민석**: 🙏