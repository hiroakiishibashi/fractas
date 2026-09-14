# Fractas 踏んだ罠（PITFALLS）

> 実際に起きたこと・起きかけたことだけを書いています。「症状 → 原因 → どうするか」の順です。
> 最終更新: 2026-09-15

| # | ひとことで | いつ |
|---|---|---|
| P1 | 同期コマンドで別のゲームに入れ替わる | 2026-09-11 に発見 |
| P2 | 古い PR の版で演出が巻き戻る | 2026-08-20 |
| P3 | 言語SDKのコピーがずれて検査が落ちる | ずっと |
| P4 | ゲームが `preferred_lang` を書いてしまう | 2026-09-10（Lumina） |
| P5 | `wrangler deploy` で他の人の変更が消える | 2026-08-19〜20 |
| P6 | 直したのに古い内容が見える（キャッシュ） | ずっと |
| P7 | PINK で git が `Operation not permitted` | 2026-08-29 |
| P8 | PINK のポータルのクローンが不整合 | 2026-09-11 |
| P9 | 手元の `npx serve` で SDK が 404 | 2026-09-11 |
| P10 | ヘッドレスでタイマーが進まない | 2026-06-06 |
| P11 | ポータルの外で遊んだ点がランキングに出ない | 2026-06-06 |
| P12 | ランキングに昔の版の点が混ざる | 2026-06〜 |
| P13 | Actions が緑なのに配信されていない | 2026-08-20 |
| P14 | `gh pr create` が回数制限で失敗 | 2026-09-15 |
| P15 | 手元で `/cdn-cgi/trace` が 404 | 2026-09-11 |
| P16 | 別の環境が `main` に push している | 2026-07-26〜 |
| P17 | 外部のライブラリがポータルで読めない | ずっと |
| P18 | 作業のゴミ（43MB）がフォルダにある | 2026-06-08〜 |
| P19 | ブランチを切り替えたら資料と道具が消えた | 2026-09-15 に対策 |

---

## P1. 同期コマンドで別のゲームに入れ替わる

- **症状**: README（や古い写し）の `cp /Volumes/PINK/Development/Fractas/index.html …/games/fractas/game/index.html` を打つと、公開中のラジアル版が正方形版に変わる。ランキングも別のゲームの点が混ざる。
- **原因**: `main` が 2026-07-27 に別のゲーム（正方形版）に作り替えられた。ポータルはラジアル版のまま。
- **どうするか**: 手で `cp` しない。`bash scripts/sync-to-portal.sh <W>` を使う（既定で `portal-radial` から写す。版が入れ替わるときは止まる）。

## P2. 古い PR の版で演出が巻き戻る

- **症状**: 2026-08-20、PR #3（`claude/fractus-mobile-dev-setup-22zje3`）の版を入れると、演出の速さが昔に戻るところだった。
- **原因**: PR の版もターン制で行数も多く、新しそうに見えたが、演出の定数だけ古かった。

| 定数 | PR #3 の版 | 公開中（正しい） |
|---|---|---|
| `CLEAR_FADE_DURATION` | 560 | **920** |
| `FALL_MOVE_DURATION` | 620 | **1560** |
| `CHARGE_MOVE_DURATION` | 700 | **1470** |
| `CHARGE_START_INTERVAL` | 30 | **85** |

- **どうするか**: 「新しそう」で判断しない。定数を見比べる。PR #3 は取り込まずに閉じた（ブランチはその後に削除。中身は PR #3 のコミット `9e6091d` から見られる）。マージのあとは、演出の定数が上の表の「正しい」値のままかを確かめる:

```bash
curl -sSL "https://hiroakiishibashi.com/games/fractas/game/?cb=$RANDOM$RANDOM" | grep -oE "const (CLEAR_FADE_DURATION|FALL_MOVE_DURATION|CHARGE_MOVE_DURATION|CHARGE_START_INTERVAL) = [0-9]+"
```

  全部の定数の一覧は [codemap/portal-radial.md](codemap/portal-radial.md) の「定数」。

