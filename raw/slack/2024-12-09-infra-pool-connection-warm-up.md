---
channel: "#infra"
date: 2024-12-09
author: 정유진
---
정유진: HikariPool initializationFailTimeout, minimumIdle 설정 점검했어요.
강민석: 배포 후 warm-up 이슈 있었나요?
정유진: connection 0에서 시작하면 트래픽 급증 시 pool 부족으로 승인 지연 날 수 있어서.
강민석: minimumIdle 설정으로 최소 connection 유지하면 되겠네요. maximumPoolSize는요?
정유진: 현재 설정 유지. 타임아웃 에러 없고 정상이에요.
강민석: warm-up 로직도 배포 스크립트에 추가해두죠.