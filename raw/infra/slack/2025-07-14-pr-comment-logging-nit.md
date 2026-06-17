---
created: 2025-07-14
channel: infra
tags:
  - pr
  - raw-dump
  - infra
  - code-review
---

# PR #142 monitoring exporter 설정 정리 — 리뷰 코멘트

작성자: 강민석 / 리뷰어: 정유진

---

**정유진** (line 18, `exporter_config.yaml`):
> nit: `scrape_interval: 15s`인데 주석엔 30s라고 적혀 있어요. 주석만 고쳐주세요

**강민석**:
> 헉 복붙 흔적이네요 ㅋㅋ 주석 수정했습니다

**정유진** (line 42):
> 변수명 `redis_conn` 보다 `redis_target` 이 어떨까요? 연결이 아니라 스크랩 대상이라

**강민석**:
> 동의요 바꿨어요

**정유진**:
> 나머지는 깔끔하네요. exporter 라벨 붙는 거 확인했고 approve 합니다 👍
