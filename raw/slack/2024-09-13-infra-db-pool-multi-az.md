---
channel: "#infra"
date: 2024-09-13
author: 정유진
---
정유진: Multi-AZ 구성에서 failover 시 HikariPool connection 재연결 동작 확인했어요.
강민석: 타임아웃 에러 많이 났어요?
정유진: maximumPoolSize 내에서 재연결 시도하는데 connectionTimeout 내 완료됐어요.
강민석: 트래픽 있는 상태에서 failover 나면 승인 지연 잠깐 생기겠는데.
정유진: 네. 약 3초 지연 있었고 pool 이상 없이 회복됐어요.
강민석: 수용 가능한 수준이네요. 문서화해두죠.