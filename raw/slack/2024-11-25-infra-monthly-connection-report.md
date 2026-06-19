---
channel: "#infra"
date: 2024-11-25
author: 정유진
---
정유진: 11월 월간 connection pool 현황. HikariPool active 평균 3.2/maximumPoolSize 기준 32%, peak 71%.
강민석: 트래픽 피크 때 71%면 아직 여유 있네요.
정유진: 승인 flow 쪽 connection 대기 타임아웃 발생 건수 월 2건. 모두 외부 PG사 지연이었고요.
강민석: pool 사이즈 조정 필요는 없겠네요. 지연 패턴 계속 보면 되겠고.
정유진: 12월 연말 트래픽 증가 대비해서 임계값 알람 낮춰두면 어떨까요?