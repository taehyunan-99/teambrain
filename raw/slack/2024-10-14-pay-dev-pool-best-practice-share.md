---
channel: "#pay-dev"
date: 2024-10-14
author: 이준호
---
이준호: HikariCP 베스트 프랙티스 글 공유. https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
김도현: maximumPoolSize 작게 가야 한다는 주장인데, 동기 외부 호출 많은 PG 승인엔 적용 어렵지.
박서연: connection 홀딩 시간이 길면 pool이 금방 소진되니까 동기 호출 빈도 트래픽 비례해서 봐야 해요.
이준호: 타임아웃 짧게 가서 빨리 실패시키는 것도 pool 보호 전략이더라고요.
김도현: 지연 허용 범위랑 pool 설정 trade-off가 서비스마다 다를 것 같아.