"""Phase 6 Step 6 — 검색→판단 2단 파이프라인 (CLI).

5b 결론(정답을 가르는 건 retrieval 아닌 reasoning)을 그대로 구현:
  1단 검색: hybrid_search가 top-N path를 넓게 떠줌 (recall 목표, top-1 아님)
  2단 판단: 후보 본문을 LLM 프롬프트에 주입 → found/answer/sources JSON으로 판단

검색은 후보 공급기, 판단은 LLM. demo_structured.py의 하드코딩 CANDIDATES를
실제 검색 결과로 바꾼 것이 핵심.

실행(프로젝트 루트에서): python3 scripts/llm/wiki_qa.py "질문"
"""

import json
import os
import sqlite3
import sys

# scripts/search 를 import 경로에 추가 (5b 검색 엔진 재사용)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "search"))
import hybrid_search  # noqa: E402

from ollama_client import chat  # noqa: E402

DB_PATH = "docs/index.db"
TOP_K = 30        # 후보 폭(5b 정답이 44~90위였으나 본문이 짧아 넓게 떠도 토큰 여유)
NUM_CTX = 16384   # top-30 본문(~14.5K 토큰) + 프롬프트 수용

SYSTEM_TMPL = """너는 Nimbus Pay 사내 위키 봇이다. 반드시 한국어로 답한다.
아래 [후보 문서]만을 근거로 답하라. 문서에 없는 내용은 절대 지어내지 마라.
여러 문서가 관련되면 종합하되, 근거가 된 문서만 sources에 넣어라.

반드시 다음 JSON 형식으로만 응답하라:
{{
  "found": true 또는 false,
  "answer": "한국어 답변. found=false면 '제공된 문서에서 답을 찾을 수 없습니다.'",
  "sources": ["근거가 된 문서 path만. found=false면 빈 배열"]
}}

[후보 문서]
{candidates}"""


def fetch_bodies(paths):
    """검색이 준 path들의 본문을 docs 테이블에서 조회. path→body 딕셔너리."""
    db = sqlite3.connect(DB_PATH)
    qmarks = ",".join("?" * len(paths))
    rows = db.execute(
        f"SELECT path, body FROM docs WHERE path IN ({qmarks})", paths
    ).fetchall()
    db.close()
    return {p: b for p, b in rows}


def build_candidates_block(hits):
    """검색 결과(path, br, vr) → 본문 포함 프롬프트 블록."""
    paths = [h[0] for h in hits]
    bodies = fetch_bodies(paths)
    lines = []
    for path, _br, _vr in hits:
        body = bodies.get(path, "").strip()
        lines.append(f"- ({path})\n  {body}")
    return "\n".join(lines)


def answer(question, mode="hybrid", top_k=TOP_K, verbose=False):
    # 1단: 넓은 검색
    hits = hybrid_search.search(question, mode=mode, top_k=top_k)
    if verbose:
        print(f"[1단 검색] {mode} top-{top_k} → {len(hits)}건 후보", file=sys.stderr)

    # 2단: 후보 본문을 system에 주입해 LLM 판단
    candidates = build_candidates_block(hits)
    system = SYSTEM_TMPL.format(candidates=candidates)
    out = chat(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        num_ctx=NUM_CTX,
        fmt="json",
    )
    result = json.loads(out)
    result["_searched"] = [h[0] for h in hits]  # 디버그: 검색이 뭘 떴는지
    return result


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "DB 커넥션 풀 고갈났을 때 어떻게 대응했어?"
    r = answer(q, verbose=True)
    print(f"\n질문: {q}\n")
    print(f"found:   {r['found']}")
    print(f"answer:  {r['answer']}")
    print(f"sources: {r['sources']}")
