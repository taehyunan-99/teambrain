#!/usr/bin/env python3
# 더미 슬랙 스레드 생성기 → raw/slack/
# 콘텐츠 원칙: 그 시점(in-the-moment) 그대로, 사후 주석 금지. 관계 발견은 wiki 빌드의 몫.
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "slack")
FILES = {}

FILES["2026-03-05-pg-interface-naming.md"] = """---
created: 2026-03-05
tags: [slack, raw-dump, payment]
channel: pay-dev
---

# slack #pay-dev 2026-03-05

**10:12 이준호**: 어제 킥오프에서 얘기한 PG 인터페이스 초안 잡는 중인데, 이름 PaymentGateway vs PgClient 뭐가 나아요?
**10:14 김도현**: PaymentGateway. PgClient는 postgres랑 헷갈림 ㅋㅋ
**10:15 박서연**: ㅋㅋㅋ 그건 좀
**10:17 이준호**: 메서드는 approve / cancel / getStatus 세 개로 시작할게요
**10:20 김도현**: ㅇㅋ 토스 어댑터부터. 나이스는 다음주
**10:21 이준호**: 넵 PR 올리면 리뷰 부탁드려요
"""

FILES["2026-03-09-idempotency-research.md"] = """---
created: 2026-03-09
tags: [slack, raw-dump, idempotency]
channel: pay-dev
---

# slack #pay-dev 2026-03-09

**14:02 박서연**: 멱등성 키 조사 중간공유. Stripe 방식이 제일 깔끔한 듯 — 클라가 Idempotency-Key 헤더로 UUID 보내고 서버가 응답 캐시
**14:05 박서연**: 서버 생성 방식은 클라 재시도랑 정당한 재결제를 구분 못 하는 문제가 있음
**14:08 이준호**: 클라 생성 +1. 우리 SDK 쓰는 가맹점이면 키 생성을 SDK가 해주면 되니까
**14:11 김도현**: 좋네요. 수요일 회의에서 확정합시다. 저장은 어디에 할 생각?
**14:13 박서연**: redis 생각 중이에요. TTL 두고
**14:14 김도현**: ㅇㅋ 그것도 수요일에
"""

FILES["2026-03-12-sdk-key-enforcement.md"] = """---
created: 2026-03-12
tags: [slack, raw-dump, idempotency, sdk]
channel: pay-dev
---

# slack #pay-dev 2026-03-12

**11:30 이준호**: 어제 결정 후속 — SDK에서 키 생성 강제하는 거, 키 없이 직접 API 치는 가맹점은 어떡하죠?
**11:33 박서연**: 결정문엔 키 없으면 400 거부로 적었어요
**11:35 이준호**: 기존 가맹점 중에 SDK 안 쓰고 직접 호출하는 데가 두 곳 있는데
**11:38 최민지**: 그 두 곳은 제가 공지 보낼게요. 마이그레이션 기한 2주 드리는 걸로
**11:40 김도현**: ㅇㅋ 2주 유예 후 400. 민지님 공지 부탁
"""

FILES["2026-03-13-redis-ttl-question.md"] = """---
created: 2026-03-13
tags: [slack, raw-dump, idempotency, redis]
channel: pay-dev
---

# slack #pay-dev 2026-03-13

**16:20 이준호**: 멱등키 TTL 24h인데, 24시간 지나고 같은 키로 재시도 오면 어떻게 되는 거예요?
**16:24 박서연**: 키가 만료됐으니 신규 결제로 처리되죠
**16:25 이준호**: 그럼 그건 중복 결제 아닌가요?
**16:28 박서연**: 이론상 맞는데, 24시간 뒤에 같은 키로 재시도하는 클라이언트가 현실적으로 있을까 싶긴 해요
**16:31 김도현**: 확률 낮으니 일단 24h로 가고 운영하면서 보죠
**16:32 이준호**: 음 넵 일단 ㅇㅋ
"""

