---
created: 2025-12-12
channel: infra
tags:
  - pr
  - raw-dump
  - code-review
  - observability
  - infra
---

# PR #58 코멘트 — chore: 알람 룰 YAML 정리

작성자: 강민석 / 리뷰어: 정유진

**정유진 (line 12)**: nit — `redis_mem_high` 룰 이름이 다른 룰들은 다 `_warn` / `_crit` 접미사 쓰는데 여기만 `_high`네요. 통일하면 좋을 듯

**강민석**: 아 맞다 그거 처음에 만든 거라 네이밍이 따로 놀았네요. `redis_used_memory_warn`으로 맞출게요

**정유진 (line 27)**: duration `5m`인데 주석에 `// 3분`이라고 적혀 있어요 ㅋㅋ 옛날 값인 듯

**강민석**: 헐 주석 안 고쳤네 ㅠㅠ 지웠어요. 값이 진실이니까

**정유진**: ㅋㅋㅋ 나머진 깔끔해요 LGTM. 머지하셔도 됩니다 👍
