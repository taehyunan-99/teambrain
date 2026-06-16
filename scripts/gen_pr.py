#!/usr/bin/env python3
# 더미 PR 리뷰 코멘트 생성기 → raw/pr/
# 콘텐츠 원칙: 그 시점 그대로, 사후 주석 금지.
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "pr")
FILES = {}

FILES["pr-101-payment-gateway-interface.md"] = """---
created: 2026-03-08
tags: [pr-review, raw-dump, payment, gateway]
pr: 101
---

# PR #101 — feat: PaymentGateway 인터페이스 정의

> 작성: 이준호 / 리뷰: 김도현, 박서연 / 머지: 2026-03-08

**김도현 (gateway.go:12)**: approve()가 PaymentResult를 동기로 리턴하는 시그니처네요. 우린 비동기 승인이라 워커가 호출할 텐데, 이 메서드 자체는 동기 블로킹이고 비동기성은 워커 레벨에서 처리하는 구조로 이해하면 되나요?
**이준호**: 네 맞아요. 어댑터는 PG 호출을 동기로 감싸고, 비동기는 워커 큐가 담당. 어댑터에 비동기를 넣으면 PG마다 콜백 방식이 달라서 추상화가 깨져요
**김도현**: ㅇㅋ 그 경계 좋네요. 주석으로 박아주세요
**박서연 (gateway.go:25)**: cancel()에 부분취소 amount 파라미터가 없는데 의도적인가요?
**이준호**: MVP는 전액취소만이요. 부분취소는 시그니처 바꾸지 않고 옵션 구조체로 확장 가능하게 해뒀어요
**박서연**: 👍 approve
"""

FILES["pr-108-toss-adapter.md"] = """---
created: 2026-03-14
tags: [pr-review, raw-dump, payment, gateway]
pr: 108
---

# PR #108 — feat: 토스페이먼츠 어댑터

> 작성: 이준호 / 리뷰: 박서연 / 머지: 2026-03-14

**박서연 (toss_adapter.go:88)**: 토스 에러코드 → 우리 에러로 매핑하는 switch가 12개 케이스인데, 매핑 안 된 코드가 오면요?
**이준호**: default에서 ErrUnknownGateway로 떨어져요
**박서연**: 그게 호출부에서 재시도 가능 에러로 분류되나요? 토스의 "잔액부족"같은 비재시도 에러가 unknown으로 빠지면 무한 재시도 위험이 있어요
**이준호**: 아 좋은 지적. unknown은 비재시도로 분류 바꿀게요. 모르는 에러는 보수적으로
**박서연**: ㅇㅋ 그리고 매핑 테이블은 코드 말고 별도 상수 파일로 빼주세요. 나이스 어댑터도 같은 패턴 쓸 거라
**이준호**: 반영했습니다
**박서연**: approve 👍
"""

FILES["pr-112-idempotency-middleware.md"] = """---
created: 2026-03-15
tags: [pr-review, raw-dump, idempotency, redis]
pr: 112
---

# PR #112 — feat: 멱등성 미들웨어 (redis)

> 작성: 박서연 / 리뷰: 김도현, 이준호 / 머지: 2026-03-16

**김도현 (idempotency.go:42)**: redis GET이 타임아웃 나면 어떻게 되나요? 여기 에러 처리가 없는 것 같은데
**박서연**: 지금은 에러면 그냥 통과(신규 취급)예요. 고민인데요 — 막으면 redis 장애 = 결제 전면 장애가 돼서...
**김도현**: 결제가 안 되는 게 더 큰 손실이죠. redis 타임아웃이면 신규로 보고 통과시키는 지금 동작 유지합시다. fail-open으로
**이준호**: 중복 결제 위험은요? 타임아웃 난 사이에 같은 키 두 개 들어오면
**김도현**: redis가 죽을 확률 vs 결제 못 받는 손실의 트레이드오프인데, redis 가용성이 높으니 전자가 훨씬 드물어요. 일단 이걸로 가고 문제 생기면 다시 봅시다
**박서연**: 넵 fail-open 유지 + 타임아웃 메트릭만 추가해둘게요
**김도현**: approve
**이준호**: approve (메트릭 추가 확인)
"""

