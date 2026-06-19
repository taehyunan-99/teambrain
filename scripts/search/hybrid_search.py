"""Phase 5b 하이브리드 검색 — BM25(FTS5) + 벡터 KNN(sqlite-vec) + RRF 병합.

설계: docs/phase5b-plan.md. top-N=100, RRF k=60, 미등재는 rank=N+1.
import해서 search(q, mode) 호출하거나 CLI로 직접 질의.
"""
import sqlite3
import struct
import sys

import sqlite_vec
from sentence_transformers import SentenceTransformer

DB_PATH = "docs/index.db"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_N = 100  # must-fix[4]: 50→100 상향
RRF_K = 60

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def connect():
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db


def bm25_search(db, q, n=TOP_N):
    """BM25 top-n path 리스트(순위순). FTS5 MATCH는 토큰 OR."""
    # 질의를 토큰 OR로 — 한 토큰이라도 맞으면 후보. 구두점/특수문자는 제거.
    terms = [t for t in "".join(c if c.isalnum() else " " for c in q).split() if t]
    if not terms:
        return []
    match = " OR ".join(terms)
    rows = db.execute(
        "SELECT path FROM fts WHERE fts MATCH ? ORDER BY rank LIMIT ?", (match, n)
    ).fetchall()
    return [r[0] for r in rows]


def vec_search(db, q, n=TOP_N):
    """벡터 KNN top-n path 리스트(거리순)."""
    emb = get_model().encode([q], normalize_embeddings=True)[0].tolist()
    blob = struct.pack(f"{len(emb)}f", *emb)
    rows = db.execute(
        """SELECT d.path FROM vec v JOIN docs d ON d.id = v.id
           WHERE v.embedding MATCH ? AND k = ? ORDER BY distance""",
        (blob, n),
    ).fetchall()
    return [r[0] for r in rows]


def rrf_merge(rankings, k=RRF_K, n=TOP_N):
    """여러 순위 리스트를 RRF로 병합. 미등재 문서는 rank=n+1(must-fix[4])."""
    all_docs = set()
    for r in rankings:
        all_docs.update(r)
    pos = [{d: i + 1 for i, d in enumerate(r)} for r in rankings]
    scores = {}
    for d in all_docs:
        s = 0.0
        for p in pos:
            rank = p.get(d, n + 1)  # 미등재 = n+1
            s += 1.0 / (k + rank)
        scores[d] = s
    return sorted(scores, key=lambda d: scores[d], reverse=True)


def search(q, mode="hybrid", top_k=10):
    """mode: 'bm25' | 'vec' | 'hybrid'. (path, bm25_rank, vec_rank) 튜플 top_k 반환."""
    db = connect()
    bm = bm25_search(db, q)
    vc = vec_search(db, q)
    db.close()
    bm_pos = {d: i + 1 for i, d in enumerate(bm)}
    vc_pos = {d: i + 1 for i, d in enumerate(vc)}
    if mode == "bm25":
        ranked = bm
    elif mode == "vec":
        ranked = vc
    else:
        ranked = rrf_merge([bm, vc])
    return [(d, bm_pos.get(d), vc_pos.get(d)) for d in ranked[:top_k]]


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("bm25", "vec", "hybrid") else "hybrid"
    q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else sys.argv[-1]
    print(f"[{mode}] {q}\n")
    for i, (path, br, vr) in enumerate(search(q, mode), start=1):
        print(f"{i:2}. {path}  (bm25={br}, vec={vr})")
