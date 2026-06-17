---
created: 2025-06-26
tags: [weekly, raw-dump]
---

# 주간단신 2025-06-26 (infra)

- [유진] DB 마이너 패치 윈도우(토 03시) 무사 완료. 페일오버 승격 정상, 커넥션 끊김 체감 없음
- [유진] 결제팀에서 멱등성/세션용 redis 운영 인스턴스 요청 들어옴 → single로 빠르게 띄워줌. 모니터링은 후속
- [민석] redis exporter 결제팀 인스턴스에도 붙이는 중 (used_memory / connected_clients부터)
- [민석] CI 빌드 캐시 미스 원인 lockfile 해시 쪽으로 좁혀지는 중
- 이슈: 없음
- 다음주: redis 기본 알람 연결, 백업 복구 리허설 일정
