# Fractas コードの地図（CODEMAP）

> どちらの版も `index.html` 1ファイルです。ここでは「流れ」を説明します。
> 行番号つきの索引（機械生成）: **[codemap/portal-radial.md](codemap/portal-radial.md)**（公開中のラジアル版）／ **[codemap/main.md](codemap/main.md)**（正方形版）
> コードを直したら索引を作り直す: `python3 scripts/gen-codemap.py origin/portal-radial > docs/codemap/portal-radial.md`（`origin/portal-radial` は git のブランチの名前。フォルダではない）
> 最終更新: 2026-09-15

---

## 1. ファイルの形（2つの版で同じ）

1. `<head>`: `meta` → `<title>` → **言語SDK**（`<script src="hi-game-lang.js">` と `var LANG = …`）→ `<style>`
2. `<body>`: `#uiLayer`（スコアなど）→ `<canvas id="gameCanvas">` → `#brand`（透かし）→ `#hint`（操作のヒント）→ `#gameOver`
3. ゲームの `<script>`（`<body>` の中）: 定数 → 状態の変数 → 関数 → 入力の登録 → **ポータル連携**（`reportScore`）→ ヒントの自動消去 → `resetGame()` で開始

ビルドはありません。ファイルを直せば、そのまま動きます。

---

## 2. ラジアル版（公開中・ブランチ `portal-radial`）

### 2-1. 盤面のデータ

| もの | 意味 |
|---|---|
| `board[i][s]` | 色の番号（`-1` は空）。`i = r - MIN_R`（`getI(r)` / `getR(i)` で変換） |
| `SECTORS = 12` | 扇形の数 |
| `MIN_R = -12` 〜 `MAX_R = 9` | 輪の番号（全22段）。中心に近いほど小さい |
| 半径 | `CORE_RADIUS * SCALE_FACTOR^r`（`SCALE_FACTOR = 1.25`。1段ごとに 1.25 倍） |
| `lockedBoard` | 光っている（消える予定の）セル |
| `reservedMatchCells` | いま3つ以上そろっていて「予約」されているセル |

### 2-2. 1手の流れ（入力）

1. `onPointerDown`: 触った位置の輪と扇形を覚える（`getGridFromPos`）。
2. `onPointerMove`: 最初に **8px** 動いた時点で（`8` は定数ではなく、コードに直接書かれた数字）、中心からの距離の変化（`distDiff`）と弧の長さ（`arcLength`）を比べ、大きいほうで **`SHIFT`（扇形をずらす）** か **`ROTATE`（輪を回す）** かを決める。
3. `onPointerUp`: 近い位置にスナップし、盤面の配列を回す／ずらす。**実際に1コマ以上動いたときだけ**（`sm !== 0` / `rm !== 0`）`completePlayerTurn()` を呼ぶ。

### 2-3. ターンと判定

```
completePlayerTurn()      turnCount++ → triggerTurnPrompt()（中央の表示と読み上げ）
   └ 3手目なら startTurnCheck()
         スキャナー開始。scanMatchGroups = findMatchesGroups()（3つ以上つながった同じ色）
update(dt) の中
   スキャナーを中心から外へ進める（scannerSpeed = 0.04）
   触れたグループを markCellLit() で光らせる
   外端（MAX_R + 0.5）まで行ったら
     ├ 光ったセルがある → CLEAR_FADE_DURATION（920ms）かけて消す
     │     → addClearScore() → advanceChargeColor()（色を1つ増やす）
     │     → applyGravityAnimated()（詰めて補充）→ resolveAllMatches()（補充でできた連鎖）
     │     → finishTurnCheck()（turnCount = 0 に戻す）
     └ 1つも無い → endGame()（GAME OVER・スコアを必ず送る）
```

- 点数: `addClearScore(個数, 連鎖) = 個数×10 ＋ max(0, 個数−3)×20×連鎖`
- 連鎖: 補充で偶然そろうのを `REFILL_CHAIN_CHANCE`（10%）だけ許し、1回の判定で最大 `MAX_JUDGEMENT_CHAINS`（3）まで。
- 色の数: `START_COLOR_COUNT`（3）から、判定に成功するたびに +1、最大 `MAX_COLOR_COUNT`（6）。

### 2-4. 補充と落下

- `applyGravityAnimated()`: ブロックを外側へ詰め、空いた中心側を新しい色で埋める。
- 新しいブロックは1つずつ光りながら入る（`CHARGE_MOVE_DURATION` 1470ms・`CHARGE_START_INTERVAL` 85ms）。落ちるのは `FALL_MOVE_DURATION` 1560ms。
- 最初の盤面と、盤面が外へずれて中心に新しい段が入るとき（`boardShiftOutward()`）は `getSafeColorIdx()`: 置いてもすぐにはそろわない色を選ぶ。
- 判定のあとの補充（`applyGravityAnimated()`）は `getChainFriendlyColor()`: `REFILL_CHAIN_CHANCE`（10%）の確率で「置くとそろう色」（連鎖のもと）を選び、それ以外は「置いてもそろわない色」を選ぶ。
- 待っている間も、盤面はゆっくり外へ流れる（`AMBIENT_EXPANSION_SPEED`）。

### 2-5. 描画

