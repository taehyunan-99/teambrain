---
created: 2024-09-24
tags: [slack, raw-dump, ops, logrotate, confirm]
channel: infra
---

# slack #infra 2024-09-24

**16:10 강민석**: logrotate 상태 확인 리포트
- /var/lib/logrotate/status 기준 마지막 실행: 2024-09-23 03:05
- rotate 대상 파일들 전부 새 파일로 교체 완료
- 구 파일 .1 → 압축 설정 아직 미적용
**16:12 정유진**: 정상이네요. 로그 서버 용량 현재 df 찍어볼까요
**16:13 강민석**: 지금 찍으면
```
/dev/sda1: 44% used
```
**16:14 정유진**: 44%면 무난해요. 이번 주도 이상 없음