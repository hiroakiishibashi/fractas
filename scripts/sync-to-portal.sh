#!/usr/bin/env bash
# ============================================================
# fractas リポジトリの版を、ポータル（hiroakiishibashi-web）のクローンへ写す。
# ⚠️ 写すだけ。コミット・push・マージはしない（それは docs/RUNBOOK.md R2 の 6）。
#
#   bash scripts/sync-to-portal.sh <hiroakiishibashi-web のクローン> [--from <ref>] [--dry-run] [--i-have-owner-approval]
#
#   --from <ref>               写す元。既定は portal-radial（＝公開中の系統）。main は正方形版
#   --dry-run                  何が変わるかを見るだけ（何も書き換えない）
#   --i-have-owner-approval    公開中と別の「版」（ラジアル ⇔ 正方形）に入れ替えるときだけ付ける
#
# 安全装置:
#   ・版が入れ替わるときは、--i-have-owner-approval が無ければ止まる（docs/DECISIONS.md D1）
#   ・写す元の hi-game-lang.js がポータルの SDK と1バイトでも違えば止まる（→ RUNBOOK R4）
# ============================================================
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WEB=""; FROM="portal-radial"; DRY=0; APPROVED=0
while [ $# -gt 0 ]; do
  case "$1" in
    --from) FROM="${2:?--from には ref が要ります}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --i-have-owner-approval) APPROVED=1; shift ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *) WEB="$1"; shift ;;
  esac
done
[ -n "$WEB" ] || { echo "使い方: bash scripts/sync-to-portal.sh <hiroakiishibashi-web のクローン> [--from <ref>] [--dry-run]"; exit 2; }
if [ ! -d "$WEB/games/fractas/game" ] || [ ! -f "$WEB/sdk/html/hi-game-lang.js" ]; then
  echo "✗ $WEB は hiroakiishibashi-web のクローンに見えません"; exit 2
fi
case "$(cd "$WEB" && pwd)" in
  /Volumes/PINK/Development/hiroakiishibashi-web)
    echo "✗ PINK の hiroakiishibashi-web は中身が不整合なので使いません（docs/PITFALLS.md P8）。新しくクローンしてください（RUNBOOK R0-2）"; exit 2 ;;
esac

git -C "$REPO" fetch -q origin --tags
if git -C "$REPO" rev-parse -q --verify "origin/$FROM" >/dev/null; then FROM="origin/$FROM"; fi
git -C "$REPO" rev-parse -q --verify "$FROM^{commit}" >/dev/null || { echo "✗ $FROM が見つかりません"; exit 2; }

DEST="$WEB/games/fractas/game"
TMP="$REPO/.tmp-sync"; rm -rf "$TMP"; mkdir -p "$TMP"; trap 'rm -rf "$TMP"' EXIT
git -C "$REPO" show "$FROM:index.html" > "$TMP/index.html"
if ! git -C "$REPO" show "$FROM:hi-game-lang.js" > "$TMP/hi-game-lang.js" 2>/dev/null; then
  echo "✗ $FROM に hi-game-lang.js がありません（言語SDKを配線する前の版です）"; exit 2
fi

kind() { if grep -q TURNS_PER_CHECK "$1"; then echo radial; elif grep -q GRID_LIMIT "$1"; then echo square; else echo unknown; fi; }
now="$(kind "$DEST/index.html")"; new="$(kind "$TMP/index.html")"
echo "写す元: $FROM ($(git -C "$REPO" rev-parse --short "$FROM")) … $new"
echo "写す先: $DEST … いまは $now"

if [ "$now" != "$new" ] && [ "$APPROVED" -ne 1 ]; then
  echo "✗ 版が入れ替わります（$now → $new）。公開中のゲームとランキングが別物になります。"
  echo "  オーナーの了承を得てから --i-have-owner-approval を付けて、もう一度実行してください（docs/DECISIONS.md D1）。"
  exit 3
fi
if ! cmp -s "$TMP/hi-game-lang.js" "$WEB/sdk/html/hi-game-lang.js"; then
  echo "✗ $FROM の hi-game-lang.js が、ポータルの SDK（sdk/html/hi-game-lang.js）と違います。"
  echo "  先に fractas 側の hi-game-lang.js を最新の SDK に置き換えてコミットしてください（docs/RUNBOOK.md R4）。"
  exit 4
fi
if cmp -s "$TMP/index.html" "$DEST/index.html" && cmp -s "$TMP/hi-game-lang.js" "$DEST/hi-game-lang.js"; then
  echo "✅ すでに同じです。写すものはありません。"; exit 0
fi
if [ "$DRY" -eq 1 ]; then
  echo "--- dry-run（何も書き換えていません）---"
  n="$(diff "$DEST/index.html" "$TMP/index.html" | grep -c '^[<>]' || true)"
  echo "index.html: 変わる行 ${n}"
  cmp -s "$TMP/hi-game-lang.js" "$DEST/hi-game-lang.js" || echo "hi-game-lang.js: 変わる"
  exit 0
fi

cp "$TMP/index.html" "$DEST/index.html"
cp "$TMP/hi-game-lang.js" "$DEST/hi-game-lang.js"
echo "✅ 写しました。言語の検査を走らせます…"
( cd "$WEB" && node tools/test-game-lang.mjs | tail -2 )
echo ""
echo "次の手順（ポータルのクローンで。docs/RUNBOOK.md R2 の 6〜7）:"
echo "  cd $WEB"
echo "  git switch -c claude/fractas-<何をしたか>"
echo "  git add games/fractas/game/index.html games/fractas/game/hi-game-lang.js    # git add -A は使わない"
echo "  git commit -m 'Fractas: <何をしたか>'"
echo "  git fetch origin && git merge origin/main && git push -u origin HEAD"
echo "  gh pr create --fill && gh pr merge --merge    # マージ＝公開"
