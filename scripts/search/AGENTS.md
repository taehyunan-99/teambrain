# scripts/search 작업 가이드

{이 영역에서 LLM이 가장 자주 틀리는 무엇을 막는가 — 1문장. update에서 채울 자리.}

<!-- 첫 줄 미션은 /update의 "컨벤션 합의"에서 사용자와 확정한다. -->

<!--
== init 시점 안내 ==
가벼운 뼈대. WHAT/CONTENTS/WHERE/COMMANDS만 코드 스캔으로 채움. HOW/HOW NOT/WHY는 /update에서.
-->

## 1. WHAT — 이 모듈은 무엇을 하는가

하이브리드 검색 엔진(Phase 5b). `raw/`(+`wiki/sources/`)를 SQLite 단일 파일에 색인하고(FTS5 BM25 + sqlite-vec 384d 임베딩), BM25·벡터 결과를 RRF로 병합한다. 목표는 **top-1 정답이 아니라 top-100 후보 recall** — 판단은 LLM(scripts/llm)이 한다.

## 2. CONTENTS — 파일/디렉토리와 기술 스택

- `build_index.py` — 색인 구축. BM25는 raw 원본만, 임베딩은 raw+sources. `docs/index.db` 생성.
- `hybrid_search.py` — BM25(FTS5) + 벡터 KNN(sqlite-vec) + RRF 병합. `search(q, mode)` import 또는 CLI. TOP_N=100, RRF k=60.
- `measure_5b.py` — 5a 6질문 recall@10 측정기.
- `requirements.txt` — sentence-transformers, sqlite-vec, python-frontmatter

기술 스택: Python (sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2` 384d, sqlite-vec, python-frontmatter)

## 3. HOW — 일반적인 수정은 어떻게 하는가

_(update 스킬에서 채워질 자리. 작업 중 패턴이 정립되면 `/update`로 인터뷰 진행)_

## 4. ⛔ HOW NOT — 시스템을 깨뜨리는 비명백한 함정 (중요)

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 5. WHERE — 다른 모듈과의 의존성

- **피의존(강결합)**: `scripts/llm`의 `wiki_qa.py`가 `hybrid_search.search()`를 호출. **`search()` 시그니처·반환 구조 변경 시 wiki_qa 즉시 깨짐** → 변경 시 [`scripts/llm/AGENTS.md`](../llm/AGENTS.md) 함께 확인.
- **약결합**: `docs/index.db`(이 영역의 산출물), `raw/`·`wiki/sources/`(색인 입력 — [`wiki/AGENTS.md`](../../wiki/AGENTS.md))
- **경계/어댑터**: `MODEL_NAME`(임베딩 모델), `DB_PATH="docs/index.db"`

## 6. WHY — 코드에 안 적힌 배경 지식

_(update 스킬에서 채워질 자리. 사용자 결정 사항이므로 init은 비워둔다)_

## 7. COMMANDS — 빌드/테스트/린트

```bash
# 모두 프로젝트 루트에서 실행
python3 scripts/search/build_index.py   # 색인 재구축 → docs/index.db
python3 scripts/search/hybrid_search.py "질의"   # CLI 직접 질의
python3 scripts/search/measure_5b.py    # recall 측정
```

## 8. ⚠️ LEARNED CAUTIONS — 학습된 주의사항

@./LEARNED_CAUTIONS.md

자세한 내용은 [LEARNED_CAUTIONS.md](./LEARNED_CAUTIONS.md) 참조.
