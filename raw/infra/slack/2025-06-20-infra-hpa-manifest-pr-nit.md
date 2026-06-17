---
created: 2025-06-20
channel: infra
tags: [pr, raw-dump, infra, k8s, code-review]
---

# PR 코멘트 — k8s manifest 정리 (infra)

**강민석 (리뷰)**:
- `deployment.yaml` resources.requests/limits에 cpu만 있고 memory limit 빠져있어요. OOM 방어용으로 memory limit도 박아두는 게 좋을 듯
- nit: env 블록 정렬이 좀 들쭉날쭉해요. 알파벳 순으로 맞추면 diff 볼 때 편해요
- liveness probe initialDelaySeconds 5초는 좀 빡센데요. 부팅 좀 느린 날 죽일 수도 있어서 15초 정도로

**정유진 (작성자)**:
- memory limit 추가했어요. requests=256Mi / limits=512Mi로
- env 정렬 ㅇㅋ 맞췄습니다 ㅋㅋ 보기 좋네요
- initialDelay 15초로 올렸어요. 확실히 너무 짧았네

**강민석**: 굿 👍 approve할게요
