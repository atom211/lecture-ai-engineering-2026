# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：第1回では不明である旨が出力されていたが、学習されたエージェントでは、学習データに基づいた回答として「基礎 / 実装 / 発展」の３つに分かれる旨が出力されていた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
def make_quiz(lecture: int) -> str:
    """指定した回の用語から1つを選び、確認問題と答えを返す。

    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
    """

## 宿題

- 取り組んだレベル：基礎
- やったこと：app/tools.py のツールの docstringの「用語を1つだけ入れる」を「まとめて入れる」に変更。
- 結果：「まとめて入れる」に変更すると、ツールの呼び出し回数が２回から１回へ減少。また、出力トークンは微増だが、入力トークンは300程度減少。
「用語を1つだけ入れる」：[usage] RunUsage(cost=Decimal('0.0008452'), details={'text_prompt_tokens': 1384}, input_text_tokens=1384, input_tokens=1384, output_tokens=172, requests=2, tool_calls=2)
「まとめて入れる」：[usage] RunUsage(cost=Decimal('0.0008488'), details={'text_prompt_tokens': 1071}, input_text_tokens=1071, input_tokens=1071, output_tokens=211, requests=2, tool_calls=1)
- 気づき・疑問：ツールの呼び出し回数を減少させることによりトークン使用量が減少するため、コスト低減に資すると理解しました。
