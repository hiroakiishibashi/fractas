# コード索引 — `origin/main`（a6fb67b・正方形版）

> 機械生成: `python3 scripts/gen-codemap.py origin/main`。行番号はこの版の `index.html`（全 1284 行）のもの。
> 手で直さない。コードを直したら作り直す。流れの説明は [../CODEMAP.md](../CODEMAP.md)。

## ファイルの区切り

| 行 | 区切り |
|---:|---|
| 3 | `<head>` |
| 14 | `<style>` |
| 319 | `<body>` |
| 379 | `ゲームの <script>（ここから下がゲームの JS）` |
| 1283 | `</body>` |

## コメントの目印

| 行 | コメント |
|---:|---|
| 384 | `// --- ゲーム定数・設定 ---` |

## 定数（調整つまみ）

| 行 | 定義 |
|---:|---|
| 385 | `const START_COLOR_COUNT = 3` |
| 386 | `const MAX_COLOR_COUNT = 6` |
| 387 | `const GRID_LIMIT = 8` |
| 391 | `const AUTO_SPAWN_INTERVAL_MS = 1500` |
| 395 | `const THEMES = { … }` |
| 404 | `const THEME_KEYS = Object.keys(THEMES)` |
| 962 | `const PORTAL_GAME_ID = 'fractas'` |
| 967 | `const SEND_THROTTLE_MS = 10000` |

## 関数（39 個）

| 行 | 関数 |
|---:|---|
| 432 | `function loadSavedData()` |
| 447 | `function updateHighScoreUI()` |
| 452 | `function updateAudioBtnUI()` |
| 466 | `function toggleMute(e)` |
| 481 | `function resize()` |
| 498 | `function doesOverlap(x1, y1, s1, x2, y2, s2)` |
| 503 | `function hasEdgeContact(x1, y1, s1, x2, y2, s2)` |
| 510 | `function isFullyConnectedCluster(testBlocks)` |
| 540 | `function isValidPosition(block, testGx, testGy, ignoreId = null)` |
| 566 | `function pushBranchOutward(spawnGx, spawnGy, size = 1)` |
| 598 | `function compactClusterTowardsCore()` |
| 661 | `function createBlock(gx, gy, size = 1, colorIdx = 0)` |
| 679 | `function updateUI()` |
| 689 | `function updateGrowthTimerUI()` |
| 699 | `function startAudio()` |
| 713 | `function playTone(freq, duration = 0.18, type = 'sine', volume = 0.08, attack = 0.01, filterFreq = 2600)` |
| 733 | `function playGlide(startFreq, endFreq, duration, type, volume)` |
| 750 | `function playMoveSfx()` |
| 755 | `function playSnapSfx()` |
| 760 | `function playClearSfx(sizeMultiplier = 1, chainMultiplier = 1)` |
| 767 | `function playGrowSfx()` |
| 772 | `function playGameOverSfx()` |
| 778 | `function checkMatches()` |
| 823 | `function addClearScore(size, chainMultiplier)` |
| 830 | `function spawnAutomaticSquare()` |
| 875 | `function resetGame()` |
| 912 | `function endGame()` |
| 957 | `function updateScoreUI()` |
| 969 | `function reportScore(force)` |
| 1007 | `function dismissHint()` |
| 1017 | `function getPxPos(gx, gy)` |
| 1024 | `function onPointerDown(e)` |
| 1048 | `function onPointerMove(e)` |
| 1085 | `function onPointerUp()` |
| 1114 | `function drawBlock(b, overridePx = null, overridePy = null, isGhost = false)` |
| 1165 | `function drawGridBackground()` |
| 1205 | `function update(dt)` |
| 1223 | `function draw()` |
| 1237 | `function gameLoop(timestamp)` |

## DOM の id（HTML の部品）

| 行 | id |
|---:|---|
| 321 | `#uiLayer` |
| 323 | `#scoreVal` |
| 324 | `#bestScoreVal` |
| 325 | `#chainContainer` |
| 325 | `#chainVal` |
| 329 | `#growthTimerBox` |
| 329 | `#growthTimerVal` |
| 330 | `#colorContainer` |
| 330 | `#colorCountVal` |
| 331 | `#themeContainer` |
| 331 | `#themeVal` |
| 333 | `#audioToggleBtn` |
| 337 | `#gameCanvas` |
| 339 | `#brand` |
| 341 | `#hint` |
| 352 | `#gameOver` |
| 355 | `#newBestBadge` |
| 359 | `#finalScoreVal` |
| 363 | `#finalBestScoreVal` |
| 367 | `#statMovesVal` |
| 371 | `#statScansVal` |
| 374 | `#restartBtn` |

## 画面に出る文字（翻訳するならここ）

| 行 | 文字 | 場所 |
|---:|---|---|
| 8 | Fractas | HTML |
| 323 | SCORE: | HTML |
| 324 | BEST: | HTML |
| 325 | CHAIN!! | HTML |
| 329 | SPAWN IN: | HTML |
| 329 | s | HTML |
| 330 | COLORS: | HTML |
| 331 | THEME: | HTML |
| 331 | COSMIC | HTML |
| 339 | FRACTAS | HTML |
| 342 | FRACTAS | HTML |
| 344 | 🖱 Drag squares along connected edges (Outer squares shift together) | HTML |
| 347 | ⏹ Match 4 same-sized squares into 2×2 to clear! | HTML |
| 349 | Squares emerge from root every 1.5s, pushing connected branches outward! | HTML |
| 354 | GAME OVER | HTML |
| 355 | NEW HIGH SCORE! | HTML |
| 358 | FINAL SCORE | HTML |
| 362 | BEST SCORE | HTML |
| 366 | TOTAL MOVES | HTML |
| 370 | SPAWNS SURVIVED | HTML |
| 374 | PLAY AGAIN | HTML |
| 375 | or press Space / Tap anywhere | HTML |
| 396 | COSMIC | JS |
| 397 | CYBER | JS |
| 398 | TROPICAL | JS |
| 399 | VIVID | JS |
| 400 | SUNSET | JS |
| 401 | NEON | JS |
| 416 | COSMIC | JS |
| 458 | Unmute Sound | JS |
| 462 | Mute Sound | JS |
| 515 | CORE | JS |
| 1200 | CORE | JS |
| 1272 | Space | JS |
| 1272 | Enter | JS |

読み上げの文は `speakTurnPrompt` の中にある（ラジアル版）。

## 端末に保存するキー（localStorage）

- `fractas_games_played`
- `fractas_high_score`
- `fractas_muted`

## イベント（入力・ページの出入り）

| 対象:イベント | 行 |
|---|---|
| `audioBtnEl:click` | 1267 |
| `audioBtnEl:touchstart` | 1268 |
| `canvas:mousedown` | 1013, 1106 |
| `canvas:mousemove` | 1107 |
| `canvas:touchmove` | 1111 |
| `canvas:touchstart` | 1014, 1110 |
| `gameOverEl:click` | 1250 |
| `gameOverEl:touchstart` | 1251 |
| `restartBtnEl:click` | 1259 |
| `window:keydown` | 1271 |
| `window:mouseup` | 1108 |
| `window:resize` | 494 |
| `window:touchend` | 1112 |

## 親（ポータル）へ送るメッセージ

- type: `SCORE_UPDATE`
- metadata.mode: `square_cluster`