FILES["pr-115-nice-adapter.md"] = """---
created: 2026-03-19
tags: [pr-review, raw-dump, payment, gateway]
pr: 115
---

# PR #115 — feat: 나이스페이 어댑터

> 작성: 이준호 / 리뷰: 박서연 / 머지: 2026-03-19

**박서연 (nice_adapter.go:30)**: 나이스는 응답이 EUC-KR로 올 때가 있다던데 인코딩 처리 있어요?
**이준호**: 헤더 보고 EUC-KR이면 UTF-8 변환해요. 테스트 케이스도 있어요 (nice_adapter_test.go:120)
**박서연 (nice_adapter.go:55)**: 토스 어댑터랑 에러 매핑 상수 파일 공유하는 구조 좋네요. unknown → 비재시도 규칙도 동일하게 적용됐고
**이준호**: 네 PR-108에서 정한 규칙 그대로요
**박서연**: approve 👍
"""

FILES["pr-118-webhook-sender-backoff.md"] = """---
created: 2026-03-21
tags: [pr-review, raw-dump, webhook]
pr: 118
---

# PR #118 — feat: 웹훅 전송기 + 지수 백오프

> 작성: 박서연 / 리뷰: 이준호, 김도현 / 머지: 2026-03-22

**이준호 (webhook_sender.go:60)**: 백오프 간격이 1m→5m→30m→2h→6h 고정인데 jitter 안 넣어요? 가맹점 서버 복구 직후 재시도가 한꺼번에 몰리면 다시 죽일 수 있어요
**박서연**: 오 thundering herd. 각 간격에 ±20% jitter 추가할게요
**김도현 (webhook_sender.go:95)**: 타임아웃도 실패로 재시도하는 거 확인. 근데 가맹점이 처리는 했는데 응답만 늦은 경우 중복 전송이 되는데 괜찮나요?
**박서연**: 그래서 페이로드에 event_id가 있어요. 가맹점이 event_id로 중복 거르는 게 계약이고, 가이드 문서에 명시돼 있어요
**김도현**: ㅇㅋ. "at-least-once + 수신측 멱등"이 우리 전달 모델이라는 걸 README에도 적어주세요
**박서연**: 반영 완료
**이준호**: approve / **김도현**: approve
"""

FILES["pr-121-dead-letter-table.md"] = """---
created: 2026-03-23
tags: [pr-review, raw-dump, webhook]
pr: 121
---

# PR #121 — feat: webhook_dead_letter 테이블 + 알림

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-03-23

**이준호 (migration/0007.sql:5)**: dead letter 행을 지우는 정책이 없는데 무한히 쌓이나요?
**박서연**: 90일 보관 후 아카이브 배치로 정리하려고요. 이번 PR엔 없고 백로그에 적어뒀어요
**이준호 (notifier.go:33)**: 이메일 발송 실패하면요? dead letter의 dead letter ㅋㅋ
**박서연**: ㅋㅋ 이메일은 best-effort예요. 실패해도 dead letter 행 자체는 남아있으니 대시보드에서 보여요. "기록은 보장, 알림은 노력"
**이준호**: ㅇㅋ 그 한 줄 주석으로 박아주세요. approve
"""

