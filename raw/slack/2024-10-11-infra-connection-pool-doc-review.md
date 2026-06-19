---
channel: "#infra"
date: 2024-10-11
author: 강민석
---
강민석: HikariCP 공식 문서 보면 maximumPoolSize 기본값이 10인데 production에서 그냥 쓰는 팀들이 꽤 있더라고요.
정유진: 낮은 트래픽 환경엔 괜찮겠지만 동기 I/O 무거운 승인 flow엔 부족할 수 있죠.
강민석: connection 대기 타임아웃 걸리기 전에 pool 모자라면 지연 생기는 거라.
정유진: connectionTimeout 기본 30초도 UX 관점에서는 너무 길고요.
강민석: 실제 부하 테스트 없이 기본값 그냥 두는 건 위험하죠. 이건 온보딩 체크리스트에 추가해야 할 것 같아요.