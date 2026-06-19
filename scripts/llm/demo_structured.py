"""Step 4 데모: 시스템 프롬프트 + JSON 구조화 출력 + "모르면 모른다" 강제.

Phase 6 2단 구조의 축소판:
  - 검색이 떠줬다고 가정한 후보 문서들(CONTEXT)을 system 프롬프트에 끼워 넣고,
  - LLM에게 "이 안에서만 답하고, 없으면 found=false"를 JSON 스키마로 강제한다.

실행: python3 scripts/llm/demo_structured.py
"""

import json
from ollama_client import chat

# 검색(5b 엔진)이 top-N으로 떠줬다고 가정한 후보 문서들.
# 실제 Phase 6에선 이 문자열이 hybrid_search 결과 본문으로 채워진다.
CANDIDATES = [
    {
        "path": "raw/slack/2024-10-30-db-connection-exhaustion.md",
        "body": "정산 배치 중 DB 커넥션 풀이 고갈돼 결제 API가 5분간 503을 반환. "
                "원인은 배치가 풀을 반환하지 않고 점유. 핫픽스로 풀 size를 20→50으로 "
                "늘리고 배치에 명시적 close 추가. 항구 대책은 배치 전용 풀 분리.",
    },
    {
        "path": "raw/slack/2025-03-12-payout-delay-holiday.md",
        "body": "추석 연휴 직전 정산 지연 문의 폭증. 은행 영업일 기준이라 연휴 다음 "
                "영업일에 일괄 처리됨을 CS에 공지.",
    },
]

# JSON 스키마를 자연어로 명시한 시스템 프롬프트.
# 핵심 3요소: (1) 역할 고정 (2) "주어진 문서 안에서만" (3) 없으면 found=false
SYSTEM = """너는 Nimbus Pay 사내 위키 봇이다. 반드시 한국어로 답한다.
아래 [참고 문서]만을 근거로 답하라. 문서에 없는 내용은 절대 지어내지 마라.

반드시 다음 JSON 형식으로만 응답하라:
{
  "found": true 또는 false,   // 참고 문서에서 답을 찾았으면 true
  "answer": "한국어 답변. found=false면 '제공된 문서에서 답을 찾을 수 없습니다.'",
  "sources": ["근거가 된 문서 path만 배열로. found=false면 빈 배열"]
}

[참고 문서]
""" + "\n".join(
    f"- ({c['path']})\n  {c['body']}" for c in CANDIDATES
)


def ask(question):
    out = chat(
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        num_ctx=8192,   # 후보 문서가 들어가므로 기본 4096보다 키움
        fmt="json",     # 응답을 유효한 JSON으로 강제
    )
    # fmt="json"이면 out은 JSON 문자열 → 파싱해서 구조 확인
    return json.loads(out)


if __name__ == "__main__":
    # 케이스 A: 후보에 정답이 있는 질문
    print("=== 케이스 A: 정답이 후보에 있음 ===")
    a = ask("DB 커넥션 풀 고갈났을 때 핫픽스로 뭘 했어?")
    print(json.dumps(a, ensure_ascii=False, indent=2))

    # 케이스 B: 후보에 전혀 없는 질문 → found=false 나와야 함(환각 방지 검증)
    print("\n=== 케이스 B: 정답이 후보에 없음 (환각 방지 테스트) ===")
    b = ask("Slack 봇 배포 파이프라인은 어떻게 구성돼 있어?")
    print(json.dumps(b, ensure_ascii=False, indent=2))
