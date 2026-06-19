---
channel: "#settlement"
date: 2024-10-12
author: 오세훈
---
오세훈: 배치 실행 중 HikariPool connection 대기 로그 뜨면 어디 보는 게 빠른가요?
한지우: hikari_connections_pending 메트릭 먼저요. maximumPoolSize 대비 active 비율도.
오세훈: 배치 트래픽이랑 겹치는 게 없는데 왜 대기가 생기는지 이해가 안 가서요.
한지우: 쿼리 실행 시간이 길면 connection 홀딩이 늘어서 pool이 차는 거예요. 타임아웃 전에 완료는 됐고요?
오세훈: 네. 에러는 없었는데 지연은 좀 있었어요.
한지우: slow query 있으면 찾아봐요.