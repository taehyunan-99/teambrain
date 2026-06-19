---
channel: "#settlement"
date: 2024-09-11
author: 한지우
---
한지우: 정산 배치 DB connection 사용 현황 보니까 HikariPool active가 배치 피크 때 높아요.
오세훈: 얼마나요?
한지우: maximumPoolSize 기준 60% 수준. 배치 전용 pool 분리할 필요 있나요?
오세훈: 지금 트래픽에서는 괜찮은데 배치 물량 늘면 생각해봐야 할 것 같아요.
한지우: 승인 flow랑 pool 공유하는 구조가 불안하긴 해요.
오세훈: 지연 나거나 타임아웃 에러 생기면 그때 분리 검토하죠.