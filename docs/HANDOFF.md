# Fractas 引き継ぎ書

- 作成: 2026-09-15（Claude Code のプランが下がる前日に、このスレッドの内容をすべて書き残したもの）
- 読む人: Fractas の開発・保守を引き継ぐ人とAI（どの性能のモデルでも読めるように、短い文で書いています）
- 正本: この文書（`hiroakiishibashi/fractas` の `docs/HANDOFF.md`・ブランチ `main`）
- 写しの場所: この文書の「13. 資料の置き場所」

> **English summary.** Fractas is a small single-file HTML5 canvas puzzle game (game_id `fractas`).
> This repo holds two different games: the **radial turn-based match-3** that hiroakiishibashi.com
> serves (source of truth: branch `portal-radial`, tag `portal-live-2026-09-11`), and on `main` an
> unpublished **square-cluster** prototype that is only served on GitHub Pages. Never copy `main`
> to the portal without the owner's approval. Publishing to the portal = branch → PR → merge in
> `hiroakiishibashi/hiroakiishibashi-web` (GitHub Actions deploys). Start with `bash scripts/status.sh`.

---

## 0. 30秒でわかる現状

| 項目 | いま（2026-09-15） |
|---|---|
| ポータルで公開中 | **ラジアル版**（ターン制の円形マッチ3）… https://hiroakiishibashi.com/games/fractas/ |
| その正本 | このリポジトリのブランチ **`portal-radial`**（タグ **`portal-live-2026-09-11`** が公開中そのもの） |
| 公開中の版を直すフォルダ | **`/Volumes/PINK/Development/Fractas-portal-radial/`**（`portal-radial` を開いた別フォルダ。資料と道具は `/Volumes/PINK/Development/Fractas/`＝`main` にある） |
| `main` の中身 | **正方形版**（2×2 で消す、別のゲーム）。ポータルには出していない。GitHub Pages で公開中 … https://hiroakiishibashi.github.io/fractas/ |
| ランキング | 動いている（Supabase の `game_catalog` に登録済み・記録 65 件） |
| 言語 | 英語のみ。ポータルの言語SDKを配線済み（2026-09-11） |
| 判断待ち | どちらの版をポータルに出すか、ほか5件（[DECISIONS.md](DECISIONS.md)） |

いちばん大事なこと: **`main` は、ポータルで遊べるゲームとは別物です。**
公開中のゲームを直すときは `portal-radial` を直します。

---

## 1. 最初の10分でやること

1. このリポジトリを最新にする（`git pull`）。別の環境も push しているため。
2. `bash scripts/status.sh` を実行する。読むだけで、何も書き換えません。
3. 結果を「0. 30秒でわかる現状」と見比べる。違っていたら、誰かが更新しています。`git log --all --oneline | head -20` と、hiroakiishibashi-web の PR を確かめます。
4. 頼まれた作業を [RUNBOOK.md](RUNBOOK.md) の表から探す。
5. 迷ったら、手を動かす前にオーナーに聞く。質問には「おすすめの答え」を添えると早い。

---

## 2. Fractas とは

- ブラウザで遊ぶ、1ファイルの HTML5 ゲーム（`index.html` だけ。ビルドなし・外部ライブラリなし）。
- マウスでもタッチでも遊べる。音は Web Audio で作っている（音声ファイルなし）。
- オーナー（石橋 広在）が AI（Claude Code、ほかに Codex・Aider）と一緒に作ってきた。
- 始まり: `/Volumes/PINK/Development/Fractas.html`（元の試作。ファイルの中の表記は「Fractus - Prototype v0.25」）。2026-06-05 に製品化して、ポータルに載せた。
- 名前は **Fractas**。「Fractus」は古い表記なので使わない。
- ゲームの番号（game_id）は **`fractas`**。ランキングやURLはすべてこの名前。

---

## 3. 2つの版

### 3-1. ラジアル版（ポータルで公開中）

円い盤面のマッチ3です。12本の扇形（セクター）と、中心から外へ広がる輪（リング）でできています。

- **動かし方**
  - 中心のまわりをドラッグ → その輪が回る
  - 中心へ／外へドラッグ → その扇形がずれる
  - 同じ色が3つ以上つながると「予約」されて光る
- **ターン**: 盤面を動かす操作を **3回** すると、スキャナー（光の輪）が中心から外へ走って判定する。
  - 消せる組があれば → 消える → 点が入る → 補充される → 次の3手へ
  - 1組もなければ → **GAME OVER**
