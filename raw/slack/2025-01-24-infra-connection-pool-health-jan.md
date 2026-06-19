---
channel: "#infra"
date: 2025-01-24
author: 정유진
---
정유진: 1월 connection pool 현황. HikariPool 전반 안정적이에요.
강민석: maximumPoolSize 대비 최대 사용률은?
정유진: 65%. 트래픽 소폭 증가했지만 pool 여유 충분.
강민석: 승인 타임아웃 에러는요?
정유진: 1건. 외부 PG사 순간 지연이었어요. 내부 connection 대기는 없었어요.
강민석: pool 고갈 없이 한 달 지났네요. 이 상태 유지하죠.