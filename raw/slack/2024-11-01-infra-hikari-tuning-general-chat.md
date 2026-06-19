---
channel: "#infra"
date: 2024-11-01
author: 강민석
---
강민석: HikariCP 튜닝 포인트 정리해보면: maximumPoolSize, connectionTimeout, maxLifetime 세 가지가 핵심이죠.
정유진: connectionTimeout은 얼마로 두는 게 일반적인가요?
강민석: PG 승인처럼 외부 호출 많은 서비스는 5~10초로 짧게 가는 게 낫고, 내부 쿼리만 하는 서비스는 30초도 괜찮아요.
정유진: pool 고갈로 지연 나는 케이스와 타임아웃으로 지연 나는 케이스를 구분해서 접근해야 하는군요.
강민석: 맞아요. 트래픽 패턴 따라 설정이 달라져야 해요. connection 모니터링 없이 기본값 유지하는 건 리스크.