- 判定に1回成功するたびに、補充されるブロックの色が1つ増える（3色から始まり、最大6色）。
- 残りのターン数を英語で読み上げる（例: "2 turns left"）。
- 画面に出るのはスコアだけ。GAME OVER の画面をタップすると最初から。

### 3-2. 正方形版（`main`・ポータル未公開）

2026-07-27 に別の環境（旧 MacBook Pro ＋ Aider）で作り替えられた、**別のゲーム**です。

- 正方形のブロックが中心（コア）から 1.5 秒ごとに生えて、外へ押し広がる。
- ブロックを辺にそってドラッグして動かす。かたまりは、いつもつながっていないといけない。
- 同じ大きさの正方形が 2×2 に並ぶと消える。消えると中心のほうへ詰まる。
- どれかのブロックが外枠（中心から 8 マス）に届くと GAME OVER。
- ハイスコア・ミュート・プレイ回数を端末に保存する（`localStorage`）。
- ポータルと同じしくみでスコアを送る（`mode: 'square_cluster'`）。**点の桁がラジアル版とまったく違う**ので、同じランキングに混ぜると比べられない。

### 3-3. 2つを比べると

| | ラジアル版 | 正方形版 |
|---|---|---|
| 正本 | ブランチ `portal-radial` | ブランチ `main` |
| 行数（`index.html`） | 1,916 | 1,284 |
| 公開先 | ポータル | GitHub Pages |
| 送るスコアの `mode` | `turn3` | `square_cluster` |
| 1回消したときの点 | 10×個数 ＋ 連鎖ボーナス | 400×大きさ×連鎖 |
| 端末に保存するもの | なし | ハイスコア・ミュート・回数 |
| 判定のタイミング | 3手ごと | 2×2 がそろった瞬間 |

### 3-4. ラジアル版の未公開の改良（`main` の履歴に残っている）

正方形版に作り替える前に、ラジアル版へ2つの改良が入りました。**ポータルには出ていません。**

| コミット | 中身 |
|---|---|
| `ce073ce` | 古い Mac 向けの軽量化（描画の解像度を最大1倍に、背景のぼかしをやめる、光の影をやめる） |
| `d282cb6` | ハイスコアの保存・ミュートボタン・GAME OVER 画面の強化（成績の表示・「PLAY AGAIN」ボタン） |

出すかどうかは判断待ちです（[DECISIONS.md](DECISIONS.md) の D2）。手順は [RUNBOOK.md](RUNBOOK.md) の R3。

---

## 4. どこに何があるか（地図）

### 4-1. GitHub

| リポジトリ | 公開 | 中身 |
|---|---|---|
| `hiroakiishibashi/fractas` | **PUBLIC** | このリポジトリ。`main`＝正方形版、`portal-radial`＝公開中のラジアル版、資料と道具 |
| `hiroakiishibashi/hiroakiishibashi-web` | PUBLIC | ポータル（hiroakiishibashi.com）全体。`games/fractas/` にゲームのコピーとページ |
| `hiroakiishibashi/dev-notes` | private | 開発メモ。`15_fractas.md` と `03_projects_overview.md` の Fractas の章 |

### 4-2. このリポジトリの中（`main`）

| パス | 中身 |
|---|---|
| `index.html` | ゲーム本体（`main` では正方形版） |
| `hi-game-lang.js` | ポータルの言語SDKの丸写し。**書き換えない** |
| `assets/` | 2026-06 に撮ったサムネ（1280×720）とプレイ動画（mp4/webm・約15秒・当時のエンドレス版）、2026-09-15 に撮った**公開中のラジアル版**の動画 `fractas-radial-preview-2026-09.mp4`（約22秒） |
| `CLAUDE.md` | Claude Code が自動で読む約束 |
| `docs/` | この引き継ぎ資料一式（`codemap/` は機械生成の索引） |
| `scripts/status.sh` | 現状の確認（読むだけ） |
| `scripts/sync-to-portal.sh` | ポータルのクローンへ写す（安全装置つき・コミットはしない） |
| `scripts/gen-codemap.py` | コードの索引を作り直す |
| `scripts/build-handoff-html.py` | `docs/*.md` から1枚の HTML（`docs/handoff.html`）を作る |
| `GAME_DEVELOPMENT_HANDOVER.md` | 別の環境（旧Mac＋Aider）が書いたメモ。**一部古い**（ゲームの説明がラジアル版のまま・パスが別の Mac のもの）。消さずに残す（その環境の記録）が、書かれているパスと説明は使わない |
| `README.md` | 概要（英語）。本文はラジアル版の説明として正しい。**手順は RUNBOOK を使う** |

