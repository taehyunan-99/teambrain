---
created: 2024-09-20
tags: [slack, raw-dump, ops, pay-dev, log]
channel: infra
---

# slack #infra 2024-09-20

**16:05 박서연**: 로그 서버에서 특정 가맹점 결제 로그 조회 방법이 어떻게 돼요?
**16:07 강민석**: /var/log/app/access.log 에서 grep으로 찾으면 돼요. 오늘 날짜 기준으로는 access.log, 이전 날짜는 access.log-YYYYMMDD.gz
**16:09 박서연**: zcat으로 gz 파일 열면 되는 거죠?
**16:10 강민석**: 네. zcat access.log-20240919.gz | grep 가맹점ID 식으로요
**16:11 정유진**: 나중에 검색 도구 제대로 만들어야 하는데. 지금은 로그 서버 디스크 용량 df 찍어보고 여유 있으면 grep 쓰는 방식이에요