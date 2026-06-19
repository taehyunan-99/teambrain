---
channel: "#pay-dev"
date: 2025-01-15
author: 박서연
---
박서연: 어제 부하 테스트 결과 공유. 동시 승인 요청 50 TPS에서 HikariPool active 70% 수준이었어요.
김도현: maximumPoolSize 대비 여유 있네. connection 대기 지연은?
박서연: 없었어요. 타임아웃 에러 0건.
김도현: 100 TPS는요?
박서연: 100 TPS에서 pool 점유율 95% 찍히고 connection 대기 지연 간헐적 발생.
김도현: 트래픽 100 TPS 도달하기 전에 pool 사이즈 올려야겠네.
박서연: maximumPoolSize 조정 PR 올릴게요.