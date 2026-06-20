"""Ollama 로컬 LLM 클라이언트.

curl로 치던 `POST http://localhost:11434/api/chat` 호출을 requests로 감싼 얇은 래퍼.
다른 프로젝트에 이 파일만 복사해도 동작한다(의존성: requests).

핵심 설계:
- 모델명은 MODEL 상수 한 곳에서만 정의 → 교체는 이 한 줄만 바꾸면 끝.
- chat()이 기본. generate()는 단발용으로 같이 둠.
"""

import requests


class OllamaError(Exception):
    """Ollama 호출 실패. 호출부가 사용자에게 보여줄 수 있는 한국어 메시지를 담는다."""


# ─── 여기 한 줄만 바꾸면 모델 교체 (e4b → 12b 등) ───────────────
MODEL = "gemma4"          # 기본 e4b. 12b로 올리려면 "gemma4:12b"
HOST = "http://localhost:11434"
# ──────────────────────────────────────────────────────────────


def _post(path, payload, timeout):
    """공통 POST. requests 예외를 OllamaError(한국어)로 변환한다."""
    try:
        resp = requests.post(f"{HOST}{path}", json=payload, timeout=timeout)
    except requests.Timeout:
        raise OllamaError(f"Ollama 응답이 {timeout}초 안에 오지 않았습니다(모델이 느리거나 멈춤).")
    except requests.ConnectionError:
        raise OllamaError("Ollama 서버에 연결할 수 없습니다. `ollama serve` 가 떠 있는지 확인하세요.")
    except requests.RequestException as e:
        raise OllamaError(f"Ollama 요청 실패: {e}")

    if resp.status_code == 404:
        # 모델 미존재가 대표적(예: gemma4:12b 를 pull 안 함)
        raise OllamaError(f"모델 '{payload.get('model')}' 을(를) 찾을 수 없습니다. `ollama pull` 했는지 확인하세요.")
    if not resp.ok:
        raise OllamaError(f"Ollama HTTP {resp.status_code}: {resp.text[:200]}")
    try:
        return resp.json()
    except ValueError:
        raise OllamaError("Ollama 응답이 JSON이 아닙니다(서버 비정상).")


def chat(messages, model=MODEL, num_ctx=8192, temperature=0.2, fmt=None, timeout=120):
    """대화형 호출. curl의 /api/chat 과 1:1 대응.

    messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
    num_ctx:  컨텍스트 토큰 한도. Ollama 기본은 4096이라 후보 문서 여러 개를
              넣으면 잘린다 → Phase 6는 넉넉히 키운다. (Gemma4는 128K까지 가능)
    temperature: 낮을수록 결정적(사실 대조용은 낮게).
    fmt:      "json"을 주면 응답을 유효한 JSON으로 강제(구조화 출력).
    반환:     생성된 문자열(message.content).
    raises:   OllamaError (연결/타임아웃/모델없음/응답형식)
    """
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,                       # 응답을 한 덩어리로 받음
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature,
        },
    }
    if fmt:
        payload["format"] = fmt                # "json" 등

    data = _post("/api/chat", payload, timeout)
    try:
        return data["message"]["content"]      # curl에서 본 그 경로
    except (KeyError, TypeError):
        raise OllamaError("Ollama 응답에 message.content 가 없습니다(스키마 예상과 다름).")


def generate(prompt, model=MODEL, num_ctx=8192, temperature=0.2, timeout=120):
    """단발 호출. curl의 /api/generate 와 대응. 응답은 response 키. raises OllamaError."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": temperature},
    }
    data = _post("/api/generate", payload, timeout)
    try:
        return data["response"]
    except (KeyError, TypeError):
        raise OllamaError("Ollama 응답에 response 가 없습니다(스키마 예상과 다름).")


def is_up():
    """서버 살아있는지 헬스체크. Phase 6 봇 기동 시 사용."""
    try:
        requests.get(f"{HOST}/api/version", timeout=3).raise_for_status()
        return True
    except requests.RequestException:
        return False


if __name__ == "__main__":
    # 스모크 테스트: python3 ollama_client.py
    assert is_up(), "Ollama 서버가 떠 있지 않다. `ollama serve` 먼저."
    print("서버 OK:", MODEL)
    out = chat([
        {"role": "system", "content": "너는 Nimbus Pay 위키 봇이다. 한 문장으로만 답한다."},
        {"role": "user", "content": "너는 누구야?"},
    ])
    print("응답:", out)
