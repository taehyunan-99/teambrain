---
channel: "#infra"
date: 2024-10-22
author: 정유진
---
정유진: ProxySQL 도입 2주 됐는데 connection pool 안정화는 잘 되고 있어요.
강민석: HikariPool active 수치 변동 줄었나요?
정유진: 네. 이전엔 트래픽 피크 때 connection 대기 지연이 간헐적으로 찍혔는데 ProxySQL 이후로 거의 없어요.
강민석: maximumPoolSize는 그대로 두고요?
정유진: 현재 설정 유지 중이에요. 승인 flow 쪽 타임아웃 에러도 없고요.
강민석: 잘 되고 있네요.