---
created: 2026-02-18
channel: platform-announce
tags: [slack, raw-dump, deploy, infra, alerting]
---

# slack #platform-announce 2026-02-18

**13:15 정유진**: [공지] 알람 라우팅 정비했습니다. 이제 알람이 심각도별로 나뉘어서 갑니다
**13:15 정유진**: WARN은 alert-bot 채널로, CRITICAL은 alert-bot + 온콜 직접 핑으로 갑니다
**13:16 정유진**: 서비스 영향 없는 알람 설정 변경이고요, 각 팀에서 보던 알람은 그대로 alert-bot에서 보시면 됩니다
**13:17 정유진**: 혹시 받던 알람이 안 오거나 이상하면 #infra로 알려주세요. 라벨 매핑 누락일 수 있어요 🙏
**13:20 한지우**: 정산 배치 실패 알람은 어느 쪽으로 가나요?
**13:22 정유진**: 배치 잡 실패는 CRITICAL로 잡아놨어요. 온콜 + alert-bot 둘 다 갑니다
**13:23 한지우**: 굿 감사합니다 👍