---
channel: "#infra"
date: 2025-01-10
author: 강민석
---
강민석: staging에서 HikariPool 한계 테스트 해봤어요. maximumPoolSize 넘기면 connection 대기 큐에 쌓이다가 connectionTimeout 후 에러.
정유진: 그게 실제 트래픽 급증 때 승인 지연으로 이어지는 패턴이군요.
강민석: 맞아요. pool 임계값 넘기면 타임아웃까지 기다리다 실패하는 거라.
정유진: staging에서 최소 몇 TPS부터 pool 고갈 시작했어요?
강민석: 현재 설정값 기준 40 TPS부터 pending connection 생겼어요.
정유진: 실제 production 트래픽 기준으로 여유 계산해봐야겠네요.