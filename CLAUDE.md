# Fractas — ブランチ `portal-radial`（ポータルで公開中のラジアル版）

> Claude Code はこのファイルを自動で読みます。最終更新: 2026-09-15

このブランチは **hiroakiishibashi.com で公開中のゲームそのもの**です。
`index.html` と `hi-game-lang.js` は、`hiroakiishibashi-web/games/fractas/game/` と1バイトも違いません
（タグ `portal-live-2026-09-11` が、2026-09-11 から公開中のもの）。

PINK では **`/Volumes/PINK/Development/Fractas-portal-radial/`**（このブランチ専用のフォルダ・git の worktree）で開いています。

- 引き継ぎの資料と道具は **`main`** にあります（このブランチには無い）。PINK なら `/Volumes/PINK/Development/Fractas/`（いつも `main`）の `CLAUDE.md` と `docs/`。
  GitHub: https://github.com/hiroakiishibashi/fractas/blob/main/docs/HANDOFF.md
- 直して公開する手順: `main` の `docs/RUNBOOK.md` の **R2**
- `main` は**正方形版＝別のゲーム**です。混ぜないこと。

## 🔴 破ってはいけない約束

1. `hi-game-lang.js` を書き換えない（ポータルの言語SDKの丸写し）。
2. ゲームから `preferred_lang` を書かない。
3. このフォルダは `portal-radial` 専用。`main` に切り替えない（`git switch main` をしない）。
4. 直したら、このフォルダで `git push origin portal-radial`。そのあと **`/Volumes/PINK/Development/Fractas`（main）で** `bash scripts/sync-to-portal.sh <ポータルのクローン>` を実行して写す（道具は main にしか無い）。
5. ポータルへの公開は hiroakiishibashi-web で「ブランチ → PR → main にマージ」。`npx wrangler deploy` と `git add -A` は使わない。
6. 本番を `?cb=毎回ちがう数字` で確かめてから「終わった」と言う。
