---
created: 2024-10-26
tags: [slack, raw-dump, ops, deploy, infra]
channel: infra
---

# slack #infra 2024-10-26

**18:00 강민석**: [배포 완료] 로그 retention 30일 → 60일 변경 완료
- cleanup 스크립트 `-mtime +30` → `-mtime +60`
- log-server-01 적용 완료
**18:02 정유진**: 로그 서버 용량 현재 df 찍어줘요
**18:03 강민석**: 42% used. 60일 retention으로 늘려도 바로 티는 안 나고 서서히 올라가겠죠
**18:04 정유진**: 여유 있으니까 괜찮아요. 트렌드 2주 후 다시 봐요