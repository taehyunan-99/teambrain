---
created: 2026-06-12
tags: [search, sqlite-vec, vector-search, local]
---

# sqlite-vec — 로컬 벡터 검색

sqlite-vec는 SQLite의 로드 가능한 익스텐션으로, 외부 벡터 DB 서버 없이 SQLite 파일 안에서 벡터 유사도 검색을 제공한다. SQLite FTS5(BM25)와 같은 DB에서 공존할 수 있어, RRF 알고리즘과 결합하면 개인 노트/wiki 규모의 로컬 Hybrid Search를 서버 없이 구현할 수 있다.

## 특징

- **Zero-dependency**: Weaviate, Qdrant, Pinecone 등 외부 서버 불필요.
- **FTS5와 공존**: 같은 SQLite DB 파일에서 sparse(BM25/FTS5)와 dense(벡터)를 함께 둘 수 있어 로컬 Hybrid Search 구현 가능.
- **소규모/중규모 타깃**: 개인 노트·wiki 정도 규모에 적합.

## 사용 패턴 (Python)

```python
import sqlite_vec
db.enable_load_extension(True)
sqlite_vec.load(db)
db.execute("CREATE VIRTUAL TABLE embeddings USING vec0(embedding float[384])")
```

검색은 `embedding MATCH ?` + `ORDER BY distance` 형태로 KNN을 수행한다.

## 한계

- IVF/HNSW 같은 ANN 인덱스 미지원 → 정확한 KNN만 제공.
- 수백만 벡터 이상 규모에서는 성능 저하.

## Hybrid Search와의 관계

벡터 검색 결과 리스트와 BM25(FTS5) 결과 리스트를 RRF로 병합하면, 별도 인프라 없이 SQLite 하나로 hybrid search 파이프라인을 구성할 수 있다. 별도 노트(RRF, BM25, hybrid search) 참조.
