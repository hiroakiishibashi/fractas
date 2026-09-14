#!/usr/bin/env python3
"""docs/*.md を1枚の HTML（docs/handoff.html）にまとめる。

正本は .md。HTML はここから作る（手で直さない）。

  python3 scripts/build-handoff-html.py                      # docs/handoff.html（完全な HTML 文書）
  python3 scripts/build-handoff-html.py --fragment <出力先>   # claude.ai アーティファクト用の断片も作る

必要なもの: python-markdown（無ければ `pip3 install markdown`）。
無い環境では、ポータルの道具でも作れる: `node <ポータルのクローン>/tools/build-handoff-html.mjs <.md のあるフォルダ>`
"""
import html
import json
import math
import os
import re
import sys
import datetime

try:
    import markdown
    from markdown.extensions.toc import slugify_unicode
except ImportError:
    sys.exit('python-markdown がありません: pip3 install markdown')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
REPO_URL = 'https://github.com/hiroakiishibashi/fractas/blob/main/'
ORDER = [
    ('HANDOFF.md', '引き継ぎ書'),
    ('RUNBOOK.md', '手順書'),
    ('PITFALLS.md', '踏んだ罠'),
    ('DECISIONS.md', '決まったこと・判断待ち'),
    ('PROMPTS.md', '貼る文'),
    ('CODEMAP.md', 'コードの地図'),
    ('codemap/portal-radial.md', '索引: 公開中のラジアル版'),
    ('codemap/main.md', '索引: main（正方形版）'),
    ('HISTORY.md', '年表'),
]


def key(path):
    return 'doc-' + re.sub(r'[^a-z0-9]+', '-', path.lower().replace('.md', '')).strip('-')


def rewrite_links(h, current):
    def repl(m):
        href = m.group(1)
        if href.startswith(('http://', 'https://', '#', 'mailto:')):
            return m.group(0)
        path, _, frag = href.partition('#')
        base = os.path.normpath(os.path.join(os.path.dirname(current), path)).replace(os.sep, '/')
        for p, _ in ORDER:
            if base == p:
                return f'href="#{key(p)}"'
        rel = os.path.normpath(os.path.join('docs', os.path.dirname(current), path)).replace(os.sep, '/')
        return f'href="{REPO_URL}{rel}{("#" + frag) if frag else ""}"'
    return re.sub(r'href="([^"]+)"', repl, h)


def polar_mark():
    # ゲームと同じ数字: 12 セクター、1段ごとに半径 1.25 倍
    c = 32
    rings = []
    r = 3.2
    k = 0
    while r <= 30.5:
        cls = 'scan' if k == 6 else 'ring'
        rings.append(f'<circle class="{cls}" cx="{c}" cy="{c}" r="{r:.2f}"/>')
        r *= 1.25
        k += 1
    spokes = []
    for s in range(12):
        a = s * math.pi * 2 / 12
        x1, y1 = c + 3.2 * math.cos(a), c + 3.2 * math.sin(a)
        x2, y2 = c + 30.2 * math.cos(a), c + 30.2 * math.sin(a)
        spokes.append(f'<line class="spoke" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    return ('<svg class="mark" viewBox="0 0 64 64" role="img" aria-label="12 セクターと 1.25 倍ずつ広がる輪">'
            + ''.join(spokes) + ''.join(rings) + '</svg>')


