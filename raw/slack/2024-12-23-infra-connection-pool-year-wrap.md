---
channel: "#infra"
date: 2024-12-23
author: 정유진
---
정유진: 2024년 connection pool 관련 이슈 연말 정리.
강민석: 외부 PG사 지연으로 인한 connection 홀딩 케이스 몇 건 있었고, pool 내부 고갈은 없었죠.
정유진: HikariPool 모니터링 붙이고 나서 이슈 조기 발견이 수월해졌어요.
강민석: maximumPoolSize 기준 peak 사용률 80% 미만 유지했고, 트래픽 대비 여유 있었습니다.
정유진: 승인 타임아웃은 모두 외부 요인. 내부 pool 설정은 안정적이었어요.
강민석: 2025년에도 이 기조 유지하면서 DataSource 분리 검토하죠.