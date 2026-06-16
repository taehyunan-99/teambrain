---
type: source
of: raw/2025-12-03-decision-sdk-v1-scope.md
source_hash: 1fd8c16543e547f1bef940c1feaa0b3a518a4955
tags: [source]
---

## Summary
가맹점 연동 부담을 줄이기 위해 결제 SDK v1 범위를 JS SDK로 한정하고 결제 호출 + 결과 폴링을 래핑하기로 확정했다. 멱등 키 자동생성은 기본 on(권장)이되 강제는 아니며, SDK를 우회한 직접 API 호출 경로는 막지 않는다.

## Concepts
- SDK v1 스코프
- JS SDK
- 결제 호출 및 폴링 래핑
- 멱등 키 자동생성
