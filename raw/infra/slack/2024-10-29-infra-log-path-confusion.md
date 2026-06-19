---
created: 2024-10-29
tags: [slack, raw-dump, ops, log, config]
channel: infra
---

# slack #infra 2024-10-29

**13:22 오세훈**: 정산 배치 로그 경로가 두 군데 있는 것 같아요. /var/log/settlement 랑 /opt/app/logs 랑
**13:24 강민석**: /opt/app/logs 는 예전 경로예요. 지금은 /var/log/settlement/ 로 통일했어요
**13:25 오세훈**: 아 그럼 /opt/app/logs 안에 있는 오래된 것들은 정리해도 되나요?
**13:27 정유진**: cleanup 스크립트 대상 경로에 /opt/app/logs 추가해서 정리해드릴게요. 서버 디스크 용량 낭비라서요
**13:28 오세훈**: 감사합니다!