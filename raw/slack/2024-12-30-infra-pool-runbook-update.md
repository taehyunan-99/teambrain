---
channel: "#infra"
date: 2024-12-30
author: 강민석
---
강민석: connection pool 장애 대응 runbook 업데이트했어요.
정유진: 주요 내용은요?
강민석: HikariPool 고갈 증상: pending connection 급증 → 승인 지연 → 타임아웃 에러. 대응: 트래픽 확인 → maximumPoolSize 임시 조정 → 근본 원인 파악.
정유진: connectionTimeout 기준 알람 추가됐고요?
강민석: 네. 단계별 에스컬레이션 절차까지 넣었어요.
정유진: 연말 대비 잘 됐네요.