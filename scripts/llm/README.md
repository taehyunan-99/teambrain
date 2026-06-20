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

---

# Phase 6 — 위키 QA 슬랙봇 (검색→판단 2단)

5b 결론("정답은 retrieval 아닌 reasoning") 그대로: 검색이 후보를 넓게(top-30) 떠주고,
LLM이 본문을 읽고 판단한다. 검색은 후보 공급기, 판단은 LLM.

## 파일

- **`wiki_qa.py`** — 2단 파이프라인. `answer(q)` → `{found, summary, points[{text,source}], sources}`.
  어떤 실패에서도 예외를 던지지 않고 표준 dict 반환(봇 안 죽음).
- **`slack_bot.py`** — Socket Mode 봇. 멘션 → `wiki_qa.answer()` → "생각중" 후 답변 교체.
- **`check_slack.py`** — 토큰/Ollama 사전점검. 봇 띄우기 전 실행.
- **`measure_models.py`** — 모델 다운그레이드/환각 방지 측정기.

## 실행

```bash
ollama serve                          # (테스트 때만 켬 — 상시 켜두면 RAM 부담)
python3 scripts/llm/check_slack.py    # 사전점검(토큰·Ollama)
python3 scripts/llm/slack_bot.py      # 봇 기동 (Ctrl+C 종료)
```
슬랙 채널에서 `@Wiki Bot 질문` 으로 멘션.

## 환각 방지 (3중 + 검증)

위키에 없는 내용은 지어내지 않고 "문서에 해당 내용이 없습니다"로 답한다.
1. 후보 0건이면 LLM 호출 없이 단축.
2. system 프롬프트가 "문서에 없으면 found=false" 강제.
3. `points`의 `source`가 실제 검색된 후보에 없으면 그 출처를 버림(LLM이 path 지어내는 것 차단).
4. found=true인데 근거 있는 항목이 0이면 found=false로 강등.

> 측정(`docs/phase6-model-eval.json`): gemma4 e4b/e2b, qwen3:4b 3모델 모두
> 위키에 없는 질문 4/4 차단. **환각 방지는 모델 크기와 무관하게 작동.**

## 모델 선택 근거 (측정 기반)

| 모델 | 속도(정답질문) | 환각방지 | 정답 recall | 결론 |
|---|---|---|---|---|
| gemma4 e4b(기본) | 34~50s | ✅ | A1·A2 다 찾음 | 안정성 최고 → 채택 |
| gemma4 e2b | 8~22s(2배 빠름) | ✅ | A2 놓침(안전 실패) | 속도 우선 시 |
| qwen3:4b | 55~75s(느림) | ✅ | A1 놓침 | 부적합 |

> 속도(e4b 30~50s)는 로컬 모델의 비용일 뿐 아키텍처 한계가 아니다. `MODEL` 한 줄로
> 클라우드(Claude API 등)로 교체하면 수초로 줄어든다 — 운영은 클라우드, 데모는 로컬.

## 출력 형식

볼드(`**`) 금지 — Slack은 `*별하나*`가 볼드라 `**`는 그대로 노출된다.
`:books:` 요약 → `• 사실` + 들여쓴 `_→ 파일명_`(각 사실의 근거를 인라인으로).
하단 출처 블록은 인라인과 중복이라 두지 않는다.
LLM은 구조화 JSON(summary+points)만 내고, 슬랙 포맷은 코드(`format_reply`)가 조립한다.
