# Fractas 手順書（RUNBOOK）

> コピペで動くように書いています。`<...>` のところだけ自分の値に置き換えます。
> 公開する前に、必ず [HANDOFF.md](HANDOFF.md) の「7. 破ってはいけない約束」を読んでください。
> 最終更新: 2026-09-15

| 番号 | やること | オーナーの了承 |
|---|---|---|
| R0 | 準備（リポジトリを用意する） | いらない |
| R1 | いまの状態を確かめる | いらない |
| R2 | 公開中のゲーム（ラジアル版）を直して出す | 中身しだい |
| R3 | 未公開のラジアル改良を入れる | **要る（D2）** |
| R4 | 言語SDKが新しくなったとき | いらない |
| R5 | 翻訳（日本語など）を足す | 中身しだい |
| R6 | 正方形版をポータルに出す | **要る（D1・D4）** |
| R7 | GitHub Pages（正方形版）を直す | いらない |
| R8 | 本番を前の版に戻す | いらない（急ぐとき） |
| R9 | サムネ・プレイ動画を撮り直す | いらない |
| R10 | 困ったとき | いらない |

---

## R0. 準備

### R0-1. fractas リポジトリ（資料と道具・いつも `main`）

```bash
cd /Volumes/PINK/Development/Fractas
git switch main                            # このフォルダは、いつも main のまま使う
git pull                                   # 別の環境（旧Mac＋Aider）も push するので必ず
git fetch origin --tags
```

`fatal: unable to access '.git/config': Operation not permitted` と出たら、PINK の一時的な不具合です（[PITFALLS.md](PITFALLS.md) の P7）。時間をおいてやり直すか、別の場所にクローンします:

```bash
mkdir -p /Volumes/PINK/Development/_work
git clone git@github.com:hiroakiishibashi/fractas.git /Volumes/PINK/Development/_work/fractas
```

### R0-2. ポータル（hiroakiishibashi-web）のクローン

⚠️ **`/Volumes/PINK/Development/hiroakiishibashi-web` は使いません**（中身が不整合・[PITFALLS.md](PITFALLS.md) の P8）。そのつど、新しくクローンします:

```bash
mkdir -p /Volumes/PINK/Development/_work
W=/Volumes/PINK/Development/_work/hiw-$(date +%Y%m%d-%H%M)
git clone --depth 60 git@github.com:hiroakiishibashi/hiroakiishibashi-web.git "$W"
echo "$W"
```

**このあとの手順の `<W>` は、いま表示されたパスに置き換えます**（同じターミナルなら `"$W"` と書いてもよい。変数が残っている）。
終わったら消してかまいません（`rm -rf "$W"`。自分で作ったものだけ）。

### R0-3. 公開中の版を直すための専用フォルダ（`portal-radial`）

`/Volumes/PINK/Development/Fractas-portal-radial/` は、ブランチ `portal-radial` を開いた**別のフォルダ**です（git の worktree。2026-09-15 に作成済み）。
**公開中のゲームは、このフォルダで直します。** 資料と道具は `/Volumes/PINK/Development/Fractas/`（`main`）に残ったままなので、行き来しても消えません。

```bash
git -C /Volumes/PINK/Development/Fractas-portal-radial pull      # 使う前に最新にする
```

フォルダが無いとき（別の Mac など）は作ります（1行目で作れなければ2行目）:

```bash
cd /Volumes/PINK/Development/Fractas && git fetch origin
git worktree add /Volumes/PINK/Development/Fractas-portal-radial portal-radial \
  || git worktree add --track -b portal-radial /Volumes/PINK/Development/Fractas-portal-radial origin/portal-radial
```

⚠️ 同じブランチは1か所でしか開けません。`/Volumes/PINK/Development/Fractas` で `git switch portal-radial` をしないこと（`already used by worktree` と出て止まる。別の方法で切り替えると、`docs/` と `scripts/` が消えたように見える＝[PITFALLS.md](PITFALLS.md) の P19）。

---

## R1. いまの状態を確かめる（読むだけ）

```bash
cd /Volumes/PINK/Development/Fractas && git pull && bash scripts/status.sh
```

