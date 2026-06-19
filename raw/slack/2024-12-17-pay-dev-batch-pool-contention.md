---
channel: "#pay-dev"
date: 2024-12-17
author: 박서연
---
박서연: 연말 배치 량 늘면서 정산 배치 DB connection pool 점유 시간 늘어났어요.
오세훈: HikariPool active 얼마나 올라갔어요?
박서연: maximumPoolSize 80%까지. 배치 돌 때만 그러니 승인 flow 트래픽이랑 겹치지 않아서 지연은 없었어요.
오세훈: 연말엔 배치 물량 더 늘 텐데 DataSource 분리 빨리 해야겠네요.
박서연: connection 타임아웃 에러는 아직 0건이에요. 근데 여유 없어지긴 했어요.
오세훈: pool 사이즈 임시로 올려둘까요?