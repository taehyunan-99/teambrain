---
created: 2025-11-10
tags: [pr, raw-dump, infra, code-review]
---

# PR 코멘트 — chore: HPA 임계치 주석/네이밍 정리

- PR: infra repo, 작성자 강민석, 리뷰어 정유진
- 작은 정리 PR (값 변경 없음)

**정유진**: `cpuTarget70` 변수명은 70이 매직넘버처럼 박혀 있으니 그냥 `cpuTargetPercent`로 두는 게 나을 듯. 나중에 값 바꿔도 이름 안 헷갈리게
**강민석**: 동의요 바꿨습니다
**정유진**: 그리고 min/max replica 주석에 "클러스터 노드 용량 기준"이라고 한 줄 남겨주면 다음 사람이 왜 10인지 알 듯
**강민석**: 추가했어요. 나머지는 포맷팅이라 그대로 머지할게요
**정유진**: 👍 LGTM
