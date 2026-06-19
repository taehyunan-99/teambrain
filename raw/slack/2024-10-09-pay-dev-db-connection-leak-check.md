---
channel: "#pay-dev"
date: 2024-10-09
author: 박서연
---
박서연: connection leak 검사 돌렸는데 이상 없어요.
김도현: HikariPool leakDetectionThreshold 설정 있어?
박서연: 2000ms로 잡아뒀어요. 승인 flow에서 2초 이상 connection 홀딩하면 로그 찍히게.
이준호: 실제로 leak 찍힌 건 있어요?
박서연: 없어요. 타임아웃 전에 다 반환되고 있어요. pool도 maximumPoolSize 한참 밑이고 트래픽 정상.
김도현: 좋아. 이대로 유지하자.