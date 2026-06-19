---
channel: "#pay-random"
date: 2024-11-16
author: 이준호
---
이준호: '개발자: maximumPoolSize 10이면 충분하겠지 / 트래픽: 안녕 ^^'
박서연: ㅋㅋㅋ HikariPool 기본값 신뢰한 결과 = 타임아웃 파티
김도현: 실화 기반인가요 ㅋㅋ
이준호: 남의 서비스 얘기입니다... connection 대기 지연으로 승인 다 터진 케이스 아티클 봤어요
박서연: 풀 고갈 상황에서 connectionTimeout 30초면 사용자는 30초 기다리는 거잖아요. 지연의 극한
이준호: 교훈: 트래픽 나오기 전에 pool 설정 점검을