ふつうの結果（2026-09-15 時点）:

```
== 1. リポジトリ hiroakiishibashi/fractas ==
  ・ origin/main = … 正方形版
  ・ origin/portal-radial = … ラジアル版(ターン制)
== 2. 本番ポータル ==
  ・ 公開中のゲーム: ラジアル版(ターン制)
  ✅ 言語SDKの配線あり
  ✅ 公開中 = portal-radial（完全一致）
== 3. SDK の同梱コピー ==
  ✅ …（3行とも ✅）
== 4. GitHub Pages（main をそのまま配信） ==
  ・ Pages: 正方形版
  ✅ Pages = origin/main
```

⚠️ が出たら、その行の説明どおりに調べます。**直す前に、何が起きているかをオーナーに報告**します。

---

## R2. 公開中のゲーム（ラジアル版）を直して出す

**1.** 専用フォルダ（R0-3）を最新にする

```bash
cd /Volumes/PINK/Development/Fractas-portal-radial
git pull
```

2. このフォルダの `index.html` を直す。どこに何があるかは、main のフォルダの資料 `/Volumes/PINK/Development/Fractas/docs/CODEMAP.md` と `docs/codemap/portal-radial.md`。

**3.** 手元で遊んで確かめる

```bash
npx serve -l 3460 --no-clipboard .
# ブラウザで http://localhost:3460/ を開く（ポータルの枠なし・単体で動く）
```

確かめること: 3手で判定が走る／消えると点が入る／GAME OVER からタップで再開できる／開発者ツールのコンソールに赤いエラーが無い。
終わったらサーバーを止める（Ctrl+C）。

**4.** `portal-radial` に記録して push する（このフォルダで）

```bash
git add index.html                        # 名指し。git add -A は使わない
git commit -m "<何を直したか>"
git push origin portal-radial
```

**5.** main のフォルダから、ポータルのクローン（R0-2 の `<W>`）へ写す

```bash
cd /Volumes/PINK/Development/Fractas && git fetch origin
bash scripts/sync-to-portal.sh <W> --dry-run    # 何が変わるかだけ見る
bash scripts/sync-to-portal.sh <W>              # 写す。写したあと中で node tools/test-game-lang.mjs も1回走る
```

**6.** ポータルで公開する（ブランチ → PR → マージ）

```bash
cd <W>
git switch -c claude/fractas-<何をしたか>
git add games/fractas/game/index.html games/fractas/game/hi-game-lang.js
git commit -m "Fractas: <何を直したか>"
git fetch origin && git merge origin/main
node tools/test-game-lang.mjs | tail -2         # 他の人の変更を取り込んだあとに、もう一度。「✅ 全部 pass」
git push -u origin HEAD
gh pr create --fill && gh pr merge --merge      # マージ＝公開
```

`gh pr create` が `API rate limit` で失敗したら R10-3。

**7.** 配信と本番を確かめる

```bash
gh run list -R hiroakiishibashi/hiroakiishibashi-web --workflow=deploy.yml --limit 3
gh run watch <いちばん上の番号> -R hiroakiishibashi/hiroakiishibashi-web --exit-status
cd /Volumes/PINK/Development/Fractas && bash scripts/status.sh
```

status.sh で「✅ 公開中 = portal-radial（完全一致）」になれば完了。

**8.** 公開中のしるし（タグ）を付ける。タグの名前は `portal-live-<公開した日>`（例: 2026-09-11 に出したものは `portal-live-2026-09-11`）

```bash
cd /Volumes/PINK/Development/Fractas && git fetch origin
T=portal-live-$(date +%Y-%m-%d)
git tag "$T" origin/portal-radial && git push origin "$T"
```

**9.** 資料を直す（main のフォルダで）: [HANDOFF.md](HANDOFF.md) の「0. 30秒でわかる現状」（タグ名）と [HISTORY.md](HISTORY.md) に1行。そのあと:

```bash
cd /Volumes/PINK/Development/Fractas
python3 scripts/gen-codemap.py origin/portal-radial > docs/codemap/portal-radial.md
python3 scripts/build-handoff-html.py
git add docs/HANDOFF.md docs/HISTORY.md docs/codemap/portal-radial.md docs/handoff.html
git commit -m "docs: <何をしたか>" && git push
```

