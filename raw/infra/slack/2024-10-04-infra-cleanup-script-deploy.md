---
created: 2024-10-04
tags: [slack, raw-dump, ops, deploy, cleanup]
channel: infra
---

# slack #infra 2024-10-04

**16:02 강민석**: [배포 완료] 로그 cleanup 스크립트 로그 서버에 배포했습니다
- /opt/scripts/log-cleanup.sh
- 30일 이상 .log.gz 삭제
- 실행 후 df -h 결과 #infra 채널에 자동 게시
- 첫 실행: 내일 새벽 02:00
**16:04 정유진**: 굿! 내일 아침에 결과 확인해봐요
**16:05 강민석**: 네. 용량 얼마나 줄지 기대되네요 ㅋㅋ