---
created: 2025-04-24
channel: infra
tags:
  - slack
  - raw-dump
  - pr
  - code-review
  - infra
  - k8s
---

# slack #infra 2025-04-24

**13:14 정유진**: 노드 리소스 대시보드 PR 봤어요. 패널 잘 정리했네요
**13:15 정유진**: 근데 memory 패널이 `container_memory_usage_bytes` 쓰는데 이거 캐시 포함이라 좀 부풀어 보일거에요
**13:16 강민석**: 아 맞다 working_set_bytes로 바꿔야겠네요. 그게 실제 압박받는 수치죠
**13:17 정유진**: 네 그게 OOM 가늠하기 좋아요. 그리고 CPU 패널 단위 millicore로 표기 좀 해주면 읽기 편할듯
**13:18 강민석**: ㅇㅋ 단위 라벨 붙일게요. 변수명도 `node_mem`이 좀 모호한데 `node_working_set`으로 바꿀게요
**13:19 정유진**: 오 그게 명확하다 👍 두 개만 고치면 머지해도 될듯
**13:20 강민석**: 넵 바로 수정해서 올릴게요
