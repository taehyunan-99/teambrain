---
channel: "#pay-dev"
date: 2024-10-08
author: 박서연
---
박서연: 정산 배치 돌 때 DB connection pool 점유율이 올라가는 게 보이네요.
김도현: 배치 전용 DataSource 분리해야 할 것 같았는데 아직 못 했죠?
박서연: 네. 지금은 메인 HikariPool 공유하는 구조라 배치 돌면 maximumPoolSize 한계 근처까지 올라와요.
김도현: 배치 트래픽 때 승인 flow 쪽 connection 대기 지연 생기면 문제인데.
박서연: 밤 11시 배치라 낮 트래픽이랑 안 겹쳐서 지금은 괜찮아요. 타임아웃 에러는 아직 없어요.
김도현: 일단 다음 스프린트에 DataSource 분리 태스크로 넣어두자.