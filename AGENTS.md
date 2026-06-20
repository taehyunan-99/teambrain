# TeamBrain (llmwiki) - Claude Code / Codex / Cursor / Antigravity 작업 지침

이 저장소의 진실 공급원은 `wiki/`·`raw/` 마크다운 파일이다 — 임베딩/벡터/그래프DB 도입 충동이 들면 멈추고 `docs/DIRECTION.md`(북극성)를 먼저 읽는다.

**Tradeoff**: 영역 경계가 모호한 작업은 두 가이드를 모두 읽어야 함 — 약간의 토큰 비용을 부담하는 대신 단일 거대 가이드의 lost-in-the-middle을 차단한다.

<!--
이 파일은 map 역할을 한다. 작업 시 해당 영역의 AGENTS.md를 먼저 읽고 진행한다.
root에 모든 가이드를 몰아넣지 않고 영역별로 분리한 이유는 토큰 효율 + 컨텍스트 정확도다.
디렉토리 트리(ls로 알 수 있는 정보)는 의도적으로 넣지 않는다(G1 안티패턴).
-->

## 영역별 가이드

작업 영역에 해당하는 AGENTS.md를 먼저 읽고 진행한다.

- **scripts/llm** — 슬랙봇 QA 파이프라인(검색→판단 2단, Ollama) → [`scripts/llm/AGENTS.md`](scripts/llm/AGENTS.md)
- **scripts/search** — 하이브리드 검색 엔진(FTS5 BM25 + sqlite-vec) → [`scripts/search/AGENTS.md`](scripts/search/AGENTS.md)
- **scripts** — 더미 데이터 생성·측정 워크플로(Phase 1~5) → [`scripts/AGENTS.md`](scripts/AGENTS.md)
- **docs** — 설계 문서(방향성·문제정의·측정 findings). **작업 전 먼저 읽는 곳** → [`docs/AGENTS.md`](docs/AGENTS.md)
- **wiki** — 데이터 계층(raw 입력 + wiki LLM 산출 = 진실 공급원) → [`wiki/AGENTS.md`](wiki/AGENTS.md)

## 영역 가이드의 구조

<!--
각 영역의 AGENTS.md는 8섹션 템플릿을 따른다.
init은 가벼운 뼈대만 만든다 — WHAT/CONTENTS/WHERE/COMMANDS는 코드 스캔 기반 초안,
HOW/HOW NOT/WHY는 placeholder. 본격 작성은 /update 인터뷰로 채운다.
-->

1. **WHAT** — 이 모듈이 무엇을 하는가 *(init에서 채움)*
2. **CONTENTS** — 디렉토리 맵 + 기술 스택 *(init에서 채움)*
3. **HOW** — 일반적인 수정은 어떻게 하는가 *(`/update` 인터뷰에서 채움)*
4. **HOW NOT** — 시스템을 깨뜨리는 비명백한 함정 *(`/update` 인터뷰에서 채움)*
5. **WHERE** — 다른 모듈과의 의존성 *(init에서 채움)*
6. **WHY** — 코드에 안 적힌 배경 지식 *(`/update` 인터뷰에서 채움)*
7. **COMMANDS** — 빌드/테스트/린트 + 영역 고유 가드 *(init은 빌드/테스트/린트만)*
8. **LEARNED CAUTIONS** — 별도 파일 `LEARNED_CAUTIONS.md`. `learn` 스킬이 누적

## 공통 명령어

<!-- 이 프로젝트는 Python 스크립트 모음 + 마크다운 vault다. 표준 빌드 시스템(npm/make)은 없다. -->

- 의존성 설치: `pip install -r scripts/llm/requirements.txt -r scripts/search/requirements.txt`
- 검색 인덱스 빌드: `python3 scripts/search/build_index.py` (루트에서 실행, `docs/index.db` 생성)
- QA CLI: `python3 scripts/llm/wiki_qa.py "질문"` (루트에서 실행)
- 위키 빌드: `wiki-build` 스킬 (raw → wiki 개념 합성, 증분)

**공통 명령어 가드** (모든 영역에 적용):

- `raw/`를 LLM이 직접 수정 금지 — 사람 작성 입력(읽기 전용). Phase 3 교훈: 워커가 raw에 직접 쓰는 부작용으로 미검 파일 양산.
- `.env` 커밋 금지 — 실제 Slack 토큰(xoxb/xapp) 포함. 이미 gitignore됨.
- `docs/index.db`를 직접 편집 금지 — 생성물. `build_index.py`로 재빌드.
- 모든 Python 스크립트는 **프로젝트 루트에서 실행** — `docs/index.db` 등 경로가 루트 기준 상대경로다.

## 주의사항 학습 (learn 스킬)

작업 중 실수가 발견되면 다음 형태로 호출해 해당 영역 폴더의 `LEARNED_CAUTIONS.md`에 누적한다. 본문 가이드(AGENTS.md)는 8번 섹션에서 `@./LEARNED_CAUTIONS.md`를 참조하므로 자동 로드된다. `learn` 스킬은 `LEARNED_CAUTIONS.md`만 갱신하고 본문 가이드는 절대 건드리지 않는다.

- Claude Code/Cursor/Antigravity: `/learn <메모>` (인자 없이도 호출 가능)
- Codex: `$learn <메모>`

스킬 위치: `.claude/skills/learn/` (Claude), `.agents/skills/learn/` (Codex/Cursor/Antigravity)