`origin/portal-radial` は git の「ブランチの名前」です（フォルダの名前ではない）。`git fetch origin` のあとに使います。

---

## R3. 未公開のラジアル改良（`ce073ce`・`d282cb6`）を入れる

**オーナーの了承（[DECISIONS.md](DECISIONS.md) の D2）を得てから。**

```bash
cd /Volumes/PINK/Development/Fractas-portal-radial
git pull
git cherry-pick ce073ce          # 軽量化
git cherry-pick d282cb6          # ハイスコア・ミュート・GAME OVER 画面
git push origin portal-radial
```

2026-09-15 に試した結果: `portal-radial` の上に、2つとも**ぶつからずに**入ります（ラジアル版のまま・言語SDKの配線も残る・ハイスコアのキー `fractas_high_score` が増える）。`d282cb6` は `GAME_DEVELOPMENT_HANDOVER.md` も一緒に足しますが、害はありません。
ぶつかった（`CONFLICT` と出た）ときは `git cherry-pick --abort` で元に戻し、オーナーに報告します（無理に直さない・force push しない）。

あとは R2 の 3 と 5〜9。とくに確かめること:
- ポータルの枠の中（縦長・スマホの幅）で、ミュートボタンと GAME OVER 画面が崩れないか
- ハイスコアが保存されるか（`localStorage` の `fractas_high_score`。これはゲームだけのキーなので書いてよい。`preferred_lang` は書かない）
- スコアが今までどおりランキングに届くか（`mode:'turn3'` のまま）

---

## R4. 言語SDKが新しくなったとき

SDK の正本は、ポータルの `sdk/html/hi-game-lang.js`。status.sh で「SDK と違う」と出たら、**丸ごと置き換える**だけです（中身を書き換えるのは禁止）。
main（資料のフォルダ）と portal-radial（直すフォルダ）の両方を置き換えます。

```bash
mkdir -p /Volumes/PINK/Development/_work
curl -fsSL "https://hiroakiishibashi.com/sdk/html/hi-game-lang.js?cb=$RANDOM$RANDOM" -o /Volumes/PINK/Development/_work/hi-game-lang.js
for d in /Volumes/PINK/Development/Fractas /Volumes/PINK/Development/Fractas-portal-radial; do
  ( cd "$d" && git pull && cp /Volumes/PINK/Development/_work/hi-game-lang.js hi-game-lang.js \
    && git add hi-game-lang.js && git commit -m "Update bundled hi-game-lang.js to the current portal SDK" && git push )
done
```

ポータル側のコピー（`games/fractas/game/hi-game-lang.js`）は、Web スレッドが SDK を更新するときに一緒に直すことが多いです。直っていなければ（status.sh の「本番ゲームの同梱コピーが SDK とずれている」）、R2 の 5〜7。

---

## R5. 翻訳（日本語など）を足す

決まりの正本: https://hiroakiishibashi.com/docs/game-language-spec.md（とくに §1・§3・§4）

**1.** 画面に出る英語を、1か所の辞書に集める。どこに英語があるかは [codemap/portal-radial.md](codemap/portal-radial.md) の「画面に出る文字」。

```js
const DICT = {
  en: { turnsLeft: 'TURNS LEFT', turnLeft: 'TURN LEFT', judgement: 'JUDGEMENT', gameOver: 'GAME OVER' /* … */ },
  ja: { turnsLeft: 'のこりターン', turnLeft: 'のこりターン', judgement: 'はんてい', gameOver: 'ゲームオーバー' /* … */ },
};
function t(key) { return DICT[LANG]?.[key] ?? DICT.en[key] ?? key; }   // || ではなく ?? を使う
```

