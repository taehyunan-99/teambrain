---
channel: "#infra"
date: 2025-01-07
author: 강민석
---
강민석: 2025년 connection pool 운영 방향 잡아봤어요.
정유진: 어떻게요?
강민석: HikariPool maximumPoolSize 재검토, ProxySQL 안정화 완성, DataSource 분리 추진 세 가지.
정유진: 승인 flow 트래픽 증가 추이 보면서 pool 사이즈 올리는 것도 고려해야겠네요.
강민석: connection 대기 타임아웃 기준도 서비스 SLA 맞춰 재설정하고.
정유진: 지연 감지 알람도 더 정교하게 만들어야 하고. 올해 인프라 과제가 많네요.