FILES["2026-03-17-webhook-merchant-500.md"] = """---
created: 2026-03-17
tags: [slack, raw-dump, webhook]
channel: pay-dev
---

# slack #pay-dev 2026-03-17

**13:45 이준호**: 가맹점 A 서버가 웹훅 받을 때마다 500 뱉는데 우린 지금 한 번 보내고 끝이라 결제 결과를 영영 못 받아요
**13:48 최민지**: A쪽 CS 문의도 그거예요. "결제됐는데 주문이 안 만들어졌다"
**13:52 김도현**: 재시도 정책이 없는 게 문제네. 내일 회의 안건으로 올릴게요
**13:54 박서연**: 재시도하면 가맹점이 같은 웹훅 두 번 받을 수도 있는데 그것도 같이 정해야 해요
**13:55 김도현**: ㅇㅋ 둘 다 내일
"""

FILES["2026-03-20-deploy-rollback-scare.md"] = """---
created: 2026-03-20
tags: [slack, raw-dump, deploy]
channel: pay-dev
---

# slack #pay-dev 2026-03-20

**17:02 이준호**: 토스 어댑터 v0.2 배포합니다
**17:15 이준호**: 어 5xx 좀 튀는데
**17:17 박서연**: 헬스체크 경로 바뀐 거 반영 안 된 듯?
**17:19 이준호**: 아 맞네요;; 롤백할게요
**17:25 이준호**: 롤백 완료, 정상. 내일 다시 갑니다
**17:26 김도현**: ㅋㅋ 수고. 배포 체크리스트에 헬스체크 항목 추가해두세요
"""

FILES["2026-03-24-settlement-dplus1-pm.md"] = """---
created: 2026-03-24
tags: [slack, raw-dump, settlement]
channel: pay-dev
---

# slack #pay-dev 2026-03-24

**10:40 김도현**: 내일 정산 회의 전에 — 민지님, 가맹점 입장에서 D+1 정산이면 충분한가요? 실시간 정산 요구는 없어요?
**10:44 최민지**: 영업쪽 확인했는데 경쟁사도 다 D+1이라 문제 없대요. 오히려 정산 명세서 정확한 게 더 중요하다고
**10:46 김도현**: ㅇㅋ 그럼 내일은 배치 구조만 정하면 되겠네
**10:48 박서연**: 환불이 정산 전에 들어오면 어떻게 되는지도 내일 정해요
**10:49 김도현**: ㅇㅋ
"""

FILES["2026-03-27-settlement-key-naming.md"] = """---
created: 2026-03-27
tags: [slack, raw-dump, settlement, idempotency]
channel: pay-dev
---

# slack #pay-dev 2026-03-27

**15:10 이준호**: 정산 멱등키 컬럼 이름 뭐로 하죠. settlement_key? merchant_date_key?
**15:12 박서연**: 그냥 (merchant_id, settlement_date) 복합 유니크로 하고 별도 키 컬럼 안 만들어도 되지 않나
**15:15 이준호**: 오 그게 낫네요. 재실행 판정도 그 두 컬럼으로 하면 되고
**15:17 김도현**: ㅇㅋ 복합 유니크로 갑시다. 결정문서까진 필요 없고 이 스레드 참조
**15:18 이준호**: 넵
"""

FILES["2026-03-31-team-dinner.md"] = """---
created: 2026-03-31
tags: [slack, raw-dump, chat]
channel: pay-random
---

# slack #pay-random 2026-03-31

**12:20 최민지**: 3월 마무리 회식 어때요. 목요일?
**12:22 이준호**: 좋아요 🙌
**12:23 박서연**: 목요일 ㅇㅋ. 고기?
**12:25 김도현**: 고기 ㅇㅋ. 법인카드 제가 들고감
**12:26 이준호**: 👍👍
"""

