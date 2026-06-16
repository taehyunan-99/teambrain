---
created: 2026-06-12
tags: [search, retrieval, hybrid]
---

# Hybrid Search 개요

Hybrid Search는 키워드 기반 검색(BM25 등 sparse retrieval)과 벡터 기반 의미 검색(dense retrieval)을 결합해 두 방식의 장점을 취하는 검색 패러다임이다.

## 왜 필요한가

- **Sparse(BM25)만 쓸 때**: 정확한 키워드 매칭에는 강하지만, 의미적으로 유사하지만 표현이 다른 문서를 놓친다.
- **Dense(벡터)만 쓸 때**: 의미 유사도는 잡지만, 특정 고유명사나 전문 용어 매칭이 약하다.
- 두 방식을 결합하면 recall과 precision을 동시에 높일 수 있다.

## 결합 방식

두 점수를 합칠 때는 스케일이 다를 수 있어서 단순 합산은 위험하다.
대표적인 결합 방법:

1. **RRF(Reciprocal Rank Fusion)**: 각 검색 결과의 순위만 사용해 병합. 점수 정규화 불필요.
2. **선형 결합**: `score = α * sparse_score + (1-α) * dense_score` — 정규화 필요.
3. **학습 기반 reranker**: Cross-encoder 등으로 재순위화.

실무에서는 RRF가 구현 단순하고 성능 안정적이어서 많이 쓰인다.

## 로컬 구현 옵션

- **sqlite-vec + BM25**: SQLite에 벡터 익스텐션 + FTS5를 함께 쓰면 외부 서버 없이 hybrid search 구현 가능.
- Elasticsearch/OpenSearch의 `hybrid` 쿼리도 동일 개념.

## 참고

- RRF 알고리즘 상세: 별도 노트 참조
- sqlite-vec으로 로컬 벡터 검색 구축: 별도 노트 참조
