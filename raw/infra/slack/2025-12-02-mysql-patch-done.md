---
created: 2025-12-02
channel: platform-announce
tags:
  - slack
  - raw-dump
  - deploy
  - mysql
  - infra
---

# slack #platform-announce 2025-12-02

**23:34 정유진**: [점검 완료] MySQL 패치 끝났습니다. standby→primary 순서대로 적용, 스위치오버 1회 태웠어요
**23:34 정유진**: 스위치오버 시점에 커넥션 잠깐 끊긴 거 외엔 에러율/지연 이상 없습니다. 10분 모니터링 마침
**23:35 정유진**: 문제 생기면 standby로 다시 페일오버하면 되고, 패치 롤백은 백업 시점 복구가 필요해서 그건 별도 판단입니다
**23:40 강민석**: 수고하셨어요 🙏 내일 아침에 슬로우쿼리 로그도 한번 훑어볼게요
