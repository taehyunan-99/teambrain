---
channel: "#pay-random"
date: 2024-10-26
author: 이준호
---
이준호: 'connection pool 관리자의 고뇌: 크면 메모리 낭비, 작으면 타임아웃'
박서연: ㅋㅋ HikariPool maximumPoolSize 설정하는 게 인생 같다
김도현: 트래픽 예측이 맞아야 승인 지연 없는데 예측은 늘 빗나가고
이준호: connection 묶이면 지연, 풀리면 정상. 이 사이클의 반복
박서연: connectionTimeout 너무 짧으면 에러, 너무 길면 지연. 중용의 미덕이죠
이준호: pool 운영은 철학이다