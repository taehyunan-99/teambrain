---
title: Redis eviction 정책 (Redis Eviction Policy)
tags: [infra, redis, eviction, memory, maxmemory, idempotency]
created: 2026-06-16
updated: 2026-06-16
sources:
  - raw/infra/2025-08-15-decision-redis-eviction-policy.md
  - raw/infra/slack/2025-08-12-redis-maxmemory-alert.md
  - raw/infra/slack/2025-08-13-redis-eviction-crossteam.md
  - raw/infra/slack/2025-08-20-platform-announce-eviction.md
source_hashes:
  - 2323210237275ca98d43476e0e08cffb2b4a32c1
  - 5d3628971d753c3b66204aa64d4ce26d862ba6d9
  - dc5d97df60936545aa39120d3e29d1b026d58b1a
  - 3fa0c52408d69e74800f4e9b1cea3379c83e333b
---

<!-- llmwiki:auto -->

## Summary
운영 Redis 메모리가 maxmemory 한계에 근접해 `noeviction`상 쓰기 거부(OOM)가 결제 실패로 이어질 위험이 커지자, eviction 정책을 `noeviction → volatile-lru`로 변경했다(allkeys-lru는 TTL 없는 보호 데이터까지 제거되어 탈락). 변경 후에는 TTL 있는 키 중에서만 LRU로 제거되고 TTL 없는 키는 보존되며, 보호 데이터는 TTL 없이 두거나 충분히 길게 설정하라는 전사 원칙을 공지했다.

## Details
### 정책값 변천 (raw 전반의 표기 불일치 — 시간순 충실 서술)
원본 raw에서 eviction 정책값이 시점마다 다르게 등장한다. 임의 보정 없이 시간순으로 정리한다.

