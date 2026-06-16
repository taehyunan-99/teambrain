---
type: source
of: raw/bm25-sparse-retrieval.md
source_hash: 4079f79fe68d4f7b97adcb2fae00f23fc1949f0d
tags: [source]
---

## Summary
BM25(Best Match 25)는 TF-IDF 기반 확률적 정보 검색 모델로 전통적 키워드 검색의 사실상 표준이다. SQLite FTS5가 BM25를 기본 랭킹 함수로 내장하며, Hybrid Search에서 sparse retrieval 파트를 담당해 RRF로 벡터 검색 결과와 병합된다.

## Concepts
- BM25
- TF-IDF
- sparse retrieval
- Hybrid Search
- RRF
- FTS5
- sqlite-vec
