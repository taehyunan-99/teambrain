---
type: source
of: raw/slack/2025-02-19-double-charge-cs-spike.md
source_hash: 9973a072974c185e479f862db8b9c083456a3cc7
tags: [source]
---

## Summary
더블클릭·네트워크 재시도로 같은 결제가 두 번 들어오는 중복 결제 환불 요청이 반복되어 CS가 수기 환불로 대응 중이다. 멱등성 키가 없어 동일 요청을 구분하지 못하는 것이 원인으로, 방향은 멱등성 도입으로 잡되 키 단위·저장소 등 구현은 별도 설계로 미뤘다.

## Concepts
- 중복 결제
- 멱등성
