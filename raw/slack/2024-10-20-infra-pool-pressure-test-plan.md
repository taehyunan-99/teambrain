---
channel: "#infra"
date: 2024-10-20
author: 강민석
---
강민석: 다음 달 HikariPool pressure test 계획 잡으려고요.
정유진: 어떤 시나리오로요?
강민석: 트래픽 급증 + 외부 PG 지연 동시 발생. connection 홀딩 길어지면 pool 어떻게 되는지.
정유진: maximumPoolSize 임계값 찾는 거네요.
강민석: 맞아요. 승인 타임아웃 에러 나기 전 pool 고갈 threshold 확인이 목표.
정유진: connectionTimeout 다르게 설정하면서 비교도 해보면 좋겠어요.
강민석: 11월 초에 staging 잡을게요.