FILES["2026-04-02-for-update-deadlock.md"] = """---
created: 2026-04-02
tags: [slack, raw-dump, database]
channel: pay-dev
---

# slack #pay-dev 2026-04-02

**14:30 이준호**: 결제 상태 갱신할 때 SELECT FOR UPDATE 두 군데서 잡으니까 로컬에서 데드락 나는데요
**14:34 박서연**: 락 잡는 순서가 달라서 그래요. payment → ledger 순서로 통일하면 돼요
**14:36 이준호**: 아 순서 문제구나. 근데 이런 거 mongo였으면 신경도 안 썼을 텐데 ㅋㅋ
**14:38 박서연**: 대신 mongo면 트랜잭션 자체가 고통이에요. 다음주에 DB 정식으로 정하죠
**14:40 김도현**: ㅇㅇ 다음주 회의 안건
"""

FILES["2026-04-07-mongo-vs-postgres.md"] = """---
created: 2026-04-07
tags: [slack, raw-dump, database]
channel: pay-dev
---

# slack #pay-dev 2026-04-07

**11:05 최민지**: 내일 DB 회의 전에 궁금한 건데, 요즘 다 mongo 쓰지 않나요? 스키마 바꾸기도 편하고
**11:09 박서연**: 결제는 돈이라서요. 트랜잭션이랑 유니크 제약이 생명인데 mongo는 그게 약해요
**11:12 이준호**: 스키마 유연성은 결제 도메인에선 오히려 단점이에요. 금액 필드에 문자열 들어가면 큰일
**11:14 최민지**: 아하 ㅋㅋ 그럼 내일은 postgres vs mysql 싸움이겠네요
**11:15 김도현**: 거의 그럴 듯. 내일 봅시다
"""

FILES["2026-04-10-numeric-vs-bigint.md"] = """---
created: 2026-04-10
tags: [slack, raw-dump, database, payment]
channel: pay-dev
---

# slack #pay-dev 2026-04-10

**16:42 이준호**: 그제 회의에서 금액 NUMERIC으로 정했는데, 어차피 KRW만 쓸 거면 BIGINT 원 단위가 더 빠르고 단순하지 않아요?
**16:47 김도현**: 수수료 계산에서 소수점 중간값이 나와요. 3.3% 떼면 원 단위로 안 떨어짐
**16:49 이준호**: 그건 계산만 NUMERIC으로 하고 저장은 BIGINT로 해도...
**16:52 김도현**: 저장이랑 계산 타입이 다르면 변환 버그 납니다. NUMERIC 유지하되 KRW는 scale 0으로 시작하죠
**16:54 이준호**: 넵 ㅇㅋ
"""

FILES["2026-04-14-promo-traffic-forecast.md"] = """---
created: 2026-04-14
tags: [slack, raw-dump, operations]
channel: pay-dev
---

# slack #pay-dev 2026-04-14

**10:15 최민지**: 공유 — 21일에 대형 가맹점 프로모션 시작해요. 마케팅 쪽 예상으로 결제 트래픽 평소 3배
**10:18 이준호**: API 서버는 오토스케일 있으니까 괜찮을 것 같은데요
**10:20 김도현**: PG 쪽 호출량 제한 걸리는지만 체크해주세요. 토스 rate limit 있었던 걸로 기억
**10:23 이준호**: 토스 확인해볼게요
**10:25 최민지**: 넵 21일 당일 모니터링만 신경써주세요~
"""

FILES["2026-04-21-inc204-realtime.md"] = """---
created: 2026-04-21
tags: [slack, raw-dump, incident, idempotency]
channel: pay-incident
---

# slack #pay-incident 2026-04-21

**21:31 alert-bot**: [ALERT] payment-api p99 latency 4.2s (threshold 2s)
**21:33 박서연**: 어 redis latency가 튀는데요. 프로모션 트래픽 때문인 듯
**21:34 이준호**: 지금 TPS 평소 3배 맞아요. 근데 결제 자체는 들어가고 있어요
**21:36 박서연**: 잠깐, 멱등키 조회가 타임아웃 나는데 결제가 들어간다고요? 막혀야 하는 거 아닌가
**21:39 박서연**: 코드 봤어요. redis 타임아웃이면 "키 없음 = 신규"로 보고 그냥 통과시켜요. fail-open이에요
**21:41 김도현**: 아... 그거 그렇게 하기로 한 거 저예요. 일단 중복 들어가고 있는지 확인
**21:43 이준호**: 같은 키로 승인 두 번 난 건 확인됨. 건수 세는 중
**21:45 최민지**: 중복 결제 CS 들어오기 시작했어요 ㅠㅠ
**21:50 김도현**: 핫픽스 갑시다 — redis 타임아웃이면 결제 거부하고 클라 재시도 유도. 준호님 배포 준비
**22:08 이준호**: 핫픽스 배포 완료. 신규 중복 멈췄어요
**22:15 김도현**: 중복 건수랑 회수는 내일 아침에. 포스트모템 수요일에 잡을게요. 고생했습니다
"""

