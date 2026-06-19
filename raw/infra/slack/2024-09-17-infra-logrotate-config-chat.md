---
created: 2024-09-17
tags: [slack, raw-dump, ops, logrotate, disk]
channel: infra
---

# slack #infra 2024-09-17

**14:23 강민석**: logrotate 설정에 compress 옵션 추가하면 용량 좀 더 아낄 수 있지 않을까요?
**14:25 정유진**: gzip 압축이요? 로그 서버는 CPU 여유 있으니까 괜찮을 것 같은데
**14:26 강민석**: 정리 후 사이즈 비교해봤더니 압축하면 70~80% 줄더라고요. 텍스트 로그라서
**14:28 정유진**: 다음 주에 테스트 서버에서 한 번 먼저 돌려봐요. compress + delaycompress 같이
**14:29 강민석**: 알겠습니다. cleanup 스크립트도 같이 정리할게요