---
type: source
of: raw/2026-05-13-incident-settlement-double-payout.md
source_hash: 1449c96b5b3d7c91b8450cc7de9b1671ef1bd166
tags: [source, incident]
---

## Summary
정산 이중 송금 장애 INC-231(2026-05-12, 가맹점 3곳·1,840만원). 배치 지연을 멈춤으로 오판해 수동 재실행했고, 정산 멱등성이 명세서 생성까지만 적용돼 송금 단계엔 가드가 없어 이중 송금. 조치로 송금 직전 payout_log UNIQUE 체크 + 배치 분산 락 도입. 교훈: 멱등성은 돈이 실제 나가는 지점에 걸어야 한다(INC-204와 동일).

## Concepts
- 정산 배치
- 멱등성
- fail-closed 원칙
