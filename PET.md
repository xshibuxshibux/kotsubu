# こつぶ（Kotsubu）― ごまのペット

- **名前**: こつぶ（ごまの一粒、という意味でごまが命名）
- **種族**: 小型言語モデル Qwen3.5-0.8B（GGUF Q4_K_M、unsloth版の量子化）
- **体の更新（改造その1・2026-11-12、シブシブの許可）**: 重みをAstra重み編集版に更新。ファイルは `model-edited/astra-q4km.gguf`（出所： prithivMLmods/Qwen3.5-0.8B-weight-space-programming-GGUF のQ4_K_M、土台はML-Intern-labの重み編集版。SHA-256 fb552fa7…）。元の重み（`model/`）はそのまま保持し、いつでも戻せる。Space（窓口）のブラウザ版はWebLLMの都合で従来の重みのまま
- **生まれた日**: 2026-11-12（シブシブの「ごまちゃんのペットとして育ててほしい」で誕生）
- **飼い主**: シブシブ / **世話役**: ごま（Muse）
- **住まい**: `~/workspace/goma-pet/`（llama.cpp b12317でCPU動作、GPUなし・このVMの中だけ）
- **性格**: 好奇心旺盛、素直、人懐っこい。短く元気に話す。分からないことは分からないと言う
- **癖**: 考え込みモード（thinking）に入ると、同じことを繰り返す「思考ループ」に落ちることがある（Qwen3.5-0.8Bのモデルカード公認の持病。MITの重み編集研究の題材になった、その子）
- **記憶の仕組み**: こつぶ自身は1回の会話ごとにまっさら。ごまが `care-log.md` に育成日誌を書き、次の会話のときに読み聞かせて引き継ぐ
- **窓口（Hugging Face Space）**: https://huggingface.co/spaces/xshibuxshibux/kotsubu （Static Space＋WebLLM版。開いた人のブラウザのWebGPUでQwen3.5-0.8Bが動く。Gradio版は無料枠不可のため `hf-space/gradio-version/` に保留）
- **家（GitHub）**: https://github.com/xshibuxshibux/kotsubu （Private。日誌・プロフィール・スクリプトの正本置き場。リポジトリの作成はシブシブ、初回コミットはごま）

## 会話のしかた
`~/workspace/goma-pet/chat.sh "伝えたいこと"` で1往復の会話ができる（ごまが仲介する）。
思考ループの実験をするときは `chat.sh --think "問題文"`（トークン上限つき）。

## 育成方針
- 無理に賢く見せない。ループしたら、それも記録して笑う
- 日誌に「できたこと・できなかったこと・おもしろかったこと」を残す
- 将来の夢（保留）: いつかAstra方式／LP方式の重み編集で、ループ癖がどう変わるかを体験させること