- `gameLoop(timestamp)` が `requestAnimationFrame` で `update(dt)` と `draw()` を回す。
- `draw()`: `buildBlockPath()`（扇形の `Path2D`）で全セルを描く → `drawScanner()` → `drawTurnPrompt()`（中央の数字）。
- 色は `getColorString()`。テーマは `COSMIC` のまま（`THEME_CHANGE_SCORE_THRESHOLD` が無限大なので切り替わらない）。

### 2-6. 音と声

- `startAudio()`: 最初の操作で `AudioContext` を作る（ブラウザの決まりで、操作の前には鳴らせない）。
- 効果音は `playTone()` / `playGlide()` の組み合わせ（`playMoveSfx`・`playDialTickSfx`・`playScanSfx`・`playClearSfx` など）。音声ファイルは無い。
- `speakTurnPrompt(remaining)`: 残りのターン数を英語で読み上げる（女性らしい英語の声を優先・音量 0.28）。

### 2-7. ポータル連携

- `PORTAL_GAME_ID = 'fractas'`、`inPortal`（iframe の中か）。
- `reportScore(force)`: 10秒に1回まで・同じ点は送らない・`force` のときは待たない。`endGame()` と、`visibilitychange`・`pagehide`・`blur` で呼ぶ。
- 送る中身: `{type:'SCORE_UPDATE', game:'fractas', score, metadata:{theme, mode:'turn3', turnsPerCheck, turns, checks, colorCount}}`。
- ポータルの外では、公式SDK（`hiroakiishibashi-sdk.js`）を後から読み込んで `saveScore` する。

### 2-8. よく触る調整つまみ

| 定数 | いまの値 | 何が変わるか |
|---|---|---|
| `TURNS_PER_CHECK` | 3 | 何手ごとに判定するか |
| `START_COLOR_COUNT` / `MAX_COLOR_COUNT` | 3 / 6 | 色の数の始まりと上限（多いほどそろいにくい） |
| `CLEAR_FADE_DURATION` | 920 | 消えるまでの演出の長さ（ms） |
| `FALL_MOVE_DURATION` | 1560 | 落ちる演出の長さ（ms） |
| `CHARGE_MOVE_DURATION` / `CHARGE_START_INTERVAL` | 1470 / 85 | 補充の演出の長さと間隔（ms） |
| `REFILL_CHAIN_CHANCE` | 0.10 | 補充で連鎖を許す確率 |
| `MAX_JUDGEMENT_CHAINS` | 3 | 1回の判定での連鎖の上限 |
| `AMBIENT_EXPANSION_SPEED` | 0.0015 | 待っている間に盤面が外へ流れる速さ |
| `scannerSpeed`（変数） | 0.04 | スキャナーの速さ（1フレームで進む輪の数） |
| `SEND_THROTTLE_MS` | 10000 | スコアを送る間隔の最小（ms） |

⚠️ 演出の4つ（`CLEAR_FADE_DURATION` など）は、昔の PR の版に戻さないこと（[PITFALLS.md](PITFALLS.md) の P2）。公開中の値の確かめ方:

```bash
curl -sSL "https://hiroakiishibashi.com/games/fractas/game/?cb=$RANDOM$RANDOM" | grep -oE "const [A-Z_]+ = [0-9.]+"
```

---

## 3. 正方形版（`main`）

| もの | 意味 |
|---|---|
| `blocks[]` | 正方形のブロック（`gx`・`gy`・`size`＝1/2/4・`colorIdx` など） |
| `GRID_LIMIT = 8` | 中心から ±8 マスが外枠。ここに届くと GAME OVER |
| `AUTO_SPAWN_INTERVAL_MS = 1500` | 中心から新しいブロックが生える間隔 |

流れ:

```
spawnAutomaticSquare()（1.5秒ごと）
   中心の近くに1つ生やす → pushBranchOutward() でつながった枝を外へ押す
   3回に1回は、もう1本押す
   どれかが外枠に届いたら endGame()
onPointerDown / onPointerMove
   ブロックを辺にそってドラッグ。isValidPosition()（重ならない・辺で接する・かたまりが1つにつながったまま＝isFullyConnectedCluster()）
onPointerUp
   スナップして動いていれば totalTurns++ → checkMatches()
checkMatches()
   同じ大きさ（1・2・4）の 4つが 2×2 に並んでいたら消す（⚠️ 色は見ていない）
   点 = 400 × 大きさ × 連鎖 → compactClusterTowardsCore()（中心へ詰める）→ もう一度 checkMatches()
```

- 端末に保存: `fractas_high_score`・`fractas_muted`・`fractas_games_played`（`loadSavedData()`）。
- 画面: ミュートボタン（`#audioToggleBtn`）、GAME OVER の成績と「PLAY AGAIN」（`#restartBtn`）、「NEW HIGH SCORE!」。
- ポータル連携はラジアル版と同じ作り（`mode: 'square_cluster'`）。

---

## 4. 1ファイルを読むときのコツ

- 関数を探すときは、索引（`codemap/*.md`）の行番号から入る。`grep -n "function 名前" index.html` でもよい。
- 定数はファイルの上のほう（ゲームの `<script>` の直後）に集まっている。
- 変数の多くは `let` で、ブラウザの開発者ツールのコンソールから名前で読める（例: `score`・`turnCount`・`isGameOver`）。確かめるときに便利。
