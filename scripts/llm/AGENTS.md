# scripts/llm 작업 가이드

{이 영역에서 LLM이 가장 자주 틀리는 무엇을 막는가 — 1문장. update에서 채울 자리.}

<!-- 첫 줄 미션은 /update의 "컨벤션 합의"에서 사용자와 확정한다. -->

<!--
== init 시점 안내 ==
가벼운 뼈대. WHAT/CONTENTS/WHERE/COMMANDS만 코드 스캔으로 채움. HOW/HOW NOT/WHY는 /update에서.
-->

## 1. WHAT — 이 모듈은 무엇을 하는가

슬랙봇 QA 파이프라인(Phase 6). 질문을 받아 **[1단 검색: scripts/search가 후보를 넓게 떠줌] → [2단 LLM 판단: 후보 본문을 읽고 사실 대조]** 2단 구조로 답한다. "정답을 가르는 건 retrieval 아닌 reasoning"(5b 결론)의 구현체. Ollama 로컬 LLM 클라이언트와 Socket Mode 슬랙봇을 포함한다.

## 2. CONTENTS — 파일/디렉토리와 기술 스택

- `wiki_qa.py` — 검색→판단 2단 파이프라인. `answer(q)` → `{found, summary, points[{text,source}], sources}`. 어떤 실패에서도 예외 안 던지고 dict 반환.
- `slack_bot.py` — Socket Mode 봇. 멘션 → `wiki_qa.answer()` → "생각중" 후 답변 교체.
- `ollama_client.py` — 재사용 Ollama 클라이언트. `chat()`/`generate()`/`is_up()`. `MODEL`/`HOST` 상수 한 곳에서 교체(로컬↔클라우드).
- `check_slack.py` — 토큰·Ollama 사전점검. 봇 띄우기 전 실행.
- `measure_models.py` — 모델 다운그레이드/환각 방지 측정기.
- `demo_structured.py` — 구조화 출력 + 환각 방지 학습용 데모(독립 실행).
- `README.md` — Ollama API 기초 + Phase 6 봇 사용법.

기술 스택: Python (requests, slack_bolt, python-dotenv) + Ollama(gemma4 e4b 로컬)

## 3. HOW — 일반적인 수정은 어떻게 하는가

_(update 스킬에서 채워질 자리. 작업 중 패턴이 정립되면 `/update`로 인터뷰 진행)_

## 4. ⛔ HOW NOT — 시스템을 깨뜨리는 비명백한 함정 (중요)

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 5. WHERE — 다른 모듈과의 의존성

<!-- 강결합 — wiki_qa.py가 sys.path로 hybrid_search를 import해 후보 공급기로 씀. 한쪽 시그니처 변경 = 즉시 깨짐. -->
@../search/AGENTS.md

- **의존(강결합)**: [`scripts/search/AGENTS.md`](../search/AGENTS.md)의 `hybrid_search.search()` — 1단 검색 후보 공급기. `wiki_qa.py`가 `sys.path.insert`로 직접 import.
- **약결합**: `docs/index.db`(검색 인덱스, search가 생성), `.env`(Slack 토큰 xoxb/xapp)
- **경계/어댑터**: Slack(Socket Mode WebSocket), Ollama(`localhost:11434` HTTP)

## 6. WHY — 코드에 안 적힌 배경 지식

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 7. COMMANDS — 빌드/테스트/린트

```bash
# 모두 프로젝트 루트에서 실행
python3 scripts/llm/check_slack.py     # 사전점검(토큰·Ollama)
python3 scripts/llm/slack_bot.py       # 봇 기동 (Ctrl+C 종료)
python3 scripts/llm/wiki_qa.py "질문"   # QA CLI 단발 테스트
```
<!-- Ollama는 테스트 때만 켠다(RAM 부담). 영역 고유 가드는 /update에서 추가. -->

## 8. ⚠️ LEARNED CAUTIONS — 학습된 주의사항

@./LEARNED_CAUTIONS.md

자세한 내용은 [LEARNED_CAUTIONS.md](./LEARNED_CAUTIONS.md) 참조.
