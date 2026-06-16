---
title: sqlite-vec
tags: [sqlite, vector-search, local]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/sqlite-vec-local-vector-search.md
  - raw/hybrid-search-overview.md
  - raw/bm25-sparse-retrieval.md
source_hashes:
  - 6c4f08491efe0b5062ca764f2f3343350be3a941
  - b505bee25152e72bf643f2d2cae9e6c8f6a43a44
  - 4079f79fe68d4f7b97adcb2fae00f23fc1949f0d
---

<!-- llmwiki:auto -->

## Summary
sqlite-vec는 SQLite의 로드 가능한 익스텐션으로, 외부 벡터 DB 서버 없이 SQLite 파일 안에서 벡터 유사도 검색을 제공한다. SQLite FTS5([[bm25]])와 같은 DB 파일에서 공존하므로 [[rrf]]로 결합하면 소규모/개인 용도의 [[hybrid-search]]를 서버 없이 구현할 수 있다.

## Details
특징:
- Zero-dependency: Weaviate, Qdrant, Pinecone 등 외부 서버 불필요
- SQLite FTS5와 같은 DB에서 공존 → 로컬 [[hybrid-search]] 구현 가능
- 소규모/중규모 용도 타깃 (수백만 벡터 이상에서 성능 저하)

사용 패턴 (Python):
```python
import sqlite_vec
db.enable_load_extension(True)
sqlite_vec.load(db)
db.execute("CREATE VIRTUAL TABLE embeddings USING vec0(embedding float[384])")
```

한계:
- IVF/HNSW 같은 ANN 인덱스 미지원 (정확한 KNN만)
- 수백만 벡터 규모에서 성능 저하

## Related
- [[hybrid-search]] — sqlite-vec + BM25(FTS5) + RRF로 구현 가능한 검색 패러다임
- [[bm25]] — 같은 SQLite DB에서 sparse 파트를 담당하는 FTS5 기반 검색
- [[rrf]] — sqlite-vec 벡터 검색 결과를 BM25 결과와 병합하는 알고리즘
