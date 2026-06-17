---
created: 2025-04-09
channel: infra
tags:
  - slack
  - raw-dump
  - pr
  - code-review
  - infra
  - monitoring
---

# slack #infra 2025-04-09

**11:05 정유진**: 강민석님 exporter 설정 PR 봤어요. 대체로 좋은데 nit 몇 개만요
**11:06 정유진**: scrape_interval이 15s인데 redis 메트릭은 30s로 늘려도 괜찮지 않을까요? 그렇게 자주 안봐도 될거같아서
**11:07 강민석**: 아 디폴트 그대로 둔거에요. 30s로 올릴게요. 어차피 메모리 천천히 차서 15s는 과해요
**11:08 정유진**: 그리고 job 이름 `redis` 보다 `redis-pay-prod`처럼 환경 붙는게 나중에 인스턴스 늘면 덜 헷갈릴듯
**11:09 강민석**: 오 그건 좋네요. 반영할게요
**11:10 정유진**: 나머진 다 ㅇㅋ. relabel 깔끔하게 잘 짰네요 👍
**11:11 강민석**: ㅋㅋ 감사합니다 두 개만 고쳐서 다시 올릴게요
