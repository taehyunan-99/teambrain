---
channel: "#infra"
date: 2025-01-02
author: 정유진
---
정유진: 신년 HikariPool 설정 감사. 모든 서비스 connection pool 설정 스프레드시트에 정리했어요.
강민석: maximumPoolSize 기준으로 보면 대부분 적절한데 한 서비스 낮더라고요.
정유진: 승인 flow 아닌 내부 서비스라 트래픽 적어서 낮게 잡은 것 같아요.
강민석: 그래도 타임아웃 에러 나면 문제니까 기준값 이상으로 올려두죠.
정유진: connectionTimeout 통일도 필요할 것 같아요. 서비스마다 달라서.
강민석: 올해 중으로 표준화 작업 하죠.