## P3. 言語SDKのコピーがずれて検査が落ちる

- **症状**: ポータルで `node tools/test-game-lang.mjs` が「同梱コピーが SDK と一致している: games/fractas/game/hi-game-lang.js ✗」。
- **原因**: `hi-game-lang.js` は SDK の丸写しで、1バイトでも違うと落ちる。SDK が更新されたか、誰かが中身を触った。
- **どうするか**: 中身を直さず、SDK で丸ごと置き換える（RUNBOOK の R4）。

## P4. ゲームが `preferred_lang` を書いてしまう

- **症状**: ゲームで言語を選ぶと、ポータルのヘッダーや他のゲームの言語まで変わる。
- **原因**: `preferred_lang` はサイト全体の設定。Lumina が実際に書いていて、2026-09-10 に直された。
- **どうするか**: ゲーム内の選択は `HiLang.set()` を使う（SDK が `hi_lang:fractas` に保存する）。

## P5. `wrangler deploy` で他の人の変更が消える

- **症状**: 本番から、他のスレッドが出した変更がまとめて消える。
- **原因**: `npx wrangler deploy` は差分でなく、ディレクトリを丸ごと置き換える。古いツリーから出すと巻き戻る（2026-08-19〜20 に何度も起きた）。
- **どうするか**: 公開は hiroakiishibashi-web の「ブランチ → PR → main にマージ」だけ。

## P6. 直したのに古い内容が見える（キャッシュ）

- **症状**: 本番を開いても変わっていない。
- **原因**: ① 同じ `?cb=` を使うとエッジのキャッシュが返る ② `/games/fractas/game/index.html` と `/games/fractas/game/` はキャッシュが別（前者は 307 で後者へ飛ぶ）。
- **どうするか**: `?cb=$RANDOM$RANDOM` を毎回付ける。`curl -L` で飛び先まで見る。

## P7. PINK で git が `Operation not permitted`

- **症状**: `fatal: unable to access '.git/config': Operation not permitted`（PINK 上のリポジトリだけ）。
- **原因**: macOS の一時的な状態らしい（2026-08-29 に全リポジトリで発生し、再起動なしで自然に直った）。
- **どうするか**: 時間をおいてやり直す。だめなら別の場所に新しくクローンして作業する（ネット越しの clone・push は動く）。

## P8. PINK のポータルのクローンが不整合

- **症状**: `/Volumes/PINK/Development/hiroakiishibashi-web` で `git status` すると、変更が79件・未追跡が48件ある。HEAD は 2026-09-02 のまま、中のファイルだけ 9/10 相当に新しい（2026-09-11 に確認）。
- **原因**: 不明（誰かがファイルだけ書き換えた）。自分の作業ではないので触っていない。
- **どうするか**: ここでは作業しない・ここから `tools/deploy.sh` もしない。毎回新しくクローンする（RUNBOOK の R0-2）。片付けは Web スレッドかオーナーに任せる。

## P9. 手元の `npx serve` で SDK が 404

- **症状**: 手元でポータルのページを開くと、ゲームの `hi-game-lang.js` が 404。言語の案内が出ない。
- **原因**: `npx serve` が `/games/fractas/game/index.html` を `/games/fractas/game`（最後のスラッシュ無し）に書き換えるので、相対パスが1階層上を指す。
- **どうするか**: ページごと確かめるときは `python3 -m http.server <ポート> --directory <W>` を使う。ゲームだけなら `/games/fractas/game/`（最後にスラッシュ）で開く。

## P10. ヘッドレスでタイマーが進まない

- **症状**: ヘッドレスのブラウザで、iframe の中のゲームの時間が進まない。「壊れている」と誤診しかけた。
- **原因**: 見えていない iframe では `requestAnimationFrame` が止まることがある。
- **どうするか**: ゲームを直接開いて確かめる。または開発者ツールで `update(16)` を1回呼んで、判定の流れを確かめる。

## P11. ポータルの外で遊んだ点がランキングに出ない

