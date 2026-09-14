# Fractas — このリポジトリで作業する前に

> Claude Code はこのフォルダで作業すると、このファイルを**自動で読みます**。
> くわしい説明は **[docs/HANDOFF.md](docs/HANDOFF.md)**（まずここ・15分）。
> 最終更新: 2026-09-15

## いまの状態（ここだけは必ず読む）

| | ラジアル版（ターン制の円形マッチ3） | 正方形版（2×2 で消す） |
|---|---|---|
| どこで公開中か | **hiroakiishibashi.com（ポータル）** | GitHub Pages だけ |
| 正本 | ブランチ **`portal-radial`** | ブランチ **`main`** |
| 公開中のファイル | `hiroakiishibashi-web/games/fractas/game/index.html` | https://hiroakiishibashi.github.io/fractas/ |
| PINK で直すフォルダ | **`/Volumes/PINK/Development/Fractas-portal-radial/`**（`portal-radial` 専用） | このフォルダ（`/Volumes/PINK/Development/Fractas/`・いつも `main`） |

**どちらをポータルに出すかは、オーナーの判断待ち**です（[docs/DECISIONS.md](docs/DECISIONS.md) の D1）。

## 🔴 破ってはいけない約束

1. **`main` をポータルへ写さない。** `main` は別のゲーム（正方形版）。写すと、公開中のゲームとランキングがまるごと別物に変わる。公開中の版を直すときは、`portal-radial` を開いた別フォルダ `/Volumes/PINK/Development/Fractas-portal-radial/` で直す（このフォルダで `git switch portal-radial` はしない）。
2. **`hi-game-lang.js` を書き換えない。** ポータルの言語SDK（`sdk/html/hi-game-lang.js`）の丸写し。1バイトでも違うと、ポータルの検査（`node tools/test-game-lang.mjs`）が落ちる。
3. **ゲームから `preferred_lang` を書かない。** サイト全体の言語設定。ゲームが書くと、ヘッダーや他のゲームまで変わる。
4. **ポータルへの公開は hiroakiishibashi-web で「ブランチ → PR → main にマージ」だけ。** `npx wrangler deploy` を直接叩かない（他の人の変更が消える）。`git add -A` を使わない（ファイルを名指しする）。
5. **作業の前に `git pull`。** 別の環境（旧 MacBook Pro ＋ Aider）も `main` に push している。
6. **秘密の値・個人のメールアドレスを書かない。** このリポジトリは公開（PUBLIC）。
7. **「直ったはず」で終わらせない。** `bash scripts/status.sh` と本番の確認（`?cb=` は毎回ちがう数字）で確かめてから報告する。

## 最初に打つコマンド

```bash
cd /Volumes/PINK/Development/Fractas
git pull
bash scripts/status.sh      # 読むだけ。何も書き換えない
```

## 迷ったら

| 知りたいこと | 読むもの |
|---|---|
| 全体像・経緯・仕組み | [docs/HANDOFF.md](docs/HANDOFF.md) |
| 手順（コピペで動く） | [docs/RUNBOOK.md](docs/RUNBOOK.md) |
| 実際に踏んだ罠 | [docs/PITFALLS.md](docs/PITFALLS.md) |
| 決まったこと・判断待ち | [docs/DECISIONS.md](docs/DECISIONS.md) |
| 新しいセッションに貼る文 | [docs/PROMPTS.md](docs/PROMPTS.md) |
| コードのどこに何があるか | [docs/CODEMAP.md](docs/CODEMAP.md) |
| 1枚で読む（スマホ） | [docs/handoff.html](docs/handoff.html) |
