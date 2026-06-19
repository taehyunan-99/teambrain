---
channel: "#infra"
date: 2024-09-19
author: 강민석
---
강민석: connectionTimeout 정책 표준화 논의. 서비스마다 제각각이라.
정유진: 승인 flow처럼 외부 PG 호출 있는 건 어떻게요?
강민석: 동기 PG 호출은 connection 홀딩 시간이 길어서 HikariPool 압박 올 수 있어요. 타임아웃 짧게 가는 게 pool 보호 측면에서 유리.
정유진: 트래픽 많을 때 지연 최소화도 되고요.
강민석: maximumPoolSize도 같이 고려해서 표준 설정 만들어봅시다.