"""Phase 6 Step 7 — Slack 슬랙봇 (Socket Mode).

채널에서 봇을 멘션하면 → wiki_qa 2단 파이프라인(검색→LLM 판단) → 답변.
Socket Mode라 공개 URL/포트 개방 불필요(우리가 슬랙에 WebSocket 연결을 건다).

준비물(.env):
  SLACK_BOT_TOKEN=xoxb-...   봇이 메시지 읽기/쓰기 (+ reactions:write 스코프 — 완료 ✅ 리액션용)
  SLACK_APP_TOKEN=xapp-...   WebSocket 연결(connections:write)

실행(프로젝트 루트에서): python3 scripts/llm/slack_bot.py
종료: Ctrl+C
"""

import logging
import os
import sys
import time

# 임베딩 모델 캐시가 있으므로 매 검색마다 HF 네트워크를 치지 않게 오프라인 강제.
# (import 전에 설정해야 적용됨 — 0원/오프라인 운영 취지와도 일치)
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# slack_bolt 내부 연결 로그까지 보이게(WebSocket 연결/이벤트 추적). 운영 디버깅에 필수.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("wiki-bot")

# wiki_qa, ollama_client 를 같은 폴더에서 import
sys.path.insert(0, os.path.dirname(__file__))
import wiki_qa  # noqa: E402
from ollama_client import is_up  # noqa: E402

load_dotenv()  # 프로젝트 루트의 .env 로드


def _require_token(name, prefix):
    """.env에서 토큰을 읽고 형식까지 검증. 없거나 형식이 틀리면 친절히 종료."""
    val = os.environ.get(name, "").strip()
    if not val:
        sys.exit(f"❌ {name} 가 .env 에 없습니다. .env.example 을 참고해 채우세요.")
    if not val.startswith(prefix):
        sys.exit(f"❌ {name} 형식이 이상합니다('{prefix}...' 이어야 함).")
    return val


BOT_TOKEN = _require_token("SLACK_BOT_TOKEN", "xoxb-")
APP_TOKEN = _require_token("SLACK_APP_TOKEN", "xapp-")

app = App(token=BOT_TOKEN)

# Slack 메시지 최대 길이 안전선(공식 4000자). 출처 블록 여유를 두고 자름.
MAX_LEN = 3500


def _basename(path):
    """긴 path 대신 파일명만 보여 가독성↑ (raw/slack/2024-10-30-x.md → 2024-10-30-x.md)."""
    return path.rsplit("/", 1)[-1]


def format_reply(result):
    """wiki_qa 결과(dict)를 슬랙 메시지로 조립.

    형식(볼드 `**` 금지 — Slack은 *별하나*가 볼드라 `**`는 그대로 노출됨):
      :books: 요약문
      • 핵심 사실
          _→ 근거파일명_
    각 사실의 근거는 인라인 `→`로 표시(하단 출처 블록은 중복이라 두지 않음).
    """
    if result.get("_error"):
        return "⚠️ " + result["summary"]          # 시스템 오류
    if not result["found"]:
        return "🤷 " + result["summary"]          # 정상적으로 못 찾음(환각 방지)

    # 1) 요약 헤더
    lines = [f":books: {result['summary']}"]

    # 2) 핵심 불릿 + 인라인 근거(파일명만, 기울임)
    points = result.get("points", [])
    if points:
        lines.append("")
        for p in points:
            lines.append(f"• {p['text']}")
            if p.get("source"):
                lines.append(f"    _→ {_basename(p['source'])}_")

    text = "\n".join(lines)
    if len(text) > MAX_LEN:
        text = text[:MAX_LEN] + "\n…(생략)"
    return text


@app.event("app_mention")
def handle_mention(event, say, client, logger):
    # 멘션 텍스트에서 "<@봇ID>" 부분을 떼고 실제 질문만 추출
    text = event.get("text", "")
    question = text.split(">", 1)[-1].strip() if ">" in text else text.strip()
    channel = event.get("channel")
    user = event.get("user")               # 질문자 — 완료 시 멘션해 알림
    mention_ts = event.get("ts")           # 원 멘션 메시지 — 완료 ✅ 리액션 대상
    thread_ts = event.get("thread_ts") or mention_ts  # 스레드로 답장

    if not question:
        say(text="질문을 같이 적어 멘션해 주세요. 예: `@Wiki Bot DB 커넥션 풀 고갈 어떻게 대응했어?`",
            thread_ts=thread_ts)
        return

    # 1) 즉시 "생각중" 임시 메시지 — LLM이 몇 초 걸리므로 UX용.
    #    이 메시지 게시가 실패하면(권한/네트워크) placeholder 없이 진행.
    placeholder = None
    try:
        placeholder = say(text="🔎 위키 검색하고 생각하는 중…", thread_ts=thread_ts)
    except Exception as e:
        logger.warning(f"placeholder 게시 실패: {e}")

    # 2) 2단 파이프라인 실행 — answer()는 예외를 던지지 않고 항상 dict 반환.
    #    그래도 만일을 대비해 최후 방어.
    log.info(f"멘션 수신: {question!r}")
    t0 = time.time()
    try:
        result = wiki_qa.answer(question)
        reply = format_reply(result)
        log.info(f"처리 완료: found={result.get('found')} "
                 f"sources={len(result.get('sources', []))} {time.time() - t0:.1f}s")
    except Exception as e:
        logger.exception("예상치 못한 처리 오류")
        reply = f"⚠️ 처리 중 알 수 없는 오류가 났어요: {e}"

    # 3) 임시 메시지를 실제 답변으로 교체. update 실패 시 새 메시지로 폴백.
    #    답변 머리에 질문자 멘션을 붙여 완료를 푸시 알림으로 전달.
    posted = reply if not user else f"<@{user}> {reply}"
    try:
        if placeholder and placeholder.get("ts"):
            client.chat_update(channel=channel, ts=placeholder["ts"], text=posted)
        else:
            say(text=posted, thread_ts=thread_ts)
    except Exception as e:
        logger.warning(f"답변 게시 실패, 재시도: {e}")
        try:
            say(text=posted, thread_ts=thread_ts)
        except Exception:
            logger.exception("답변 게시 최종 실패")

    # 4) 원 멘션 메시지에 완료 ✅ 리액션 — 부가 신호라 실패해도 답변엔 영향 없음.
    #    reactions:write 스코프가 없으면 여기서 조용히 실패한다(로그만).
    if mention_ts:
        try:
            client.reactions_add(channel=channel, timestamp=mention_ts, name="white_check_mark")
        except Exception as e:
            logger.warning(f"완료 리액션 실패(무시): {e}")


if __name__ == "__main__":
    if not is_up():
        sys.exit("❌ Ollama 서버가 꺼져 있습니다. 먼저 `ollama serve` 를 실행하세요.")
    log.info("임베딩 모델 warm-up 중…")
    wiki_qa.warm_up()  # 첫 멘션 지연 제거
    log.info("Ollama OK / Slack Socket Mode 연결 중… (Ctrl+C 종료)")
    try:
        SocketModeHandler(app, APP_TOKEN).start()
    except KeyboardInterrupt:
        log.info("봇을 종료합니다.")
    except Exception as e:
        sys.exit(f"❌ Slack 연결 실패: {e}")
