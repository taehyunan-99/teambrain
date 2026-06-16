---
created: 2025-08-20
tags: [pr, webhook, payment, mvp]
---

# PR #074 — 웹훅 발송기 v1 (fire-and-forget)

작성: 이준호
리뷰: 박서연

## 설명

가맹점에 결제 결과를 알려주는 웹훅 발송기 첫 버전입니다.
approve/cancel 처리 직후 가맹점이 등록한 endpoint로 단일 HTTP POST 1회 전송.
2xx면 성공으로 보고 종료, 아니면 실패 로깅하고 종료합니다.

범위:
- 단일 POST, 재시도 없음
- dead letter / 재시도 큐 없음
- 서명 없음 (가맹점 식별은 본문 merchant_id로)

일단 결과 알림이 나가는 것 자체가 목표라 MVP 수준으로 잡았습니다.

## 변경 파일

- `webhook/WebhookSender.java` (신규)
- `webhook/WebhookPayload.java` (신규)
- `payment/PaymentService.java` (approve/cancel 후 sender 호출 1줄)

---

## 리뷰 코멘트

**박서연 (webhook/WebhookSender.java:41)**: 여기 send() 한 번 쏘고 끝인데, 가맹점 서버가 잠깐 502 떠도 그냥 누락되는 구조네요. v1 범위라는 건 이해했고 지금 큐까지 붙이자는 건 아닌데, 최소한 `// TODO: 실패 시 재시도/dead letter 필요` 주석이라도 박아두면 좋겠어요. 나중에 누가 봐도 "여기 일부러 비워둔 자리"라는 게 보이게.

**이준호 (webhook/WebhookSender.java:41)**: 헉 사실 어제 여기 TODO 적어놨었는데 키보드가 또 씹혀서 한 줄 통째로 날아갔네요 ㅋㅋㅋ 진짜임 변명아님 추가하겠습니다 🙏

**박서연 (webhook/WebhookSender.java:48)**: non-2xx일 때 status code랑 endpoint는 로그에 같이 남겨주세요. 나중에 어느 가맹점이 자꾸 실패하는지 봐야 할 텐데 지금은 "전송 실패"만 찍혀서 추적이 안 돼요.

**이준호 (webhook/WebhookSender.java:48)**: 넵 merchant_id / endpoint / status code 같이 찍도록 수정했습니다.

**박서연 (webhook/WebhookSender.java:53)**: 타임아웃은 걸려있죠? connect/read 둘 다.

**이준호 (webhook/WebhookSender.java:53)**: 넵 둘 다 5초로 잡아놨습니다. 가맹점 서버 느릴 때 우리 스레드 물고 있으면 안 되니까요.

**박서연 (webhook/WebhookSender.java:41)**: ㅇㅋ TODO 들어간 거 확인했어요. 재시도/서명은 다음 버전에서 따로 잡는 걸로. 이번엔 v1 범위 그대로 가시죠.

approve 👍
