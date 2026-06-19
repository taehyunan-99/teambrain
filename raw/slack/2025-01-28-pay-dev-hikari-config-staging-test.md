---
channel: "#pay-dev"
date: 2025-01-28
author: 박서연
---
박서연: staging에서 HikariPool 설정 변경 테스트 중이에요. maximumPoolSize 올리고 connectionTimeout 줄여서.
이준호: 어떤 결과 나왔어요?
박서연: 동시 승인 요청 늘렸을 때 pool 여유 생기고 타임아웃 에러 줄었어요.
이준호: connection 대기 지연은요?
박서연: 거의 사라졌어요. 트래픽 늘어도 pool에서 바로 할당되니까.
이준호: 이 설정으로 production 올리면 되겠네요.
박서연: 리뷰 한 번 더 받고 올릴게요.