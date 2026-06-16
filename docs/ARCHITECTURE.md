# Architecture — llmwiki

> 작성일 2026-06-12 · 상태: 설계 확정 · 결정 근거는 [ADR.md](ADR.md)

## 1. 설계 원칙 (second-brain 계승)

1. **가역성:** 모든 변경 = git working tree. 복구 = git. (review 루프를 없앤 근거)
2. **출처 필수:** 모든 wiki 아티클은 `sources`로 raw를 추적. 근거 없으면 안 만듦.
3. **조용한 실패 금지:** 실패/스킵/병합은 `_log.md`에 기록.
4. **마크다운 우선:** 임베딩/벡터/그래프DB 도입 충동이 들면 멈춘다 — 그게 second-brain을 죽인 길.

## 2. 계층 구조

```
저장 계층   : git + 마크다운(Obsidian vault)
입력 계층   : raw/ (사람 작성, 읽기 전용 입력) + raw/inbox/ (덤프)
산출 계층   : wiki/<concept>.md (개념 아티클) + wiki/sources/<raw>.md (소스 요약)
인덱스 계층 : index.md (개념 카탈로그 = 임베딩 인덱스 대체)
실행 계층   : Claude Code 스킬 (wiki-build / wiki-inbox / wiki-doctor)
변경감지    : frontmatter source_hash 대조 + git diff (state.db 없음)
```

## 3. 폴더 구조

```
wiki/                          (= 작업 디렉토리, 그 자체가 Obsidian vault)
├── raw/                       # 원본 입력 (사람 작성, LLM은 읽기만)
│   ├── inbox/                 # 미분류 덤프
│   └── *.md                   # 분류된 raw 노트
├── wiki/                      # LLM 생성 개념 아티클
│   ├── <concept-slug>.md      # 개념 1개 = 아티클 1개
│   └── sources/<raw-slug>.md  # raw 1:1 소스 요약 (raw↔개념 인덱스)
├── index.md                   # 개념 카탈로그 (MOC, 진입점)
├── _log.md                    # 빌드 감사 로그
└── .claude/skills/
    ├── wiki-build/SKILL.md
    ├── wiki-inbox/SKILL.md    # (v0.2)
    └── wiki-doctor/SKILL.md   # (v0.3)
```

## 4. 데이터 포맷

### Raw 노트 (사람 작성, 자유 형식)
frontmatter는 `created`, `tags`만 권장 (없어도 됨). 마찰 0이 목표.

### Wiki 개념 아티클 (LLM 생성, Karpathy 스타일)
- **frontmatter:** `title`, `tags`, `created`, `updated`, `sources[]`, `source_hashes[]`
- **본문:** `## Summary` / `## Details` / `## Related` (`[[wikilink]]`는 **본문에만**)
- **마커:** `<!-- llmwiki:auto -->` (자동생성물 표시 = 손수정 보호 기준)

### 소스 요약 (LLM 생성)
- **frontmatter:** `type: source`, `of: <raw 경로>`, `source_hash`, `tags`
- **본문:** `## Summary` / `## Concepts` (이 raw가 낳은 개념을 `[[..]]`로 나열)

> **Obsidian 함정 반영** (전임 insights.md 실측):
> - wikilink는 frontmatter에 **절대 안 넣음** (property 내 링크 따옴표 함정).
> - `tags`는 Obsidian 예약 property로 통일 (그래프뷰/태그검색 네이티브 연동).
> - text property는 마크다운 렌더 안 됨 → summary는 본문 `## Summary`로.
> - 파일명 금지문자 `\ / : * ? " < > |` → slug 정규화 (소문자 영문/숫자/하이픈).

## 5. 데이터 흐름 (wiki-build)

1. **변경 감지:** `git diff raw/` + source_hash 대조 → dirty raw 집합. 없으면 스킵 (멱등).
2. **소스 요약 갱신:** dirty raw 각각 → `wiki/sources/<slug>.md` 재작성, 개념 후보 추출.
3. **개념 합성:** 개념별로 기존 아티클이 있으면 **머지**, 없으면 신규. 손수정 마커 없으면 스킵+로그.
4. **wikilink 연결:** 본문 언급 개념을 `[[..]]`로. dangling은 `_log.md` 기록 (stub 자동생성 OFF).
5. **index.md 갱신:** 태그/주제별 그룹핑 재생성 (마커 영역만).
6. **frontmatter 위생:** `updated`/`source_hashes` 재기록.
7. **로그+보고:** 생성/갱신/스킵/실패를 `_log.md`에 append, 사용자에게 요약. **커밋은 안 함.**

## 6. 변경 감지 (state.db 없이, 3중)

1. **1차 git diff:** `git status --porcelain raw/` (MVP 빠른 경로).
2. **2차 source_hash ★기본:** 아티클 frontmatter `source_hashes` vs 현재 raw 해시 (`git hash-object`).
3. **3차 orphan prune:** raw 삭제 시 stale 아티클 → wiki-doctor가 아카이브 (삭제 대신).

> `git hash-object`가 이미 content hash를 제공하므로 별도 해시 함수/캐시 파일 **0줄**.

## 7. 에러 처리

- raw 1개 실패가 전체 빌드를 막지 않음 (try-skip-log).
- dangling wikilink: 로그만 (빈 페이지 양산 방지).
- orphan: 삭제 아니라 `wiki/_archive/`로 이동 (가역성).

## 8. 기술 스택

Claude Code 스킬 + Obsidian vault + git. 외부 의존 없음.
