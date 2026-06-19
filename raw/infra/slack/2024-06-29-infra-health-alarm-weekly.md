---
created: 2024-06-29
tags: [slack, raw-dump, ops, monitoring, alarm]
channel: infra
---

# slack #infra 2024-06-29

**16:30 정유진**: 이번 주 알람 오탐 현황이에요. 헬스체크 오탐 2건, timeout 오탐 5건, 기타 3건이에요

**16:32 강민석**: 오탐 5건 중 timeout 관련이 제일 많네요. 어떤 서비스들이에요?

**16:33 정유진**: 결제 API PG 연동 timeout이 3건, Redis 커넥션 timeout이 2건이에요

**16:34 강민석**: 새벽에 집중돼요?

**16:35 정유진**: 맞아요. 새벽 2시~4시에 몰려있어요. 임계치 조정이랑 모니터링 시간대 설정 검토할게요
