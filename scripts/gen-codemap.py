#!/usr/bin/env python3
"""Fractas の index.html から、コードの索引を Markdown で出す（機械生成）。

使い方:
  python3 scripts/gen-codemap.py origin/portal-radial > docs/codemap/portal-radial.md
  python3 scripts/gen-codemap.py origin/main          > docs/codemap/main.md

出すもの: 区切りの目印・定数（調整つまみ）・関数・DOM の id・画面に出る文字・
          端末に保存するキー・イベント・親へ送るメッセージ。
行番号は、その版の index.html のもの。コードを直したら作り直すこと。
"""
import os
import re
import subprocess
import sys

ref = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=True).stdout


src = git('show', f'{ref}:index.html')
sha = git('rev-parse', '--short', ref).strip()
lines = src.split('\n')
if lines and lines[-1] == '':
    lines = lines[:-1]


def cell(s):
    return s.replace('|', '\\|').strip()


kind = 'ラジアル版（ターン制）' if 'TURNS_PER_CHECK' in src else ('正方形版' if 'GRID_LIMIT' in src else '不明')
out = [
    f'# コード索引 — `{ref}`（{sha}・{kind}）',
    '',
    f'> 機械生成: `python3 scripts/gen-codemap.py {ref}`。行番号はこの版の `index.html`（全 {len(lines)} 行）のもの。',
    '> 手で直さない。コードを直したら作り直す。流れの説明は [../CODEMAP.md](../CODEMAP.md)。',
    '',
]

# 大きな区切り
# ゲームの <script> = <body> より後にある最初の <script>（<head> の言語SDKの <script> と取り違えない）
body_line = next((i for i, l in enumerate(lines, 1) if re.search(r'<body>', l)), 0)
script_line = next((i for i, l in enumerate(lines, 1) if i > body_line and re.match(r'^\s*<script>\s*$', l)), None)
marks = [('<head>', r'<head>'), ('<style>', r'<style>'), ('<body>', r'<body>'),
         ('</body>', r'</body>')]
out += ['## ファイルの区切り', '', '| 行 | 区切り |', '|---:|---|']
rows = []
for label, pat in marks:
    n = next((i for i, l in enumerate(lines, 1) if re.search(pat, l)), None)
    if n:
        rows.append((n, label))
if script_line:
    rows.append((script_line, 'ゲームの <script>（ここから下がゲームの JS）'))
out += [f'| {n} | `{cell(label)}` |' for n, label in sorted(rows)]
out.append('')

# コメントの目印
cm = [(i, l.strip()) for i, l in enumerate(lines, 1)
      if re.match(r'^\s*//\s*(-{2,}|={3,}|★|【|■)', l) or re.match(r'^\s*//\s*[A-Za-z].*(-{3,}|={3,})\s*$', l)]
if cm:
    out += ['## コメントの目印', '', '| 行 | コメント |', '|---:|---|']
    out += [f'| {i} | `{cell(t)[:110]}` |' for i, t in cm]
    out.append('')

# 定数
consts = [(i, l.strip()) for i, l in enumerate(lines, 1) if re.match(r'^\s{8}const [A-Z][A-Z0-9_]+ = ', l)]
out += ['## 定数（調整つまみ）', '', '| 行 | 定義 |', '|---:|---|']
for i, l in consts:
    l = re.sub(r'\s*//.*$', '', l).rstrip(';').rstrip()
    if l.endswith('{'):
        l += ' … }'
    out.append(f'| {i} | `{cell(l)[:120]}` |')
out.append('')

# 関数
funcs = [(i, re.sub(r'\s*\{.*$', '', l.strip())) for i, l in enumerate(lines, 1)
         if re.match(r'^\s{8}(async )?function [A-Za-z0-9_]+\(', l)]
out += [f'## 関数（{len(funcs)} 個）', '', '| 行 | 関数 |', '|---:|---|']
out += [f'| {i} | `{cell(f)[:120]}` |' for i, f in funcs]
out.append('')

# DOM の id
ids = []
for i, l in enumerate(lines, 1):
    for m in re.findall(r'id="([A-Za-z0-9_-]+)"', l):
        ids.append((i, m))
out += ['## DOM の id（HTML の部品）', '', '| 行 | id |', '|---:|---|']
out += [f'| {i} | `#{m}` |' for i, m in ids]
out.append('')

# 画面に出る文字
texts = []
end = script_line or len(lines)
for i, l in enumerate(lines[:end], 1):
    if '<style' in l or re.match(r'^\s*[.#@a-z-]+[^<>]*\{', l):
        continue
    for t in re.findall(r'>([^<>{}]*[A-Za-z][^<>{}]*)<', l):
        t = t.strip()
        if t and not t.startswith('//'):
            texts.append((i, t, 'HTML'))
for i, l in enumerate(lines, 1):
    if script_line and i <= script_line:
        continue
    for m in re.findall(r"['`]([A-Z][A-Za-z !?.,:]{2,}[A-Za-z!?.])['`]", l):
        if re.fullmatch(r'[A-Z_]+', m) and '_' in m:
            continue
        texts.append((i, m, 'JS'))
seen = set()
texts = [t for t in texts if not ((t[0], t[1]) in seen or seen.add((t[0], t[1])))]
out += ['## 画面に出る文字（翻訳するならここ）', '', '| 行 | 文字 | 場所 |', '|---:|---|---|']
out += [f'| {i} | {cell(t)[:100]} | {w} |' for i, t, w in texts]
out += ['', '読み上げの文は `speakTurnPrompt` の中にある（ラジアル版）。', '']

# 端末に保存するキー
ls = sorted(set(re.findall(r"localStorage\.(?:get|set|remove)Item\('([^']+)'", src)))
out += ['## 端末に保存するキー（localStorage）', '']
out += [f'- `{k}`' for k in ls] if ls else ['- なし']
out.append('')

# イベント
ev = {}
for i, l in enumerate(lines, 1):
    for t, e in re.findall(r"([A-Za-z]+)\.addEventListener\('([a-z]+)'", l):
        ev.setdefault(f'{t}:{e}', []).append(i)
out += ['## イベント（入力・ページの出入り）', '', '| 対象:イベント | 行 |', '|---|---|']
out += [f'| `{k}` | {", ".join(map(str, v))} |' for k, v in sorted(ev.items())]
out.append('')

# 親へ送るメッセージ
pm = sorted(set(re.findall(r"type:\s*'([A-Z_]+)'", src)))
modes = sorted(set(re.findall(r"mode:\s*'([a-z0-9_]+)'", src)))
out += ['## 親（ポータル）へ送るメッセージ', '']
out += [f'- type: `{p}`' for p in pm] or ['- なし']
out += [f'- metadata.mode: `{m}`' for m in modes]
out.append('')

sys.stdout.write('\n'.join(out) + '\n')
