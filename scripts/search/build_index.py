"""Phase 5b 하이브리드 색인 구축.

raw/(_archive 제외) + wiki/sources/ 를 SQLite 단일 파일에 색인한다.
- BM25(FTS5): raw 원본만 (sources 요약은 길이정규화 편향 회피 위해 제외)
- 임베딩(sqlite-vec): raw + sources 모두 (C6의 wiki 합성 효과를 벡터 recall로 측정)

설계 근거: docs/phase5b-plan.md. 비평 must-fix 반영(vec0 id 명시, FTS5 content-less,
_archive 제외, python-frontmatter 파싱).
"""
import glob
import sqlite3
import struct
import sys

import frontmatter
import sqlite_vec
from sentence_transformers import SentenceTransformer

DB_PATH = "docs/index.db"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # 384d 다국어
DIM = 384


def collect_docs():
    """색인 대상 수집. (path, kind, body) 리스트. _archive 제외."""
    docs = []
    for f in sorted(glob.glob("raw/**/*.md", recursive=True)):
        if "/_archive/" in f:
            continue  # must-fix[12]: 검색 이론 참고문서 제외
        body = frontmatter.load(f).content.strip()  # must-fix[14]: 본문 HR 충돌 방지
        if body:
            docs.append((f, "raw", body))
    for f in sorted(glob.glob("wiki/sources/**/*.md", recursive=True)):
        body = frontmatter.load(f).content.strip()
        if body:
            docs.append((f, "source", body))
    return docs


def serialize(vec):
    """float 리스트를 sqlite-vec 바이너리(float32)로."""
    return struct.pack(f"{len(vec)}f", *vec)


def build():
    docs = collect_docs()
    raw_n = sum(1 for _, k, _ in docs if k == "raw")
    src_n = sum(1 for _, k, _ in docs if k == "source")
    print(f"색인 대상: raw {raw_n} + source {src_n} = {len(docs)}")

    print(f"임베딩 모델 로드: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    bodies = [b for _, _, b in docs]
    print(f"임베딩 생성 {len(bodies)}건...")
    embs = model.encode(bodies, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    db.executescript(
        """
        DROP TABLE IF EXISTS docs;
        DROP TABLE IF EXISTS fts;
        DROP TABLE IF EXISTS vec;
        CREATE TABLE docs(id INTEGER PRIMARY KEY, path TEXT UNIQUE, kind TEXT, body TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(path UNINDEXED, body, tokenize='unicode61');
        CREATE VIRTUAL TABLE vec USING vec0(id INTEGER PRIMARY KEY, embedding float[384]);
        """
    )

    for i, ((path, kind, body), emb) in enumerate(zip(docs, embs), start=1):
        db.execute("INSERT INTO docs(id, path, kind, body) VALUES (?,?,?,?)", (i, path, kind, body))
        # must-fix[13]: sources는 BM25(fts) 제외, 벡터만
        if kind == "raw":
            db.execute("INSERT INTO fts(rowid, path, body) VALUES (?,?,?)", (i, path, body))
        # must-fix[10]: vec0 id 명시 INSERT (rowid 자동부여 의존 금지)
        db.execute("INSERT INTO vec(id, embedding) VALUES (?,?)", (i, serialize(emb.tolist())))

    db.commit()
    fts_n = db.execute("SELECT count(*) FROM fts").fetchone()[0]
    vec_n = db.execute("SELECT count(*) FROM vec").fetchone()[0]
    print(f"완료: docs {len(docs)}, fts(BM25, raw만) {fts_n}, vec {vec_n} → {DB_PATH}")
    db.close()


if __name__ == "__main__":
    build()
