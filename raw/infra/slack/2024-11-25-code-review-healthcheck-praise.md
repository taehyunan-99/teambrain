---
created: 2024-11-25
tags: [slack, raw-dump, code-review, pr, infra]
channel: infra
---

# slack #infra 2024-11-25

**11:30 정유진**: 민석님 헬스체크/매니페스트 PR 봤어요. probe 분리 깔끔하게 잘했네요 👍
**11:31 정유진**: liveness랑 readiness 따로 둔거 좋아요. 예전엔 그냥 하나로 퉁쳤는데
**11:32 강민석**: 헤헤 readiness는 db 커넥션까지 확인하게 해놨어요. 안붙으면 트래픽 안받게
**11:33 정유진**: 굿. nit 하나만 — initialDelaySeconds 5초는 부팅 좀 걸리면 짧을수도 있어요. 10초로 보죠
**11:34 강민석**: 아 맞네요 부팅 시간 보고 올릴게요
**11:35 정유진**: 나머진 approve 할게요
