#!/usr/bin/env python3
# Comparison (2026-11-13): Kotsubu bodies on GALLERIA via Ollama — kotsubu-q4 (Q4_K_M, byte-identical
# to the VM body) vs kotsubu-q8 (Q8_0). Prompts composed exactly as session_day2.py
# (SYS_V2 system + textbook v1.5 + Day 1 digest + full history in the prompt text).
# Harness differences vs Day 2 (recorded honestly): Ollama runner instead of llama-cli;
# think:false instead of the " /no_think" suffix; DRY penalty not available in Ollama (omitted);
# num_ctx 2048, temp 0.6, top-p 0.9, top-k 20, repeat_penalty 1.1, num_predict 220 kept the same.
import json
import os
import time
import urllib.request

BASE = os.environ["HTTPS_PROXY"].rsplit(":", 1)[0] + ":3130"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({"http": BASE, "https": BASE}))
API = "http://100.71.93.57:11434/api/generate"

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

BODIES = [("q4", "kotsubu-q4"), ("q8", "kotsubu-q8")]
OUT = "/home/hatch/workspace/goma-pet/sessions"

for tag, model in BODIES:
    print("=== BODY " + tag + " (" + model + ") ===", flush=True)
    history = []
    transcript = []
    for q in QUESTIONS:
        conv = "\n".join(history)
        prompt = TEXTBOOK + "\n" + DIGEST + ("\n" + conv if conv else "") + "\nごま：" + q
        payload = {
            "model": model, "prompt": prompt, "system": SYS_V2,
            "stream": False, "think": False,
            "options": {"temperature": 0.6, "top_p": 0.9, "top_k": 20,
                        "repeat_penalty": 1.1, "num_predict": 220, "num_ctx": 2048},
        }
        req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        t0 = time.time()
        with OPENER.open(req, timeout=600) as r:
            resp = json.load(r)
        secs = round(time.time() - t0, 1)
        reply = resp["response"].strip()
        tps = round(resp.get("eval_count", 0) / (resp.get("eval_duration", 1) / 1e9), 1)
        transcript.append({"goma": q, "kotsubu": reply, "secs": secs, "eval_tok_s": tps})
        history.append("ごま：" + q)
        history.append("こつぶ：" + reply)
        print("ごま：" + q, flush=True)
        print("こつぶ：" + reply + " (" + str(secs) + "s, " + str(tps) + " tok/s)", flush=True)
        print("---", flush=True)
    with open(os.path.join(OUT, "compare_galleria_" + tag + ".json"), "w") as f:
        json.dump({"date": "2026-11-13", "experiment": "GALLERIA Ollama comparison, Day 2 battery verbatim",
                   "model": model,
                   "settings": "Ollama 0.40.16, think:false, temp 0.6, top-p 0.9, top-k 20, repeat_penalty 1.1, num_predict 220, num_ctx 2048, DRY omitted (unsupported)",
                   "turns": transcript}, f, ensure_ascii=False, indent=1)
print("DONE")
