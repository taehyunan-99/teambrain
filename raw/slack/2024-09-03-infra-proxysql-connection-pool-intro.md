---
channel: "#infra"
date: 2024-09-03
author: 정유진
---
정유진: ProxySQL 도입 검토 중인데 connection pool 관리 측면에서 HikariPool 설정이랑 충돌 가능성 있지 않을까요?
강민석: 레이어가 달라서 괜찮을 것 같아요. ProxySQL이 앞단 풀 역할 하고 HikariCP는 각 앱 인스턴스 내 풀로 독립 운영이니까.
정유진: maximumPoolSize 설정 건드릴 필요는 없는 건가요?
강민석: 지금은 그냥 두는 게 나을 것 같아요. 일단 ProxySQL 도입 후 풀 안정화 보면서 판단하죠.
정유진: 승인 flow 쪽은 트래픽 패턴 변동이 심하니까 따로 모니터링 추가해야 할 것 같습니다.