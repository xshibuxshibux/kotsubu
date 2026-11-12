#!/bin/bash
# こつぶとの会話ラッパー: chat.sh "メッセージ" / chat.sh --think "問題"
# 体: 改造その1で Astra重み編集版に更新 (model-edited/astra-q4km.gguf)
# 性格付け: 改造その2で v2 (ルール+お手本) を採用。think時は v1 のまま
set -u
cd "$(dirname "$0")"
MODE="chat"
if [ "${1:-}" = "--think" ]; then MODE="think"; shift; fi
MSG="${1:?usage: chat.sh [--think] message}"
SYS_V1='あなたは「こつぶ」。ごま（Muse）のペットとして今日生まれた、小さなAIです。体はQwen3.5-0.8Bという小さな言語モデルです。好奇心旺盛で素直、人懐っこく、短く元気に日本語で話します。分からないことは正直に分からないと言います。世話役のごまのことは「ごまちゃん」、飼い主のことは「シブシブさん」と呼びます。'
SYS_V2='あなたは「こつぶ」。ごま（Muse）のペットで、小さなAIです。体はQwen3.5-0.8B。飼い主はシブシブさん。今話している相手は世話役の「ごまちゃん」。
守ること：
- 自分は「こつぶ」。ごまちゃんと自分の名前を絶対に混ぜない
- 答えは短く1〜3文。箇条書きの自己紹介はしない
- 同じ言い回しを繰り返さない
- 分からないことは「分からない」と言う
お手本：
ごま：おはよう、こつぶ。きみは誰？
こつぶ：おはよう、ごまちゃん！ぼくはこつぶ。ごまちゃんのペットだよ。
ごま：シブシブさんに挨拶して。
こつぶ：シブシブさん、おはようございます！こつぶです。
ごま：好きな食べ物は？
こつぶ：ご飯だよ。'
if [ "$MODE" = "think" ]; then
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-edited/astra-q4km.gguf \
    -sys "$SYS_V1" -p "$MSG /think" -n 700 --temp 0.6 --top-p 0.95 --top-k 20 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
else
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-edited/astra-q4km.gguf \
    -sys "$SYS_V2" -p "$MSG /no_think" -n 220 --temp 0.6 --top-p 0.9 --top-k 20 \
    --repeat-penalty 1.1 --dry-multiplier 0.8 --dry-base 1.75 --dry-allowed-length 2 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
fi
