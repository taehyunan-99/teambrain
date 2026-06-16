---
type: source
of: raw/2025-05-19-decision-mysql-failover-policy.md
source_hash: 5101edd2700a6bb141f5bca216e2bed3321eecd2
tags: [source]
---

## Summary
결제·정산의 금전 트랜잭션 무손실을 보장하기 위해 MySQL 프라이머리 페일오버 표준 정책을 자동 페일오버로 확정하되, 반동기 복제(RPO≈0)·헬스체크/펜싱·페일오버 윈도우 쓰기 거부를 표준 제약으로 두었다. 쓰기 실패는 일시 오류로 간주해 절대 성공 처리하지 않고 멱등 경로로 재시도한다.

## Concepts
- MySQL 페일오버 정책
- 자동 페일오버
- 반동기 복제
- 펜싱 및 스플릿브레인 방지
- 페일오버 윈도우 쓰기 거부
- 멱등 재시도