FILES["2026-04-22-inc204-refund-ops.md"] = """---
created: 2026-04-22
tags: [slack, raw-dump, incident, cs]
channel: pay-incident
---

# slack #pay-incident 2026-04-22

**09:10 이준호**: 어제 중복 청구 최종 87건이요. 명단 뽑았습니다
**09:15 최민지**: 제가 CS팀이랑 일괄 환불 + 사과 안내 진행할게요. 오늘 중 완료 목표
**09:18 김도현**: 부탁드려요. 환불은 전액 + 쿠폰 보상까지
**14:40 최민지**: 87건 전건 환불 완료. 항의 가맹점 두 곳은 제가 직접 통화했어요
**14:42 김도현**: 감사합니다 🙏 내일 포스트모템에서 재발방지 정리합니다
"""

FILES["2026-04-23-failopen-debate.md"] = """---
created: 2026-04-23
tags: [slack, raw-dump, incident, idempotency]
channel: pay-dev
---

# slack #pay-dev 2026-04-23

**11:20 이준호**: 포스트모템 전에 생각 정리 — fail-open 자체가 무조건 틀린 건 아니지 않아요? 조회수 카운터 같은 거면 fail-open이 맞고
**11:24 박서연**: ㅇㅇ 도메인 따라 달라요. 근데 결제는 "잘못 통과"의 비용이 "잘못 거부"보다 압도적으로 커서 fail-closed가 맞다고 봐요
**11:27 이준호**: 잘못 거부면 고객이 재시도하면 되는데 잘못 통과면 돈이 두 번 나가니까... ㅇㅈ
**11:30 김도현**: 그게 오늘 포스트모템 결론이 될 것 같네요. "결제 경로 외부 의존은 fail-closed 기본"
**11:32 박서연**: 그리고 redis 단독 의존도 풀어야 해요. DB 유니크로 백업 치는 안 가져갈게요
"""

FILES["2026-04-28-idem-table-ddl.md"] = """---
created: 2026-04-28
tags: [slack, raw-dump, idempotency, database]
channel: pay-dev
---

# slack #pay-dev 2026-04-28

**15:00 박서연**: 내일 결정 회의 전에 payment_idempotency 테이블 DDL 초안 공유해요
```
CREATE TABLE payment_idempotency (
  idempotency_key UUID PRIMARY KEY,
  request_hash    TEXT NOT NULL,
  response_snapshot JSONB,
  created_at      TIMESTAMPTZ DEFAULT now()
);
```
**15:05 이준호**: PK가 곧 유니크 제약이니 깔끔하네요. request_hash는 왜 있어요?
**15:08 박서연**: 같은 키인데 바디가 다른 요청 잡아내려고요. 그건 클라 버그라 409로 거부
**15:10 김도현**: 좋네요. 내일 이 안으로 확정합시다
"""

FILES["2026-05-02-webhook-secret-storage.md"] = """---
created: 2026-05-02
tags: [slack, raw-dump, webhook, security]
channel: pay-dev
---

# slack #pay-dev 2026-05-02

**13:30 이준호**: 웹훅 서명 구현하려는데 가맹점별 webhook_secret을 어디 보관하죠? vault 같은 거 도입해요?
**13:34 박서연**: vault 운영 부담이 커요. DB 암호화 컬럼으로 시작하는 게 낫지 않나
**13:37 김도현**: ㅇㅇ DB 암호화 컬럼(pgcrypto)으로 가고, KMS 연동은 다음 분기에 검토. 지금 vault까지 가면 과해요
**13:39 이준호**: 넵 pgcrypto로 구현할게요
**13:40 김도현**: 시크릿 회전 API도 같이 — 대시보드에서 가맹점이 직접 돌릴 수 있게
"""