FILES["pr-125-settlement-aggregation.md"] = """---
created: 2026-03-28
tags: [pr-review, raw-dump, settlement, database]
pr: 125
---

# PR #125 — feat: 정산 집계 쿼리

> 작성: 이준호 / 리뷰: 박서연, 김도현 / 머지: 2026-03-29

**박서연 (settlement_query.sql:1)**: CTE 4단 중첩인데 성능 확인했어요? 거래 100만 건 기준
**이준호**: 스테이징에서 120만 건으로 돌려봤어요. 4.2초. 새벽 배치라 허용 범위라고 봐요
**김도현**: 집계 기준시각 경계 확인하고 싶은데 — approved_at이 정확히 23:59:59.999인 거래는 어느 날 정산이죠?
**이준호**: `approved_at >= D AND approved_at < D+1` 반개구간이라 그날 정산이에요. 경계 중복/누락 없어요
**김도현**: 👍 그 구간 정의가 회의 때 정한 "전일 00:00~23:59:59"의 정확한 구현이네요. approve
**박서연**: approve (성능 수치 코멘트로 남겨주세요)
"""

FILES["pr-127-fee-rounding.md"] = """---
created: 2026-03-30
tags: [pr-review, raw-dump, settlement, payment]
pr: 127
---

# PR #127 — feat: 수수료 계산

> 작성: 이준호 / 리뷰: 박서연, 최민지(정책확인) / 머지: 2026-03-31

**박서연 (fee.go:21)**: 수수료 3.3% 곱하면 소수점 나오는데 절사예요 반올림이에요? 1원 차이가 가맹점 정산 클레임이 될 수 있어요
**이준호**: 코드는 지금 반올림인데... 정책이 정해진 게 없네요
**최민지**: 영업 계약서 확인했어요 — "수수료는 원 단위 미만 절사"가 표준 약관이에요. 가맹점에 유리한 방향
**이준호**: 절사로 수정했습니다. 약관 조항 번호를 주석으로 달아뒀어요 (5조 2항)
**박서연**: 👍 테스트에 경계값(33.0원, 33.4원, 33.9원) 추가 확인. approve
"""

FILES["pr-133-polling-worker.md"] = """---
created: 2026-04-03
tags: [pr-review, raw-dump, payment]
pr: 133
---

# PR #133 — feat: PENDING 상태 폴링 워커

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-04-04

**이준호 (polling_worker.go:40)**: PENDING 10분 넘은 결제를 PG에 재조회하는 거죠? 조회 결과 PG엔 승인인데 우리 DB가 PENDING이면요?
**박서연**: PG 기준으로 동기화해요. PG가 진실의 원천(source of truth). 승인이면 APPROVED로 올리고 웹훅 발송
**이준호 (polling_worker.go:72)**: 폴링 주기 1분인데 PG 조회 API에도 rate limit 있지 않아요?
**박서연**: 토스 조회는 분당 600건이라 여유 있어요. 초과 시 다음 주기로 밀리게 백프레셔 있고
**이준호**: approve 👍
"""

FILES["pr-136-db-migration-numeric.md"] = """---
created: 2026-04-09
tags: [pr-review, raw-dump, database]
pr: 136
---

# PR #136 — feat: 결제 테이블 마이그레이션 (postgres)

> 작성: 박서연 / 리뷰: 이준호, 김도현 / 머지: 2026-04-09

**이준호 (migration/0012.sql:8)**: amount NUMERIC(19,4)인데 scale 4는 왜요? KRW는 소수점 없잖아요
**박서연**: 어제 회의에서 NUMERIC 결정 났고, scale은 수수료 중간 계산(3.3%) 손실 방지 + 나중에 외화 결제 대비로 4 잡았어요
**김도현**: 외화는 아직 계획에 없으니 over-engineering 같기도 한데... 근데 scale 바꾸는 마이그레이션이 더 비싸니 4로 두는 데 동의
**이준호**: ㅇㅋ. 저장은 어차피 원 단위 정수값이고 계산 여유분이라고 이해할게요
**김도현**: approve / **이준호**: approve
"""

