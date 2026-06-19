---
channel: "#pay-dev"
date: 2025-01-08
author: 이준호
---
이준호: 토스 어댑터 추가하면 PG 호출 connection 패턴이 바뀔 것 같아요.
김도현: HikariPool에 영향 있겠지? 동시 승인 호출 늘면 pool 점유도 늘고.
이준호: maximumPoolSize 같이 검토해야 할 것 같아요.
박서연: 타임아웃 설정도요. 카드사마다 응답 속도 달라서 트래픽 mix 바뀌면 지연 패턴도 달라질 수 있어요.
김도현: 어댑터 추가 전 pool 여유 확인하고 connection 모니터링 강화하는 게 좋겠어.
이준호: 네, 그렇게 진행할게요.