2. `<head>` の初期化の `langs` に、**本当に辞書がある言語だけ**を書く: `HiLang.init({ id:'fractas', langs:['en','ja'] })`
3. 遊んでいる途中の切り替えに対応できないなら `live:false`（既定）のまま。ポータルが「次の読み込みから」と案内する。**自動でリロードしない**。
4. 読み上げ（`speakTurnPrompt`）の文と、声の言語も `LANG` に合わせる。
5. `preferred_lang` には書かない。
6. ポータルの説明文（`js/i18n/*.js` の `game.fractas.*`）は、もう6言語ある。
7. R2 の 3〜9 で公開。確かめ方: ポータルで JA → 日本語／KO → 英語＋枠の下に「이 게임은 English / 日本語 로 이용할 수 있습니다.」

---

## R6. 正方形版をポータルに出す

**オーナーの了承（D1）を得てから。** ランキングの扱い（D4）も一緒に決めること。

**1.** 写す（安全装置を外すフラグが要る）

```bash
bash scripts/sync-to-portal.sh <W> --from main --i-have-owner-approval
```

**2.** 説明文を正方形版に書き換える:
- `js/i18n/{en,ja,ko,es,pt,zh}.js` の `game.fractas.desc` と `game.fractas.how`（6言語すべて）
- `games/fractas/index.html` の最初に出る文（103〜104行目付近）
- トップの `index.html` のカード（117行目付近）
3. キービジュアル: 新しい版を足して、参照を切り替える（上書きしない）。`assets/games/keyvisuals/variants/fractas-hero-<次の文字>.jpg` を作り、`js/user-ui.js` と `index.html` の参照を変える。`node tools/check-assets.mjs` で確かめる。
4. ランキング: D4 の決定どおりにする（game_id `fractas` をそのまま使うと、ラジアル版の点と混ざる）。
5. R2 の 6〜9。資料の「0. 30秒でわかる現状」を必ず書き換える（ポータル＝正方形版に変わるので）。

---

## R7. GitHub Pages（正方形版）を直す

```bash
cd /Volumes/PINK/Development/Fractas
git switch main && git pull
# index.html を直す → 手元で確かめる: npx serve -l 3459 --no-clipboard . → http://localhost:3459/
git add index.html && git commit -m "<何を直したか>" && git push
gh api repos/hiroakiishibashi/fractas/pages/builds/latest --jq .status     # built になるまで1〜2分
curl -sS "https://hiroakiishibashi.github.io/fractas/?cb=$RANDOM$RANDOM" | grep -c GRID_LIMIT
```

⚠️ `main` を直しても、**ポータルは変わりません**（それで正しい）。

---

## R8. 本番を前の版に戻す

いちばん安全なのは、問題のマージを打ち消す PR を作ることです:

```bash
cd <W>
git log --oneline -10 -- games/fractas/          # 戻したいマージを探す
git switch -c claude/fractas-revert
git revert -m 1 <マージのコミット>
git push -u origin HEAD
gh pr create --fill && gh pr merge --merge
```

公開していた版のタグから写し直すこともできます（そのあと R2 の 6〜7）:

```bash
bash scripts/sync-to-portal.sh <W> --from portal-live-2026-09-11
```

---

## R9. サムネ・プレイ動画を撮り直す

### R9-1. 全ゲーム共用の道具 gamerec（おすすめ）

場所: `/Volumes/PINK/Development/tools/gamerec/`（使い方は同じ場所の `README.md`）。ヘッドレスの Chrome で裏で録画するので、作業を止めません。

Fractas の台本は **作成済み**（2026-09-15・`games/fractas.mjs`）。公開中のラジアル版を開き、録画の前に3手を指しておくので、**最初の3秒でスキャナーが走り、10秒あたりで光ったブロックが消えて点が入る**映像になります（1280×720・約22秒・約1.9MB。2026-09-15 に撮って確かめた）。

```bash
cd /Volumes/PINK/Development/tools/gamerec
node record.mjs fractas            # → out/fractas.mp4
node record.mjs fractas --gif      # GIF も作る
```

- 台本の座標は **1280×720 が前提**です（`--size` で縦にするなら、台本の中心の座標 `640, 360` と半径も変える）。
- 手元の `portal-radial` を撮りたいときは、`games/fractas.mjs` の `url` を `http://localhost:3460/` に変え、`/Volumes/PINK/Development/Fractas-portal-radial` で `npx serve -l 3460 --no-clipboard .` を動かしておく。
- 音は入りません（ヘッドレスのため）。撮った動画は、このリポジトリの `assets/` に置きます（例: `assets/fractas-radial-preview-2026-09.mp4`）。

