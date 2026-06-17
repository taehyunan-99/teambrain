---
created: 2026-02-09
channel: infra
tags: [slack, raw-dump, deploy, infra, k8s]
---

# slack #infra 2026-02-09

**17:05 강민석**: [배포] ingress 설정만 살짝 바꿨어요. keepalive timeout이랑 worker 커넥션 수 조정
**17:06 강민석**: 트래픽 늘 때 커넥션 일찍 끊기는 케이스 있어서 keepalive 늘렸습니다. 서비스 재시작 없이 reload만 했어요
**17:07 강민석**: 5분 봤는데 에러율 변화 없고 정상이에요. 이상하면 직전 설정으로 reload 돌리면 됩니다
**17:10 정유진**: 굿 👍 reload만이라 롤백도 가벼워서 좋네요
**17:11 강민석**: 넵 설정은 git에 박아뒀어요