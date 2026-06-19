---
channel: "#pay-dev"
date: 2024-10-16
author: 김도현
---
김도현: 승인 slow log 분석 중. connection 대기 지연이 원인인 케이스 보려고.
박서연: HikariPool 메트릭이랑 같이 보면 좋겠는데요.
김도현: pending connection 수 시간대별로 뽑아봤는데 평시는 0이에요.
이준호: PG사 응답 느렸던 날이랑 비교해봐야겠네요.
김도현: 나이스 점검 때 connection 홀딩 시간 길어진 게 보이고. maximumPoolSize 한계까지는 안 갔고.
박서연: 트래픽 정상이면 타임아웃 전 회복되는 패턴이네요.