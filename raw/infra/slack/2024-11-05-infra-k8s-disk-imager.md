---
created: 2024-11-05
tags: [slack, raw-dump, ops, k8s, disk]
channel: infra
---

# slack #infra 2024-11-05

**10:45 강민석**: k8s 이미지 cleanup cron 배포 완료했어요
- 매주 일요일 01:00 `docker image prune -a --filter until=168h`
- df -h 결과 슬랙 리포트 추가
**10:47 정유진**: 굿. 이제 로그 서버 cleanup이랑 k8s 이미지 cleanup 둘 다 자동화됐네요
**10:48 강민석**: 서버 용량 관리 체계가 제대로 잡힌 것 같아서 뿌듯해요 ㅎ
**10:49 정유진**: 디스크 걱정 없이 운영할 수 있겠다. 알람도 조용하고