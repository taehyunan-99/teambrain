---
created: 2024-08-31
tags: [slack, raw-dump, ops, k8s, monitoring]
channel: infra
---

# slack #infra 2024-08-31

**15:00 강민석**: readinessProbe timeout 설정 PR 올렸어요. 오탐 줄이는 게 목적이에요

**15:02 정유진**: `timeoutSeconds` 얼마로 바꿨어요?

**15:03 강민석**: 1초 → 3초로요. 새벽에 pod 뜰 때 헬스체크 오탐 나는 케이스가 있었거든요

**15:04 정유진**: 알람은 readinessProbe 실패로 울리는 거죠?

**15:05 강민석**: 맞아요. 임계치랑 timeout 같이 조정한 PR이에요. 모니터링 알람 연동도 같이 수정했어요
