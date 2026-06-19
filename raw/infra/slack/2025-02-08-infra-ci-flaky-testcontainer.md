---
channel: "#infra"
date: "2025-02-08"
author: 강민석
---

**강민석** 14:00  
CI 빌드 간헐적 깨짐. Testcontainer로 띄운 Postgres 기동이 느린 타이밍에 테스트 먼저 실행돼서 연결 실패

**정유진** 14:03  
Testcontainer에 waitStrategy 설정돼있어요?

**강민석** 14:05  
있는데 LogMessageWaitStrategy라서 로그 메시지 나오기 전에 통과하는 케이스가 있어요. sleep 넣어서 우회하는 코드도 있는데 러너 부하 높은 타이밍엔 여전히 깨짐

**정유진** 14:07  
캐시된 이미지 레이어 있으면 기동 시간이 일정한데 miss 나면 pull부터 해야 해서 타이밍 가변

**강민석** 14:09  
빌드 깨짐 원인 중 컨테이너 기동 타이밍이 꽤 많아요. 이미지 pre-pull 하는 게 도움이 될 것 같아요
