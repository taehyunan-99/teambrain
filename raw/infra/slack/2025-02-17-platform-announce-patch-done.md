---
created: 2025-02-17
tags: [slack, raw-dump, deploy, infra, announcement]
channel: platform-announce
---

# slack #platform-announce 2025-02-17

**09:50 강민석**: [공지] 2/15 노드 OS 패치 점검 완료 보고
**09:50 강민석**: 전 노드 순차 재기동 정상 완료, 서비스 영향 없었습니다
**09:51 강민석**: 패치 중 노드 1대가 재기동 후 NotReady로 5분 정도 머물렀는데, kubelet 재시작으로 정상 복귀했습니다. 트래픽은 다른 노드로 분산돼서 영향 없었어요
**09:53 정유진**: 수고했어요. 그 노드만 따로 한번 더 지켜보죠