CSS = r"""
:root{
  --ground:#f4f3f9;--surface:#ffffff;--ink:#1b1930;--muted:#5b5874;--line:#dedbeb;
  --accent:#5b34c9;--accent-soft:#ece6fd;--warn:#8a5300;--warn-soft:#fdf2d6;
  --ok:#1d7a45;--ok-soft:#e3f4ea;--code-bg:#efedf7;--scan:#c28a00;color-scheme:light;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --ground:#0f0d1a;--surface:#17142a;--ink:#ebe8f7;--muted:#a39fbe;--line:#2c2844;
  --accent:#b39cff;--accent-soft:#241c44;--warn:#f5c542;--warn-soft:#2c2410;
  --ok:#62d394;--ok-soft:#10271b;--code-bg:#1c1832;--scan:#facc15;color-scheme:dark;}}
:root[data-theme="dark"]{
  --ground:#0f0d1a;--surface:#17142a;--ink:#ebe8f7;--muted:#a39fbe;--line:#2c2844;
  --accent:#b39cff;--accent-soft:#241c44;--warn:#f5c542;--warn-soft:#2c2410;
  --ok:#62d394;--ok-soft:#10271b;--code-bg:#1c1832;--scan:#facc15;color-scheme:dark;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"BIZ UDPGothic","Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP",system-ui,sans-serif;
  font-size:16px;line-height:1.85;padding-inline:16px}
.masthead{max-width:1180px;margin:0 auto;padding-block:28px 22px;display:flex;gap:18px;align-items:center;border-bottom:1px solid var(--line)}
.mark{width:68px;height:68px;flex:none}
.mark .ring{fill:none;stroke:var(--accent);stroke-width:1;opacity:.7}
.mark .spoke{stroke:var(--accent);stroke-width:.8;opacity:.4}
.mark .scan{fill:none;stroke:var(--scan);stroke-width:2.2}
.brand{min-width:0}
.wordmark{font-family:"Kaushan Script","Brush Script MT","Snell Roundhand",cursive;font-weight:400;
  font-size:clamp(34px,6vw,50px);line-height:1;margin:0;letter-spacing:.01em}
.sub{margin:.4rem 0 0;color:var(--muted);font-size:14px;line-height:1.6}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.chip{display:inline-flex;align-items:center;gap:7px;font-size:13px;line-height:1.45;padding:4px 11px;border-radius:999px;border:1px solid var(--line);background:var(--surface)}
.chip .dot{width:8px;height:8px;border-radius:50%;background:var(--muted);flex:none}
.chip.live{background:var(--ok-soft);border-color:color-mix(in srgb,var(--ok) 40%,var(--line))}
.chip.live .dot{background:var(--ok)}
.chip.hold{background:var(--warn-soft);border-color:color-mix(in srgb,var(--warn) 40%,var(--line))}
.chip.hold .dot{background:var(--warn)}
.chip code{font-size:12px;white-space:nowrap}
.layout{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr);gap:28px;padding-block:24px 56px}
@media (min-width:1080px){.layout{grid-template-columns:250px minmax(0,1fr)}
  .toc{position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto}}
.toc{font-size:14px;line-height:1.6;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;align-self:start}
.toc>summary{font-weight:700;cursor:pointer}
.toc ol{list-style:none;margin:6px 0 0;padding:0}
.toc>ol>li{margin:6px 0}
.toc a{color:var(--ink);text-decoration:none}
.toc a:hover{color:var(--accent);text-decoration:underline}
.toc details{margin:2px 0 0 10px}
.toc details summary{cursor:pointer;color:var(--muted);font-size:12.5px}
.toc details ol{margin:2px 0 4px 6px}
.toc details li{font-size:13px}
article{min-width:0;max-width:48em}
.doc{margin-bottom:56px}
.doc+.doc{border-top:2px solid var(--line);padding-top:30px}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace;font-size:12px;letter-spacing:.05em;color:var(--accent);margin:0}
h1,h2,h3,h4{text-wrap:balance;line-height:1.45;font-weight:700}
h1{font-size:28px;margin:.15em 0 .7em}
h2{font-size:21px;margin:2.2em 0 .6em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
h3{font-size:17px;margin:1.8em 0 .5em}
p,li{overflow-wrap:anywhere}
ul,ol{padding-left:1.4em}
a{color:var(--accent)}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
code{font-family:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace;font-size:.86em;background:var(--code-bg);padding:.08em .35em;border-radius:4px}
pre{position:relative;background:var(--code-bg);border:1px solid var(--line);border-radius:8px;padding:14px 16px;overflow-x:auto;line-height:1.6;font-size:13.5px;margin:1em 0}
pre code{background:none;padding:0;font-size:inherit}
.copy{position:absolute;top:6px;right:6px;font:700 12px/1 "BIZ UDPGothic",system-ui,sans-serif;padding:6px 9px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.copy:hover{border-color:var(--accent);color:var(--accent)}
.tbl{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14.5px;line-height:1.6;font-variant-numeric:tabular-nums}
th,td{padding:8px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
thead th{background:var(--accent-soft);white-space:nowrap}
tbody tr:last-child td{border-bottom:0}
blockquote{margin:1.2em 0;padding:10px 16px;border-left:4px solid var(--warn);background:var(--warn-soft);border-radius:0 8px 8px 0}
blockquote p{margin:.3em 0}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
.foot{max-width:1180px;margin:0 auto;padding-block:20px 40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
@media (max-width:600px){body{font-size:15.5px}h1{font-size:23px}h2{font-size:19px}pre{font-size:12.5px}.mark{width:52px;height:52px}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

JS = r"""
(function () {
  var t = document.querySelector('details.toc');
  if (t && window.matchMedia && window.matchMedia('(max-width: 1079px)').matches) t.removeAttribute('open');
})();
document.querySelectorAll('pre').forEach(function (pre) {
  var b = document.createElement('button');
  b.type = 'button'; b.className = 'copy'; b.textContent = 'コピー';
  b.addEventListener('click', function () {
    var c = pre.querySelector('code'); var t = c ? c.innerText : pre.innerText;
    var done = function () { b.textContent = 'コピーしました'; setTimeout(function () { b.textContent = 'コピー'; }, 1600); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(done, function () { b.textContent = '選んでコピーしてください'; });
    } else { b.textContent = '選んでコピーしてください'; }
  });
  pre.appendChild(b);
});
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700'
         '&family=IBM+Plex+Mono:wght@400;600&family=Kaushan+Script&display=swap">')


