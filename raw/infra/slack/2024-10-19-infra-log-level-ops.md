---
created: 2024-10-19
tags: [slack, raw-dump, ops, log-level, disk]
channel: infra
---

# slack #infra 2024-10-19

**15:00 강민석**: DEBUG 레벨 로그 엄청 쌓이고 있어요. 서버 /var/log/app/debug.log 가 하루 300MB씩
**15:02 정유진**: 프로덕션에서 DEBUG가 켜져 있었나요? INFO로 내려야 할 것 같은데
**15:03 강민석**: 이준호 씨가 웹훅 디버깅하면서 임시로 올린 것 같아요
**15:05 정유진**: 로그 서버 용량이 지금 df 기준 45%인데 DEBUG 계속 켜두면 올라가겠네요. 끄는 게 맞아요
**15:06 강민석**: 이준호 씨한테 INFO로 되돌려달라고 연락할게요. cleanup도 오늘 미리 한 번 수동 정리하고