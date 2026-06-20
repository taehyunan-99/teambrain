# wiki 작업 가이드 (데이터 계층 — raw 입력 + wiki 산출)

이 저장소의 **진실 공급원**이다 — `raw/`(사람 입력)는 LLM이 읽기만 하고, `wiki/`(LLM 산출)는 `wiki-build` 스킬로만 생성한다. 손으로 직접 만들지 않는다.

<!--
첫 줄 미션은 /update에서 다듬는다. 핵심 함정: raw는 읽기 전용(사람 작성), wiki는 wiki-build 산출.
-->

<!--
== init 시점 안내 ==
이 가이드는 raw/(입력)와 wiki/(산출)를 함께 다룬다. 가이드 파일은 wiki/에 둔다.
가벼운 뼈대. HOW/HOW NOT/WHY는 /update에서. 변경감지·합성 메커니즘 상세는 wiki-build SKILL.md.
-->

## 1. WHAT — 이 모듈은 무엇을 하는가

데이터 계층. `raw/`는 팀이 던지는 원본 입력(슬랙·회의록·PR·인시던트, 자유 형식 마크다운), `wiki/`는 LLM이 raw를 합성한 개념 아티클(`[[wikilink]]`로 연결)이다. raw가 진실의 1차 출처이고, wiki는 그 합성·인덱스다. 둘 다 git + 마크다운 = 진실 공급원.

## 2. CONTENTS — 파일/디렉토리와 기술 스택

- `raw/<team>/<source>/*.md` — 원본 입력. `raw/{infra,settlement}/{slack,pr,transcripts}/`, `raw/slack/`, `raw/transcripts/`, `raw/pr/`, `raw/inbox/`(미분류 덤프), `raw/_archive/`(검색 제외).
- `wiki/<concept>.md` — LLM 생성 개념 아티클(frontmatter `sources[]`·`source_hashes[]`).
- `wiki/sources/<raw-slug>.md` — raw 1:1 소스 요약(raw↔개념 인덱스).
- `index.md`(루트) — 개념 카탈로그(MOC, 진입점). wiki-build가 마커 영역 자동 갱신.

기술 스택: 마크다운 + git (코드 아님). 변환은 `.claude/skills/wiki-build`.

## 3. HOW — 일반적인 수정은 어떻게 하는가

_(update 스킬에서 채워질 자리. wiki-build SKILL.md에 빌드 흐름 상세. `/update`로 인터뷰 진행)_

## 4. ⛔ HOW NOT — 시스템을 깨뜨리는 비명백한 함정 (중요)

_(update 스킬에서 채워질 자리. init은 비워둔다 — 단 공통 가드 "raw 직접 수정 금지"는 root AGENTS.md 참조)_

## 5. WHERE — 다른 모듈과의 의존성

- **피의존(약결합)**: `scripts/search/build_index.py`가 `raw/`·`wiki/sources/`를 색인 입력으로 읽는다(`_archive` 제외). `scripts/`(생성기)가 `raw/`에 더미를 쓴다.
- **경계/어댑터**: 변환 스킬 `wiki-build`(raw→wiki 합성·증분), frontmatter 스키마(raw: `created`/`tags` / wiki: `sources`/`source_hashes`).

## 6. WHY — 코드에 안 적힌 배경 지식

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 7. COMMANDS — 빌드/테스트/린트

_(빌드 명령 아님 — `wiki-build` 스킬로 raw→wiki 합성. 검색 색인은 scripts/search 참조.)_

## 8. ⚠️ LEARNED CAUTIONS — 학습된 주의사항

@./LEARNED_CAUTIONS.md

자세한 내용은 [LEARNED_CAUTIONS.md](./LEARNED_CAUTIONS.md) 참조.
