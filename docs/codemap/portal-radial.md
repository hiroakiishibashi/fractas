# コード索引 — `origin/portal-radial`（4db0da4・ラジアル版（ターン制））

> 機械生成: `python3 scripts/gen-codemap.py origin/portal-radial`。行番号はこの版の `index.html`（全 1916 行）のもの。
> 手で直さない。コードを直したら作り直す。流れの説明は [../CODEMAP.md](../CODEMAP.md)。

## ファイルの区切り

| 行 | 区切り |
|---:|---|
| 3 | `<head>` |
| 14 | `<style>` |
| 217 | `<body>` |
| 252 | `ゲームの <script>（ここから下がゲームの JS）` |
| 1915 | `</body>` |

## コメントの目印

| 行 | コメント |
|---:|---|
| 257 | `// --- ゲーム定数・設定 ---` |
| 312 | `// ★ スキャナー管理変数` |
| 1000 | `// ★ バグ修正: 未定義だった isSwapping を削除` |
| 1304 | `// ★ 修正：縦スライドの感度を1.5倍に引き上げ、より動かしやすく` |
| 1598 | `// ★ 追加：スキャナーが来る前の予兆演出` |
| 1699 | `// ★ 予兆演出を背面に描画` |
| 1826 | `// =====================================================` |
| 1835 | `// =====================================================` |
| 1890 | `// ---- 操作ヒントの自動消去 ----` |

## 定数（調整つまみ）

| 行 | 定義 |
|---:|---|
| 258 | `const SECTORS = 12` |
| 259 | `const SCALE_FACTOR = 1.25` |
| 262 | `const MIN_R = -12` |
| 263 | `const MAX_R = 9` |
| 264 | `const TOTAL_R = MAX_R - MIN_R + 1` |
| 266 | `const THEMES = { … }` |
| 275 | `const THEME_KEYS = Object.keys(THEMES)` |
| 276 | `const WAVE_TYPES = ['DEPTH', 'REVERSE', 'SPIRAL', 'SWEEP', 'NOISE']` |
| 286 | `const TURNS_PER_CHECK = 3` |
| 287 | `const START_COLOR_COUNT = 3` |
| 288 | `const MAX_COLOR_COUNT = 6` |
| 289 | `const AMBIENT_EXPANSION_SPEED = 0.0015` |
| 290 | `const CLEAR_FADE_DURATION = 920` |
| 291 | `const REFILL_CHAIN_CHANCE = 0.10` |
| 292 | `const MAX_JUDGEMENT_CHAINS = 3` |
| 293 | `const FALL_MOVE_DURATION = 1560` |
| 294 | `const CHARGE_MOVE_DURATION = 1470` |
| 295 | `const CHARGE_START_INTERVAL = 85` |
| 322 | `const WAVE_DURATION = 1500` |
| 326 | `const THEME_CHANGE_SCORE_THRESHOLD = Number.POSITIVE_INFINITY` |
| 1836 | `const PORTAL_GAME_ID = 'fractas'` |
| 1841 | `const SEND_THROTTLE_MS = 10000` |

## 関数（62 個）

| 行 | 関数 |
|---:|---|
| 364 | `function cellKey(r, s)` |
| 368 | `function getI(r)` |
| 369 | `function getR(i)` |
| 371 | `function resize()` |
| 385 | `function updateUI()` |
| 397 | `function updateTurnUI()` |
| 410 | `function startAudio()` |
| 459 | `function playTone(freq, duration = 0.18, type = 'sine', volume = 0.08, attack = 0.01, filterFreq = 2600)` |
| 479 | `function playGlide(startFreq, endFreq, duration, type, volume)` |
| 496 | `function playMoveSfx()` |
| 501 | `function playDialTickSfx(step = 0)` |
| 508 | `function playReserveSfx(count = 1)` |
| 515 | `function playScanSfx()` |
| 521 | `function playClearSfx(blockCount, chainMultiplier = 1)` |
| 528 | `function playVanishSfx(blockCount = 1)` |
| 536 | `function playLightSfx(cell)` |
| 546 | `function playChargeSfx(count)` |
| 555 | `function playGameOverSfx()` |
| 560 | `function pickSpeechVoice()` |
| 577 | `function speakTurnPrompt(remaining)` |
| 595 | `function endGame()` |
| 614 | `function addClearScore(blockCount, chainMultiplier)` |
| 621 | `function clearLockedVisuals()` |
| 630 | `function markCellLit(cell, time)` |
| 639 | `function refreshReservedMatches()` |
| 661 | `function setBlocksToClear(cells)` |
| 667 | `function clearBlocksToClear()` |
| 673 | `function advanceChargeColor()` |
| 678 | `function startTurnCheck()` |
| 694 | `function finishTurnCheck()` |
| 708 | `function triggerTurnPrompt()` |
| 719 | `function completePlayerTurn()` |
| 729 | `function triggerThemeChange()` |
| 751 | `function lerpColor(c1, c2, t)` |
| 763 | `function pseudoRandom(r, s)` |
| 768 | `function getColorString(r, s, colorIdx, lightnessMultiplier = 1.0)` |
| 805 | `function getColorAt(r, s)` |
| 811 | `function createsMatch(targetR, targetS, color)` |
| 829 | `function createsMatchInSim(simBoard, targetR, targetS, color)` |
| 845 | `function getSafeColorIdx(r, s)` |
| 853 | `function getChainFriendlyColor(simBoard, r, s)` |
| 865 | `function resetGame()` |
| 944 | `function isBusy()` |
| 948 | `function boardShiftOutward()` |
| 999 | `function applyGravityAnimated()` |
| 1080 | `function findMatchesGroups()` |
| 1125 | `function resolveAllMatches()` |
| 1194 | `function getGridFromPos(x, y)` |
| 1214 | `function onPointerDown(e)` |
| 1242 | `function onPointerMove(e)` |
| 1320 | `function onPointerUp(e)` |
| 1423 | `function update(dt)` |
| 1545 | `function buildBlockPath(r, s, additionalAngleOffset = 0, additionalRadiusOffset = 0)` |
| 1568 | `function getAnimatedBlockPathInfo(animObj)` |
| 1599 | `function drawScannerWaitEffect()` |
| 1619 | `function drawScanner()` |
| 1651 | `function drawTurnPrompt()` |
| 1695 | `function draw()` |
| 1809 | `function gameLoop(timestamp)` |
| 1821 | `function updateScoreUI()` |
| 1843 | `function reportScore(force)` |
| 1893 | `function dismissHint()` |

