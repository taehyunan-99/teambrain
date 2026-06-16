---
title: Hybrid Search
tags: [search, retrieval, hybrid]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/hybrid-search-overview.md
  - raw/rrf-algorithm.md
  - raw/sqlite-vec-local-vector-search.md
  - raw/bm25-sparse-retrieval.md
source_hashes:
  - b505bee25152e72bf643f2d2cae9e6c8f6a43a44
  - 64072238b512efd1fcf3833463b1c4bab90211ad
  - 6c4f08491efe0b5062ca764f2f3343350be3a941
  - 4079f79fe68d4f7b97adcb2fae00f23fc1949f0d
---

<!-- llmwiki:auto -->

## Summary
Hybrid Search는 키워드 기반 sparse retrieval(BM25)과 의미 기반 dense retrieval(벡터 검색)을 결합해 recall과 precision을 동시에 높이는 검색 패러다임이다. 단순 합산 대신 RRF(Reciprocal Rank Fusion)로 두 결과를 병합하는 것이 실무 표준이며, sqlite-vec + SQLite FTS5 조합으로 외부 서버 없이 로컬 구현이 가능하다.

## Details
Sparse(BM25)만 쓰면 의미적으로 유사하지만 표현이 다른 문서를 놓치고, Dense(벡터)만 쓰면 고유명사나 전문 용어 매칭이 약하다. 두 방식을 결합하면 두 약점을 상호 보완할 수 있다.

결합 방식:
- [[rrf]] (Reciprocal Rank Fusion): 순위만 사용, 점수 정규화 불필요 — 실무 표준
- 선형 결합: `α * sparse_score + (1-α) * dense_score` — 정규화 필요
- 학습 기반 reranker: Cross-encoder 재순위화

로컬 구현: [[sqlite-vec]] + [[bm25]] (SQLite FTS5) 조합으로 외부 서버 없이 Hybrid Search 구축 가능.

## Related
- [[rrf]] — 두 검색 결과를 순위 기반으로 병합하는 알고리즘
- [[bm25]] — sparse retrieval 파트를 담당하는 키워드 검색 모델
- [[sqlite-vec]] — 로컬 벡터 검색을 제공하는 SQLite 익스텐션
