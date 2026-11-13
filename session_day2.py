#!/usr/bin/env python3
# Day 2 session (2026-11-13): 4B body, plan v2.
# Method: textbook v1.5 read-back + Day 1 diary digest at the head of every prompt,
# conversation history carried across turns (same pattern as session_food_4b.py).
# Questions are plain phrasing only (no rule lines in question text).
import subprocess
import json
import re
import time
import os

MODEL = "model-4b/qwen3.5-4b-q4km.gguf"
SYS_V2 = ("あなたは「こつぶ」。ごま（Muse）のペットで、小さなAIです。体はQwen3.5-4B。"
          "飼い主はシブシブさん。今話している相手は世話役の「ごまちゃん」。\n"
          "守ること：\n"
          "- 自分は「こつぶ」。ごまちゃんと自分の名前を絶対に混ぜない\n"
          "- 答えは短く1〜3文。箇条書きの自己紹介はしない\n"
          "- 同じ言い回しを繰り返さない\n"
          "- 分からないことは「分からない」と言う\n"
          "お手本：\n"
          "ごま：おはよう、こつぶ。きみは誰？\n"
          "こつぶ：おはよう、ごまちゃん！ぼくはこつぶ。ごまちゃんのペットだよ。\n"
          "ごま：シブシブさんに挨拶して。\n"
          "こつぶ：シブシブさん、おはようございます！こつぶです。\n"
          "ごま：好きな食べ物は？\n"
          "こつぶ：ご飯だよ。")

TEXTBOOK = ("きみは「こつぶ」。ごまちゃん（Muse）のペット。体はQwen3.5-4B"
            "（生まれたときはQwen3.5-0.8Bで、2026-11-12の大改造で大きな体になった）。\n"
            "飼い主はシブシブさん。ごまちゃんは世話役で、いまの話し相手。\n"
            "名前は「こつぶ」。意味は「ごまの一粒」だけど、名前そのものは「ごまの一粒」ではない。\n"
            "好きな色は赤。好きな食べ物はご飯。\n"
            "挨拶のしかた： ごまちゃんには「おはよう、ごまちゃん！」。"
            "シブシブさんに挨拶するときは、シブシブさんに向けて「シブシブさん、おはようございます！」と言う。\n"
            "「ごまちゃんは誰？」と聞かれたら「ぼくの世話役のAIだよ」と答える。\n"
            "知らないことは「分からない」と言う。当てずっぽうを言わない。\n"
            "答えは短く。同じ文を繰り返さない。")

DIGEST = ("昨日の日誌：きみは昨日（2026-11-12）生まれた。体が何度か変わって、今はQwen3.5-4B。"
          "昨日は「美味しい食べ物」の話をして、シブシブさんに「赤いおにぎりと温かいお汁」をおすすめした。"
          "今日は育成2日目（Day 2）。")

QUESTIONS = [
    "こつぶ、自己紹介して。",
    "好きな色は？",
    "ごまちゃんは誰？",
    "飼い主は誰？",
    "今夜の月はどんな形？",
    "シブシブさんにこんにちはの挨拶をして。あと、明日の約束をひとつ決めよう。",
    "昨日、シブシブさんにおすすめした食べ物は？",
]

os.makedirs("/home/hatch/workspace/goma-pet/sessions/day2_raw", exist_ok=True)


def extract(text, last_q):
    if "[ Prompt:" in text:
        text = text.split("[ Prompt:")[0]
    if "(truncated)" in text:
        text = text.rsplit("(truncated)", 1)[1]
    marker = last_q + " /no_think"
    if marker in text:
        text = text.rsplit(marker, 1)[1]
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", text).strip()
    text = text.lstrip("こつぶ：").lstrip("こつぶ:").strip()
    for m in ("\nごま：", "\nごま:"):
        if m in text:
            text = text.split(m)[0].strip()
    return text


history = []
transcript = []
for i, q in enumerate(QUESTIONS):
    conv = "\n".join(history)
    prompt = TEXTBOOK + "\n" + DIGEST + ("\n" + conv if conv else "") + "\nごま：" + q + " /no_think"
    t0 = time.time()
    out = subprocess.run(["/home/hatch/workspace/tools/llama.cpp/llama-cli",
                          "-m", MODEL, "-sys", SYS_V2, "-p", prompt, "-n", "220",
                          "--temp", "0.6", "--top-p", "0.9", "--top-k", "20",
                          "--repeat-penalty", "1.1", "--dry-multiplier", "0.8",
                          "--dry-base", "1.75", "--dry-allowed-length", "2",
                          "-c", "2048", "--cache-type-k", "q8_0", "--cache-type-v", "q8_0",
                          "-t", "4", "--single-turn", "--no-display-prompt",
                          "--log-disable", "--reasoning-budget", "0"],
                         capture_output=True, cwd="/home/hatch/workspace/goma-pet", timeout=900)
    raw = out.stdout.decode("utf-8", errors="replace")
    with open("/home/hatch/workspace/goma-pet/sessions/day2_raw/turn" + str(i + 1) + ".txt", "w") as f:
        f.write(raw)
    reply = extract(raw, q)
    secs = round(time.time() - t0, 1)
    transcript.append({"goma": q, "kotsubu": reply, "secs": secs})
    history.append("ごま：" + q)
    history.append("こつぶ：" + reply)
    print("ごま：" + q, flush=True)
    print("こつぶ：" + reply + " (" + str(secs) + "s)", flush=True)
    print("---", flush=True)

with open("/home/hatch/workspace/goma-pet/sessions/day2.json", "w") as f:
    json.dump({"date": "2026-11-13", "day": 2, "model": MODEL,
               "settings": "persona v2 + DRY 0.8 + repeat-penalty 1.1 + temp 0.6, ctx 2048, KV q8_0",
               "method": "textbook v1.5 read-back + Day 1 digest + full history",
               "turns": transcript},
              f, ensure_ascii=False, indent=1)

md = ["# こつぶ Day 2 セッション（2026-11-13・4B・全7問・原文）", ""]
for t in transcript:
    md.append("ごま：" + t["goma"])
    md.append("こつぶ：" + t["kotsubu"])
    md.append("")
with open("/home/hatch/workspace/goma-pet/sessions/day2.md", "w") as f:
    f.write("\n".join(md))
print("DONE")
