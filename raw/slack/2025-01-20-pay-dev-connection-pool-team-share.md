---
channel: "#pay-dev"
date: 2025-01-20
author: 박서연
---
박서연: connection pool 트러블슈팅 가이드 정리해서 공유해요.
김도현: 어떤 내용으로요?
박서연: HikariPool 고갈 증상, maximumPoolSize 설정 기준, connectionTimeout 조정 포인트, 지연 원인 분류 (외부 PG vs 내부 pool).
이준호: 승인 flow 특화 내용도 있어요?
박서연: 동기 PG 호출 특성상 connection 홀딩 시간 길다는 거랑 트래픽 증가 시 타임아웃 에러 패턴.
김도현: 온보딩 자료로 쓰기 딱 좋겠다.