ブランチ `portal-radial` にあるのは、公開中の `index.html`・`hi-game-lang.js`・短い `CLAUDE.md` と、2026-07-26 時点の `README.md`・`assets/`・`.gitignore` です。**資料（`docs/`）と道具（`scripts/`）は `main` にしかありません。**
PINK では `portal-radial` を **`/Volumes/PINK/Development/Fractas-portal-radial/`**（git の worktree）で開いているので、`main` のフォルダで切り替える必要はありません（切り替えると `docs/` と `scripts/` が消えたように見える＝[PITFALLS.md](PITFALLS.md) の P19）。

### 4-3. ポータル（hiroakiishibashi-web）の中の Fractas

| パス | 中身 |
|---|---|
| `games/fractas/index.html` | Fractas のページ（枠・説明・TOP5・全ランキング・評価とコメント・言語の案内） |
| `games/fractas/game/index.html` | **公開中のゲーム**（`portal-radial` と同じ） |
| `games/fractas/game/hi-game-lang.js` | 言語SDKの同梱コピー |
| `games/fractas/CLAUDE.md` | このフォルダで作業するときの約束（自動で読まれる） |
| `docs/handoff/fractas/` | この引き継ぎ資料の公開版 |
| `js/user-ui.js` | ゲーム一覧 `GAMES` の `fractas`（50行目付近）と表示名（465行目付近） |
| `index.html` | トップページのカード（110行目付近） |
| `leaderboard/index.html` | ランキングのタブ（30行目付近） |
| `js/i18n/{en,ja,ko,es,pt,zh}.js` | 説明文 `game.fractas.desc` / `game.fractas.how`（6言語すべてある） |
| `js/continue.js` | 「続きから」の対象一覧 `KNOWN` |
| `assets/games/keyvisuals/variants/fractas-hero-b.jpg` | キービジュアル（トップ・About・その他のゲームに出る） |
| `assets/games/fractas.jpg`・`fractas-preview.{mp4,webm}` | 2026-06 の旧サムネと動画 |
| Supabase の `game_catalog` | `fractas`（enabled=true）。ランキングに投稿してよいゲームの一覧 |

### 4-4. PINK（外付けドライブ）

| パス | 中身 |
|---|---|
| `/Volumes/PINK/Development/Fractas/` | このリポジトリのクローン（`main`）。`.tmp-chrome-ui-check/`（43MB の Chrome の一時データ）と `outputs/` は無視する設定のゴミ |
| `/Volumes/PINK/Development/Fractas-portal-radial/` | **公開中の版を直すフォルダ**（ブランチ `portal-radial` の worktree。2026-09-15 作成） |
| `/Volumes/PINK/Development/Fractas.html` | 最初の試作（参考） |
| `/Volumes/PINK/Development/hiroakiishibashi-web/` | ポータルのクローン。⚠️ 2026-09-11 の時点で**不整合**（HEAD は 9/02 のまま、中のファイルだけ新しい）。ここでは作業しない → 新しくクローンする（[PITFALLS.md](PITFALLS.md) の P8） |
| `/Volumes/PINK/Development/_handover/2026-09-15/fractas/` | この資料の写し（HTML・状態の JSON つき） |
| `/Volumes/PINK/Development/tools/gamerec/` | 全ゲーム共用のプレイ動画の撮影道具 |
| `/Volumes/PINK/Development/.claude/launch.json` | 設定 `fractas`（ポート3459）＝このフォルダを手元で配信 |

### 4-5. URL

| URL | 中身 |
|---|---|
| https://hiroakiishibashi.com/games/fractas/ | 公開中のページ |
| https://hiroakiishibashi.com/games/fractas/game/ | ゲーム本体（iframe の中身） |
| https://hiroakiishibashi.com/leaderboard/ | ランキング（Fractas のタブ） |
| https://hiroakiishibashi.github.io/fractas/ | GitHub Pages（`main`＝正方形版） |
| https://github.com/hiroakiishibashi/fractas | このリポジトリ |
| https://hiroakiishibashi.com/docs/handoff/fractas/ | この資料の公開版 |

---

## 5. 公開中の版（ラジアル）がポータルで動くしくみ

