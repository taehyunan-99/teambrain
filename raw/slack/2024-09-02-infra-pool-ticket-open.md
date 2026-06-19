---
channel: "#infra"
date: 2024-09-02
author: 강민석
---
강민석: HikariPool 설정 표준화 티켓 오픈했어요. 목표는 maximumPoolSize, connectionTimeout, maxLifetime 기준 통일.
정유진: 각 서비스 현황 파악이 먼저죠.
강민석: 맞아요. 승인 flow처럼 동기 I/O 많은 서비스와 정산 배치처럼 내부 쿼리 위주 서비스 나눠서.
정유진: 트래픽 패턴도 같이 보면 pool 압박 포인트 보이겠어요.
강민석: connection 지연, 타임아웃 에러 이력도 참고할 거예요.
정유진: 다음 주 리뷰 미팅에 올려요.