FILES["pr-140-hotfix-fail-closed.md"] = """---
created: 2026-04-22
tags: [pr-review, raw-dump, incident, idempotency]
pr: 140
---

# PR #140 — hotfix: 멱등성 조회 타임아웃 시 fail-closed

> 작성: 이준호 / 리뷰: 김도현, 박서연 / 머지: 2026-04-21 22:05 (긴급)

**이준호**: [긴급] INC-204 핫픽스. redis 타임아웃/에러 시 503 반환 + Retry-After 헤더. 통과시키던 기존 동작 제거
**김도현**: diff 확인. 이게 PR-112에서 제가 fail-open으로 가자고 한 그 지점이네요. 제 판단이 틀렸습니다. approve
**박서연 (idempotency.go:48)**: 503에 Retry-After 3s 박혀있는데 클라 SDK가 이 헤더 읽고 자동 재시도하나요?
**이준호**: SDK는 지수 백오프 자체 재시도라 헤더는 힌트용이에요. 직접 호출 가맹점을 위해 넣었어요
**박서연**: ㅇㅋ approve. 상세 리뷰는 내일 후속 PR에서 — 지금은 멈추는 게 우선
"""

FILES["pr-142-payment-idempotency-unique.md"] = """---
created: 2026-04-30
tags: [pr-review, raw-dump, idempotency, database]
pr: 142
---

# PR #142 — feat: payment_idempotency 테이블 + DB 유니크 가드

> 작성: 박서연 / 리뷰: 김도현, 이준호 / 머지: 2026-05-01

**김도현 (idempotency_store.go:55)**: INSERT ... ON CONFLICT DO NOTHING 후에 영향 행 수가 0이면 중복으로 판단하는 거죠? 23505를 직접 잡는 게 아니라
**박서연**: 네 ON CONFLICT DO NOTHING + RETURNING으로 처리해요. 23505 예외 핸들링보다 깔끔하고 postgres 관용구라서
**이준호 (idempotency_store.go:80)**: 중복이면 기존 응답 스냅샷을 돌려주는데, 1차 요청이 "아직 처리 중"이라 스냅샷이 비어있으면요?
**박서연**: 그 경우 409 + "processing"으로 응답해요. 클라는 잠시 후 재시도. 동시 도착한 같은 키의 둘째 요청이 여기 떨어져요
**김도현**: redis는 이제 순수 캐시 역할이고 진실은 DB라는 거 — 주석으로 계층 역할 명시해주세요. 다음 사람이 redis를 다시 진실로 착각하면 안 되니
**박서연**: 추가했어요. "redis = 응답 재생 캐시, DB UNIQUE = 멱등성의 진실"
**김도현**: approve / **이준호**: approve
"""

FILES["pr-145-sdk-key-enforcement.md"] = """---
created: 2026-05-03
tags: [pr-review, raw-dump, idempotency, sdk]
pr: 145
---

# PR #145 — feat: SDK 멱등키 자동 생성 강제

> 작성: 이준호 / 리뷰: 박서연 / 머지: 2026-05-04

**박서연 (sdk/payment.ts:25)**: SDK가 키를 자동 생성하면, 사용자가 명시적으로 키를 넘기는 경우와 충돌 안 해요?
**이준호**: 명시 키가 있으면 그걸 쓰고, 없으면 요청 객체 생성 시점에 UUID 자동 채움. 호출자가 같은 요청 객체로 재시도하면 같은 키가 유지돼요
**박서연**: 아 "요청 객체 = 멱등성 단위"가 되는 거네요. 새 객체 만들면 새 결제고. 그 의미를 SDK 문서에 크게 적어주세요 — 가맹점 개발자가 헷갈릴 1순위
**이준호**: 문서에 예제 두 개(재시도 vs 신규 결제) 추가했어요
**박서연**: approve 👍
"""

