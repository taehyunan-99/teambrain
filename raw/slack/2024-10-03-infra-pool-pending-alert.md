---
channel: "#infra"
date: 2024-10-03
author: 강민석
---
강민석: HikariPool pending connection 알람 추가했어요. pool에 대기하는 connection 5개 이상이면 경고.
정유진: 실제로 발생하면 어떤 대응 플로우로요?
강민석: maximumPoolSize 여유 확인 → 트래픽 급증 여부 확인 → 승인 쪽 지연 동시 확인.
정유진: 타임아웃 에러 알람이랑 같이 보면 좋겠네요.
강민석: 묶어서 대시보드에 넣어뒀어요. 대응 시간 단축 목표.