FILES["2026-05-07-hmac-encoding-issue.md"] = """---
created: 2026-05-07
tags: [slack, raw-dump, webhook]
channel: pay-dev
---

# slack #pay-dev 2026-05-07

**16:10 이준호**: HMAC 서명이 가끔 검증 실패하는데 원인 찾았어요. 우리가 json 재직렬화한 바디로 서명하는데 키 순서가 달라질 수 있어요
**16:13 박서연**: 아 서명은 raw_body 바이트 그대로 해야죠. 재직렬화 금지
**16:15 이준호**: ㅇㅇ 전송 직전의 바이트로 서명하게 고쳤어요. 가맹점 가이드에도 "받은 바디 그대로 검증" 명시할게요
**16:17 김도현**: 그 가이드 중요해요. 가맹점이 파싱 후 재직렬화해서 검증 실패하는 게 단골 문의가 될 거라
"""

FILES["2026-05-08-merchant-signature-docs.md"] = """---
created: 2026-05-08
tags: [slack, raw-dump, webhook, cs]
channel: pay-dev
---

# slack #pay-dev 2026-05-08

**10:20 최민지**: 가맹점 B가 서명 검증 샘플 코드 달라는데 언어별로 있어요?
**10:23 이준호**: node랑 python은 있어요. java는 아직
**10:25 최민지**: B가 java예요 ㅋㅋ
**10:27 이준호**: ㅋㅋ 오늘 만들어서 드릴게요
**10:28 최민지**: 감사합니다 🙏 7월 필수화 전에 언어별 샘플 다 갖춰두면 좋겠어요
"""

FILES["2026-05-12-inc231-realtime.md"] = """---
created: 2026-05-12
tags: [slack, raw-dump, incident, settlement]
channel: pay-incident
---

# slack #pay-incident 2026-05-12

**04:31 alert-bot**: [ALERT] settlement-batch running over 30m (started 04:00)
**04:38 김도현**: 배치 로그가 04:20부터 안 올라오는데, 멈춘 것 같네요
**04:41 김도현**: 재실행 돌릴게요. 아침 전에 정산 끝내야 해서
**04:43 김도현**: 재실행 시작
**04:52 이준호**: 어?? 저 지금 봤는데 1차 배치 아직 살아있었어요. 송금 API가 느려서 오래 걸린 거지 죽은 게 아니에요
**04:55 김도현**: ??? payout 로그 두 번 찍힌 가맹점 보이는데
**04:58 이준호**: 1차도 송금하고 2차도 송금한 거예요. 같은 정산일로
**05:03 박서연**: 명세서 생성엔 멱등키(merchant+date) 걸려있는데 송금 호출엔 가드가 없네요...
**05:08 김도현**: 송금 즉시 중단해주세요. 이중 송금 가맹점 추리고, 아침에 회수 진행. 제가 사고쳤네요
**05:15 이준호**: 중단 완료. 이중 송금 3곳, 합계 1,840만원
**05:20 김도현**: 9시에 회수 시작하고 포스트모템 잡겠습니다
"""

FILES["2026-05-13-inc231-recovery.md"] = """---
created: 2026-05-13
tags: [slack, raw-dump, incident, settlement]
channel: pay-incident
---

# slack #pay-incident 2026-05-13

**09:05 최민지**: 이중 송금 3곳 모두 통화 완료. 다들 협조적이세요. 당일 반환 약속받았어요
**11:30 최민지**: 2곳 반환 입금 확인
**16:45 최민지**: 마지막 1곳도 입금 확인. 1,840만원 전액 회수 완료
**16:50 김도현**: 민지님 최고십니다 🙏 포스트모템은 오늘 오후에 했고 회고문서 올라갑니다
**16:52 이준호**: payout_log 유니크 가드 PR 오늘 올릴게요
"""