FILES["pr-148-hmac-signature.md"] = """---
created: 2026-05-07
tags: [pr-review, raw-dump, webhook, security]
pr: 148
---

# PR #148 — feat: 웹훅 HMAC-SHA256 서명

> 작성: 이준호 / 리뷰: 박서연, 김도현 / 머지: 2026-05-08

**박서연 (signer.go:18)**: 서명 대상이 재직렬화된 json이네요. 키 순서 바뀌면 같은 페이로드도 다른 서명이 나와요. 전송 버퍼의 raw bytes로 서명해야 해요
**이준호**: 맞아요, 어제 슬랙에서 그 버그 잡은 게 이거예요. 전송 직전 바이트로 서명하게 수정했어요
**김도현 (signer.go:40)**: timestamp 허용 오차 5분의 근거가 뭐죠?
**이준호**: 가맹점 서버 시계 오차(NTP 미동기 흔함) + 재시도 지연 고려예요. Stripe도 기본 5분이고요. 너무 짧으면 정상 웹훅이 거부되고 너무 길면 리플레이 윈도우가 커져요
**김도현**: ㅇㅋ 근거 주석으로. 그리고 시크릿 회전 중엔 구/신 시크릿 둘 다 유효해야 하는데 그건 이 PR 범위예요?
**이준호**: 회전은 PR-159(회전 API)에서 듀얼 키 검증으로 다뤄요
**김도현**: approve / **박서연**: approve
"""

FILES["pr-151-payout-unique-guard.md"] = """---
created: 2026-05-14
tags: [pr-review, raw-dump, settlement, idempotency]
pr: 151
---

# PR #151 — fix: 송금 직전 payout_log 유니크 가드 (INC-231)

> 작성: 이준호 / 리뷰: 박서연, 김도현 / 머지: 2026-05-15

**박서연 (payout.go:62)**: 순서가 중요해요 — payout_log INSERT가 송금 API 호출 *전*인가요 *후*인가요?
**이준호**: 전이요. INSERT(status=initiated) 성공 → 송금 호출 → status=completed 갱신. INSERT가 유니크 충돌하면 송금 자체를 안 해요
**박서연**: 그럼 INSERT 성공 후 송금 호출이 실패하면 initiated 행이 남는데, 재실행 시 그 가맹점은 유니크 충돌로 스킵돼서 영영 송금이 안 되지 않아요?
**이준호**: 좋은 지적... initiated 상태로 1시간 넘은 행은 송금 API에 결과 조회 후 수동 확인 큐로 보내는 보정 로직 추가할게요. 자동 재송금은 위험해서 안 하고요
**김도현**: "자동 재송금 안 함" 동의해요. 돈 나가는 건 모호하면 사람이 봐야죠. INC-231 직후라 더더욱
**박서연**: 보정 로직 확인. approve
**김도현**: approve
"""

FILES["pr-153-batch-distributed-lock.md"] = """---
created: 2026-05-15
tags: [pr-review, raw-dump, settlement, batch]
pr: 153
---

# PR #153 — fix: 정산 배치 분산 락 (INC-231)

> 작성: 박서연 / 리뷰: 이준호 / 머지: 2026-05-16

**이준호 (batch_lock.go:20)**: lock TTL 2시간 — 배치가 2시간 넘게 걸리면 락이 풀려서 INC-231이 재현될 수 있는 거 아닌가요?
**박서연**: 배치 진행 중 30분마다 TTL 연장(heartbeat)해요. 프로세스가 진짜 죽으면 연장이 멈춰서 락이 풀리고, 살아있으면 계속 잡고 있고
**이준호 (batch_lock.go:45)**: 락 획득 실패 시 동작은요?
**박서연**: 즉시 종료 + "이미 실행 중" 로그. 실행 안 하는 게 기본값(fail-closed). 슬랙에서 정한 그대로요
**이준호**: heartbeat 좋네요. approve 👍
"""

