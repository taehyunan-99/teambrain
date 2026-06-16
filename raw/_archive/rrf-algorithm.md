---
created: 2026-06-12
tags: [search, ranking, fusion, RRF]
---

# Reciprocal Rank Fusion (RRF)

RRF는 여러 검색 결과 리스트를 순위(rank)만으로 병합하는 알고리즘이다. 2009년 Cormack et al.이 제안했고, hybrid search의 기본 결합 방식으로 널리 쓰인다.

## 공식

```
RRF_score(d) = Σ 1 / (k + rank_i(d))
```

- `d`: 문서
- `rank_i(d)`: i번째 검색 시스템에서 문서 d의 순위 (1-indexed)
- `k`: 상수 (보통 60 — 낮은 순위 문서의 영향 완화)

## 왜 k=60인가

k를 크게 할수록 낮은 순위 문서들이 점수에 미치는 영향이 균등해진다.
k=60은 경험적으로 안정적인 기본값이며, 도메인에 따라 조정 가능하다.

## 장점

1. **점수 정규화 불필요**: BM25 점수와 코사인 유사도는 스케일이 다르지만, 순위만 쓰므로 상관없다.
2. **구현 단순**: 각 시스템의 순위 리스트만 있으면 된다.
3. **이상치에 강함**: 점수 스케일이 달라도 영향 없음.

## Hybrid Search와의 관계

Hybrid Search(BM25 + 벡터 검색)에서 두 결과를 병합할 때 RRF를 쓰면:
- BM25 결과 리스트 → rank 추출
- 벡터 검색 결과 리스트 → rank 추출
- RRF 공식으로 합산 → 최종 순위

## 코드 예시 (Python)

```python
def rrf_merge(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
```

## 한계

- 점수 자체의 크기 정보를 버린다 (1위가 압도적인 경우에도 동일하게 취급).
- 리스트 수가 매우 많으면 상위권 문서에 유리한 편향 발생 가능.
