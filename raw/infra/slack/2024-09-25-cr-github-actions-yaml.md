---
created: 2024-09-25
tags: [pr, raw-dump, code-review, ci]
---

# PR #infra/44 GitHub Actions 배포 워크플로 — 리뷰 코멘트

작성자: 강민석 / 리뷰어: 정유진

---

**정유진** (deploy.yml L8):
> `on: push` 면 모든 브랜치 푸시마다 이미지 빌드 돌아요. `branches: [main]` 으로 묶어주세요

**강민석**: 아 그렇네요. 의도는 main만이었는데 빠졌어요. 수정

---

**정유진** (deploy.yml L22):
> 이미지 태그 `latest` 말고 커밋 SHA(`${{ github.sha }}`)로 박아주세요. latest 하나로 돌리면 "지금 prod에 뭐 떠있나"를 또 못 봐요. 우리 이거 때문에 사고 났잖아요 ㅎㅎ

**강민석**: ㅋㅋ 맞다. SHA 태그 + latest 둘 다 푸시하게 해둘게요. 롤백은 SHA로

---

**정유진** (nit, L30):
> 레지스트리 자격증명 plain으로 들어가 있는데 이거 Actions secrets로 빼주세요 🙏

**강민석**: 헉 이거 커밋되면 안 되는데 바로 secrets로 뺄게요

---

**정유진**: SHA 태그랑 secrets 두 개만 꼭 반영하고 머지하죠. 나머진 좋습니다 👍