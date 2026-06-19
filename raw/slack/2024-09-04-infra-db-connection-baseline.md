---
channel: "#infra"
date: 2024-09-04
author: 정유진
---
정유진: 오늘 DB connection 기준치 측정했어요. 평시 승인 flow connection 사용량 평균 2~3.
강민석: HikariPool maximumPoolSize 대비 여유 많네요.
정유진: 트래픽 피크 때 최대 6 정도였어요.
강민석: pool 사이즈 충분한 것 같은데 타임아웃 설정은요?
정유진: connectionTimeout 기본값 그대로예요. 아직 지연 이슈 없어서.
강민석: 이 기준치 저장해두고 나중에 비교하면 좋겠어요.