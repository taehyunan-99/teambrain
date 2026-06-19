---
channel: "#pay-dev"
date: 2024-12-13
author: 이준호
---
이준호: 승인 retry 로직이 pool 압박 줄 수 있지 않을까요?
김도현: retry 중에도 connection 홀딩하면 HikariPool 부담 있지.
이준호: maximumPoolSize가 충분하지 않으면 retry 겹치면서 pool 고갈 위험도 있겠는데요.
박서연: retry timeout 짧게 하고 connection 반환 후 retry 하는 패턴이 나아요.
이준호: 트래픽 많을 때 승인 타임아웃 에러에 retry까지 겹치면 지연 심해지겠다.
김도현: retry 정책 재검토 같이 하자.