FILES["2026-05-14-batch-lock-discussion.md"] = """---
created: 2026-05-14
tags: [slack, raw-dump, settlement, batch]
channel: pay-dev
---

# slack #pay-dev 2026-05-14

**14:00 이준호**: 배치 동시 실행 막는 락, redis로 해요 아니면 pg advisory lock?
**14:04 이준호**: 저는 advisory lock 쪽인데 — 어차피 배치가 DB 쓰니까 의존성 추가가 없고, 커넥션 끊기면 락도 자동 해제돼요
**14:08 박서연**: 반론 — INC-204에서 봤듯이 redis가 죽으면? 근데 advisory lock도 커넥션 풀 거치면 세션 경계가 애매해질 수 있어요
**14:12 김도현**: 둘 다 일리 있는데, 락 획득 실패 = 실행 안 함(fail-closed)이라 redis 죽어도 "배치가 안 도는" 쪽으로 망해요. 그건 안전한 실패라 redis lock으로 갑시다. 이미 쓰는 거기도 하고
**14:15 이준호**: 음 ㅇㅋ. lock TTL은 배치 최대 시간 고려해서 2시간으로
**14:16 김도현**: ㅇㅋ
"""

FILES["2026-05-16-keyboard-chat.md"] = """---
created: 2026-05-16
tags: [slack, raw-dump, chat]
channel: pay-random
---

# slack #pay-random 2026-05-16

**12:40 이준호**: 새 키보드 샀어요 ㅋㅋ 저소음 적축
**12:42 박서연**: 어차피 한 달 뒤에 또 사실 거잖아요
**12:43 이준호**: ㅋㅋㅋㅋ 아닌데요
**12:45 김도현**: 지난달에도 그 말 했음
**12:46 이준호**: 🤐
"""

FILES["2026-05-19-pg-timeout-first-report.md"] = """---
created: 2026-05-19
tags: [slack, raw-dump, payment, gateway]
channel: pay-dev
---

# slack #pay-dev 2026-05-19

**15:30 최민지**: 가맹점 두 곳에서 "결제가 한참 빙글빙글 돈다"는 문의가 왔어요. 어제부터요
**15:33 박서연**: 토스 승인 타임아웃이 하루 10~20건 잡히네요. PENDING에 묶여있어요
**15:36 김도현**: 토스 쪽 장애예요?
**15:38 박서연**: 토스 status 페이지는 정상이에요. 우리 쪽 같은데 내일 제대로 파볼게요
**15:40 김도현**: ㅇㅋ 우선순위 높게 부탁해요
"""

FILES["2026-05-21-bulkhead-deploy-result.md"] = """---
created: 2026-05-21
tags: [slack, raw-dump, payment, gateway]
channel: pay-dev
---

# slack #pay-dev 2026-05-21

**11:00 박서연**: 어제 정리한 워커풀 분리(결제승인/웹훅 bulkhead) 배포했어요. 오늘 새벽부터 PG 타임아웃 0건
**11:03 김도현**: 깔끔하네요 👏
**11:05 박서연**: 웹훅 재전송이 몰릴 때 결제 승인이 굶는 구조였던 거라, 풀 분리 + 결제 우선순위로 해결. 트러블슈팅 문서 올렸어요
**11:07 이준호**: PG 타임아웃 10s 단축 + 재시도 1회도 같이 나간 거죠?
**11:08 박서연**: ㅇㅇ 멱등키 있으니 재시도 안전해요
"""

FILES["2026-05-23-oncall-rotation.md"] = """---
created: 2026-05-23
tags: [slack, raw-dump, operations]
channel: pay-dev
---

# slack #pay-dev 2026-05-23

**10:10 김도현**: 새벽 장애 두 번 겪고 나니 온콜 체계가 필요하네요. 주 단위 로테이션 어때요? 서연-준호-민지 3인 로테이션, 저는 상시 백업
**10:13 박서연**: 민지님도 들어가요? 기술 대응이 필요할 텐데
**10:15 최민지**: 1차 탐지/에스컬레이션은 제가 할 수 있어요. 기술 대응은 백업 콜
**10:17 김도현**: ㅇㅇ 1차는 탐지+판단, 기술 대응은 백업 호출. 04시 배치 알람은 온콜 폰으로 가게 설정해주세요
**10:19 이준호**: 넵 알람 라우팅 제가 잡을게요. 다음주 월요일부터 시작하죠
**10:20 김도현**: ㅇㅋ 확정
"""

