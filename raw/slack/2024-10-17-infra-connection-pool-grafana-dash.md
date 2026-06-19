---
channel: "#infra"
date: 2024-10-17
author: 정유진
---
정유진: Grafana에 HikariPool 대시보드 패널 추가했어요. maximumPoolSize 대비 active/idle/pending 한 눈에 보이게.
강민석: 승인 flow 트래픽이랑 pool 사용률 겹쳐 보이면 좋겠는데요.
정유진: 그것도 추가했어요. 트래픽 피크 때 pool 점유율 상관관계 보이게.
강민석: connection 대기 타임아웃 에러 카운트도 패널에?
정유진: 네. 지연 즉시 보이게 했어요. 내일부터 활용해보죠.