---
channel: "#infra"
date: 2025-01-23
author: 정유진
---
정유진: HikariPool 알람 임계값 조정했어요.
강민석: 어떻게요?
정유진: maximumPoolSize 대비 active 80%→70% 경고, 95%→85% 긴급으로 낮췄어요. 트래픽 피크 대비.
강민석: connection 대기 타임아웃 알람은요?
정유진: connectionTimeout 에러 발생 즉시 알람 붙였고요.
강민석: 승인 flow 지연 감지가 훨씬 빨라지겠네요.
정유진: 대응 시간이 관건이니까요.