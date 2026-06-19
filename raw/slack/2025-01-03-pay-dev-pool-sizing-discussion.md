---
channel: "#pay-dev"
date: 2025-01-03
author: 김도현
---
김도현: 올해 connection pool 운영 방향 잠깐 얘기하자.
박서연: HikariPool maximumPoolSize 올리는 것 고려 중이에요.
김도현: 얼마나?
박서연: 트래픽 예측치 기준으로 현재값에서 50% 올리는 걸 검토하고 있어요.
이준호: 승인 flow에서 동기 PG 호출 연결 시간 고려하면 pool 여유 있는 게 나아요.
김도현: connectionTimeout도 같이 검토해야지. 타임아웃 너무 길면 connection 묶이는 시간 길어지니까.
박서연: 지연 발생 전 pool 고갈 방지하는 게 목표죠.