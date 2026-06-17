---
created: 2024-09-17
channel: infra
tags: [slack, raw-dump, ops, ci, build]
---

# slack #infra 2024-09-17

**16:30 강민석**: CI에서 이미지 빌드 한 번에 6분쯤 걸리네요
매번 npm install부터 다시 도니까

**16:31 정유진**: 레이어 캐시 안 먹고 있어요?

**16:32 강민석**: package.json 먼저 COPY하고 install하는 순서로 바꾸면 의존성 안 바뀔 땐 캐시 탈 텐데 지금 소스 통째로 COPY부터 하고 있어서
그래서 코드 한 줄만 고쳐도 install 다시 돎

**16:33 정유진**: 아 그거 순서만 바꾸면 되겠네
`COPY package*.json` → install → `COPY . .` 순서로

**16:34 강민석**: 넵 바꿔서 돌려보니 의존성 안 바뀐 빌드는 6분 → 1분 40초로 줄었어요

**16:35 정유진**: 굿 그 정도면 쓸만하네요 👍