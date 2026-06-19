---
created: 2024-10-17
tags: [slack, raw-dump, ops, logrotate, verify]
channel: infra
---

# slack #infra 2024-10-17

**11:15 강민석**: compress 배포 다음 날이라 결과 확인해봤어요
- /var/log/app/access.log.1.gz 생성됨
- 파일 크기: rotate 전 200MB → gz 후 38MB
**11:17 정유진**: 81% 압축이네요. 로그 서버 df 지금 어떤가요
**11:18 강민석**: compress 전 43%, 지금도 43%예요. 하루치라 티가 안 나요. 한 달 쌓이면 체감할 거예요
**11:19 정유진**: ㅇㅇ 기대해봐요. 용량 트렌드 그래프 다음 달 말에 다시 보면 차이 보이겠죠