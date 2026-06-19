---
channel: "#infra"
date: 2024-10-04
author: 정유진
---
정유진: HikariPool 메트릭 Prometheus에 노출시키는 작업 오늘 머지됐어요.
강민석: 어떤 메트릭 붙였어요?
hikari_connections_active, hikari_connections_idle, hikari_connections_pending 세 개요.
정유진: maximumPoolSize 대비 active 비율 알람 임계값은?
강민석: 일단 80% 넘으면 경고, 95% 넘으면 긴급으로 잡아뒀는데 트래픽 패턴 보고 조정하려고요.
정유진: 승인 flow 쪽 connection 지연 감지에 도움이 되겠네요.