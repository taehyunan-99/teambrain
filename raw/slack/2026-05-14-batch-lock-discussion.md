---
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
