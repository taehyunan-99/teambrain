---
channel: "#pay-dev"
date: 2024-11-28
author: 박서연
---
박서연: slow query 있으면 connection 홀딩 시간 길어져서 HikariPool 압박 오는 거 맞죠?
김도현: 그렇지. 슬로우 쿼리가 connection 묶어두면 pool 소진 속도 빨라지고 타임아웃 에러로 이어질 수 있어.
박서연: 승인 flow에서 느린 쿼리 있으면 트래픽 증가 시 지연 먼저 오겠네요.
김도현: maximumPoolSize 늘리는 것도 방법이지만 근본은 쿼리 최적화죠.
박서연: 둘 다 병행하는 게 안전하겠어요.