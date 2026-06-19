---
channel: "#pay-dev"
date: 2025-01-17
author: 최민지
---
최민지: 신규 가맹점 온보딩 예정인데 트래픽 급증 대비 필요할까요?
김도현: 어느 정도 규모예요?
최민지: 현재 TPS 대비 30% 증가 예상이에요.
김도현: connection pool 여유 있어서 괜찮을 것 같아. HikariPool maximumPoolSize 보면 여유 충분하거든.
박서연: 승인 flow에서 DB connection 지연은 없을 것 같아요. 타임아웃 에러 걱정할 수준은 아니에요.
김도현: 오픈 후 모니터링 강화하자.