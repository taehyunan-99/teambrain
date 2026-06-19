---
created: 2024-10-16
tags: [slack, raw-dump, ops, compress, disk]
channel: infra
---

# slack #infra 2024-10-16

**09:30 강민석**: [배포 완료] logrotate compress 프로덕션 적용 완료
- log-server-01 적용 완료
- 첫 압축 실행은 내일 새벽 logrotate 타임에 자동
**09:32 정유진**: 내일 아침 df 결과 보면 변화 보이겠네요
**09:33 강민석**: 실제 용량 정리는 내일부터 쌓이는 로그부터 적용이라 바로 눈에 띄는 차이는 없을 거예요
**09:34 정유진**: 맞아요. 일주일 후쯤 트렌드 보면 확실히 알겠죠