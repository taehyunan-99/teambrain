# scripts 작업 가이드 (더미 데이터 생성·측정 워크플로)

{이 영역에서 LLM이 가장 자주 틀리는 무엇을 막는가 — 1문장. update에서 채울 자리.}

<!--
첫 줄 미션 후보(추정 — /update에서 확정): "future-leak(과거 문서에 미래 사건 누설)을 막는다.
생성 워크플로는 staging 경유 + result만 신뢰(raw 직접 쓰기 금지)." Phase 3 교훈.
-->

<!--
== init 시점 안내 ==
가벼운 뼈대. WHAT/CONTENTS/WHERE/COMMANDS만 코드 스캔으로 채움. HOW/HOW NOT/WHY는 /update에서.
이 영역은 하위 scripts/llm·scripts/search를 제외한 '생성기·측정 워크플로' 영역이다.
-->

## 1. WHAT — 이 모듈은 무엇을 하는가

더미 데이터 생성·검색 한계 측정 워크플로(Phase 1~5). 가상 PG사 'Nimbus Pay'(결제·정산·인프라 3팀, 24개월) raw 더미를 생성하고, 노이즈·near-miss를 의도적으로 증식해 검색이 깨지는 임계를 재현·측정한다. 이 프로젝트의 "지저분한 실무 데이터" 시뮬레이션을 만드는 곳.

## 2. CONTENTS — 파일/디렉토리와 기술 스택

- `gen_slack.py` / `gen_pr.py` / `gen_transcripts.py` / `gen_weekly.py` — 소스별 raw 더미 생성기.
- `gen_source_summaries.py` — wiki/sources 요약 생성.
- `phase3_noise.wf.js` / `phase3_repair.wf.js` — 노이즈 824건 증식 + 수리 다이나믹 워크플로.
- `phase4_measure.wf.js` — 검색 한계 측정.
- `phase5a_*.wf.js` — near-miss 표적 증식(hardnoise/nearmiss/reinforce) + 재측정.
- `phase5b_design_critique.wf.js` — 5b 설계 비평 워크플로.
- 하위 영역: `llm/`, `search/` (별도 가이드)

기술 스택: Python (생성기 `gen_*.py`) + JavaScript 다이나믹 워크플로 (`*.wf.js`)

## 3. HOW — 일반적인 수정은 어떻게 하는가

_(update 스킬에서 채워질 자리. 작업 중 패턴이 정립되면 `/update`로 인터뷰 진행)_

## 4. ⛔ HOW NOT — 시스템을 깨뜨리는 비명백한 함정 (중요)

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다 — Phase 3의 future-leak·raw 직접쓰기 함정은 /update에서 정식 기재)_

## 5. WHERE — 다른 모듈과의 의존성

- **약결합**: `raw/`(생성 대상 — [`wiki/AGENTS.md`](../wiki/AGENTS.md)), `docs/`(측정 결과 findings — [`docs/AGENTS.md`](docs/AGENTS.md))
- **하위 영역**: `scripts/llm`, `scripts/search`는 독립 가이드를 가진 별도 영역.
- **경계/어댑터**: 생성물은 항상 `raw/` 마크다운(frontmatter `created`/`tags`)

## 6. WHY — 코드에 안 적힌 배경 지식

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 7. COMMANDS — 빌드/테스트/린트

_(개별 생성기·워크플로 — 표준 빌드 명령 없음. 실행 방식은 /update에서 정리)_

## 8. ⚠️ LEARNED CAUTIONS — 학습된 주의사항

@./LEARNED_CAUTIONS.md

자세한 내용은 [LEARNED_CAUTIONS.md](./LEARNED_CAUTIONS.md) 참조.
