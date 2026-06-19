---
channel: "#infra"
date: 2024-11-22
author: 강민석
---
강민석: 내년 트래픽 예측치 기반 connection pool capacity planning 했어요.
정유진: HikariPool maximumPoolSize 어떻게 나왔어요?
강민석: 승인 flow 기준 현재 설정 +40% 필요 예상이에요. 내년 Q2 이전에 올려야 할 것 같아요.
정유진: connectionTimeout은 그대로 유지해도 되나요?
강민석: 네. 지연 허용 기준 변경 없으면 타임아웃 건드릴 이유 없어요.
정유진: 스케일링 계획 문서화해두죠.