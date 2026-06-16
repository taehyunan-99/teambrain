---
created: 2026-06-12
tags: [search, BM25, sparse-retrieval, TF-IDF]
---

# BM25 — Sparse Retrieval의 기본

BM25(Best Match 25)는 TF-IDF 기반의 확률적 정보 검색 모델로, 전통적인 키워드 검색의 사실상 표준이다.

## 공식 (단순화)

```
BM25(d, q) = Σ IDF(t) * (tf(t,d) * (k1+1)) / (tf(t,d) + k1*(1 - b + b*|d|/avgdl))
```

- `tf(t,d)`: 문서 d에서 단어 t의 빈도
- `IDF(t)`: 역문서 빈도 (희귀 단어일수록 높음)
- `k1`, `b`: 하이퍼파라미터 (보통 k1=1.2~2.0, b=0.75)
- `|d|/avgdl`: 문서 길이 정규화

## SQLite FTS5에서의 BM25

SQLite의 FTS5(Full-Text Search 5)는 BM25를 기본 랭킹 함수로 사용한다.

```sql
CREATE VIRTUAL TABLE notes_fts USING fts5(title, body, tokenize='unicode61');

-- BM25 점수로 정렬 (음수 반환 → ORDER BY rank ASC)
SELECT *, rank FROM notes_fts WHERE notes_fts MATCH 'hybrid search' ORDER BY rank;
```

## Hybrid Search에서의 역할

BM25는 Hybrid Search의 sparse retrieval 파트를 담당한다:
- 정확한 용어 매칭에 강함 (코드 이름, 고유명사, 전문 용어).
- 의미 유사도는 벡터 검색(dense)이 보완.
- 두 결과를 RRF로 병합하면 Hybrid Search 완성.

## Dense vs Sparse 비교

| | Sparse (BM25) | Dense (벡터) |
|---|---|---|
| 장점 | 정확 매칭, 해석 가능 | 의미 유사도 |
| 단점 | 어휘 불일치 취약 | 전문 용어 취약 |
| 속도 | 빠름 | 임베딩 연산 필요 |
| 인프라 | FTS5(SQLite 내장) | sqlite-vec 등 |