FILES["2026-05-26-newhire-news.md"] = """---
created: 2026-05-26
tags: [slack, raw-dump, team]
channel: pay-random
---

# slack #pay-random 2026-05-26

**14:00 김도현**: 좋은 소식 — 백엔드 신입 채용 확정됐어요. 7월 초 입사 예정
**14:02 박서연**: 오 드디어 🎉
**14:03 이준호**: 🎉🎉
**14:05 최민지**: 온보딩 자료 준비해야겠네요. 우리 결정 히스토리가 문서 곳곳에 흩어져 있어서
**14:07 김도현**: 제가 온보딩 가이드 초안 내일 써볼게요. 멱등성 히스토리는 꼭 넣어야 함 ㅋㅋ
"""

FILES["2026-05-28-batch-alert-tuning.md"] = """---
created: 2026-05-28
tags: [slack, raw-dump, settlement, monitoring]
channel: pay-dev
---

# slack #pay-dev 2026-05-28

**13:20 이준호**: 배치 알람 기준 손봤어요. "30분 초과 = 알람"이 INC-231 오판의 시작이었어서
**13:23 이준호**: 이제 단계가 나뉘어요 — 60분 초과: 경고만 / 송금 API 응답 없음 10분: 긴급 / 락 있는데 프로세스 없음: 긴급(진짜 죽은 케이스)
**13:26 김도현**: "오래 걸리는 것"과 "죽은 것"을 알람이 구분해주는 거네요. 좋아요
**13:28 박서연**: 거기에 +1 — 알람 메시지에 "재실행 전 락 상태 확인" 문구 박아두면 새벽에 졸린 사람이 실수 안 해요
**13:30 이준호**: ㅋㅋ 넣었습니다 "재실행 금지. 락 확인 먼저"
"""

FILES["2026-06-02-refund-flow-open.md"] = """---
created: 2026-06-02
tags: [slack, raw-dump, payment, refund]
channel: pay-dev
---

# slack #pay-dev 2026-06-02

**11:15 최민지**: 부분 환불 요구하는 가맹점이 늘었어요. 지금은 전액 환불만 되죠?
**11:18 박서연**: 네 전액만. 부분 환불은 정산이랑 얽혀서 설계가 좀 필요해요 — 이미 정산된 거래의 부분 환불이면 차감을 다음 정산에서 해야 하고
**11:21 이준호**: 환불 멱등성도 따로 필요해요. 같은 환불 요청 두 번 오면?
**11:24 김도현**: 규모 있는 작업이네요. 이번 분기는 어렵고 다음 분기 초 설계 시작합시다. 민지님 가맹점에는 그렇게 안내 부탁
**11:26 최민지**: 넵 ㅠ 다음 분기로 안내할게요
"""

FILES["2026-06-04-pg-minor-upgrade.md"] = """---
created: 2026-06-04
tags: [slack, raw-dump, database, operations]
channel: pay-dev
---

# slack #pay-dev 2026-06-04

**09:30 박서연**: 공지 — postgres 마이너 버전 패치(보안픽스) 이번주 토요일 02시에 적용해요. 페일오버 1회 발생, 예상 다운 10초 미만
**09:32 김도현**: 결제 쪽 영향은요?
**09:34 박서연**: 페일오버 순간 in-flight 쿼리 재시도로 흡수돼요. 혹시 모르니 02시 전후 모니터링은 제가
**09:35 김도현**: ㅇㅋ 토요일 온콜이 누구죠
**09:36 이준호**: 접니다. 같이 볼게요
"""

