#!/usr/bin/env bash
# ============================================================
# Fractas の「いまの状態」を1コマンドで確かめる（読み取り専用。何も書き換えない）
#
#   bash scripts/status.sh
#
# 見るもの: ① このリポジトリ ② 本番ポータル ③ 言語SDKの同梱コピー ④ GitHub Pages
# 結果の読み方: docs/HANDOFF.md の「0. 30秒でわかる現状」と見比べる
# ============================================================
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CB="$RANDOM$RANDOM"
PORTAL_GAME="https://hiroakiishibashi.com/games/fractas/game/"
PORTAL_PAGE="https://hiroakiishibashi.com/games/fractas/"
PAGES="https://hiroakiishibashi.github.io/fractas/"
SDK_URL="https://hiroakiishibashi.com/sdk/html/hi-game-lang.js"
TMP="$REPO/.tmp-status"                      # .gitignore の .tmp-*/ に入る
rm -rf "$TMP"; mkdir -p "$TMP"; trap 'rm -rf "$TMP"' EXIT

ok()   { printf '  ✅ %s\n' "$*"; }
warn() { printf '  ⚠️  %s\n' "$*"; }
info() { printf '  ・ %s\n' "$*"; }
kind() {                                     # ファイルがどちらの版か
  if grep -q 'TURNS_PER_CHECK' "$1" 2>/dev/null; then echo "ラジアル版(ターン制)"
  elif grep -q 'GRID_LIMIT' "$1" 2>/dev/null; then echo "正方形版"
  else echo "不明"; fi
}

echo "== 1. リポジトリ hiroakiishibashi/fractas =="
git -C "$REPO" fetch -q origin --tags 2>/dev/null || warn "fetch に失敗（ネットワーク、または PINK の git の不具合 → docs/PITFALLS.md P7）"
for ref in origin/main origin/portal-radial; do
  name="${ref#origin/}"
  if git -C "$REPO" rev-parse -q --verify "$ref" >/dev/null; then
    git -C "$REPO" show "$ref:index.html" > "$TMP/$name.html" 2>/dev/null
    info "$ref = $(git -C "$REPO" rev-parse --short "$ref") … $(kind "$TMP/$name.html")"
  else
    warn "$ref が見つからない（git fetch origin を試す）"
  fi
done
info "いまのブランチ: $(git -C "$REPO" branch --show-current 2>/dev/null)（ふだんは main）"
[ -n "$(git -C "$REPO" status --porcelain 2>/dev/null)" ] && warn "手元に未コミットの変更がある（git status で確かめる）"
WT="/Volumes/PINK/Development/Fractas-portal-radial"
if [ -d "$WT" ]; then
  info "直すフォルダ: $WT（ブランチ $(git -C "$WT" branch --show-current 2>/dev/null)）"
  [ -n "$(git -C "$WT" status --porcelain 2>/dev/null)" ] && warn "直すフォルダに未コミットの変更がある"
  ahead="$(git -C "$WT" rev-list --count origin/portal-radial..HEAD 2>/dev/null || echo 0)"
  [ "${ahead:-0}" != "0" ] && warn "直すフォルダに push していないコミットが ${ahead} 件"
else
  info "直すフォルダ $WT は無い（docs/RUNBOOK.md の R0-3 で作る）"
fi
live_tag="$(git -C "$REPO" tag -l 'portal-live-*' --sort=-creatordate 2>/dev/null | head -1)"
[ -n "$live_tag" ] && info "いちばん新しい公開のしるし: $live_tag"

echo "== 2. 本番ポータル =="
if curl -fsSL "$PORTAL_GAME?cb=$CB" -o "$TMP/live.html" 2>/dev/null; then
  info "公開中のゲーム: $(kind "$TMP/live.html")（$(wc -c < "$TMP/live.html" | tr -d ' ') bytes）"
  if grep -q "HiLang.init({ id: 'fractas'" "$TMP/live.html"; then ok "言語SDKの配線あり"; else warn "言語SDKの配線が見当たらない"; fi
  if [ -f "$TMP/portal-radial.html" ]; then
    if cmp -s "$TMP/live.html" "$TMP/portal-radial.html"; then ok "公開中 = portal-radial（完全一致）"
    else warn "公開中と portal-radial が違う（どちらかが更新された。git log と hiroakiishibashi-web の PR を確かめる）"; fi
  fi
else
  warn "本番のゲームを取得できない（ネットワーク？）"
fi
code="$(curl -s -o /dev/null -w '%{http_code}' "$PORTAL_PAGE?cb=$CB")"
if [ "$code" = "200" ]; then ok "ポータルのページ 200"; else warn "ポータルのページ HTTP $code"; fi

echo "== 3. 言語SDKの同梱コピー =="
if curl -fsSL "$SDK_URL?cb=$CB" -o "$TMP/sdk.js" 2>/dev/null; then
  if git -C "$REPO" show origin/main:hi-game-lang.js > "$TMP/main-sdk.js" 2>/dev/null && cmp -s "$TMP/sdk.js" "$TMP/main-sdk.js"; then ok "main の hi-game-lang.js = 本番の SDK"
  else warn "main の hi-game-lang.js が本番の SDK と違う（SDK が更新された → docs/RUNBOOK.md R4）"; fi
  if git -C "$REPO" show origin/portal-radial:hi-game-lang.js > "$TMP/pr-sdk.js" 2>/dev/null && cmp -s "$TMP/sdk.js" "$TMP/pr-sdk.js"; then ok "portal-radial の hi-game-lang.js = 本番の SDK"
  else warn "portal-radial の hi-game-lang.js が本番の SDK と違う（→ R4）"; fi
  if curl -fsSL "${PORTAL_GAME}hi-game-lang.js?cb=$CB" -o "$TMP/live-sdk.js" 2>/dev/null && cmp -s "$TMP/sdk.js" "$TMP/live-sdk.js"; then ok "本番ゲームの同梱コピー = 本番の SDK"
  else warn "本番ゲームの同梱コピーが SDK とずれている（→ R4 のあと R2 の 5〜7）"; fi
else
  warn "本番の SDK を取得できない"
fi

echo "== 4. GitHub Pages（main をそのまま配信） =="
if curl -fsSL "$PAGES?cb=$CB" -o "$TMP/pages.html" 2>/dev/null; then
  info "Pages: $(kind "$TMP/pages.html")"
  if [ -f "$TMP/main.html" ]; then
    if cmp -s "$TMP/pages.html" "$TMP/main.html"; then ok "Pages = origin/main"
    else info "Pages と origin/main が違う（push 直後なら1〜2分待つ）"; fi
  fi
else
  warn "GitHub Pages を取得できない（止めた？ → DECISIONS D5）"
fi

echo ""
echo "読み方: docs/HANDOFF.md の「0. 30秒でわかる現状」と見比べてください。⚠️ はその行の説明どおりに調べます。"
