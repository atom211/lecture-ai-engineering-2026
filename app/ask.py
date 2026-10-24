"""第1回: 素のLLMに会話しながら質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールは使わず、同じ会話の履歴を保って質問を続けられる「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time
from dataclasses import dataclass

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


@dataclass
class AskResult:
    text: str
    elapsed_seconds: float
    input_tokens: int | None
    output_tokens: int | None


def ask(question: str, chat=None) -> AskResult:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
    started_at = time.perf_counter()
    response = chat.send_message(question)
    elapsed_seconds = time.perf_counter() - started_at
    usage = response.usage_metadata

    return AskResult(
        text=response.text,
        elapsed_seconds=elapsed_seconds,
        input_tokens=usage.prompt_token_count if usage else None,
        output_tokens=usage.candidates_token_count if usage else None,
    )


def chat_loop(chat, first_question: str) -> None:
    question = first_question
    while True:
        print(f"[質問] {question}\n")
        result = ask(question, chat)
        print(result.text)
        input_tokens = result.input_tokens if result.input_tokens is not None else "不明"
        output_tokens = result.output_tokens if result.output_tokens is not None else "不明"
        print(f"\n[応答時間] {result.elapsed_seconds:.2f}秒")
        print(f"[トークン] 入力: {input_tokens} / 出力: {output_tokens}")
        try:
            question = input("\n続けて質問できます（終了: exit）> ").strip()
        except EOFError:
            print()
            break
        if question.lower() in {"exit", "quit", "終了"}:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        chat_loop(chat, args.question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
