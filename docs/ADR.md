# ADR — llmwiki 아키텍처 결정 기록

> 작성일 2026-06-12. 각 결정의 맥락·선택·근거·trade-off.

## ADR-001: LLM Wiki(Karpathy) 방식 채택, RAG 폐기

- **맥락:** second-brain의 RAG(임베딩+4축+그래프)가 과설계로 중단.
- **결정:** build-time에 LLM이 wiki를 컴파일하는 Karpathy LLM Wiki 채택.
- **근거:** second-brain을 죽인 라이브 함정(거부 임계값 0.35→0.75, structured output, qwen3 모델 튜닝)이 전부 임베딩·구조화출력 계층에서 발생 → 그 계층 제거 시 함정 원천 차단. LLM이 마크다운을 직접 읽음.
- **Trade-off:** ~100노트 초과 시 중복판단 비용 ↑ → index.md 카탈로그로 완화 ([ADR-005](#adr-005-임베딩-인덱스-대신-indexmd-카탈로그)).

## ADR-002: Hermes Agent 미채택, Claude Code 스킬 채택

- **맥락:** "옵시디언 + 클로드 코드" vs "옵시디언 + 헤르메스 에이전트" 비교.
- **결정:** Claude Code 내부 스킬 형태로 구현.
- **근거:** Hermes Agent(Nous Research, 2026-02, MIT)는 persistent memory·skill creation의 범용 자율 에이전트지만 wiki 빌드 특화 기능이 없고 멀티플랫폼 게이트웨이 등 불필요한 무게를 더함 → "단순화" 목표에 역행. Claude Code는 vault 직접 읽기/쓰기에 최적이고 별도 인프라 0.
- **Trade-off:** 외부 자율성(스케줄러/메신저)을 포기 — 현재 MVP에 불필요하므로 수용.
- **참고:** 전임 insights.md에서 제외했던 "Hermes 4 **LLM 모델**"과 이 "Hermes **Agent**"는 이름만 같은 별개.

## ADR-003: 외부 API/Ollama 대신 Claude Code 인-스킬 구동

- **맥락:** LLM을 무엇으로 구동할지 (클라우드 API / 로컬 Ollama / 하이브리드 / 인-스킬).
- **결정:** Claude Code 세션 내부에서 스킬로 구동 (별도 API 호출·Ollama·Python 파이프라인 X).
- **근거:** 코드 ≈ 0줄. olw의 Python 파이프라인을 SKILL.md 절차서로 치환. 설치/의존 마찰 제거.
- **Trade-off:** 클라우드(Claude) 의존 — second-brain의 "비용0/로컬" 원칙은 일부 양보하나, 데이터(vault)는 여전히 로컬 git에 남고 빌드만 세션 중 수행.

## ADR-004: 사람 review 루프 폐기, 자동 적용 + git 안전망

- **맥락:** olw는 LLM 초안을 사람이 승인/거절하고 피드백을 다음 컴파일에 주입.
- **결정:** 자동 적용. review 루프 없음.
- **근거:** 가역성(git)이 곧 review. 잘못 만들면 `git diff`/`git revert`로 즉시 복구. MVP 단순화.
- **Trade-off:** 손수정 덮어쓰기 위험 → `<!-- llmwiki:auto -->` 마커 3중 방어 ([ADR-006](#adr-006-변경감지--source_hash--git-statedb-없음)).

## ADR-005: 임베딩 인덱스 대신 index.md 카탈로그

- **맥락:** 개념 100개 초과 시 중복 개념 판단을 위해 전체 아티클을 읽을 수 없음.
- **결정:** index.md를 항상 최신 개념 카탈로그(개념명+1줄요약)로 유지, 빌드 시 이것만 읽어 중복 후보를 좁힘. 필요 시 wiki/를 주제 서브트리로 분할.
- **근거:** 임베딩 없이도 "중복 판단 인덱스" 역할. 유지 비용 << 전체 재독 비용.

## ADR-006: 변경감지 = source_hash + git (state.db 없음)

- **맥락:** olw는 SQLite state.db로 노트-개념 맵핑/해시를 추적.
- **결정:** 아티클 frontmatter의 `source_hashes`(`git hash-object` 값) 대조 + git diff. DB 없음.
- **근거:** git이 이미 모든 파일의 content hash를 제공 → 별도 해시 함수/캐시 파일 0줄. raw↔아티클 역추적은 `sources` 필드 + `wiki/sources/` 인덱스로.
- **Trade-off:** 빌드/커밋 타이밍 어긋나면 git diff 부정확 → source_hash 대조를 ★기본으로 병행.