FILES["pr-156-bulkhead-worker-pools.md"] = """---
created: 2026-05-20
tags: [pr-review, raw-dump, payment, gateway]
pr: 156
---

# PR #156 — fix: 결제승인/웹훅 워커풀 분리 (bulkhead)

> 작성: 박서연 / 리뷰: 이준호, 김도현 / 머지: 2026-05-21

**이준호 (worker_pool.go:30)**: 풀 사이즈 — 결제 32 / 웹훅 16의 산정 근거 있어요?
**박서연**: 피크 TPS(프로모션 3배 기준) × PG 평균 응답 0.8s로 계산하면 결제는 26개 필요, 여유분 포함 32. 웹훅은 지연 허용이라 절반
**김도현 (worker_pool.go:55)**: 웹훅 풀이 가득 차면 웹훅 작업은 어떻게 되나요? 버려지면 안 되는데
**박서연**: 큐에 대기해요. 큐도 차면 디스크 백업 큐로 넘어가서 유실은 없어요. 늦게 가는 것뿐
**김도현**: ㅇㅋ "결제는 빠르게, 웹훅은 반드시" — 이 우선순위 철학 그대로네요. approve
**이준호**: approve (풀 사이즈 산정식 주석 확인)
"""

FILES["pr-159-secret-rotation-api.md"] = """---
created: 2026-05-24
tags: [pr-review, raw-dump, webhook, security]
pr: 159
---

# PR #159 — feat: 웹훅 시크릿 회전 API

> 작성: 이준호 / 리뷰: 박서연 / 머지: 보류 → 2026-06-12 기준 리뷰 진행 중

**박서연 (rotation.go:33)**: 회전 시 구 시크릿 유예 기간이 24h 하드코딩인데, 가맹점이 배포가 느리면 24h 안에 신 시크릿 반영 못 할 수도 있어요
**이준호**: 유예를 가맹점이 선택(24h/72h/7d)하게 할까요?
**박서연**: 옵션이 늘면 설명 비용도 늘어서... 기본 72h 고정이 낫지 않을까 싶기도 하고. 도현님 의견 듣고 정하죠
**이준호**: 넵 보류로 두고 휴가 다녀와서 마무리할게요
"""

FILES["pr-162-settlement-csv-export.md"] = """---
created: 2026-06-10
tags: [pr-review, raw-dump, settlement]
pr: 162
---

# PR #162 — feat: 정산명세서 CSV 내보내기 (draft)

> 작성: 박서연 (준호 휴가로 초안만) / 리뷰: 미시작 / 상태: draft

**박서연**: 가맹점 C 요구 컬럼(거래ID/승인일시/금액/수수료/정산액)으로 draft 올려둡니다. 준호님 복귀하면 인계. 명세서 생성 로직에 exporter 인터페이스만 하나 추가한 구조라 PDF/CSV가 같은 데이터 소스를 봐요
**박서연**: TODO — 인코딩(엑셀 호환 BOM), 10만 행 스트리밍, 대시보드 다운로드 버튼
"""

FILES["pr-164-alert-tuning.md"] = """---
created: 2026-05-29
tags: [pr-review, raw-dump, monitoring, settlement]
pr: 164
---

# PR #164 — feat: 배치 알람 단계화 (INC-231 후속)

> 작성: 이준호 / 리뷰: 박서연 / 머지: 2026-05-29

**박서연 (alerts.yaml:12)**: "60분 초과 = 경고"의 60분 근거는요? 평소 배치가 40분대면 정상도 경고 뜰 텐데
**이준호**: 최근 60일 배치 소요 p99가 52분이에요. 60분이면 오탐 거의 없어요. 수치는 분기마다 재점검 주석 달아뒀어요
**박서연 (alerts.yaml:30)**: "락 있는데 프로세스 없음 = 긴급" 이거 좋네요. 진짜 죽은 것만 잡는 시그널
**이준호**: INC-231이 "오래 걸림"을 "죽음"으로 오판한 사고라서, 알람이 그 둘을 구분해주는 게 핵심이에요
**박서연**: 알람 메시지의 "재실행 금지. 락 확인 먼저" 문구 확인 ㅋㅋ approve
"""

def main():
    os.makedirs(BASE, exist_ok=True)
    for name, content in FILES.items():
        with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
            f.write(content.lstrip("\n"))
    print(f"pr {len(FILES)}개 생성 완료 → raw/pr/")

if __name__ == "__main__":
    main()
