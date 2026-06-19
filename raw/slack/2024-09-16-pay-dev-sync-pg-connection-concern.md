---
channel: "#pay-dev"
date: 2024-09-16
author: 김도현
---
김도현: 동기 PG 승인 호출이 connection 홀딩 시간이 긴 건 구조적 이슈야.
이준호: 비동기로 가면 pool 문제 줄겠죠?
김도현: 그렇지. 동기 호출 구조에서 타임아웃이 길면 connection이 오래 묶여서 pool 소진 위험이 있어.
박서연: 지금 당장은 트래픽이 낮아서 HikariPool maximumPoolSize 여유 있지만.
김도현: 트래픽 늘면 구조 개선 검토해야 할 것 같아. 승인 지연도 연관 있고.
이준호: 비동기 전환이 복잡한데 일단 pool 모니터링 강화하면서 보죠.