---
created: 2025-08-21
tags: [raw-dump, pay-dev, SDK, 기술논의]
channel: "#pay-dev"
---

**이준호** 15:00  
SDK v2 API 설계 초안 공유합니다. 간단히 보시고 의견 주세요.

주요 변경:
- 결제 초기화: `NimbusPay.init(apiKey)` → `NimbusPay.create({ apiKey, env })`
- 결제 요청: 콜백 방식 → Promise 기반
- 에러 코드: 기존 숫자 코드 → 의미 있는 문자열

**박서연** 15:08  
Promise 기반 좋아요. 에러 코드는 가맹점 SDK 업그레이드 할 때 breaking change 주의해야 해요.

**김도현** 15:12  
9월에 알파 빌드 목표로 가는 거죠? 추석 연휴 전에 초안 확정하면 좋겠어요.

**이준호** 15:15  
네. 이번 주 피드백 반영하고 다음 주 확정 목표로요. 명절 전에 배포 가능한 상태까지 만들고 싶어요.
