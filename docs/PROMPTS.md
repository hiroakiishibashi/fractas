# Fractas 新しいセッションに貼る文（PROMPTS）

> Claude Code（や、ほかのAI）を新しく始めるときに、そのまま貼って使う文です。
> `〈〉` のところだけ書き換えます。性能の低いモデルでも同じ入り方ができるように、読む順番・守ること・止まるところを必ず入れています。
> 最終更新: 2026-09-15

---

## 0. どの作業でも、まずこれ（入り方）

```
Fractas（hiroakiishibashi.com の円形パズル）の作業をします。手をつける前に、必ずこの順で読んでください。

1. /Volumes/PINK/Development/Fractas/CLAUDE.md        … 破ってはいけない約束
2. /Volumes/PINK/Development/Fractas/docs/HANDOFF.md  … 全体像（とくに「0. 30秒でわかる現状」）
3. cd /Volumes/PINK/Development/Fractas && git pull && bash scripts/status.sh の結果

守ること:
・main（正方形版）をポータルへ写さない。公開中の版はブランチ portal-radial（PINK では /Volumes/PINK/Development/Fractas-portal-radial で直す）
・hi-game-lang.js を書き換えない／ゲームから preferred_lang を書かない
・ポータルへの公開は hiroakiishibashi-web で「ブランチ → PR → main にマージ」。npx wrangler deploy と git add -A は使わない
・PINK の hiroakiishibashi-web は使わず、新しくクローンする（docs/RUNBOOK.md の R0-2）
・終わったら本番を ?cb=毎回ちがう数字 で確かめ、結果（コマンドの出力）を見せる

まず status.sh の結果と「0. 30秒でわかる現状」との違いを報告し、作業に入る前に計画を短く見せてください。

今日やってほしいこと: 〈ここに書く〉
```

PINK が見えない環境（クラウドなど）では、1〜2 のかわりにこちらを読んでもらいます:

- https://raw.githubusercontent.com/hiroakiishibashi/fractas/main/CLAUDE.md
- https://raw.githubusercontent.com/hiroakiishibashi/fractas/main/docs/HANDOFF.md
- まとめて1本: https://hiroakiishibashi.com/docs/handoff/fractas/fractas.md

---

## 1. 状態を点検するだけ（何も変えない）

```
〈0. の文〉
今日やってほしいこと: 何も変更せずに、Fractas の現状を点検してください。
・scripts/status.sh の結果
・本番のページ https://hiroakiishibashi.com/games/fractas/ が 200 で開くか
・ランキングの上位3件（読むだけ。docs/RUNBOOK.md の R10-5 の方法）
・docs/DECISIONS.md の判断待ちで、状況が変わったものはあるか
報告は、やさしい日本語・短い文で。
```

## 2. 公開中のゲーム（ラジアル版）を直す

```
〈0. の文〉
今日やってほしいこと: 公開中の Fractas（ラジアル版）で 〈直したいこと〉 を直して、公開してください。
・手順は docs/RUNBOOK.md の R2 のとおり（直すのは /Volumes/PINK/Development/Fractas-portal-radial ＝ portal-radial 専用フォルダ → push → /Volumes/PINK/Development/Fractas で scripts/sync-to-portal.sh → ポータルで PR → マージ）
・直す前に、どの関数・どの定数を触るかを docs/codemap/portal-radial.md で示して、計画を見せてください
・手元で遊んで確かめたこと、配信の結果、status.sh の結果を最後に見せてください
・main には触らないこと
```

## 3. 未公開のラジアル改良（ハイスコア・ミュート）を出す

```
〈0. の文〉
今日やってほしいこと: オーナーの了承が出たので（DECISIONS の D2＝A）、ラジアル版に ce073ce と d282cb6 を入れて公開してください。
・手順は docs/RUNBOOK.md の R3 → R2 の 3〜9
・ポータルの枠の中（縦長・スマホの幅）で、ミュートボタンと GAME OVER 画面が崩れないかを、スクリーンショットで見せてください
・preferred_lang は書かないこと（ハイスコアなどゲームだけのキーは書いてよい）
```

## 4. 翻訳を足す

```
〈0. の文〉
今日やってほしいこと: Fractas（ラジアル版）に 〈言語〉 の表示を足してください。
・決まりは https://hiroakiishibashi.com/docs/game-language-spec.md。手順は docs/RUNBOOK.md の R5
・langs には、本当に辞書がある言語だけを書く。辞書引きは ?? を使う（|| は使わない）
・遊んでいる途中の切り替えに対応できないなら live:false のまま。自動でリロードしない
・ポータルで JA／KO／EN に切り替えたときの表示を、それぞれ確かめて見せてください
```

## 5. 正方形版をポータルに出す

```
〈0. の文〉
今日やってほしいこと: オーナーの了承が出たので（DECISIONS の D1＝〈B または C〉、D4＝〈決まった方法〉）、正方形版をポータルに出してください。
・手順は docs/RUNBOOK.md の R6
・scripts/sync-to-portal.sh には --from main --i-have-owner-approval が要る
・説明文（6言語）・キービジュアル・ランキングの扱いを、作業の前に一覧にして見せてください
・終わったら docs/HANDOFF.md の「0. 30秒でわかる現状」を書き換えること
```

## 6. サムネ・プレイ動画を撮り直す

```
〈0. の文〉
今日やってほしいこと: 公開中の Fractas のサムネ（1280×720）と、15秒ほどのプレイ動画を撮り直してください。
・手順は docs/RUNBOOK.md の R9（まず gamerec: cd /Volumes/PINK/Development/tools/gamerec && node record.mjs fractas。うまくいかなければ R9-2）
・最初の3秒に、スキャナーが走って消える場面を入れる
・ファイルは PINK に置く（Mac 本体の Downloads に置きっぱなしにしない）。ポータルのキービジュアルは上書きせず、新しい版を足す
```

## 7. 本番がおかしいとき

```
〈0. の文〉
今日やってほしいこと: 本番の Fractas で 〈起きていること〉 が起きています。直す前に、まず原因を切り分けてください。
・docs/PITFALLS.md と docs/RUNBOOK.md の R10 を先に読む
・キャッシュ（?cb= は毎回ちがう数字）、配信のステップ（skipped でないか）、ポータルのコミットを順に確かめる
・原因が分かったら、直し方の案を（おすすめつきで）見せて、了承を待ってから直す
・急いで戻すときは RUNBOOK の R8
```

---

## 8. オーナーへの報告の型

```
【Fractas】〈何をしたか 1行〉
・結果: 〈本番の URL と確かめ方〉
・変えたファイル: 〈リポジトリとパス〉
・残っていること: 〈あれば〉
・判断してほしいこと: 〈あれば。おすすめを添える〉
```
