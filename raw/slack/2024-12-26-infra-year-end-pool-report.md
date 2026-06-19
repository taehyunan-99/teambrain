---
channel: "#infra"
date: 2024-12-26
author: 정유진
---
정유진: 연말 connection pool 운영 리포트. 전반적으로 안정적이었어요.
강민석: 승인 flow HikariPool 최대 사용률은?
정유진: maximumPoolSize 대비 78%. 타임아웃 에러 2건, 모두 외부 PG 지연.
강민석: 내부 pool 고갈은 없었군요.
정유진: 맞아요. 트래픽 피크 때도 pool 여유 유지했어요. connection 대기 지연 0건.
강민석: 2025 년에도 이 기조로 가죠.