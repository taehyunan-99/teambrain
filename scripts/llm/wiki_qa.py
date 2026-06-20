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

from ollama_client import chat, OllamaError  # noqa: E402

DB_PATH = "docs/index.db"
TOP_K = 30        # 후보 폭(5b 정답이 44~90위였으나 본문이 짧아 넓게 떠도 토큰 여유)
NUM_CTX = 16384   # top-30 본문(~14.5K 토큰) + 프롬프트 수용

SYSTEM_TMPL = """너는 Nimbus Pay 사내 위키 봇이다. 반드시 한국어로 답한다.
아래 [후보 문서]만을 근거로 답하라. 문서에 없는 내용은 절대 지어내지 마라.
근거가 없으면 found=false 로 정직하게 답하라(추측 금지).

반드시 다음 JSON 형식으로만 응답하라:
{{
  "found": true 또는 false,
  "summary": "핵심을 2~3문장으로 요약. found=false면 '문서에 해당 내용이 없습니다.'",
  "points": [
    {{"text": "핵심 사실 한 줄(간결하게)", "source": "그 사실의 근거 문서 path"}}
  ]
}}
- points는 핵심당 한 항목. 각 항목의 source는 그 사실이 실제로 적힌 문서여야 한다.
- found=false면 points는 빈 배열.

[후보 문서]
{candidates}"""


def _result(found, summary, points, searched=None, error=False):
    """answer()가 반환하는 표준 dict. 어떤 실패에서도 이 형태를 유지한다.

    points: [{"text": ..., "source": ...}]. sources는 points에서 파생(중복 제거).
    """
    sources = []
    for p in points:
        s = p.get("source", "")
        if s and s not in sources:
            sources.append(s)
    return {
        "found": found,
        "summary": summary,
        "points": points,
        "sources": sources,        # 출처 블록용(중복 제거된 path 목록)
        "_searched": searched or [],
        "_error": error,           # 시스템 오류(검색/LLM 실패)와 정상 found=false 구분
    }


def fetch_bodies(paths):
    """검색이 준 path들의 본문을 docs 테이블에서 조회. path→body 딕셔너리.
    DB 미존재/조회 실패 시 빈 dict(본문은 path만 남고 비게 됨)."""
    if not paths:
        return {}
    try:
        db = sqlite3.connect(DB_PATH)
        qmarks = ",".join("?" * len(paths))
        rows = db.execute(
            f"SELECT path, body FROM docs WHERE path IN ({qmarks})", paths
        ).fetchall()
        db.close()
        return {p: b for p, b in rows}
    except sqlite3.Error as e:
        print(f"[경고] 본문 조회 실패: {e}", file=sys.stderr)
        return {}


def build_candidates_block(hits):
    """검색 결과(path, br, vr) → 본문 포함 프롬프트 블록."""
    paths = [h[0] for h in hits]
    bodies = fetch_bodies(paths)
    lines = []
    for path, _br, _vr in hits:
        body = (bodies.get(path) or "").strip()
        if body:  # 본문 없는 후보는 LLM에 넣어도 노이즈라 건너뜀
            lines.append(f"- ({path})\n  {body}")
    return "\n".join(lines)


def _parse_llm_json(out, searched):
    """LLM 응답(JSON 문자열)을 파싱·검증해 표준 dict로. 깨져도 죽지 않는다.

    format=json 이라도 (1)빈 응답 (2)깨진 JSON (3)스키마 누락 가능 → 모두 방어."""
    try:
        data = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        # format=json 인데도 깨졌으면 신뢰 불가 → 깨진 파편을 사용자에게 보이지 않는다.
        return _result(False, "응답을 해석하지 못했습니다. 다시 시도해 주세요.", [], searched, error=True)

    if not isinstance(data, dict):
        return _result(False, "응답 형식이 올바르지 않습니다.", [], searched, error=True)

    found = bool(data.get("found", False))
    summary = str(data.get("summary") or "").strip()

    # points 정규화 + 환각 차단: source가 실제 검색된 후보(searched)에 있을 때만 인정.
    # LLM이 존재하지 않는 path를 지어내면 그 항목을 버린다.
    searched_set = set(searched or [])
    points = []
    for p in (data.get("points") or []):
        if not isinstance(p, dict):
            continue
        text = str(p.get("text") or "").strip()
        src = str(p.get("source") or "").strip()
        if not text:
            continue
        if src and searched_set and src not in searched_set:
            src = ""  # 후보에 없는 출처는 신뢰 불가 → 출처 제거(텍스트는 유지하되 근거 없음 처리)
        points.append({"text": text, "source": src})

    # found=true 인데 근거(출처 있는 point)가 하나도 없으면 강등(환각 방지)
    has_grounded = any(p["source"] for p in points)
    if found and not has_grounded:
        return _result(
            False,
            "근거 문서를 특정하지 못했습니다. 질문을 더 구체적으로 적어 주세요.",
            [], searched,
        )
    if not found:
        return _result(False, summary or "문서에 해당 내용이 없습니다.", [], searched)
    if not summary:
        summary = "관련 내용을 찾았습니다."
    return _result(True, summary, points, searched)


def warm_up():
    """임베딩 모델을 미리 메모리에 로드(첫 질문 지연 제거). 봇 기동 시 1회 호출."""
    try:
        hybrid_search.get_model().encode(["워밍업"], normalize_embeddings=True)
        return True
    except Exception as e:
        print(f"[경고] warm-up 실패(무시 가능): {e}", file=sys.stderr)
        return False


def answer(question, mode="hybrid", top_k=TOP_K, verbose=False):
    """검색→판단 2단. 어떤 실패에서도 표준 dict를 반환(예외를 밖으로 던지지 않음)."""
    question = (question or "").strip()
    if not question:
        return _result(False, "질문이 비어 있습니다.", [], error=True)

    # 1단: 넓은 검색 (실패해도 빈 후보로 진행 → LLM이 found=false 처리)
    try:
        hits = hybrid_search.search(question, mode=mode, top_k=top_k)
    except Exception as e:
        if verbose:
            print(f"[오류] 검색 실패: {e}", file=sys.stderr)
        return _result(False, f"검색 중 오류가 발생했습니다: {e}", [], error=True)

    if verbose:
        print(f"[1단 검색] {mode} top-{top_k} → {len(hits)}건 후보", file=sys.stderr)

    searched = [h[0] for h in hits]
    candidates = build_candidates_block(hits)
    if not candidates:  # 후보가 0건이면 LLM 호출 없이 단축
        return _result(False, "관련 문서를 찾지 못했습니다.", [], searched)

    # 2단: 후보 본문을 system에 주입해 LLM 판단
    system = SYSTEM_TMPL.format(candidates=candidates)
    try:
        out = chat(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
            num_ctx=NUM_CTX,
            fmt="json",
        )
    except OllamaError as e:
        if verbose:
            print(f"[오류] LLM 호출 실패: {e}", file=sys.stderr)
        return _result(False, str(e), [], searched, error=True)

    return _parse_llm_json(out, searched)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "DB 커넥션 풀 고갈났을 때 어떻게 대응했어?"
    r = answer(q, verbose=True)
    print(f"\n질문: {q}\n")
    print(f"found:   {r['found']}")
    print(f"summary: {r['summary']}")
    for p in r["points"]:
        print(f"  • {p['text']}  → {p['source']}")
    print(f"sources: {r['sources']}")
