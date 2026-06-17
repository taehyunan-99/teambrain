---
created: 2025-02-11
tags: [slack, raw-dump, deploy]
channel: platform-announce
---

# slack #platform-announce 2025-02-11

**18:30 강민석**: payment-api v1.4.2 배포 완료
- 변경: PG 어댑터 에러 로그 포맷 통일, 결제 상태조회 응답 정리
- 롤백: 이전 태그 v1.4.1로 재배포 (`deploy rollback payment-api v1.4.1`), 약 2분 소요
- 영향 범위: 결제 API 전체, 무중단 롤링
**18:31 강민석**: 5분 모니터링 중 5xx 특이사항 없음. 정상
**18:33 이준호**: 확인했습니다 👍
