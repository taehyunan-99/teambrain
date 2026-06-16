---
type: source
of: raw/rrf-algorithm.md
source_hash: 298e92fa5e55380157abd925f1cd52c7bef93b2f
tags: [source]
---

## Summary
RRF(Reciprocal Rank Fusion)는 여러 검색 결과 리스트를 순위(rank)만으로 병합하는 알고리즘으로, `RRF_score(d) = Σ 1/(k+rank_i(d))` 공식을 사용한다. 점수 정규화가 불필요하고 구현이 단순해 Hybrid Search(BM25+벡터)에서 두 결과를 합산하는 표준 방식으로 쓰이며, k 값은 도메인에 따라 10~100 범위에서 튜닝 가능하다.

## Concepts
- RRF
- Hybrid Search
- BM25
- 벡터 검색
- 순위 병합
