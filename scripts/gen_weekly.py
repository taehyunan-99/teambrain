#!/usr/bin/env python3
# 더미 주간회의 단신 생성기 → raw/ (정형이지만 짧고 단편적)
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw")
FILES = {}

FILES["2026-03-06-weekly.md"] = """---
created: 2026-03-06
tags: [meeting, weekly]
---

# 주간회의 2026-03-06

- 킥오프 결정 공유: 비동기 승인 / PG 어댑터 추상화 (3/4 회의록 참조)
- [준호] PaymentGateway 인터페이스 PR 머지 예정 (PR-101 리뷰 중)
- [서연] 멱등성 조사 진행 중 → 3/11 결정 회의
- [민지] 가맹점 A, B 연동 일정 협의 시작
- 블로커: 없음
"""

FILES["2026-03-13-weekly.md"] = """---
created: 2026-03-13
tags: [meeting, weekly]
---

# 주간회의 2026-03-13

- 멱등성 결정 완료(3/11): 클라 생성 키 + redis. 미들웨어 PR-112 리뷰 중
- [준호] 토스 어댑터 개발 중, 금요일 PR
- [민지] SDK 미사용 가맹점 2곳에 키 의무화 공지 발송 (2주 유예)
- 논의: 키 TTL 24h 이후 재시도 케이스 — 확률 낮아 보류 (슬랙 스레드 참조)
- 블로커: 없음
"""

FILES["2026-03-20-weekly.md"] = """---
created: 2026-03-20
tags: [meeting, weekly]
---

# 주간회의 2026-03-20

- 웹훅 재시도 정책 결정 완료(3/18): 지수 백오프 6회 + dead letter
- [준호] 토스 어댑터 배포(롤백 1회 후 재배포 완료), 나이스 어댑터 머지(PR-115)
- [서연] 웹훅 전송기 구현 중 (PR-118, jitter 반영)
- [민지] 가맹점 A에 재시도 정책 안내 — 만족
- 다음주: 정산 아키텍처 회의(3/25)
"""

FILES["2026-03-27-weekly.md"] = """---
created: 2026-03-27
tags: [meeting, weekly]
---

# 주간회의 2026-03-27

- 정산 결정 완료(3/25): D+1 일배치 04:00, 멱등키 = 가맹점+정산일(복합 유니크, 슬랙 결정)
- [준호] 정산 집계 쿼리 작성 중 (PR-125)
- [서연] dead letter 테이블 머지(PR-121)
- 수수료 절사/반올림 정책 확인 필요 → 민지님 약관 확인 (PR-127 블로킹)
"""

FILES["2026-04-03-weekly.md"] = """---
created: 2026-04-03
tags: [meeting, weekly]
---

# 주간회의 2026-04-03

- 수수료 절사 확정(약관 5조 2항), PR-127 머지
- [서연] 폴링 워커 머지(PR-133). PENDING 정체 자동 해소 동작
- [준호] FOR UPDATE 데드락 이슈 해결(락 순서 통일)
- 다음주: DB 선택 회의(4/8) — postgres vs mysql vs mongo
- [민지] 가맹점 B 연동 완료, 첫 결제 발생 🎉
"""

FILES["2026-04-10-weekly.md"] = """---
created: 2026-04-10
tags: [meeting, weekly]
---

# 주간회의 2026-04-10

- DB 결정 완료(4/8): PostgreSQL + NUMERIC. 마이그레이션 머지(PR-136)
- NUMERIC scale 4 채택 (수수료 중간계산 + 확장 여유, 슬랙 후속 논의 참조)
- [준호] 토스 rate limit 확인 중 (4/21 프로모션 대비)
- [민지] 4/21 프로모션 트래픽 3배 예상 — 당일 모니터링 당번 정하기
"""

FILES["2026-04-17-weekly.md"] = """---
created: 2026-04-17
tags: [meeting, weekly]
---

# 주간회의 2026-04-17

- [준호] 토스 rate limit 확인 완료 — 승인 분당 1,000건, 프로모션 피크 예상 분당 600건으로 여유
- [서연] 웹훅 대시보드(전송 성공률/dead letter 현황) 베타 오픈
- [민지] 프로모션 D-4 — 가맹점 측 준비 완료
- 4/21 당일 모니터링: 전원 대기 (퇴근 후 슬랙 핫라인)
"""

FILES["2026-04-24-weekly.md"] = """---
created: 2026-04-24
tags: [meeting, weekly, incident]
---

# 주간회의 2026-04-24

- **INC-204 중복결제(4/21)**: 87건 전액 환불 완료. 포스트모템 완료(4/23)
- 핫픽스 배포됨: 멱등성 조회 타임아웃 시 fail-closed (PR-140)
- 결정 예정: 멱등성 저장소 DB 이중화 → 4/29 회의
- [서연] payment_idempotency DDL 초안 작성 중
- 프로모션 자체 실적: 결제 성공률 99.2% (장애 시간 제외)
"""

FILES["2026-05-01-weekly.md"] = """---
created: 2026-05-01
tags: [meeting, weekly]
---

# 주간회의 2026-05-01

- 멱등성 2.0 결정 완료(4/29): redis 캐시 + DB UNIQUE 2중화, fail-closed 공식화
- [서연] 구현 PR-142 리뷰 중 (ON CONFLICT 방식)
- [준호] SDK 키 강제 PR-145 작성 중
- 다음 결정: 웹훅 서명(HMAC) → 5/6 회의
- [민지] 가맹점 C 신규 연동 착수
"""

FILES["2026-05-08-weekly.md"] = """---
created: 2026-05-08
tags: [meeting, weekly]
---

# 주간회의 2026-05-08

- 웹훅 HMAC 서명 결정 완료(5/6). 구현 PR-148 머지 — raw body 서명, timestamp 5분
- 시크릿 보관: DB 암호화 컬럼(pgcrypto), KMS는 다음 분기 검토 (슬랙 결정)
- [준호] 가맹점용 서명 검증 샘플 코드 node/python/java 제공
- [민지] 7/1 서명 필수화 가맹점 공지 초안 작성
"""

FILES["2026-05-15-weekly.md"] = """---
created: 2026-05-15
tags: [meeting, weekly, incident]
---

# 주간회의 2026-05-15

- **INC-231 정산 이중송금(5/12)**: 3곳 1,840만원 당일 전액 회수. 포스트모템 완료(5/13)
- 재발방지 진행: payout_log 유니크 가드(PR-151 머지), 배치 분산 락(PR-153 리뷰 중, redis lock + heartbeat)
- 배치 알람 단계화 작업 착수 (오래 걸림 vs 죽음 구분)
- [민지] 이중송금 가맹점 3곳 관계 회복 — 사과 방문 완료
"""

FILES["2026-05-22-weekly.md"] = """---
created: 2026-05-22
tags: [meeting, weekly]
---

# 주간회의 2026-05-22

- PG 타임아웃 트러블슈팅 완료(5/20 문서): 워커풀 분리(bulkhead, PR-156) 배포 후 타임아웃 0건
- [준호] 시크릿 회전 API 개발 중 (PR-159) — 유예기간 정책 미결
- 온콜 로테이션 다음주 시작 (슬랙 결정: 3인 주단위 + 도현 백업)
- 신입 채용 확정 — 온보딩 준비 시작, 도현님 가이드 초안 작성 예정
"""

def main():
    for name, content in FILES.items():
        with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
            f.write(content.lstrip("\n"))
    print(f"weekly {len(FILES)}개 생성 완료 → raw/")

if __name__ == "__main__":
    main()
