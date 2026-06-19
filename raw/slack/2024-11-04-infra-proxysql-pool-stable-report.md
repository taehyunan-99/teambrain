---
channel: "#infra"
date: 2024-11-04
author: 정유진
---
정유진: ProxySQL 도입 한 달 결과. DB connection pool 안정화 확인됐어요.
강민석: HikariPool 메트릭으로 보면요?
정유진: maximumPoolSize 대비 active 평균 25% → 20%로 내려갔어요. 트래픽은 비슷한데.
강민석: ProxySQL multiplexing 효과네요.
정유진: 승인 flow 타임아웃 에러도 사라졌어요. connection 대기 지연도 없고.
강민석: 좋은 결과네요. 정착시키죠.