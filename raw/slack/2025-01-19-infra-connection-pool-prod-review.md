---
channel: "#infra"
date: 2025-01-19
author: 정유진
---
정유진: production HikariPool 설정 감사. maximumPoolSize, connectionTimeout, maxLifetime 세 가지.
강민석: 결과는요?
정유진: 모두 현재 트래픽 대비 적절한 값이에요. 승인 flow 지연 없고 타임아웃 에러도 없어요.
강민석: connection pool 건강 상태 A등급이네요.
정유진: 다음 검토는 3월 트래픽 증가 예측 시점에.
강민석: 그때 maximumPoolSize 재검토 같이 하죠.