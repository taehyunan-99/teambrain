---
created: 2025-10-13
tags:
  - pr
  - raw-dump
  - infra
  - code-review
---

# PR #31 코멘트 — feat: 결제 API HPA(오토스케일) 도입 + resource requests/limits

작성자: 강민석 / 리뷰어: 정유진

---

**정유진** (manifests/payment-api-hpa.yaml):
> minReplicas 2 좋네요. nit인데 `targetCPUUtilizationPercentage` 주석에 왜 70인지 한 줄 남겨두면 나중에 튜닝할 때 덜 헷갈릴 거 같아요

**강민석**:
> 넵 결정문서 링크랑 같이 주석 달아둘게요

**정유진** (deployment resources):
> requests/limits 값은 최근 한 달 사용량 기준으로 잡은 거죠? limit이 너무 빡빡하면 스케일 도는 와중에 OOM 날 수 있어서

**강민석**:
> 네 p95 기준 + 여유 둬서 잡았어요. 운영 올린 다음 실제 그래프 보고 한 번 더 조정하려고요

**정유진**:
> 굿. 코드 자체는 이상 없어요. resources 분리한 커밋 깔끔하네요 👍
