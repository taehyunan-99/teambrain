---
title: 프로모션 용량 계획 (Promotion Capacity Planning)
tags: [infra, capacity, promotion, redis, hpa, proxysql, oncall]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2026-02-10-decision-promo-capacity-plan.md
  - raw/infra/transcripts/2026-02-04-promo-readiness-review.md
  - raw/infra/slack/2026-02-14-platform-announce-promo-readiness.md
source_hashes:
  - 816bc6dbfd8874ee56974aedc819dcc5b99c849f
  - 964c943c38be09ec5a8dd3098743139db29990c9
  - d00e37fe562691258f83e8da30752e114072e272
---

<!-- llmwiki:auto -->

## Summary
대형 가맹점 프로모션(2/21, 결제 승인 약 3배 트래픽) 대비 인프라 용량 계획으로, 앞단(HPA)만 늘리면 다운스트림(Redis/ProxySQL/PG)이 병목으로 남기 때문에 전 구간 동시 증설 + 온콜 강화를 결정했다. HPA maxReplicas 상향, Redis 메모리 증설 및 지연 알람 강화, ProxySQL 커넥션 풀 상향, 인프라/결제 교차 온콜을 채택하고, 헤드룸·커넥션·PG rate limit을 숫자로 검증하기로 했다.

## Details
### 사전 점검 회의 (2026-02-04)
정유진·강민석이 결제팀 최민지가 공유한 프로모션을 사전 점검했다. 최민지: 2/21 대형 가맹점 행사, 마케팅 예상 트래픽 평시 대비 약 3배(결제 승인 요청 기준, 조회는 더 튈 수 있음), 오전 11시 오픈 + 점심·저녁 8시 두 피크 추정.

- **HPA**: 당시 결제 API Deployment min 3 / max 10. 평소 피크 7~8개까지 가는데 3배면 20여 개까지 갈 수 있어 max 10은 막힘 → **max 20~25 상향**. Cluster Autoscaler가 노드를 띄우나 새 노드는 2~3분 걸려 피크 시 펜딩 우려 → **당일 오전 min을 8~10으로 임시 상향(워밍업)** 후 max까지 자연 증가, 행사 후 원복. 강민석 작업으로 배정.
- **Redis**: maxmemory 4GB, used 평소 1.4~1.6GB(약 40% 미만). 멱등키(24h TTL)·세션·자잘한 캐시. 결제 승인 3배면 멱등키도 ~3배 쌓이고 24h TTL이라 당일 저녁~다음날이 메모리 최대 시점. 키당 수백 바이트라 절대 증가량은 수백 MB 추정이나 **정확히 재측정(평균 키 사이즈 × 일 발행 수 × 3 → used 예측 → 4GB 헤드룸 산출)** 후 빠듯하면 8GB로 한 단계 상향 검토. **maxmemory-policy는 `noeviction` 유지** — 멱등키는 데이터라 함부로 못 날리므로 노에빅션이 맞고, 대신 메모리가 안 차게 헤드룸을 확보하는 쪽으로 간다(정유진).
- **ProxySQL/MySQL**: ProxySQL 백엔드 풀 DB당 20, MySQL max_connections 100. 파드 25개 × 앱 풀 10 = 250 커넥션 요청이나 ProxySQL 멀티플렉싱으로 백엔드 20개로 수렴. 3배 시 동시 트랜잭션 증가로 풀 대기(큐잉) 가능 → 백엔드 풀 상향 검토하되 **풀 사이즈 × DB 수가 max_connections 100을 넘지 않게 역산**, MySQL 커넥션당 메모리도 고려.
- **PG 다운스트림**: 우리 트래픽 3배면 토스/나이스로 나가는 호출도 3배 → PG사 rate limit에 막히면 스케일아웃이 무의미. **결제팀(최민지/이준호)에 토스·나이스 각 계약상 rate limit과 3배 트래픽 수용 여부 확인 요청**(정유진이 #pay-dev에 남김).
- **관측성**: Redis가 인프라 중심 컴포넌트(멱등키·세션 의존)라 흔들리면 다 영향. 메모리뿐 아니라 **지연(command latency) 기준 알람 추가 + 대시보드 p99 패널을 행사 전 미리 세팅**(강민석, 이번 주 내).

정리: 강민석이 (1) HPA max 25 상향 + 당일 min 임시 상향, (2) Redis 헤드룸 계산, (3) DB 커넥션 풀 계산을 숫자로 정리. PG rate limit은 정유진이 결제팀에 요청. 다음 주 초 재집결.

### 결정문서 (2026-02-10, 결정자 정유진)
검토 대안: (1) 증설 없이 HPA만 상향(기각 — 파드만 늘려도 Redis 메모리/지연·PG rate limit·DB 풀이 병목으로 남고, 앞단만 키우면 다운스트림 포화가 더 빨리 발생), (2) **앞단(HPA)+후단(Redis/ProxySQL) 동시 증설 + 온콜 강화(채택)**.

결정:
1. HPA — 결제 워크로드 maxReplicas 10 → 20 상향.
2. Redis — 인스턴스 메모리 1.5배 증설(헤드룸), 지연 알람 임계 강화(평시보다 낮은 임계로 조기 감지).
3. ProxySQL — 커넥션 풀 상향(MySQL 최대 커넥션 한도 내).
4. 온콜 — 프로모션 기간 강화, 인프라/결제 교차 대응 채널 사전 합의.

리스크: Redis 지연이 튀면 동기 의존 경로(세션/캐시/멱등성)가 영향 → 각 팀이 타임아웃 동작(대기/실패/폴백) 사전 확인 권고. HPA max 상향 시 파드 급증이 ProxySQL 풀·MySQL 한도를 초과하지 않는지 재확인. 사양 변경 시 배포 윈도우 확보. 후속: 결제팀에 Redis 동기 의존 경로 타임아웃 동작 확인 요청, 행사 전 부하 점검·알람 임계 재검토.

### 전사 공지 (2026-02-14)
강민석이 #platform-announce에 완료 조치와 협조사항을 공지했다. 완료: HPA max replica 약 2배 상향, Redis 인스턴스 증설 + 메모리 여유, 온콜 24/7 강화(인프라 1차 대응, 알람 채널 분리). 안내: 피크 시 Redis 응답이 일시적으로 느려질 수 있음(3배 가정이라 100% 장담 어려움). 협조요청: Redis/DB 호출의 **타임아웃 시 동작** 점검 — 특히 결제 critical 경로(막는지/통과시키는지)와 정산 배치(DB 락/타임아웃 시 재시도·중복). 정유진은 당일 Redis/DB 지표(레이턴시·커넥션) 실시간 모니터링을 안내. 김도현(결제 멱등성 타임아웃), 한지우(정산 D+1 배치 재시도)가 점검 의사를 밝혔다.

## Related
이 용량 계획은 인프라 전 구간을 한 번에 본다: [[autoscaling-hpa]](maxReplicas·당일 워밍업), [[redis-introduction]]·[[redis-eviction-policy]](메모리 헤드룸·`noeviction` 유지·지연 알람), [[mysql-ha-failover]](ProxySQL 풀·max_connections 역산). 결제 critical 경로의 타임아웃 시 동작은 [[fail-closed-principle]]·[[idempotency]]와, 정산 배치 재시도/중복은 [[settlement-batch]]와, PG rate limit은 [[payment-gateway-abstraction]]와 맞닿는다. 온콜·알람 강화는 [[infra-baseline]] 관측성 및 oncall-and-alerting과 연결된다.
