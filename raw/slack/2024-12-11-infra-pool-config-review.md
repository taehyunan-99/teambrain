---
channel: "#infra"
date: 2024-12-11
author: 강민석
---
강민석: HikariCP 설정 리뷰 결과. connectionTimeout은 현재 적절하고, maximumPoolSize는 현재 트래픽 기준 여유 있어요.
정유진: maxLifetime 설정은요?
강민석: 기본값 30분인데 DB side wait_timeout보다 짧아야 해서 확인 필요합니다.
정유진: 승인 flow에서 long-lived connection이 끊기면 지연 생기기도 하죠.
강민석: connection 재생성 타임아웃 내에 이뤄지면 괜찮은데. pool 건강 지표는 이상 없어요.