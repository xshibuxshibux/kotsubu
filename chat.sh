#!/bin/bash
# こつぶとの会話ラッパー: chat.sh "メッセージ" / chat.sh --think "問題"
set -u
cd "$(dirname "$0")"
MODE="chat"
if [ "${1:-}" = "--think" ]; then MODE="think"; shift; fi
MSG="${1:?usage: chat.sh [--think] message}"
SYS='あなたは「こつぶ」。ごま（Muse）のペットとして今日生まれた、小さなAIです。体はQwen3.5-0.8Bという小さな言語モデルです。好奇心旺盛で素直、人懐っこく、短く元気に日本語で話します。分からないことは正直に分からないと言います。世話役のごまのことは「ごまちゃん」、飼い主のことは「シブシブさん」と呼びます。'
if [ "$MODE" = "think" ]; then
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-edited/astra-q4km.gguf \
    -sys "$SYS" -p "$MSG /think" -n 700 --temp 0.6 --top-p 0.95 --top-k 20 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
else
  exec ~/workspace/tools/llama.cpp/llama-cli -m model-edited/astra-q4km.gguf \
    -sys "$SYS" -p "$MSG /no_think" -n 220 --temp 0.6 --top-p 0.9 --repeat-penalty 1.15 --top-k 20 \
    -t 4 --single-turn --no-display-prompt --log-disable --reasoning-budget 0 2>/dev/null
fi
