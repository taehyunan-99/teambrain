---
type: source
of: raw/hybrid-search-overview.md
source_hash: b505bee25152e72bf643f2d2cae9e6c8f6a43a44
tags: [source]
---

## Summary
Hybrid Search는 BM25(sparse) 키워드 검색과 벡터(dense) 의미 검색을 결합해 recall과 precision을 동시에 높이는 검색 패러다임이다. 결합 방식으로 RRF가 구현 단순하고 안정적이어서 실무에서 많이 쓰이며, sqlite-vec + BM25(FTS5) 조합으로 외부 서버 없이 로컬 구현이 가능하다.

## Concepts
- Hybrid Search
- BM25
- RRF
- sqlite-vec
- sparse retrieval
- dense retrieval