- **症状**: ゲームを直接開いて遊ぶと（ログインしていても）、ポータルのランキングに出ない。
- **原因**: ポータルの外では公式SDK（`hiroakiishibashi-sdk.js`）で保存するが、SDK は `scores` テーブルに書く。ランキングは `plays` テーブルを見る。
- **どうするか**: 仕様としてそのまま（ポータルで遊ぶのが本筋）。直すならポータル側の SDK の設計の話になる（Web スレッド）。

## P12. ランキングに昔の版の点が混ざる

- **症状**: 1位が 631,360 点（2026-06-05）。いまのターン制では届きにくい。
- **原因**: ランキングは `plays` の全記録の「1人1件のベスト」。版が変わっても同じ `fractas` に積まれる。`metadata.mode` で見分けられる（無し＝最初期、`60sec`、`turn3`）。
- **どうするか**: オーナーの判断待ち（DECISIONS の D4）。勝手に消さない。

## P13. Actions が緑なのに配信されていない

- **症状**: GitHub Actions の `deploy` は緑なのに、本番が変わらない。
- **原因**: 2026-08-20 の時点では配信用のトークンが未登録で、配信のステップが「skipped」になっていた（2026-08-21 に有効化済み）。緑＝配信した、ではない。
- **どうするか**: ステップを見る（RUNBOOK の R10-1 の 3）。「配信」が success であること。

## P14. `gh pr create` が回数制限で失敗

- **症状**: `GraphQL: API rate limit already exceeded`。
- **原因**: GitHub の GraphQL の1時間あたりの上限（ほかのスレッドと同じアカウントで使っている）。
- **どうするか**: REST で PR を作ってマージする（RUNBOOK の R10-3）。

## P15. 手元で `/cdn-cgi/trace` が 404

- **症状**: 手元でページを開くと、コンソールに `/cdn-cgi/trace` の 404 が2つ出る。
- **原因**: Cloudflare の本番にしかない場所。手元には無い。
- **どうするか**: 無視してよい（本番では出ない）。

## P16. 別の環境が `main` に push している

- **症状**: 知らないコミットが `main` にある。`GAME_DEVELOPMENT_HANDOVER.md` にこのリポジトリが「/Users/hiroakiishibashi/Projects/fractas」にあると書いてある。
- **原因**: 旧 MacBook Pro（Late 2011）＋ Aider の環境でも開発している。2026-07-26〜27 の改良と正方形版はそこから。
- **どうするか**: 作業の前に必ず `git pull`。その文書は一部古い（ゲームの説明がラジアル版のまま）ので、この資料を正とする。

## P17. 外部のライブラリがポータルで読めない

- **症状**: ゲームに CDN のライブラリを足すと、ポータルでだけ動かない。
- **原因**: ポータルの CSP（`_headers`）が外部の読み込みを弾く。
- **どうするか**: ライブラリはゲームのフォルダに同梱する（いまの Fractas は外部ライブラリなし）。

## P18. 作業のゴミ（43MB）がフォルダにある

- **症状**: `/Volumes/PINK/Development/Fractas/.tmp-chrome-ui-check/`（Chrome の一時データ・43MB）と `outputs/`。
- **原因**: 2026-06-08 ごろ、別のAIが画面を確かめたときの残り。
- **どうするか**: `.gitignore` 済みなのでコミットには入らない。消すならオーナーに確かめてから（自分で作ったものではないため）。

## P19. ブランチを切り替えたら資料と道具が消えた

- **症状**: `/Volumes/PINK/Development/Fractas` で `portal-radial` に切り替えると、`docs/` と `scripts/` と `CLAUDE.md`（main のもの）が見えなくなる。
- **原因**: `portal-radial` には、ゲームのファイルと短い `CLAUDE.md` しか入れていない（資料と道具は `main` だけにある）。
- **どうするか**: 切り替えない。公開中の版は、専用フォルダ `/Volumes/PINK/Development/Fractas-portal-radial/`（git の worktree）で直す（RUNBOOK の R0-3）。`/Volumes/PINK/Development/Fractas` はいつも `main` のまま。
