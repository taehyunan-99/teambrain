---
channel: "#pay-random"
date: 2024-11-20
author: 이준호
---
이준호: HikariCP 이름이 왜 HikariPool이냐면 히카리(光)가 빛이라 '빠른 connection pool'이라는 의미래요.
김도현: 모르고 썼네 ㅋㅋ
이준호: maximumPoolSize 기본값 10도 Brett Wooldridge가 의도적으로 낮게 잡은 거라고 하던데.
박서연: 그 기본값 믿고 트래픽 많은 데서 그냥 쓰다가 승인 지연 나는 케이스 꽤 있다고 해요.
이준호: connectionTimeout 기본 30초도 너무 관대하죠. 저 같으면 타임아웃 훨씬 짧게 잡겠는데.