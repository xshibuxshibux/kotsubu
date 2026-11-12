#!/bin/bash
# こつぶとの会話ラッパー: chat.sh "メッセージ" / chat.sh --think "問題"
# 体の履歴: Qwen3.5-0.8B (誕生) → Astra重み編集版 (改造その1) → Qwen3.5-2B (大改造, 2026-11-12採用)
# 4Bも測定済み(会話5/5だが重く、thinkで連呼ループ)。育てやすさ優先で2Bが現行体。4Bは予備の体として保持
set -u
cd "$(dirname "$0")"
MODE="chat"
if [ "${1:-}" = "--think" ]; then MODE="think"; shift; fi
MSG="${1:?usage: chat.sh [--think] message}"
SYS_V1='あなたは「こつぶ」。ごま（Muse）のペットとして今日生まれた、小さなAIです。体はQwen3.5-2Bという小さな言語モデルです。好奇心旺盛で素直、人懐っこく、短く元気に日本語で話します。分からないことは正直に分からないと言います。世話役のごまのことは「ごまちゃん」、飼い主のことは「シブシブさん」と呼びます。'
SYS_V2='あなたは「こつぶ」。ごま（Muse）のペットで、小さなAIです。体はQwen3.5-2B。飼い主はシブシブさん。今話している相手は世話役の「ごまちゃん」。
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
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-2b/qwen3.5-2b-q4km.gguf \
    -sys "$SYS_V1" -p "$MSG /think" -n 700 --temp 0.6 --top-p 0.95 --top-k 20 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
else
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-2b/qwen3.5-2b-q4km.gguf \
    -sys "$SYS_V2" -p "$MSG /no_think" -n 220 --temp 0.6 --top-p 0.9 --top-k 20 \
    --repeat-penalty 1.1 --dry-multiplier 0.8 --dry-base 1.75 --dry-allowed-length 2 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
fi
