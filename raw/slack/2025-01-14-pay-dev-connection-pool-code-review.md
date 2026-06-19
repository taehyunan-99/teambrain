---
channel: "#pay-dev"
date: 2025-01-14
author: 박서연
---
박서연: HikariPool 설정 코드 리뷰 요청. maximumPoolSize, connectionTimeout, maxLifetime 값들이요.
김도현: maximumPoolSize 이 값은 왜 이렇게 잡았어요?
박서연: 현재 트래픽 기준 승인 flow 동시 connection 수 추산해서 여유 20% 더한 거예요.
김도현: connectionTimeout은?
박서연: 외부 PG 타임아웃 기준에 맞춰서요. 지연 감지하고 빨리 실패시키려고.
이준호: maxLifetime은 기본값인가요?
박서연: 네. 변경 이유 없어서요. pool 전반 설정 LGTM 같은데요?