---
title: RRF (Reciprocal Rank Fusion)
tags: [search, ranking, fusion]
created: 2026-06-12
updated: 2026-06-12
sources:
  - raw/rrf-algorithm.md
  - raw/hybrid-search-overview.md
  - raw/sqlite-vec-local-vector-search.md
  - raw/bm25-sparse-retrieval.md
source_hashes:
  - 298e92fa5e55380157abd925f1cd52c7bef93b2f
  - b505bee25152e72bf643f2d2cae9e6c8f6a43a44
  - 6c4f08491efe0b5062ca764f2f3343350be3a941
  - 4079f79fe68d4f7b97adcb2fae00f23fc1949f0d
---

<!-- llmwiki:auto -->

## Summary
RRF(Reciprocal Rank Fusion)는 여러 검색 결과 리스트를 순위(rank)만으로 병합하는 알고리즘이다. `RRF_score(d) = Σ 1/(k + rank_i(d))` 공식을 사용하며(k=60이 기본값), 점수 스케일이 다른 BM25와 벡터 검색 결과를 정규화 없이 합산할 수 있어 Hybrid Search의 표준 결합 방식으로 쓰인다.

## Details
공식: `RRF_score(d) = Σ 1 / (k + rank_i(d))`
- `k=60`: 경험적 기본값, 낮은 순위 문서의 영향을 완화
- 점수 정규화 불필요: BM25 점수와 코사인 유사도의 스케일 차이를 순위로 흡수
- 이상치에 강함

[[hybrid-search]]에서 사용 예:
1. [[bm25]] 결과 리스트 → rank 추출
2. 벡터 검색([[sqlite-vec]]) 결과 리스트 → rank 추출
3. RRF 공식으로 합산 → 최종 순위

한계: 1위가 압도적인 경우에도 점수 크기 정보를 버림.

## Related
- [[hybrid-search]] — RRF를 결합 방식으로 사용하는 검색 패러다임
- [[bm25]] — RRF로 병합되는 sparse retrieval 결과의 출처
- [[sqlite-vec]] — RRF로 병합되는 dense retrieval 결과의 출처