### R9-2. 2026-06 に使った方法（canvas から直接撮る）

ブラウザでゲームを開き（`https://hiroakiishibashi.com/games/fractas/game/`）、開発者ツールのコンソールで:

```js
// サムネ（いまの1コマを JPEG で保存）
document.getElementById('gameCanvas').toBlob(b => { const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'fractas-thumb.jpg'; a.click(); }, 'image/jpeg', 0.95);
```

```js
// 15秒の動画（webm）
const s = document.getElementById('gameCanvas').captureStream(30);
const r = new MediaRecorder(s, { mimeType: 'video/webm;codecs=vp9', videoBitsPerSecond: 7e6 });
const c = []; r.ondataavailable = e => e.data.size && c.push(e.data);
r.onstop = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(c, { type: 'video/webm' })); a.download = 'fractas-raw.webm'; a.click(); };
r.start(); setTimeout(() => r.stop(), 15000);
```

保存されたファイルは PINK に移します（Mac 本体に置かない決まり）。mp4 にするには:

```bash
ffmpeg -y -i fractas-raw.webm -r 30 -c:v libx264 -pix_fmt yuv420p -crf 26 -preset slower -maxrate 3500k -bufsize 7000k -movflags +faststart -an fractas-preview.mp4
```

2026-06 の実績: 1280×720・15秒で mp4 が約5.4MB。
置き場所: このリポジトリの `assets/`。ポータルのキービジュアルは R6 の 3 と同じ作法（新しい版を足して参照を切り替える）。

---

## R10. 困ったとき

### R10-1. 直したのに本番が変わらない

1. `?cb=` を毎回ちがう数字にしたか（`?cb=$RANDOM$RANDOM`）
2. `/games/fractas/game/index.html` と `/games/fractas/game/` は、キャッシュが別。両方を見る
**3.** 配信が走ったか:
```bash
gh run view <番号> -R hiroakiishibashi/hiroakiishibashi-web --json jobs --jq '.jobs[].steps[] | "\(.conclusion) \(.name)"'
```
「配信」が success か（skipped なら配信されていない）
4. `git fetch origin && git log origin/main -- games/fractas/` に自分のコミットがあるか（無ければ push 漏れか、マージ漏れ）

### R10-2. `node tools/test-game-lang.mjs` が落ちる

「同梱コピーが SDK と一致している: games/fractas/game/hi-game-lang.js」が ✗ なら R4。

### R10-3. `gh pr create` が `API rate limit exceeded` で失敗する

GitHub の GraphQL の回数制限です（1時間で戻る）。REST で代わりができます:

```bash
N=$(gh api repos/hiroakiishibashi/hiroakiishibashi-web/pulls -f title="Fractas: <何をしたか>" -f head="<ブランチ名>" -f base=main -f body="<説明>" --jq .number)
gh api -X PUT repos/hiroakiishibashi/hiroakiishibashi-web/pulls/$N/merge -f merge_method=merge
```

残りの回数: `gh api rate_limit --jq '.resources.graphql'`

### R10-4. PINK で git が動かない

[PITFALLS.md](PITFALLS.md) の P7。新しくクローンして作業する（R0）。

### R10-5. ランキングに点が入らない

1. ログインしているか（していないと保存されない）
2. ブラウザの開発者ツールに `[saveScore] saved:` が出ているか
**3.** `game_catalog` に `fractas` があるか（2026-09-15 時点で enabled=true）。読むだけの確認:
```bash
ANON=$(grep -oE "eyJ[A-Za-z0-9._-]{100,}" <W>/js/supabase-client.js | head -1)
curl -sS "https://ddfhngfymavzsyktiuua.supabase.co/rest/v1/game_catalog?select=game_id,enabled&game_id=eq.fractas" -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
```
（公開用の anon キーを、ポータルのファイルから読んでいるだけ。秘密の値ではない。`tools/new-game-check.mjs` は秘密の設定ファイルを読むので、AI は勝手に実行しない）
