# plan — llmwiki 구현 로드맵

> 작성일 2026-06-12 · 상태: 계획 확정 · 구현은 `/awa` 세션에서 진행
> 선행 문서: [PRD.md](PRD.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ADR.md](ADR.md)

## 단계별 로드맵 (4-Phase 과설계 회피)

전임 second-brain은 4-Phase 사전계획 → 마이크로결정 누적으로 죽었다.
**여기선 "가장 작은 동작하는 것"부터, 다음 단계는 실제 막힐 때만.**

### MVP (Day 1 — 동작하는 최소)
- vault 레이아웃 생성: `raw/`, `raw/inbox/`, `wiki/`, `wiki/sources/`, `index.md`, `_log.md`.
- **`wiki-build` 스킬 1개만.** 변경감지는 **source_hash(2차)만** 구현 (git diff는 보조).
- 손수정 보호 마커(`<!-- llmwiki:auto -->`), 출처 추적(`sources`/`source_hashes`), 로그.
- **검증:** raw 노트 3~5개 → wikilink로 연결된 개념 아티클 + index.md 생성. 재빌드 시 변경 없으면 스킵(멱등). 손수정 아티클 보존.

### v0.2 — 마찰 줄이기 (실제로 자주 던지게 되면)
- `wiki-inbox` 스킬: `raw/inbox/` 덤프 → `created`/`tags` 부여 → `raw/`로 승격.
- index.md 그룹핑 품질 개선.

### v0.3 — 규모/정합성 (아티클이 늘어 깨지기 시작하면)
- `wiki-doctor`: dangling/orphan/stale 리포트(읽기전용) + `--fix`(아카이브).
- [ADR-005](ADR.md) 주제 서브트리 분할 도입.

### v1.0 — 선택 (정말 필요해지면)
- 검색 Q&A는 별도 스킬 없이 Claude Code가 wiki를 직접 읽는 것으로 충분(LLM wiki의 본질). 정 필요하면 임베딩 없이 index.md + grep 기반 `wiki-ask` 추가.

### 과설계 회피 가드레일 (각 SKILL.md 상단에 명시)
- 새 frontmatter 필드 추가 전 "변경감지/출처추적에 꼭 필요한가?" 자문.
- 임베딩/벡터/그래프DB/FTS 도입 충동 → **second-brain을 죽인 길.** 멈추고 마크다운으로 먼저.

## wiki-build SKILL.md 핵심 지침 (구현 명세)

`.claude/skills/wiki-build/SKILL.md` — 시스템의 90%가 여기 담긴다.

- **frontmatter:** `name: wiki-build`, `description`(트리거: "wiki 빌드", "위키 업데이트").
- **본문 절차** = [ARCHITECTURE §5](ARCHITECTURE.md) 데이터 흐름 1~7 (변경감지→소스요약→개념합성→링크→index→위생→로그).
- **함정 방지 명시:** raw 1개 실패가 전체 막지 않음 / summary는 자체 완결 / slug 정규화 / 손수정 마커 없으면 스킵 / dangling은 로그만 / 커밋은 사용자 결정.

## 주요 Trade-off / 리스크

| ID | 리스크 | 완화 |
|----|--------|------|
| R1 | ~100노트 초과 시 중복 개념 | index.md 카탈로그만 읽어 중복 후보 좁힘 + 주제 서브트리 분할 (ADR-005) |
| R2 | wikilink 깨짐(dangling/이름변경) | 빌드 시 링크 무결성 패스 → 로그만(stub OFF). slug는 안정 키로 고정. wiki-doctor 점검 |
| R3 | 손수정 덮어쓰기 (자동적용 최대 리스크) | `<!-- llmwiki:auto -->` 마커 + 섹션 단위 보호 + git 복구 (3중, ADR-004/006) |
| R4 | LLM 비결정성으로 개념 경계 흔들림 | 변경감지로 안 바뀐 raw 재방문 안 함(멱등). 기존 아티클은 머지지 재생성 아님 |
| R5 | wiki가 raw를 잘못 요약 | 출처 필수 — sources로 raw 역추적, wiki/sources/가 검증 레이어 |

## 검증 방법 (구현 후)

1. `raw/`에 샘플 raw 3~5개 작성(겹치는 개념 포함, 예: RRF·hybrid-search·sqlite-vec).
2. `wiki-build` 실행 → `wiki/<concept>.md`들이 `[[wikilink]]`로 연결되고 `index.md`·`wiki/sources/` 생성 확인.
3. 재실행 → "변경 없음, 스킵"(멱등성) 확인.
4. raw 1개 수정 → 해당 개념 아티클만 갱신, `source_hashes` 변경 확인.
5. 아티클 1개 손수정 + 마커 제거 → 재빌드 후 보존 확인.
6. raw 1개에 의도적 오류(빈 파일 등) → `_log.md`에 스킵 기록되고 빌드 계속 확인.
7. `git diff`로 모든 변경이 working tree에 있고 복구 가능한지 확인.

## 참고 자료

- 전임 second-brain docs: `../../second-brain-project/docs/{insights,architecture,PRD}.md` (계승/회피 근거).
- 외부: Karpathy LLM Wiki 개념, `obsidian-llm-wiki-local`(olw) 3단계 파이프라인, Hermes Agent(hermes-agent.org).