def build():
    status = {}
    sp = os.path.join(DOCS, 'STATUS.json')
    if os.path.exists(sp):
        status = json.load(open(sp, encoding='utf-8'))
    sections, nav = [], []
    for path, label in ORDER:
        fp = os.path.join(DOCS, path)
        if not os.path.exists(fp):
            continue
        k = key(path)
        md = markdown.Markdown(
            extensions=['tables', 'fenced_code', 'sane_lists', 'toc'],
            extension_configs={'toc': {'slugify': (lambda v, s, k=k: k + '-' + slugify_unicode(v, s))}})
        body = md.convert(open(fp, encoding='utf-8').read())
        body = rewrite_links(body, path)
        body = body.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')
        subs = []
        for t in md.toc_tokens:
            for ch in (t.get('children') or []) if t.get('level') == 1 else [t]:
                if ch.get('level') == 2:
                    subs.append((ch['id'], ch['name']))
        sections.append(f'<section class="doc" id="{k}"><p class="eyebrow">docs/{html.escape(path)}</p>{body}</section>')
        sub = ''
        if subs:
            sub = ('<details><summary>節を見る</summary><ol>'
                   + ''.join(f'<li><a href="#{i}">{n}</a></li>' for i, n in subs) + '</ol></details>')
        nav.append(f'<li><a href="#{k}">{html.escape(label)}</a>{sub}</li>')

    live = status.get('portal_live', {})
    main = status.get('main_branch', {})
    chips = (
        f'<span class="chip live"><span class="dot"></span>公開中: ラジアル版 <code>{html.escape(live.get("source_branch", "portal-radial"))}</code></span>'
        f'<span class="chip hold"><span class="dot"></span><code>main</code> = 正方形版・ポータル未公開</span>'
        f'<span class="chip"><span class="dot"></span>判断待ち {html.escape(", ".join(status.get("pending_owner_decisions", [])))}</span>'
    )
    today = status.get('as_of') or datetime.date.today().isoformat()
    header = (f'<header class="masthead">{polar_mark()}<div class="brand">'
              f'<p class="wordmark">Fractas</p>'
              f'<p class="sub">引き継ぎ書 ・ {html.escape(today)} ・ game_id <code>fractas</code> ・ '
              f'正本 <a href="https://github.com/hiroakiishibashi/fractas/tree/main/docs">hiroakiishibashi/fractas/docs</a></p>'
              f'<div class="chips">{chips}</div></div></header>')
    toc = f'<details class="toc" open><summary>目次</summary><ol>{"".join(nav)}</ol></details>'
    main_html = f'<div class="layout"><nav aria-label="目次">{toc}</nav><article>{"".join(sections)}</article></div>'
    foot = (f'<footer class="foot">この1枚は <code>python3 scripts/build-handoff-html.py</code> で docs/*.md から作ったものです。'
            f'手で直さず、.md を直して作り直してください。食い違ったら .md と実物（git・本番）が正です。</footer>')
    title = 'Fractas 引き継ぎ書'
    inner = f'{header}{main_html}{foot}<script>{JS}</script>'
    full = ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n{FONTS}\n<style>{CSS}</style>\n</head>\n<body>\n{inner}\n</body>\n</html>\n')
    fragment = f'<title>{title}</title>\n{FONTS}\n<style>{CSS}</style>\n{inner}\n'
    return full, fragment, len(sections)


if __name__ == '__main__':
    full, fragment, n = build()
    outp = os.path.join(DOCS, 'handoff.html')
    open(outp, 'w', encoding='utf-8').write(full)
    print(f'✅ {os.path.relpath(outp, ROOT)}（{n} 本の .md から {len(full) // 1024}KB）')
    if '--fragment' in sys.argv:
        fp = sys.argv[sys.argv.index('--fragment') + 1]
        open(fp, 'w', encoding='utf-8').write(fragment)
        print(f'✅ {fp}（アーティファクト用の断片）')
