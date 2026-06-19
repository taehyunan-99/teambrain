---
channel: "#pay-random"
date: 2024-10-25
author: 이준호
---
이준호: 'High Performance MySQL' 읽는데 connection pool 챕터가 좋네요.
김도현: HikariPool 관련 내용도 나와?
이준호: 직접은 아니지만 maximumPoolSize 같은 설정 원리 이해에 도움 돼요.
박서연: 동기 PG 승인처럼 external I/O 긴 서비스의 pool 운영이 특히 어렵다고 하던데.
이준호: 맞아요. 타임아웃이랑 pool 사이즈 같이 봐야 한다고. 트래픽 급증 시 지연으로 이어지기 쉬우니까.