---
created: 2026-02-13
tags: [pr, raw-dump, infra, code-review, k8s]
---

# PR 코멘트: HPA 임계치 튜닝 (infra)

작성자: 강민석 / 리뷰어: 정유진

---

**정유진** (`hpa-payment.yaml` L18):
> targetCPUUtilization 60으로 내린 건 의도된 거죠? 기존 70이었는데

**강민석**:
> 네 의도한 거예요. 스케일아웃이 좀 늦게 붙는 느낌이라 60으로 당겼어요. 70이면 이미 부하 차고 나서 파드 뜨더라구요

**정유진** (`hpa-payment.yaml` L22):
> nit: maxReplicas 주석에 "임시"라고 달려있는데 이거 떼도 되지 않나요? 한참 됐는데 ㅋㅋ

**강민석**:
> 아 맞다 그거 옛날 흔적이네요. 떼겠습니다

**정유진**:
> 나머진 LGTM 👍 머지하셔도 돼요

**강민석**:
> 감사합니다 🙏