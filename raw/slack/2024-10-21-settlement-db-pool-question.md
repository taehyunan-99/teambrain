---
channel: "#settlement"
date: 2024-10-21
author: 오세훈
---
오세훈: 정산 배치에서 connection pool 대기가 가끔 생기는데 HikariPool pending 로그 남아요.
한지우: maximumPoolSize 얼마예요?
오세훈: 현재 설정값 보니 그렇게 높진 않아요. 배치 쿼리 concurrent 실행이 많아서.
한지우: 타임아웃 에러는 났어요?
오세훈: 아직 없어요. 지연은 있지만 완료됐고. 트래픽(배치 물량) 더 늘면 문제 될 것 같아요.
한지우: pool 사이즈 올리거나 배치 concurrency 줄이거나 둘 중 하나죠.