## DOM の id（HTML の部品）

| 行 | id |
|---:|---|
| 219 | `#uiLayer` |
| 221 | `#scoreVal` |
| 222 | `#chainContainer` |
| 222 | `#chainVal` |
| 225 | `#turnContainer` |
| 225 | `#turnVal` |
| 225 | `#turnMaxVal` |
| 226 | `#colorContainer` |
| 226 | `#colorCountVal` |
| 227 | `#themeContainer` |
| 227 | `#themeVal` |
| 231 | `#gameCanvas` |
| 233 | `#brand` |
| 235 | `#hint` |
| 246 | `#gameOver` |
| 248 | `#finalScoreVal` |

## 画面に出る文字（翻訳するならここ）

| 行 | 文字 | 場所 |
|---:|---|---|
| 8 | Fractas | HTML |
| 221 | SCORE: | HTML |
| 222 | CHAIN!! | HTML |
| 225 | TURNS: | HTML |
| 226 | COLORS: | HTML |
| 227 | THEME: | HTML |
| 227 | COSMIC | HTML |
| 233 | FRACTAS | HTML |
| 236 | FRACTAS | HTML |
| 238 | ↻ Drag around — rotate ring | HTML |
| 241 | ↕ Drag in/out — slide sector | HTML |
| 243 | Make 3 moves. If nothing matches, it is game over. | HTML |
| 247 | GAME OVER | HTML |
| 248 | FINAL SCORE: | HTML |
| 249 | No matches found. Tap or click to restart. | HTML |
| 267 | COSMIC | JS |
| 268 | CYBER | JS |
| 269 | TROPICAL | JS |
| 270 | VIVID | JS |
| 271 | SUNSET | JS |
| 272 | NEON | JS |
| 276 | DEPTH | JS |
| 276 | REVERSE | JS |
| 276 | SPIRAL | JS |
| 276 | SWEEP | JS |
| 276 | NOISE | JS |
| 318 | COSMIC | JS |
| 319 | COSMIC | JS |
| 320 | DEPTH | JS |
| 331 | WAIT | JS |
| 582 | One turn left | JS |
| 582 | Judgement | JS |
| 600 | WAIT | JS |
| 713 | SCAN | JS |
| 714 | TURN LEFT | JS |
| 714 | TURNS LEFT | JS |
| 714 | JUDGEMENT | JS |
| 781 | DEPTH | JS |
| 782 | REVERSE | JS |
| 783 | SPIRAL | JS |
| 787 | SWEEP | JS |
| 788 | NOISE | JS |
| 895 | COSMIC | JS |
| 896 | COSMIC | JS |
| 897 | DEPTH | JS |
| 920 | WAIT | JS |
| 1225 | WAIT | JS |
| 1255 | WAIT | JS |
| 1262 | SHIFT | JS |
| 1263 | ROTATE | JS |
| 1267 | ROTATE | JS |
| 1294 | SHIFT | JS |
| 1328 | WAIT | JS |
| 1333 | ROTATE | JS |
| 1370 | SHIFT | JS |
| 1678 | Brush Script MT | JS |
| 1678 | Snell Roundhand | JS |
| 1678 | Apple Chancery | JS |
| 1678 | Segoe Script | JS |
| 1683 | SCAN | JS |
| 1686 | Brush Script MT | JS |
| 1686 | Snell Roundhand | JS |
| 1686 | Apple Chancery | JS |
| 1686 | Segoe Script | JS |
| 1708 | ROTATE | JS |
| 1710 | ROTATE | JS |
| 1716 | SHIFT | JS |
| 1718 | SHIFT | JS |

読み上げの文は `speakTurnPrompt` の中にある（ラジアル版）。

## 端末に保存するキー（localStorage）

- なし

## イベント（入力・ページの出入り）

| 対象:イベント | 行 |
|---|---|
| `canvas:mousedown` | 1414, 1899 |
| `canvas:mousemove` | 1415 |
| `canvas:touchmove` | 1418 |
| `canvas:touchstart` | 1417, 1900 |
| `gameOverEl:click` | 1905 |
| `gameOverEl:touchstart` | 1906 |
| `window:blur` | 1880 |
| `window:mouseup` | 1416 |
| `window:pagehide` | 1879 |
| `window:resize` | 382 |
| `window:touchend` | 1419 |
| `window:visibilitychange` | 1876 |

## 親（ポータル）へ送るメッセージ

- type: `SCORE_UPDATE`
- metadata.mode: `turn3`