```
ブラウザ
 └ hiroakiishibashi.com/games/fractas/        … ページ（games/fractas/index.html）
    ├ ランキング・評価とコメント・言語の案内（ポータルの js/*.js）
    └ <iframe> /games/fractas/game/            … ゲーム（games/fractas/game/index.html）
         ├ hi-game-lang.js で表示の言語を決める（いまは常に英語）
         └ スコアを postMessage で親へ送る ─→ 親は、ログイン中なら Supabase に保存
```

### 5-1. スコアが保存されるまで

**1.** ゲームの `reportScore()` が、親に `postMessage({type:'SCORE_UPDATE', game:'fractas', score, metadata})` を送る。
- 遊んでいる間は **10秒に1回まで**。同じ点は2回送らない。
- GAME OVER のときと、タブを離れたとき（`visibilitychange`・`pagehide`・`blur`）は必ず送る。
- `metadata` は `{ theme, mode:'turn3', turnsPerCheck:3, turns, checks, colorCount }`。
2. 親（`games/fractas/index.html`）が受け取る。**送り主が自分の iframe で、同じオリジンのときだけ**受け付ける（にせのスコアを弾く）。
**3.** ログインしていれば、`js/scores.js` の `saveScore('fractas', …)` が
- `plays` テーブルに1行を足す（これが本体）
- `scores` テーブルを上書きする（補助。失敗してもよい）
4. ランキングは `plays` から「1人1件のベスト」を集めて出す。

ログインしていない人のスコアは保存されません（ゲームはそのまま遊べます）。

### 5-2. ポータルの外で開いたとき

ゲームを直接開くと（iframe の中ではないとき）、ゲームは公式SDK（`https://hiroakiishibashi.com/sdk/html/hiroakiishibashi-sdk.js`）を読み込んで、直接保存しようとします。
ただし SDK は `scores` テーブルに書くので、**ポータルのランキング（`plays` を見る）には出ません**。SDK は、ランキングを `scores` で持っていたころの設計のままで、ポータルはのちに `plays`（全部のプレイの記録）を正にしました。バグではなく、古い設計の名残です（[PITFALLS.md](PITFALLS.md) の P11）。

### 5-3. 表示の言語

- `<head>` の最初で `hi-game-lang.js` を読み、`var LANG = (window.HiLang && HiLang.init({ id:'fractas', langs:['en'] })) || 'en';` で決める。
- Fractas は英語しか持っていないので、いつも `en`。
- ポータルで日本語などを選んでいる人には、ゲームの枠の下に「このゲームは English でご利用いただけます。」と出る（ポータル側の `js/game-lang-bridge.js` が出す）。
- 決まりの正本: https://hiroakiishibashi.com/docs/game-language-spec.md
- 検査: ポータルのクローンで `node tools/test-game-lang.mjs`（同梱コピーが SDK と1バイトも違わないかも見る）

### 5-4. ページがほかに持っている機能（ポータル側。ゲームは関係なし）

TOP5・全ランキング（上位／最近）・評価とコメント（`js/game-social.js`）・共有ボタン・全画面ボタン・「その他のゲーム」。
スクリーンショット（📷）は、ゲーム側が対応していません（仕様: `docs/game-screenshot-spec.md`・DECISIONS の D6）。

---

## 6. 正方形版（`main`）の状態

- 動く。GitHub Pages（`main` のルートをそのまま配信）で公開されている。
- ポータルと同じ配線（スコア送信・言語SDK）が入っているので、写せばポータルでも動く作りにはなっている。
- ただし、ポータルに出すには決めることがある（ランキングをどうするか・説明文・キービジュアル）。[DECISIONS.md](DECISIONS.md) の D1。
- 注意: 2×2 の判定は **大きさと位置だけを見ていて、色を見ていない**（`checkMatches()`）。意図かどうかは分からない（D6）。

---

## 7. 破ってはいけない約束（理由つき）

