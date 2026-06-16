---
title: Redis 도입 — 캐시/세션 표준화 (Redis Introduction)
tags: [infra, redis, cache, session, standardization]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2025-02-18-decision-redis-introduction.md
  - raw/infra/slack/2025-02-25-redis-ready-announce.md
  - raw/infra/slack/2025-03-05-platform-announce-redis.md
source_hashes:
  - c49d8ba41ab6cdec6ed582f5c5527c06f88eb6a5
  - 9e9e32ff41f41299cecde6dbd866fcc292e8dabc
  - 249b6f294f56db84914178d888fcd61d6aebea28
---

<!-- llmwiki:auto -->

## Summary
팀마다 제각각이던 캐시·세션 저장소를 표준화하기 위해 관리형 Redis를 사내 표준으로 도입했다(memcached·DB 세션 테이블 대안 탈락). 단일 인스턴스로 시작하고 maxmemory는 넉넉히, 키 네이밍 컨벤션과 용도별 TTL 명시를 규칙으로 정했으며, 모든 키에 TTL을 거는 것을 전사 필수 원칙으로 공지했다.

## Details
### 결정 — Redis 표준화 (2025-02-18)
정유진(제안·운영)과 강민석(클라이언트 연결 검토)이 결정했다. 서비스가 늘면서 캐시·세션 저장소가 팀마다 제각각이고(일부는 애플리케이션 메모리, 일부는 DB 세션), K8s 위에서 파드가 수시로 재기동되면서 로컬 메모리 캐시·세션의 일관성이 깨진다는 문제가 배경이었다.

검토한 대안:
1. **Redis (채택)** — 관리형 Redis를 K8s 워크로드에서 접근. 풍부한 자료구조(string/hash/sorted set), 키별 TTL 네이티브 지원, 운영·관측 도구 성숙.
2. memcached — 단순 K-V로는 가볍지만 자료구조 빈약, 영속화·세션 활용 제약. 탈락.
3. DB 세션 테이블 — 별도 인프라 불필요하나 세션 R/W가 DB 부하로 직결되고 만료 정리를 배치로 돌려야 함. TTL 직접 구현 부담. 탈락.

결정 세부:
- Redis를 캐시·세션 저장소 사내 표준으로 도입. 운영(인스턴스/알람/백업/배포)은 인프라팀(정유진), 클라이언트 연결·커넥션 풀은 강민석.
- **단일 인스턴스로 시작.** 가용성 요구가 커지면 추후 replica(읽기 분산·HA) 검토.
- maxmemory는 일단 넉넉히 잡아 여유 확보.
- eviction 정책은 `noeviction`(메모리가 차도 키를 버리지 않고 쓰기를 거부) — 데이터 유실 방지를 기본값으로. (이후 변천은 [[redis-eviction-policy]] 참조.)
- 키 네이밍은 `{도메인}:{용도}:{식별자}` 컨벤션, TTL은 용도별로 호출 측에서 명시.

알려진 리스크: 단일 인스턴스 SPOF(replica 도입 전까지 critical 경로 사용 자제), `noeviction`+단일 인스턴스의 메모리 한계 시 쓰기 거부(maxmemory 사용률 알람을 운영 초기부터), 파드 증설 시 커넥션 폭증(풀 상한·타임아웃 정리).

### 클러스터 준비 공유 (2025-02-25)
강민석이 관리형 Redis 클러스터 준비 완료를 공유했다.
- 엔드포인트 `redis.internal.nimbuspay:6379`, TLS 활성, 비밀번호는 vault `redis/prod`.
- 커넥션 풀 권장: max active 50 / max idle 10 / min idle 2, timeout 2s, **앱 인스턴스당 풀 1개**(매 요청마다 새로 만들지 말 것).
- 세션 저장소부터 이관(인메모리 → Redis로 옮겨 파드 재시작/스케일링 시 세션 보존). 캐시는 팀별 자유 사용, namespace prefix(`pay:`, `settle:`)로 키 충돌 방지.
- 정유진이 "캐시든 뭐든 TTL 꼭 걸라"고 당부. 이 시점 maxmemory-policy는 `allkeys-lru`로 잡혀 있었다.

> 정책값 메모: 결정문서(2/18)는 `noeviction`을 명시했으나, 이 #infra 공유(2/25)에서는 `allkeys-lru`로 잡아둔 상태였고, 전사 공지(3/5)에서는 다시 `noeviction`으로 안내된다. 시간순 변천과 최종 상태는 [[redis-eviction-policy]]에 정리.

### 전사 공지 (2025-03-05)
정유진이 #platform-announce에 공용 Redis 캐시/세션 인프라 오픈을 전사 공지했다.
- 내부 엔드포인트 `redis.internal.nimbuspay.io:6379`, VPC 내부에서만 접근, vault `infra/redis/common`.
- 팀별 prefix 권장(`pay:`, `settle:`, `infra:`).
- **모든 키 TTL 필수**. 현재 maxmemory 정책은 `noeviction`이라 메모리가 차면 쓰기가 그냥 실패하므로 "TTL은 선택이 아니라 필수". 대용량 키는 사용 전 인프라팀과 사전 협의.
- 결제·정산팀에 세션/멱등성 도입 검토 시 함께 보겠다고 안내. 김도현(멱등성 단기 저장소), 한지우(정산 배치 중간상태 캐싱)가 검토 의사를 밝혔다.

## Related
Redis는 NimbusPay 인프라의 중심 컴포넌트로 멱등키·세션·캐시가 모두 의존한다([[idempotency]] 키 저장이 대표 사례). eviction 정책의 시간순 변천(`noeviction`/`allkeys-lru`/`volatile-lru`)과 최종 상태는 [[redis-eviction-policy]]에서 다룬다. 단일 인스턴스 SPOF·메모리 운영은 [[infra-baseline]] 관측성 대시보드의 Redis 패널로 감시하며, 프로모션 시 메모리 헤드룸·증설은 [[promo-capacity-planning]], 파드 증설과 다운스트림 커넥션 연동은 [[autoscaling-hpa]]에서 함께 본다.
