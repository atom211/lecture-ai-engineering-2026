from app.ask import ask, chat_loop


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        usage = type("Usage", (), {"prompt_token_count": 12, "candidates_token_count": 7})()
        return type("Response", (), {"text": f"回答: {question}", "usage_metadata": usage})()


def test_ask_sends_question_to_existing_chat():
    chat = FakeChat()

    result = ask("最初の質問", chat)

    assert result.text == "回答: 最初の質問"
    assert result.elapsed_seconds >= 0
    assert result.input_tokens == 12
    assert result.output_tokens == 7
    assert chat.questions == ["最初の質問"]


def test_chat_loop_keeps_sending_questions_to_same_chat(monkeypatch, capsys):
    chat = FakeChat()
    questions = iter(["続けて質問", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    chat_loop(chat, "最初の質問")

    assert chat.questions == ["最初の質問", "続けて質問"]
    output = capsys.readouterr().out
    assert "回答: 続けて質問" in output
    assert "[応答時間]" in output
    assert "[トークン] 入力: 12 / 出力: 7" in output