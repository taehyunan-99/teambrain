---
channel: "#infra"
date: 2024-11-12
author: 정유진
---
정유진: 서비스 복잡해지면서 DataSource 여러 개 관리할 일이 생길 것 같아요. HikariPool을 각 DataSource별 분리 운영하는 방식 검토 중이에요.
강민석: 각 pool의 maximumPoolSize 합이 DB max_connections 넘으면 안 되겠죠.
정유진: 맞아요. 승인 용 DataSource, 정산 용 DataSource 나눠서 트래픽 격리하면 한쪽 지연이 다른 쪽에 영향 안 주고.
강민석: connection 대기 타임아웃도 용도별로 달리 설정할 수 있고요.
정유진: 한 3개월 후에 검토하죠.