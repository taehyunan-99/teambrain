---
created: 2025-08-15
tags: [slack, raw-dump, deploy, infra, announcement, monitoring]
channel: platform-announce
---

# slack #platform-announce 2025-08-15

**17:10 강민석**: [배포 공지] 모니터링 에이전트 v2.3.1 전 노드 롤아웃 완료
**17:10 강민석**: 변경: 메트릭 수집 주기 30s→15s, redis exporter 패널 보강(evicted_keys, keyspace_misses). 기능 영향 없음
**17:11 강민석**: 순차 적용했고 수집 끊김 없었습니다. 대시보드 약간 더 촘촘해진 것만 체감되실 거예요
**17:12 강민석**: 문제 생기면 이전 버전 v2.3.0으로 롤백 가능. 절차는 핀 런북 참고
**17:14 정유진**: 수집 주기 짧아져서 알람 반응 빨라질 거예요. 노이즈 늘면 임계치 다시 조정하죠
**17:15 강민석**: 넵 며칠 보고 플래핑 있으면 디바운스 넣을게요
