---
channel: "#infra"
date: 2024-09-10
author: 강민석
---
강민석: DB connection pool 사이즈 결정 방법론 공유 하나. T2 공식: pool = (core_count * 2) + effective_spindle_count.
정유진: maximumPoolSize 설정 때마다 이 공식 쓰면 되는 건가요?
강민석: 기준값으로 쓰되 승인처럼 동기 I/O 무거운 flow는 실측 후 조정해야 해요.
정유진: 타임아웃 설정은요?
강민석: connectionTimeout은 보통 30초 기본값 두고 지연 패턴 보면서 줄이는 편인데, 케이스 바이 케이스.
정유진: 정리해서 wiki에 올려두죠.