- **2025-02-18 (도입 결정문서)**: `noeviction` 명시 — 데이터 유실 방지 기본값.
- **2025-02-25 (#infra 준비 공유)**: maxmemory-policy를 `allkeys-lru`로 "일단 잡아놨다"고 언급.
- **2025-03-05 (#platform-announce 전사 공지)**: 현재 정책은 `noeviction`, 메모리가 차면 쓰기 실패한다고 안내.
- **2025-08-12 (메모리 경보 대응)**: `config get maxmemory-policy` 실행 결과 `noeviction` 확인("설정 안 건드렸으면 디폴트일걸요").
- **2025-08-15 (eviction 변경 결정문서, 회의 일시 8-12)**: `noeviction → volatile-lru` 결정.
- **2025-08-20 (전사 공지)**: 8/26 정기 점검 시 `noeviction → volatile-lru` 변경 예정 공지.

즉 2/25의 `allkeys-lru`는 잠깐 잡아둔 상태였던 것으로 보이며, 실제 운영 기준 상태는 `noeviction`이었고(2/25 이후 공지·경보 시점 모두 `noeviction`), **최종 결정·공지된 상태는 `volatile-lru`**다. (이후 [[promo-capacity-planning]] 사전점검(2026-02-04) 회의에서는 멱등키 보호를 위해 `noeviction` 유지를 전제로 헤드룸 확보를 논의해, 시점·맥락별로 정책 판단이 갈렸음을 raw가 보여준다.)

### maxmemory 경보와 임시 대응 (2025-08-12)
alert-bot이 redis-prod-01 used_memory 90.2%(5.4GB / 6GB) 경보를 띄웠다. 당시 정책이 `noeviction`이라 한계 도달 시 `OOM command not allowed`로 쓰기(SET)가 막혀 결제까지 영향(사실상 장애, 읽기는 되나 쓰기 불가)이라는 점을 정유진·강민석이 확인했다.
- `allkeys-lru`로 바꾸면 OOM은 피하지만 TTL 안 끝난 키(결제팀 멱등키 24h TTL 등)까지 LRU로 날아가 캐시 미스 → 중복 처리 위험.
- `volatile-lru`도 멱등키가 TTL을 두고 있어 결국 evict 후보에 들어가므로 정책만으로 멱등키만 콕 집어 살릴 수 없음을 확인("어떤 키가 진짜 못 죽는 건지 우리가 모름").
- 임시 처방: maxmemory 6GB → 8GB로 상향(`config set maxmemory 8gb`)해 used 5.4GB/8GB = 67%로 하락, 시간 확보. 강민석이 `--bigkeys`/프리픽스(`idem:`/`sess:`)별 메모리 점유를 뽑고 결제팀과 협의해 정책을 정하기로 했다.

### 결제팀 교차 협의 (2025-08-13, 원문 헤더는 8-12 표기)
정유진이 결제팀 박서연과 #infra에서 협의했다.
- `allkeys-lru` 폐기 합의: 멱등키는 24h TTL 안에 살아있는 것이 보호의 전부인데, allkeys-lru면 메모리 압박 시(=트래픽 많을 때=결제 많을 때=멱등키가 제일 필요할 때) LRU로 evict되어 중복청구로 이어질 수 있음. 박서연은 fail-closed 관점에서 "멱등 판정 데이터 유실은 조용히 틀린 결과로 이어져 위험하며, 차라리 OOM으로 시끄럽게 막히는 게 낫다"고 봤다.
- `volatile-lru` 방향 합의: TTL 없는 영구키를 절대 안 건드리는 보장이 생기고, 세션·캐시류 TTL 키와 함께 후보가 되어 멱등키만 콕 집혀 날아갈 확률은 낮아짐. 다만 volatile-lru도 TTL 키는 날릴 수 있어 멱등키가 후보엔 들어간다는 한계는 남음.
- 두 트랙으로 결론: (1) 정책 `volatile-lru`, (2) maxmemory 상향으로 평시 eviction 자체를 회피하는 헤드룸 확보("정책은 안전망, 진짜 해결은 메모리 헤드룸"). 멱등키 TTL 24h 재검토(짧다는 의견, TTL↑=보호↑=메모리↑=비용↑ 트레이드오프)는 결제팀이 별도 진행하기로 했다.

### 변경 결정 (2025-08-15, 결정자 정유진)
| 정책 | 동작 | 평가 |
|---|---|---|
| `noeviction`(현행) | maxmemory 도달 시 쓰기 거부(OOM) | 한계에서 결제 쓰기 통째 실패. 탈락 |
| `allkeys-lru` | TTL 무관 아무 키나 LRU 제거 | TTL 없는 보호 데이터까지 제거. 탈락 |
| **`volatile-lru`(채택)** | **TTL 있는 키 중에서만 LRU 제거** | TTL 없는 보호키 안전, 캐시성 키만 제거 |

결정: `noeviction → volatile-lru`. 변경 후 maxmemory 도달 시 TTL 키 중 LRU부터 제거, TTL 없는 키 보존. 사용률 경보 임계는 유지(eviction은 한계 회피 수단이지 정상 운영 상태가 아님). 전사 원칙: **유실되면 안 되는 데이터는 TTL 없이 저장하거나 TTL을 충분히 길게.** 리스크로 "짧은 TTL + 보호 필요" 조합 경고, 멱등키 TTL 점검, eviction 실제 발생 시 캐시 미스 부하를 명시했다.

### 전사 공지 (2025-08-20)
강민석이 #platform-announce에 8/26 점검 시 `noeviction → volatile-lru` 변경을 공지했다. volatile-lru는 TTL 있는 키만 제거 대상이나 "메모리가 정말 빠듯하면 TTL이 남아있어도 LRU로 밀려 사라질 수 있다"고 경고하며, 보호 목적 키에는 (1) TTL 충분히 길게, (2) DB 이중화(UNIQUE 등)를 권고했다. 결제팀(박서연)은 멱등키 24h TTL과 DB 가드 부재를 재검토하기로, 정산팀(한지우)은 payout 락/가드 키 TTL을 점검하기로 했다.

## Related
이 정책은 [[redis-introduction]]에서 `noeviction`으로 출발한 운영의 후속 조정이다. 멱등키 evict가 중복청구로 이어지는 위험은 [[idempotency]]와 직결되며, 박서연의 판단 근거인 [[fail-closed-principle]]이 정책 선택의 축이었다. DB 이중화 권고(UNIQUE)는 멱등키 DB 가드 논의로, maxmemory 헤드룸 확보는 [[promo-capacity-planning]]의 Redis 증설로 이어진다. 메모리/지연 경보는 [[infra-baseline]] 관측성 대시보드에서 감시한다.
