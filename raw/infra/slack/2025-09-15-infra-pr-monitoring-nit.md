---
created: 2025-09-15
tags:
  - pr
  - raw-dump
  - infra
  - monitoring
  - code-review
---

# PR 코멘트 — infra: redis 메모리 알람 규칙 정리

작성: 강민석 / 리뷰: 정유진 / 2025-09-15

- **정유진** (alerts/redis.yaml): `redis_mem_high` 임계가 80인데 주석엔 75라고 적혀 있어요. 주석만 맞춰주세요 (nit)
- **강민석**: 앗 옛날 값이네요. 주석 80으로 수정했습니다
- **정유진**: idem 인스턴스 알람 규칙 이름이 `idem_redis_mem` 인데 다른 규칙은 `redis_*_mem` 패턴이라 `redis_idem_mem`이 일관적일 듯요
- **강민석**: 오 맞네요 네이밍 통일하겠습니다. 한 번에 grep 되니까 이게 낫겠어요
- **정유진**: 나머진 깔끔해요 👍 라벨에 `team: infra` 붙여둔 거 좋네요. approve
- **강민석**: 감사합니다 🙏 머지할게요
