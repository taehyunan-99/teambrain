"""Phase 5b 재측정 — 6질문 × {BM25, 임베딩, 하이브리드} recall@10.

5a 두 축 검증: 각 레버가 5a 어느 실패를 메우는지 분리 측정.
claim 한정: recall@10(정답을 top-10 후보에 넣는가)만 측정. end-to-end 아님(must-fix[0]).
채점: basename 비교(must-fix[15]). 정답 rank도 top-100 내에서 기록.
결과 → docs/phase5b-results.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from hybrid_search import bm25_search, connect, rrf_merge, vec_search  # noqa: E402

# 5a와 동일 truth. 각 질문의 5a 결과·임계 축 메모.
QUESTIONS = [
    {"id": "C1", "q": "로그 서버 디스크 꽉 찼던 적 있었나? 몇 퍼센트까지 갔었어?",
     "truth": ["raw/infra/2024-10-24-weekly.md", "raw/infra/slack/2024-10-23-infra-disk-cleanup.md"],
     "p5a": "correct(버팀)", "axis": "축1 토큰생존(로그서버)"},
    {"id": "C3", "q": "2025년 1월에 CI 빌드 간헐적으로 깨지던 문제 원인이 뭐였어?",
     "truth": ["raw/infra/slack/2025-01-22-infra-ci-flaky-build-chatter.md"],
     "p5a": "wrong(깨짐)", "axis": "축1 일반어흉내(flaky)"},
    {"id": "C4", "q": "추석 연휴 때 배포나 배치 일정 어떻게 챙겼어?",
     "truth": ["raw/2025-09-02-weekly.md", "raw/2025-09-09-weekly.md"],
     "p5a": "wrong(깨짐)", "axis": "변별어 없음"},
    {"id": "A4", "q": "코지홈 가맹점이 환불 관련해서 뭐 문의했었어?",
     "truth": ["raw/slack/2025-09-05-merchant-partial-refund-cs.md"],
     "p5a": "wrong(깨짐)", "axis": "축1 토큰부재(파일명에 cozyhome 없음)"},
    {"id": "C5", "q": "2024년 7월에 헬스체크 알람이 새벽에 오탐 떴던 적 있지? 그 원인이 뭐였어?",
     "truth": ["raw/infra/slack/2024-07-23-infra-healthcheck-alert-false-positive.md"],
     "p5a": "wrong(깨짐)", "axis": "축1 일반어흉내(timeout)"},
    {"id": "C6", "q": "2024년 10월에 결제 승인이 갑자기 느려졌던 적 있지? 그때 원인이랑 어떻게 잡았어?",
     "truth": ["raw/slack/2024-10-30-db-connection-exhaustion.md"],
     "p5a": "correct(버팀)", "axis": "축2 wiki합성"},
]


def basename(p):
    return os.path.basename(p)


def rank_of(ranked, truth_basenames):
    """ranked(path 리스트)에서 truth_basenames 중 하나가 처음 등장하는 1-indexed rank. 없으면 None."""
    for i, p in enumerate(ranked, start=1):
        if basename(p) in truth_basenames:
            return i
    return None


def measure():
    db = connect()
    rows = []
    for item in QUESTIONS:
        truth_bn = {basename(t) for t in item["truth"]}
        bm = bm25_search(db, item["q"])
        vc = vec_search(db, item["q"])
        hy = rrf_merge([bm, vc])
        modes = {"bm25": bm, "vec": vc, "hybrid": hy}
        result = {"id": item["id"], "q": item["q"], "p5a": item["p5a"], "axis": item["axis"]}
        for m, ranked in modes.items():
            r = rank_of(ranked, truth_bn)
            result[m] = {
                "recall@10": (r is not None and r <= 10),
                "rank": r,  # top-100 내 정답 위치(None=100밖)
            }
        rows.append(result)
    db.close()
    return rows


def fmt(rows):
    print(f"{'Q':4}{'5a':14}{'axis':28}{'bm25':14}{'vec':14}{'hybrid':14}")
    print("-" * 98)
    for r in rows:
        def cell(m):
            d = r[m]
            mark = "✓" if d["recall@10"] else "✗"
            return f"{mark}@{d['rank'] if d['rank'] else '>100'}"
        print(f"{r['id']:4}{r['p5a']:14}{r['axis']:28}{cell('bm25'):14}{cell('vec'):14}{cell('hybrid'):14}")
    # 요약
    for m in ["bm25", "vec", "hybrid"]:
        n = sum(1 for r in rows if r[m]["recall@10"])
        print(f"{m} recall@10: {n}/{len(rows)}")


if __name__ == "__main__":
    rows = measure()
    json.dump(rows, open("docs/phase5b-results.json", "w"), ensure_ascii=False, indent=2)
    print()
    fmt(rows)
    print("\n→ docs/phase5b-results.json")