| # | 約束 | 理由（実際に起きたこと） |
|---|---|---|
| 1 | オーナーの了承なしに `main` をポータルへ写さない | `main` は別のゲーム。古い同期コマンドをそのまま打つと、公開中のゲームとランキングが入れ替わる |
| 2 | 公開中の版を直すときは `portal-radial` で直す | `main` には正方形版しかない |
| 3 | `hi-game-lang.js` を書き換えない | ポータルの SDK の丸写し。ずれると検査が落ちる |
| 4 | ゲームから `preferred_lang` を書かない | サイト全体の設定。書くと他のゲームまで変わる（Lumina で実際に起きた） |
| 5 | `npx wrangler deploy` を叩かない | 差分でなく丸ごと置き換える。古いツリーから出すと他の人の変更が消える（2026-08-19〜20 に何度も起きた） |
| 6 | `git add -A` / `git add .` を使わない | 同じツリーで他のスレッドも作業している。関係ないファイルまで入る |
| 7 | 作りかけをポータルの `main` に入れない | マージした瞬間に本番に出る |
| 8 | 古い PR の版でゲームを上書きしない | 2026-08-20、PR #3 の版を入れると演出の速さが4か所とも昔に戻るところだった |
| 9 | 秘密の値・個人のメールアドレスを書かない（例: API キー・トークン・パスワード・`.dev.vars` の中身・個人の Gmail） | 両方のリポジトリが公開。この資料も本番の URL で誰でも読める。公開用の Supabase の anon キーはページに載っているもので秘密ではないが、資料には貼らない |
| 10 | マネタイズ系のゲームサイト（Playgama・CrazyGames・itch.io など）への導線をサイトに置かない | オーナーの方針（2026-09-03）。Roblox だけは例外 |
| 11 | 「直ったはず」で終わらせない | 本番を `?cb=毎回ちがう数字` で確かめる。同じ数字だと古いキャッシュが返る |

---

## 8. よくある作業

手順はすべて [RUNBOOK.md](RUNBOOK.md) にあります（コピペで動くように書いています）。

| やりたいこと | 手順 |
|---|---|
| いまの状態を知る | R1 |
| 公開中のゲームを直して出す | R2 |
| 未公開のラジアル改良（ハイスコアなど）を入れる | R3（D2 の了承が要る） |
| 言語SDKが新しくなった | R4 |
| 日本語などの翻訳を足す | R5 |
| 正方形版をポータルに出す | R6（D1 の了承が要る） |
| GitHub Pages（正方形版）を直す | R7 |
| 本番を前の版に戻す | R8 |
| サムネ・プレイ動画を撮り直す | R9 |
| 直したのに本番が変わらない | R10 |

---

## 9. 確かめ方

| 何を | どうやって | 期待する結果 |
|---|---|---|
| 全体の状態 | `bash scripts/status.sh` | 公開中＝ラジアル版、`portal-radial` と完全一致、SDK と一致 |
| 言語の配線 | ポータルのクローンで `node tools/test-game-lang.mjs` | 「✅ 全部 pass」 |
| 公開中のゲームの中身 | `curl -sSL "https://hiroakiishibashi.com/games/fractas/game/?cb=$RANDOM$RANDOM" \| grep -c TURNS_PER_CHECK` | 1以上ならラジアル版 |
| 配信が本当に走ったか | `gh run list -R hiroakiishibashi/hiroakiishibashi-web --workflow=deploy.yml --limit 3` → `gh run view <番号> -R hiroakiishibashi/hiroakiishibashi-web` | 「配信」「本番の応答を確認」が success（skipped なら配信されていない） |
| 言語の案内 | ブラウザでポータルを日本語にして /games/fractas/ を開く | 枠の下に「このゲームは English でご利用いただけます。」 |
| ランキング | ログインして遊び、GAME OVER まで行く | TOP5 と「Your Score」が更新される |

---

## 10. オーナーの判断待ち

[DECISIONS.md](DECISIONS.md) に、選択肢と、それぞれを選んだときの手順・影響をまとめています。短く言うと:

- **D1** ポータルに出すのは、ラジアル版のままか、正方形版か
- **D2** ラジアル版の未公開の改良（`ce073ce`・`d282cb6`）を出すか
- **D3** このリポジトリを公開（PUBLIC）のままにするか
- **D4** ランキングに昔の版の高得点が残っている件をどうするか
- **D5** GitHub Pages で正方形版を公開し続けるか
- **D6** 急がない改善（翻訳・スクショ対応・撮影の台本・正方形版の色）

---

## 11. このスレッドだけが知っていたこと

記録（git・メモリ）に残りにくい話を書き残します。

