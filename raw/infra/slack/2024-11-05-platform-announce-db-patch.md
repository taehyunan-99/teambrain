---
created: 2024-11-05
tags: [slack, raw-dump, infra, announcement, maintenance]
channel: platform-announce
---

# slack #platform-announce 2024-11-05

**18:30 정유진**: [점검 예고] prod-db 마이너 보안패치
**18:30 정유진**: 일정: 2024-11-07(목) 03:00~03:30 KST
**18:31 정유진**: 대상: prod-db-01 / prod-db-02 (MySQL 마이너 버전 패치)
**18:31 정유진**: 영향: 패치 중 short read-only 구간 수 분 발생 가능. 새벽 트래픽 적은 시간대라 결제 영향 최소화 예상
**18:32 정유진**: 문제 생기면 즉시 #infra로 핑 주세요. 패치 전 스냅샷 떠둡니다
**18:35 김도현**: 넵 결제팀쪽 모니터링 켜둘게요
