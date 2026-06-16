---
type: source
of: raw/slack/2025-03-24-pg-vendor-lockin-risk.md
source_hash: 8e6a7635aa97eecdbb2de6894e868b60fd16c472
tags: [source]
---

## Summary
이달 두 번째 토스 점검으로 결제가 전면 중단되면서, 결제 로직이 토스 SDK에 직결돼 단일 PG에 종속된 리스크가 부각됐다. 나이스 등 추가 PG를 붙이려면 호출부를 다 뜯어야 하므로 "단일 PG 종속 리스크"와 "추상화 한 겹 필요"를 공식 백로그로 올려 나이스 연동 논의와 함께 다루기로 했다.

## Concepts
- PG 게이트웨이 추상화
- 페일오버 정책
- 기술부채
