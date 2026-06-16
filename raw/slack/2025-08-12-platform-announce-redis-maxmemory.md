---
created: 2025-08-12
tags: [slack, raw-dump, redis, infra, announcement]
channel: platform-announce
---

# slack #platform-announce 2025-08-12

**14:00 정유진**: [공지] Redis maxmemory-policy 변경 안내
**14:00 정유진**: 대상: 공용 Redis 클러스터 (prod-redis-01/02)
**14:01 정유진**: 최근 인스턴스 메모리 사용률이 지속적으로 80% 이상이고 피크에 90%를 넘는 구간이 잡힙니다. 현재 maxmemory-policy가 `noeviction`이라 한계 도달 시 write 명령이 OOM 에러로 거부됩니다
**14:02 정유진**: 변경 내용: `noeviction` → `allkeys-lru`. maxmemory 한계 도달 시 LRU 기준으로 임의 키가 evict됩니다
**14:02 정유진**: 적용 일정: 2025-08-19(화) 02:00~02:30 KST, 무중단 config set으로 반영 예정. 재시작 없음
**14:03 정유진**: 영향: TTL 없이 무기한 보관하는 키나, 메모리 압박 시 evict되면 안 되는 키가 있으면 미리 알려주세요. 팀별로 사용 중인 키 prefix 점검 부탁드립니다
**14:05 강민석**: 메모리 추이/키 개수 대시보드 링크 첨부합니다 → grafana.nimbus.internal/d/redis-prod
**14:06 강민석**: 패널에 used_memory, evicted_keys, keyspace_misses 추가해뒀어요. 적용 후 evict 발생량 여기서 보시면 됩니다
**14:11 박서연**: 결제팀에서 멱등키를 Redis에 올려두는데(`idem:` prefix, TTL 24h), allkeys-lru면 TTL 남아있어도 메모리 압박 때 evict 될 수 있는 거죠?
**14:13 정유진**: 네 allkeys-lru는 TTL 유무와 무관하게 전체 키 대상으로 LRU evict 합니다. TTL 키만 대상으로 하려면 volatile-lru가 맞고요
**14:15 박서연**: 음 멱등키가 evict되면 같은 키로 재시도 들어왔을 때 신규 결제로 처리돼서 중복청구 위험이 있어요. 결제팀 키는 evict 대상에서 빠지는 게 안전합니다
**14:18 정유진**: 그럼 volatile-lru로 갈까요? 그러면 TTL 걸린 키만 evict 후보가 되고, TTL 없는 키는 보호됩니다. 근데 멱등키도 TTL 24h라 volatile-lru에서도 evict 후보긴 해요
**14:20 박서연**: 그 부분이 걸리네요. 멱등키는 TTL은 있지만 만료 전까지는 절대 사라지면 안 되는 키라서요. lru 정책 자체가 멱등키랑 안 맞는 느낌
**14:23 정유진**: 그럼 멱등키는 메모리 압박이랑 분리하는 게 깔끔하겠네요. 결제 멱등키용 Redis를 따로 떼거나, 최소한 evict 안 되는 인스턴스로 옮기는 방향
**14:25 김도현**: 인스턴스 분리는 비용/운영 이슈 있으니 바로는 어렵고요. 일단 이번 정책 변경 적용 전에 결제팀 키 사용량부터 정유진님이 뽑아주실 수 있을까요. 멱등키가 전체 메모리에서 차지하는 비중 보고 결정하죠
**14:27 정유진**: 넵 prefix별 메모리 점유 뽑아서 #pay-dev에 공유할게요. 그 결과 보고 결제 키를 protected 인스턴스로 뺄지 정책을 volatile-lru로 갈지 정하시죠
**14:28 박서연**: 좋아요. 그 데이터 나오기 전까지는 prod-redis 멱등키 evict 리스크가 열려있는 거니까, 8/19 적용을 결제팀 검토 끝날 때까지 미뤄주실 수 있나요
**14:30 정유진**: 알겠습니다. 8/19 일정은 홀드하고, 결제 키 사용량 공유 → 결제팀 OK 받은 뒤 새 일정 다시 공지할게요
**14:31 김도현**: 감사합니다 🙏
**14:33 강민석**: 대시보드에 `idem:` prefix 메모리 점유 패널도 따로 만들어둘게요
