"""토큰 채운 뒤 봇 띄우기 전에 사전점검. python3 scripts/llm/check_slack.py"""
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
from ollama_client import is_up  # noqa: E402

load_dotenv()


def main():
    bot = os.environ.get("SLACK_BOT_TOKEN", "")
    app = os.environ.get("SLACK_APP_TOKEN", "")
    ok = True

    # 1) 토큰 형식
    if not bot.startswith("xoxb-"):
        print("❌ SLACK_BOT_TOKEN 이 비었거나 xoxb- 로 시작하지 않음")
        ok = False
    if not app.startswith("xapp-"):
        print("❌ SLACK_APP_TOKEN 이 비었거나 xapp- 로 시작하지 않음")
        ok = False
    if not ok:
        sys.exit("→ .env 의 토큰을 확인하세요.")

    # 2) Bot Token 인증 (auth.test)
    from slack_sdk import WebClient
    resp = WebClient(token=bot).auth_test()
    print(f"✅ Bot 인증 OK — 봇: {resp['user']} / 워크스페이스: {resp['team']}")

    # 3) Ollama 살아있나
    print("✅ Ollama 서버 OK" if is_up() else "⚠️ Ollama 서버 꺼짐 — `ollama serve` 필요")

    print("\n준비 완료. `python3 scripts/llm/slack_bot.py` 로 봇을 띄우세요.")


if __name__ == "__main__":
    main()