FILES["2026-06-05-junho-handover.md"] = """---
created: 2026-06-05
tags: [slack, raw-dump, team]
channel: pay-dev
---

# slack #pay-dev 2026-06-05

**17:00 이준호**: 다음주 월~수 휴가입니다. 인수인계 메모:
- 웹훅 시크릿 회전 API → 코드리뷰 대기 상태, 서연님이 머지 판단
- 정산 CSV 내보내기 → 가맹점 C 요구사항 확인 중, 민지님이 스펙 받으면 제 복귀 후 시작
- 온콜은 이번주 일요일까지 저, 월요일부터 서연님
**17:05 박서연**: ㅇㅋ 잘 다녀와요
**17:06 최민지**: C 스펙은 제가 받아둘게요~
"""

FILES["2026-06-09-settlement-csv-request.md"] = """---
created: 2026-06-09
tags: [slack, raw-dump, settlement, cs]
channel: pay-dev
---

# slack #pay-dev 2026-06-09

**14:20 최민지**: 가맹점 C 정산명세서 요구사항 받았어요. 지금 PDF만 주는데 회계 시스템에 넣게 CSV도 달라고. 컬럼은 거래ID/승인일시/금액/수수료/정산액
**14:24 박서연**: 명세서 생성 로직에 export 포맷 하나 추가하는 거라 크지 않아요. 준호님 복귀하면 시작하는 걸로
**14:26 김도현**: ㅇㅋ. 다른 가맹점도 쓸 수 있게 대시보드 공통 기능으로 만들죠. C 전용 아니라
**14:28 최민지**: 좋아요. C에는 이번달 내 제공으로 안내할게요
"""

FILES["2026-06-10-idem-ttl-48h-proposal.md"] = """---
created: 2026-06-10
tags: [slack, raw-dump, idempotency]
channel: pay-dev
---

# slack #pay-dev 2026-06-10

**15:40 박서연**: 데이터 공유 — 지난 한 달간 멱등키 TTL(24h) 만료 *이후* 같은 키로 재시도 온 게 7건 있었어요. 3월에 준호님이 걱정했던 그 케이스가 실제로 있긴 하네요
**15:43 박서연**: 7건 모두 가맹점 배치 재처리가 다음날 도는 패턴이었어요. TTL 48h로 늘리는 거 제안합니다
**15:46 김도현**: DB 유니크가 있으니 지금도 중복 결제까진 안 가죠?
**15:48 박서연**: 네 DB가 막아서 사고는 아니에요. 다만 캐시 미스라 응답 재생이 안 되고 409로 떨어져서 가맹점이 혼란스러워해요
**15:51 김도현**: 음 redis 메모리 영향 보고 정합시다. 서연님 메모리 증가량 추산해서 다음 주간회의에 올려주세요
**15:52 박서연**: 넵
"""

FILES["2026-06-11-onboarding-checklist.md"] = """---
created: 2026-06-11
tags: [slack, raw-dump, team, onboarding]
channel: pay-dev
---

# slack #pay-dev 2026-06-11

**10:00 최민지**: 신입 온보딩 준비 체크리스트 만들어봤어요
- 계정/권한 발급 (입사 전주)
- 온보딩 가이드 문서 읽기 (도현님 5월 작성본)
- 멱등성 히스토리 세션 — 도현님이 직접 설명 (3/11 결정 → INC-204 → 4/29 수정)
- 정산 배치 + INC-231 리뷰
- 첫 과제: 정산 CSV 내보내기 코드리뷰 참관?
**10:05 김도현**: 좋네요. 멱등성 세션은 제가 합니다. 사고 친 사람이 설명해야 진정성이 있죠 ㅋㅋ
**10:07 박서연**: ㅋㅋㅋ 첫 과제는 CSV 참관 좋아요. 규모도 적당하고
**10:08 최민지**: 확정. 위키 정리되면 문서 링크도 채울게요
"""

def main():
    os.makedirs(BASE, exist_ok=True)
    for name, content in FILES.items():
        with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
            f.write(content.lstrip("\n"))
    print(f"slack {len(FILES)}개 생성 완료 → raw/slack/")

if __name__ == "__main__":
    main()
