---
created: 2025-09-19
channel: platform-announce
tags:
  - slack
  - raw-dump
  - deploy
  - infra
  - redis
  - idempotency
---

# slack #platform-announce 2025-09-19

**20:05 정유진**: [점검 공지] idem 전용 Redis 인스턴스 보안 패치 점검창 안내
**20:05 정유진**: 대상: 결제 멱등키 전용 Redis (idem-redis-01)
**20:06 정유진**: 일정: 2025-09-20(토) 03:00~03:15 KST. 결제팀과 미리 협의했고, 새벽 트래픽 최저 시간대로 잡았습니다
**20:07 정유진**: 작업 중 짧은 페일오버가 있어서 그 순간 멱등키 조회/쓰기에 ms 단위 재연결이 생길 수 있어요. 클라이언트 재시도로 흡수되는 수준입니다
**20:08 정유진**: maxmemory-policy(volatile-lru) 유지, 데이터 보존됩니다. 문제 시 즉시 롤백
**20:10 박서연**: 협의한 대로네요. 03시면 결제 거의 없으니 ㅇㅋ 합니다. 작업 끝나고 한 번 핑만 주세요 🙏
**20:11 정유진**: 넵 끝나면 #pay-dev에도 결과 남길게요
