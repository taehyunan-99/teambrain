---
channel: "#infra"
date: 2024-11-27
author: 강민석
---
강민석: Q4 트래픽 기준 connection pool 사이즈 재검토.
정유진: HikariPool maximumPoolSize 현재 설정 충분한가요?
강민석: Q4 피크 예측치 기준으로 승인 flow에서 pool 사용률 최대 70% 예상이에요.
정유진: 여유 있네요. 타임아웃 에러 없을 것 같고.
강민석: connection 대기 지연 없이 연말 지나갈 것 같아요.
정유진: 트래픽 예상치 초과하면 알람 바로 오게 해뒀으니까 대응 빠르게 할 수 있어요.