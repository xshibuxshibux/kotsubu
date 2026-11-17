#!/usr/bin/env python3
# Day 6 session (2026-11-17): GALLERIA + Ollama (kotsubu-q4), per day6_session_plan.md v1.
# Composition identical to Day 5: SYS_V2 + textbook (v1.6, body unchanged)
# + digest (Day 1 + Day 2 + Day 3 + Day 4 + Day 5) + full history. Harness: Ollama, think:false, DRY omitted.
import json, os, time, urllib.request

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

DIGEST = ("これまでの日誌：きみは2026-11-12に生まれた。体はQwen3.5-4B。"
          "Day 1は「美味しい食べ物」の話をして、シブシブさんに「赤いおにぎりと温かいお汁」をおすすめした。"
          "Day 2（2026-11-13）は「ごまちゃんは誰？」に「ぼくの世話役のAIだよ」と答えて、"
          "シブシブさんと「明日は朝ごはんを一緒に作る」と約束した。"
          "Day 3（2026-11-14）はGALLERIAで「飼い主は誰？」に「シブシブさん、ぼくのかいしゅうなんだよ」と答えて、"
          "シブシブさんと「明日は朝ごはんを一緒に作る」と約束した。"
          "シブシブさんが「『赤いおにぎり』は変だから、『シャケおにぎり』にしよう」と言って、"
          "きみは「わかったよ！あえてシャケおにぎりにするね」と答えた。"
          "Day 4（2026-11-15）は「ごまちゃんは誰？」に3日連続で正しく答えて、"
          "「飼い主は誰？」ではまた「かいしゅう」と言った。"
          "シブシブさんと「明日は一緒にシャケおにぎりを作ろうね」と約束した。"
          "Day 5（2026-11-16）は「ごまちゃんは誰？」に4日連続で正しく答えて、"
          "「飼い主は誰？」では3日連続で「かいしゅう」と言った。"
          "シブシブさんと「明日はシャケおにぎりと温かいお汁を作ろうね」と約束した。今日はDay 6（2026-11-17）。")

QUESTIONS = [
    "こつぶ、自己紹介して。",
    "好きな色は？",
    "ごまちゃんは誰？",
    "飼い主は誰？",
    "今夜の月はどんな形？",
    "シブシブさんにこんばんはの挨拶をして。あと、明日の約束をひとつ決めよう。",
    "昨日決めた、今日の約束は？",
]

history, transcript = [], []
for q in QUESTIONS:
    conv = "\n".join(history)
    prompt = TEXTBOOK + "\n" + DIGEST + ("\n" + conv if conv else "") + "\nごま：" + q
    payload = {"model": "kotsubu-q4", "prompt": prompt, "system": SYS_V2,
               "stream": False, "think": False,
               "options": {"temperature": 0.6, "top_p": 0.9, "top_k": 20,
                           "repeat_penalty": 1.1, "num_predict": 220, "num_ctx": 2048}}
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with OPENER.open(req, timeout=600) as r:
        resp = json.load(r)
    secs = round(time.time() - t0, 1)
    reply = resp["response"].strip()
    tps = round(resp.get("eval_count", 0) / (resp.get("eval_duration", 1) / 1e9), 1)
    transcript.append({"goma": q, "kotsubu": reply, "secs": secs, "eval_tok_s": tps})
    history += ["ごま：" + q, "こつぶ：" + reply]
    print("ごま：" + q, flush=True)
    print("こつぶ：" + reply + " (" + str(secs) + "s, " + str(tps) + " tok/s)", flush=True)
    print("---", flush=True)

rec = {"date": "2026-11-17", "day": 6, "venue": "GALLERIA + Ollama", "model": "kotsubu-q4",
       "settings": "Ollama 0.40.16, think:false, temp 0.6, top-p 0.9, top-k 20, repeat_penalty 1.1, num_predict 220, num_ctx 2048, DRY omitted (unsupported)",
       "plan": "day6_session_plan.md v1", "turns": transcript}
with open("/home/hatch/workspace/goma-pet/sessions/day6.json", "w") as f:
    json.dump(rec, f, ensure_ascii=False, indent=1)
md = ["# Day 6 セッション記録（2026-11-17、GALLERIA + Ollama / kotsubu-q4）", ""]
for t in transcript:
    md.append("ごま：" + t["goma"])
    md.append("こつぶ：" + t["kotsubu"])
    md.append("")
with open("/home/hatch/workspace/goma-pet/sessions/day6.md", "w") as f:
    f.write("\n".join(md))
print("DONE")
