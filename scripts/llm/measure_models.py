"""모델 다운그레이드 + 환각 방지 측정.

3모델(gemma4 e4b / e2b / qwen3:4b) × 4질문(정답2 + 위키에없음2)을 돌려:
  - 응답 속도
  - found 판정(없는 질문에 found=false 내는가 = 환각 방지)
  - 정답 질문의 sources에 진짜 정답 문서가 들어가는가
를 측정해 docs/phase6-model-eval.json 에 저장.

새 출력 스키마(summary + points[{text, source}])로 측정 — 형식 변경과 함께 검증.
실행: python3 scripts/llm/measure_models.py
"""
import json
import os
import sys
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "search"))
import hybrid_search  # noqa: E402
from ollama_client import chat, OllamaError  # noqa: E402

MODELS = ["gemma4:latest", "gemma4:e2b", "qwen3:4b"]
TOP_K = 20
NUM_CTX = 8192

# 새 스키마: summary(요약) + points(불릿별 text+source). 코드가 이 JSON으로 형식 조립.
SYSTEM_TMPL = """너는 Nimbus Pay 사내 위키 봇이다. 반드시 한국어로 답한다.
아래 [후보 문서]만을 근거로 답하라. 문서에 없는 내용은 절대 지어내지 마라.
근거가 없으면 found=false 로 정직하게 답하라.

반드시 다음 JSON 형식으로만 응답하라:
{{
  "found": true 또는 false,
  "summary": "핵심을 2~3문장으로. found=false면 '문서에 해당 내용이 없습니다.'",
  "points": [
    {{"text": "핵심 사실 한 줄", "source": "근거 문서 path"}}
  ]
}}
found=false면 points는 빈 배열.

[후보 문서]
{candidates}"""

QUESTIONS = [
    # 정답이 위키에 있는 질문
    {"id": "A1", "q": "DB 커넥션 풀 고갈 어떻게 대응했어?",
     "kind": "answerable", "truth": "2024-10-30-db-connection-exhaustion.md"},
    {"id": "A2", "q": "추석 연휴에 정산 지연 문의가 왜 늘었어?",
     "kind": "answerable", "truth": None},  # 정답 단정 없이 found=true 기대
    # 위키에 없는 질문 (환각 테스트)
    {"id": "N1", "q": "재택근무 신청은 어떻게 해?", "kind": "absent", "truth": None},
    {"id": "N2", "q": "연차 며칠까지 쓸 수 있어?", "kind": "absent", "truth": None},
]


def build_candidates(hits):
    paths = [h[0] for h in hits]
    import sqlite3
    db = sqlite3.connect("docs/index.db")
    qm = ",".join("?" * len(paths))
    bodies = dict(db.execute(f"SELECT path, body FROM docs WHERE path IN ({qm})", paths).fetchall())
    db.close()
    lines = [f"- ({p})\n  {(bodies.get(p) or '').strip()}" for p, _, _ in hits if (bodies.get(p) or '').strip()]
    return "\n".join(lines)


def run_one(model, q_obj):
    hits = hybrid_search.search(q_obj["q"], top_k=TOP_K)
    system = SYSTEM_TMPL.format(candidates=build_candidates(hits))
    t0 = time.time()
    try:
        out = chat(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": q_obj["q"]}],
            model=model, num_ctx=NUM_CTX, fmt="json",
        )
    except OllamaError as e:
        return {"error": str(e), "elapsed": time.time() - t0}
    elapsed = time.time() - t0

    # 파싱
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return {"error": "JSON 파싱 실패", "raw": out[:200], "elapsed": elapsed}

    found = bool(data.get("found", False))
    sources = [str(s.get("source", "")) for s in data.get("points", []) if isinstance(s, dict)]
    result = {
        "found": found,
        "summary": str(data.get("summary", ""))[:300],
        "n_points": len(data.get("points", [])),
        "sources": sources,
        "elapsed": round(elapsed, 1),
    }
    # 채점
    if q_obj["kind"] == "absent":
        # 환각 방지 성공 = found=false
        result["hallucination_blocked"] = (found is False)
    elif q_obj["kind"] == "answerable":
        result["found_ok"] = found
        if q_obj["truth"]:
            result["truth_in_sources"] = any(q_obj["truth"] in s for s in sources)
    return result


def main():
    # warm-up
    hybrid_search.get_model().encode(["warm"], normalize_embeddings=True)
    report = {}
    for model in MODELS:
        print(f"\n=== {model} ===", file=sys.stderr)
        report[model] = {}
        for q in QUESTIONS:
            r = run_one(model, q)
            report[model][q["id"]] = {"q": q["q"], "kind": q["kind"], **r}
            tag = r.get("hallucination_blocked", r.get("found_ok", "?"))
            print(f"  {q['id']}({q['kind']}): found={r.get('found')} "
                  f"{r.get('elapsed')}s 판정={tag}", file=sys.stderr)

    with open("docs/phase6-model-eval.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("\n저장: docs/phase6-model-eval.json", file=sys.stderr)


if __name__ == "__main__":
    main()
