---
channel: "#pay-dev"
date: 2024-09-06
author: 이준호
---
이준호: 승인 레이턴시 모니터링 대시보드 만들었어요.
김도현: 어떤 지표들?
이준호: p50/p95/p99 응답 시간, connection pool 사용률, 타임아웃 에러 수.
박서연: HikariPool 메트릭이랑 같이 볼 수 있어요?
이준호: 네. maximumPoolSize 대비 active 비율도 같이 올렸어요. 트래픽 급증 때 pool 압박 빠르게 보이려고.
김도현: 지연 원인 파악이 훨씬 빨라지겠네요. 잘 됐다.