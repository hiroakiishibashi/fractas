# 🎮 GAME DEVELOPMENT MEMORY & HANDOVER DOCUMENT
**Project**: Fractas (フラクタス)  
**Author**: Hiroaki Ishibashi (@hiroakiishibashi)  
**Last Updated**: 2026-07-26  

---

## 💻 1. Target Hardware & Environment Philosophy
- **Device**: MacBook Pro (13-inch, Late 2011)
  - CPU: Intel Core i5 (2.4 GHz Dual-Core)
  - RAM: 8 GB
  - OS: macOS Monterey 12.7.6
- **Core Philosophy**: **"High-performance & silky-smooth operation even on legacy 2011 Macs"**
  - Lightweight HTML5 Canvas architectures.
  - Offloading heavy AI tasks to cloud APIs (Gemini 2.5 Flash / Claude 3.5 Sonnet).

---

## 🛠️ 2. Installed Tools & Developer Stack
- **Node.js**: `v20.18.0 (LTS)` (`~/node/bin/node`)
- **Python**: `3.12.13` via `uv` (`~/.local/bin/python3`)
- **Aider AI CLI**: `v0.86.2` (`~/.local/bin/aider` / alias `ai`)
- **VS Code**: `v1.130.0` (`/Applications/Visual Studio Code.app`, CLI `code`)
  - Installed Extensions: Japanese Language Pack (`ms-ceintl.vscode-language-pack-ja`), Continue (`continue.continue`)
- **GitHub CLI**: `v2.96.0` (`~/.local/bin/gh`) — Authenticated for `@hiroakiishibashi`
- **Shell & Prompt**: Zsh with `Starship 1.26.0`, `bat`, `fzf`
- **Productivity**: `Raycast.app`, Google Japanese Input

---

## 🎲 3. Active Game Project: Fractas (フラクタス)

### 📌 Repositories & Locations
- **GitHub Repo**: [`hiroakiishibashi/fractas`](https://github.com/hiroakiishibashi/fractas) (Public)
- **Local Path**: `/Users/hiroakiishibashi/Projects/fractas`
- **Published Live Game (GitHub Pages)**: 👉 **[https://hiroakiishibashi.github.io/fractas/](https://hiroakiishibashi.github.io/fractas/)**

### 🧩 Game Concept & Mechanics
- **Genre**: Turn-based Radial Match-3 Puzzle Game (HTML5 Canvas, Single-file `index.html`).
- **Board Structure**: Polar grid consisting of 12 sectors and concentric expanding rings.
- **Rules**:
  - Drag around to rotate rings; drag toward/away from center to slide sectors.
  - Judgement occurs every 3 valid moves (scanner sweeps the board).
  - 3+ matching colored blocks are cleared, awarding scores and triggering gravity refills.
  - Game over occurs if no matches are found during a judgement check.

---

## ⚡ 4. Applied Performance Optimizations (Turbo Optimizations)
1. **Capped Resolution Scale**: Set `dpr = Math.min(1.0, window.devicePixelRatio)` in `resize()` to prevent 4x-8x Retina over-rendering.
2. **Removed Heavy CSS Blur**: Removed `backdrop-filter: blur(...)` to eliminate Metal GPU composition bottlenecks on Intel HD 3000.
3. **Disabled ShadowBlur Computation**: Set `ctx.shadowBlur = 0` in per-frame rendering loops to drastically reduce CPU overhead.

---

## 🚀 5. Quick Commands for Next Session

```bash
# Navigate to game project
cd ~/Projects/fractas

# Open in VS Code
code .

# Run local web server (when testing)
python3 -m http.server 3459
# Open in browser: http://localhost:3459

# Commit & Push changes to GitHub & GitHub Pages
git add .
git commit -m "Update game feature"
git push
```
