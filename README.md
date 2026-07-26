# Fractas

A turn-based **radial match‑3** score game. The board is a polar grid of 12 sectors
and concentric rings that slowly expand outward from a central core. Rotate a ring
or slide a sector to line up **3+ same‑colored** blocks. Every 3 valid moves, the
scanner judges the board. If at least one match exists, matched blocks are cleared,
score is awarded, gravity refills the board, and the next 3-move cycle begins. If no
matches exist at judgement time, the run ends immediately. Each successful judgement
adds one color to newly charged/refilled blocks (3 colors at start, up to 6).
Only matched/reserved blocks glow, so the light art directly shows the scoring
opportunities while idle block colors remain stable and readable. During judgement,
the extra-slow scanner lights blocks as the ring passes them; those blocks then dim
and fade out before gravity refills the board. Refills can occasionally create capped
follow-up chains. Block outlines are intentionally removed for a cleaner color-field
look. Newly charged blocks now arrive one by one with a staged in-cell charge
animation that avoids overlapping refill blocks, paired with a procedural ambient soundtrack and soft Web Audio SFX for
moves, dial-like rotation ticks, match reservation, scans, clears, refills, and game
over. Rotation and radial slides use quieter high-frequency tick feedback, lit blocks
get a small musical sparkle, and remaining turns are spoken in English with the
browser's speech synthesis, preferring a female-style English voice when available.

The in-game HUD is intentionally minimal: only the score remains visible during play.

Single self‑contained HTML5 canvas game — no build step, no dependencies. Works on
desktop (mouse) and mobile (touch).

---

## Controls

| Gesture | Action |
|--------|--------|
| Drag **around** the center | Rotate the ring you grabbed |
| Drag **toward / away** from the center | Slide that sector in/out |
| Every 3 valid moves | Scanner judgement starts |
| Tap/click after GAME OVER | Start a fresh run |

An auto‑dismissing hint overlay explains this on first load.

---

## Project structure

```
Fractas/
├── index.html            # Canonical game source (playable standalone)
├── README.md
└── assets/
    ├── thumbnail.jpg          # 1280×720 portal thumbnail (radial art)
    ├── fractas-preview.mp4     # ~15s gameplay clip (H.264, web-ready)
    └── fractas-preview.webm    # ~15s gameplay clip (VP9)
```

`index.html` is the **single source of truth**. The copy deployed to the game portal
lives at `hiroakiishibashi-web/games/fractas/game/index.html` and must be kept in sync
(see below).

---

## Portal integration (hiroakiishibashi.com)

Published on the personal game portal as a browser ("Play Now") game with a Supabase
score leaderboard.

- **game_id:** `fractas`
- **Wrapper page:** `hiroakiishibashi-web/games/fractas/index.html`
  (iframe + login prompt + TOP 5 + full‑ranking modal — adapted from the Block Slide wrapper)
- **Game iframe:** `hiroakiishibashi-web/games/fractas/game/index.html` (copy of this `index.html`)
- **Thumbnail:** `hiroakiishibashi-web/assets/games/fractas.jpg`
- **Preview video:** `hiroakiishibashi-web/assets/games/fractas-preview.{mp4,webm}`

### Score reporting (leaderboard)

The game stays fully playable standalone. When embedded as an `<iframe>` it streams the
score to the parent portal via `postMessage`, matching the portal's existing protocol:

```js
window.parent.postMessage({
  type: 'SCORE_UPDATE',
  game: 'fractas',
  score: <int>,
  metadata: {
    theme: '<current theme>',
    mode: 'turn3',
    turnsPerCheck: 3,
    turns: <int>,
    checks: <int>,
    colorCount: <int>
  }
}, '*');
```

The portal wrapper listens for `SCORE_UPDATE`, and (if the user is logged in) calls
`saveScore('fractas', score, metadata)` → Supabase `plays`/`scores` tables. The
leaderboard takes the **max score per user**.

Because Fractas is now turn-based, there is no countdown timer. The game throttles
in-play updates to **once per ~10s** and always sends the final score on game over. It
also sends on `visibilitychange`/`pagehide`/`blur` so partial scores are captured if the
player leaves early.

**Standalone / external hosting (SDK):** when the game is *not* embedded in the portal
(`window.parent === window`), it lazy-loads the official
[`HiroakiSDK`](https://hiroakiishibashi.com/sdk/html/hiroakiishibashi-sdk.js) and routes
the same score through `sdk.saveScore()` (direct Supabase). The SDK is **only** loaded in
this case, so the embedded portal path is byte-for-byte unchanged (and incurs no extra
request). Cross-origin import of the SDK is enabled by the `/sdk/*` CORS rule in the
portal's `_headers` file. If the SDK can't load, scoring degrades gracefully (the game
still plays; a single console warning is logged).

### Registered in

- `index.html` — Games grid card
- `js/user-ui.js` — `GAMES` registry + `GAME_LABELS_FOR_CARD`
- `js/i18n.js` — `game.fractas.desc`, `game.fractas.how`, `tag.arcade` (EN + JA)
- `leaderboard/index.html` — game tab

### Sync command (dev → portal)

After editing the canonical `index.html`, copy it into the portal:

```bash
cp /Volumes/PINK/Development/Fractas/index.html \
   /Volumes/PINK/Development/hiroakiishibashi-web/games/fractas/game/index.html
```

---

## Run locally

```bash
npx serve -l 3459 /Volumes/PINK/Development/Fractas
# → http://localhost:3459
```

(Also registered as the `fractas` config in `/Volumes/PINK/Development/.claude/launch.json`.)

---

## Notes / ideas for later

- Current mode is a 3-turn judgement loop. Tuning knobs: `TURNS_PER_CHECK`,
  `START_COLOR_COUNT`, and `MAX_COLOR_COUNT`.
- Cloud‑save (resume best score / theme) could be added via the portal's
  `GAME_REQUEST_RESTORE` / `GAME_SAVE_DATA` protocol — see
  `hiroakiishibashi-web/docs/cloud-save-spec.md`.
- Could be submitted to CrazyGames / Playgama later (add their SDK + a `Playgama_Config.json`).
