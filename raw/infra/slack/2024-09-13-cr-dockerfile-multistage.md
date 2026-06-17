---
created: 2024-09-13
tags: [pr, raw-dump, code-review, docker]
---

# PR #infra/41 결제 API Dockerfile 초안 — 리뷰 코멘트

작성자: 강민석 / 리뷰어: 정유진

---

**정유진** (Dockerfile L3):
> `FROM node:18` 인데 멀티스테이지로 빌드/런타임 나누면 이미지 훨씬 가벼워져요. 런타임은 `node:18-slim` 정도로

**강민석**: 넵 멀티스테이지로 바꿀게요. builder에서 빌드하고 slim에 산출물만 복사

---

**정유진** (Dockerfile L9):
> `COPY . .` 말고 `.dockerignore` 추가해서 node_modules / .git 빼주세요. 안 그러면 빌드 컨텍스트 무거움

**강민석**: 아 맞다 .dockerignore 까먹었네요 추가

---

**정유진** (nit, L14):
> `CMD ["npm", "start"]` 보다 `node dist/server.js` 직접 띄우는 게 시그널 전달 깔끔해요. npm이 중간에 끼면 SIGTERM 안 먹는 경우 있어서

**강민석**: 오 그렇군요 반영할게요 🙏

---

**정유진**: 나머진 좋아요. 위 세 개만 반영해서 다시 올려주세요 👍