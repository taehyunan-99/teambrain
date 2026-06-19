---
channel: "#pay-dev"
date: 2024-09-27
author: 이준호
---
이준호: 승인 flow에서 DB connection이 PG 호출 전후로 모두 필요한 건가요?
박서연: 트랜잭션 감싸면 PG 호출 중에도 connection 홀딩하는 거죠.
이준호: 그럼 HikariPool 압박이 생기는 거군요. 외부 PG 응답이 느리면 connection 더 오래 묶이고.
박서연: maximumPoolSize가 충분하지 않으면 타임아웃으로 이어지죠.
이준호: 트래픽 많을 때 특히 위험하겠네요. 지금은 괜찮지만.
박서연: 구조 개선 우선순위로 올려야 할 것 같아요.