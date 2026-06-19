---
channel: "#pay-dev"
date: 2024-12-03
author: 김도현
---
김도현: 연말 트래픽 대비해서 승인 flow connection pool 여유도 점검 필요해.
박서연: HikariPool 현재 maximumPoolSize 설정값 보니까 여유 있어요.
김도현: 지난번 외부 PG 지연 때처럼 connection 묶이면 pool 점유율 갑자기 오르니까.
이준호: connectionTimeout 설정 짧게 두면 pool 고갈 전에 실패로 빠지는 효과도 있잖아요.
김도현: 맞아. 타임아웃 설정이 pool 보호 역할도 하지. 지금 설정 확인해보자.
박서연: 12월엔 트래픽 증가 있을 수 있으니 알람 임계값도 같이 체크할게요.