---
channel: "#infra"
date: 2024-09-25
author: 정유진
---
정유진: Redis 쪽 Lettuce connection pool 사이즈 얼마로 두고 있어요?
강민석: 현재 maxTotal 8인데, 세션 트래픽 증가하면 늘려야 할 것 같아요.
정유진: 타임아웃은요?
강민석: commandTimeout 5초, pool 쪽 연결 대기는 따로 안 걸려 있어요.
정유진: 승인 flow에서 Redis 쓰는 구간도 있어서 지연 나면 연결 유지 시간 영향 있을 것 같은데.
강민석: 그건 HikariPool 아니고 Lettuce라 별개로 모니터링해야죠.