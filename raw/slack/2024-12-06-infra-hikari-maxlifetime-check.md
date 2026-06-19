---
channel: "#infra"
date: 2024-12-06
author: 정유진
---
정유진: HikariPool maxLifetime 설정 확인했어요. 현재 30분.
강민석: DB wait_timeout이랑 비교해봤어요?
정유진: DB wait_timeout 8시간이라 여유 있어요. 그런데 maxLifetime 너무 길면 stale connection 위험이.
강민석: 그래서 30분 유지는 적절해 보여요. connection 갱신 주기가 pool 안정성 유지에 중요하니까.
정유진: 승인 타임아웃이랑은 별개 설정이고. 트래픽 기준으로 maximumPoolSize는 현재 충분합니다.