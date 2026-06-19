---
channel: "#pay-dev"
date: 2024-11-14
author: 박서연
---
박서연: 장애 드릴. HikariPool pool 고갈 시나리오 테스트.
김도현: maximumPoolSize 어떻게 설정하고?
박서연: 의도적으로 작게 줄여서 트래픽 넣어봤어요. connection 대기 → 타임아웃 에러 → 승인 실패 패턴 재현됐어요.
이준호: 실제로 저런 지연이 사용자한테 노출되면 CS 터지겠네.
박서연: connectionTimeout 줄이면 빨리 실패해서 pool 점유 줄어드는 효과 있어요.
김도현: 드릴 결과 문서화해두자. pool 사이즈 설정 기준이랑 대응 플레이북.