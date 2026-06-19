---
channel: "#pay-dev"
date: 2024-10-27
author: 박서연
---
박서연: HikariPool 디버그 모드 켜면 connection 생성/반환 로그 다 나오는데 production에선 부담스럽죠.
김도현: staging에서만 쓰는 게 낫겠지. production에서 너무 많은 로그는 오히려 지연 유발.
이준호: maximumPoolSize 관련 이슈 생기면 hikari_connections_pending 메트릭으로 충분하지 않나요?
박서연: 맞아요. 타임아웃 에러 로그랑 같이 보면 승인 flow pool 문제 금방 잡혀요.
김도현: 트래픽 패턴 이상할 때만 디버그 모드 켜는 걸로.