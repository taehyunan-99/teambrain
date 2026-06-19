---
channel: "#infra"
date: 2024-10-02
author: 강민석
---
강민석: 주간 connection pool 헬스 체크. HikariPool 이상 없음.
정유진: maximumPoolSize 대비 사용률?
강민석: 40% 미만. 트래픽 평시 수준이에요.
정유진: 승인 flow 타임아웃 에러는요?
강민석: 0건. connection 지연도 없어요.
정유진: 안정적이네요. 이 상태 유지하면서 다음 주에 ProxySQL 설정 최종 검토하죠.