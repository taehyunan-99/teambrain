---
channel: "#infra"
date: 2024-12-27
author: 강민석
---
강민석: Nimbus Pay connection pool 운영 가이드 최종본 올렸어요.
정유진: 핵심 내용은?
강민석: HikariPool maximumPoolSize 기준 산정 공식, connectionTimeout 서비스 타입별 권장값, maxLifetime 설정 이유, 승인 flow 특이사항.
정유진: 트래픽 기준 pool 사이즈 재산정 주기도?
강민석: 분기별 체크로 명시했어요. 타임아웃 에러 급증하면 즉시 검토.
정유진: 지연 감지 → pool 사이즈 조정 → 원인 파악 순서도 있고요?
강민석: 네. connection 이슈 대응 플레이북이에요.