- **README の古い「同期コマンド」は危ない。** 2026-09-11 に README へ警告を足しましたが、古い写し（dev-notes の 03 など）には警告なしの版が残っていました（2026-09-15 に直した）。見かけても使わず、`scripts/sync-to-portal.sh` を使います。
- **2つの版が分かれたいきさつ。** 2026-07-26 にこのリポジトリを private で作りました（最初のコミット `6a1e28a` はポータルと同じラジアル版）。同じ日の夜から翌未明に、別の環境（旧 MacBook Pro ＋ Aider）が改良を2つ push し、リポジトリを PUBLIC にして GitHub Pages を有効にし、正方形版に作り替えました。ポータルにはどれも出ていません。
- **公開中のゲームは `6a1e28a` ＋ 言語SDKの配線5行。** 2026-09-11 に Web スレッドから「正本とポータルが約2,300行食い違う」と言われて調べた結果です。どちらかが新しいのではなく、別のゲームでした。
- **ランキング1位（631,360点・2026-06-05）は最初期の版の点。** 当時は自動スキャナーが勝手に消していくエンドレス版で、何もしなくても点が入りました（60秒版では、放置で約1,270万点）。いまのターン制とは比べられません（D4）。
- **2026-06 のサムネと動画の撮り方。** canvas の `toBlob` でサムネを、`canvas.captureStream()`＋`MediaRecorder` で動画を撮り、使い捨ての node サーバに送って保存し、ffmpeg で mp4 にしました（RUNBOOK の R9）。2026-09-15 に、全ゲーム共用の撮影道具 `tools/gamerec/` に Fractas の台本（`games/fractas.mjs`）を作ったので、いまは `node record.mjs fractas` の1行で撮れます。
- **ヘッドレスのブラウザでは、iframe の中の `requestAnimationFrame` が止まることがある。** そのせいでタイマーが進まず、「壊れている」と誤診しかけました。ゲームを直接開いて確かめるか、`update()` を1回呼んで確かめます。
- **`npx serve` は `/game/index.html` を `/game` に書き換える。** 相対パスの `hi-game-lang.js` が 404 になります。ページごと手元で確かめるときは `python3 -m http.server` を使いました。
- **GitHub の GraphQL の回数制限にかかることがある**（2026-09-15 に発生）。`gh pr create` が失敗したら、REST（`gh api`）で代わりができます（RUNBOOK の R10-3）。
- **オーナーへの説明は、やさしい日本語・短い文で。** スマホ（iPhone・iPad）から読むことが多い。「推奨で」「進めてください」は「おすすめどおりに進めてよい」という意味。

---

## 12. 用語集

| ことば | 意味 |
|---|---|
| ポータル | hiroakiishibashi.com。オーナーのゲームサイト |
| 正本 | いちばん正しい元のファイル。写しと食い違ったら正本に合わせる |
| リング（輪） | ラジアル版の、中心から同心円に並ぶ段 |
| セクター（扇形） | ラジアル版の、12本に分かれた放射状の列 |
| スキャナー | 判定のときに中心から外へ走る光の輪 |
| 予約 | 3つ以上そろっていて、次の判定で消える予定のブロック（光る） |
| 判定 | 3手ごとにスキャナーが走り、消せる組を消すこと。1組もなければ GAME OVER |
| ラッパー | ゲームを iframe で囲む、ポータル側のページ（`games/fractas/index.html`） |
| `SCORE_UPDATE` | ゲームが親にスコアを知らせるメッセージの名前 |
| `plays` / `scores` | Supabase のテーブル。ランキングは `plays` を見る |
| `game_catalog` | ランキングに投稿してよいゲームの一覧（Supabase） |
| 言語SDK | `hi-game-lang.js`。ポータルの言語設定をゲームに伝える小さなファイル |
| マージ＝公開 | ポータルの `main` にマージすると、GitHub Actions が本番へ配信する |
| `?cb=` | キャッシュをよけるために、URL の最後に付ける毎回ちがう数字 |

---

## 13. 資料の置き場所（どれも同じ内容）

| 置き場所 | 形 | 使いどころ |
|---|---|---|
| `hiroakiishibashi/fractas` の `docs/`（`main`） | .md ＋ `handoff.html` | **正本** |
| https://hiroakiishibashi.com/docs/handoff/fractas/ | HTML ＋ .md | スマホ・クローンできない環境から |
| `/Volumes/PINK/Development/_handover/2026-09-15/fractas/` | .md ＋ HTML ＋ 状態の JSON | PINK だけで読める写し |
| dev-notes の `15_fractas.md` | .md（要約） | 開発メモの目次から |
| Claude のメモリ `project_fractas.md` | .md（要約） | Claude Code が自動で読む |
| claude.ai のアーティファクト | HTML | どの端末からでも |

食い違ったら、**正本（このリポジトリ）と実物（git・本番）** を正とします。
