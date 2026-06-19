---
channel: "#pay-dev"
date: 2024-11-18
author: 이준호
---
이준호: 오늘 오후 PG 승인 타임아웃 1건 간헐적으로.
김도현: connection pool 상태?
이준호: HikariPool 정상이에요. 트래픽도 평소 수준. PG 응답 지연 일시적인 것 같아요.
박서연: maximumPoolSize 한도까지 올라간 건 아니었고요?
이준호: 아니요. active 4~5 수준이었어요.
김도현: PG사 간헐적 지연이면 retry 로직으로 커버되는 거 아냐?
이준호: 한 건은 retry 후 성공했어요. 이 정도면 허용 범위인 것 같아요.