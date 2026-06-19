# Ollama 로컬 LLM — API 사용 기초

Phase 6 슬랙봇의 LLM 호출 계층. 로컬에서 도는 Ollama 서버를 HTTP로 부른다.
**클라우드 LLM과 호출 방식이 동일하므로(주소만 다름), 다른 프로젝트에도 그대로 재사용 가능.**

## 핵심 개념 한 줄

> Ollama = 내 맥에서 `localhost:11434`로 도는 HTTP 서버. 거기에 평범한 POST 요청을 보내 LLM을 부른다.

## 사전 준비

```bash
ollama serve &              # 서버 기동 (macOS 앱이 떠 있으면 생략 가능)
ollama pull gemma4          # 모델 받기 (e4b 기본, 9.6GB)
curl -s localhost:11434/api/version   # 헬스체크
```

## 두 엔드포인트

| 엔드포인트 | 입력 | 응답 키 | 용도 |
|---|---|---|---|
| `/api/generate` | `prompt` 문자열 | `response` | 단발 완성 |
| `/api/chat` | `messages` 배열(role별) | `message.content` | 대화·역할 고정 → **Phase 6가 사용** |

요청 시 `"stream": false`로 응답을 한 덩어리로 받는다(기본은 토큰 스트리밍).

## 파일

- **`ollama_client.py`** — 재사용 클라이언트. `chat()` / `generate()` / `is_up()`.
  - 모델명은 `MODEL` 상수 **한 곳**에서만 정의 → 교체는 이 한 줄, 또는 호출 시 `model=` 인자.
- **`demo_structured.py`** — 시스템 프롬프트 + `format=json` 구조화 출력 + "모르면 모른다(found=false)" 환각 방지 데모. Phase 6 2단 구조(검색→판단)의 2단 축소판.

```python
from ollama_client import chat
out = chat(
    messages=[
        {"role": "system", "content": "역할/규칙"},
        {"role": "user", "content": "질문"},
    ],
    num_ctx=8192,   # 후보 문서를 넣으면 기본 4096보다 키워야 안 잘림
    fmt="json",     # 응답을 유효 JSON으로 강제
)
```

## 알아둘 함정

- **첫 호출은 느리다** — 모델을 메모리에 올리는 `load_duration`(~4초)이 첫 호출에만 든다. 기본 5분 유휴 후 내려감 → `keep_alive`로 조절.
- **num_ctx 기본 4096** — Gemma4는 128K까지 가능하나 Ollama 기본이 4096이라, 검색 후보 본문 여러 개를 넣으면 조용히 잘린다. `options.num_ctx`로 키울 것.
- **환각 방지는 출력 규칙으로 강제** — system에 "주어진 문서 안에서만, 없으면 found=false"를 박고 `format=json`으로 구조를 가둬야 위키 봇이 지어내지 않는다.

## 모델 교체

```python
chat(msgs, model="gemma4:12b")   # 코드 수정 없이 인자만
# 또는 ollama_client.py 의 MODEL 상수 한 줄 변경
```

> ⚠️ `gemma4:12b`(2026-06 신규 태그)는 Ollama ≥ 최신 버전 필요. 0.24.0에선 `brew upgrade ollama` 후 사용. e4b는 0.24.0에서 동작.
