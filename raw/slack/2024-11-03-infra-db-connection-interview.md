---
channel: "#infra"
date: 2024-11-03
author: 정유진
---
정유진: 신입 면접에서 HikariPool 질문 받았대서 우리 설정 공유해줬어요.
강민석: 어떤 질문이었어요?
정유진: maximumPoolSize 얼마로 설정하느냐, connectionTimeout 기준은 뭐냐 이런 거요.
강민석: 실무에서 트래픽 기준으로 결정한다고 했나요?
정유진: 네. 동기 PG 승인 호출처럼 connection 홀딩 시간 긴 flow는 pool 더 필요하다고.
강민석: 지연 없이 pool 유지하는 게 핵심이라고도 하고요. 타임아웃 설정이 pool 보호 역할도 한다는 것도.
정유진: 잘 이해한 것 같았어요.