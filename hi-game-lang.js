// ============================================================
// hi-game-lang.js — ゲーム側SDK（表示言語をポータルに合わせる）v1.0
// 仕様の正本: /docs/game-lang-spec.md
// 置き場所  : /sdk/html/hi-game-lang.js
//
// 使い方（ゲームの初期化で1回。**同期で**言語コードが返る）:
//   const lang = HiLang.init({
//     id:       'spades',              // 保存キーの名前空間（ゲームごとに固有）
//     langs:    ['en','ja','ko'],      // このゲームが実際に持つ言語（'en' は必ず入れる）
//     onChange: (code) => applyLang(code),   // Web側で切り替わったとき（省略可）
//   });
//
// 決まり（オーナー方針 2026-09-10）:
//   * Web(ポータル)で選ばれている言語をこのゲームが持っていなければ **英語**。
//     ブラウザの言語(navigator.language)には落とさない。← ここが要望の本体
//   * ポータルの preferred_lang には **絶対に書かない**。ゲーム内の選択は自分のキーへ。
//   * ポータル外(Playgama / itch / GitHub Pages / YouTube Playables / file://)でも
//     壊れない。読めるものが無ければ navigator.language → 'en' の順に静かに落ちる。
//
// 読み込み方（3通り・中身は同じ1ファイル）:
//   ① ポータル内・classic : <script src="/sdk/html/hi-game-lang.js"></script>
//                           ← 同期なので、言語を決めるインラインscriptの**前**に置ける
//   ② ポータル内・module  : import '/sdk/html/hi-game-lang.js';   // window.HiLang が生える
//                           named import が要るなら /sdk/html/hi-game-lang.esm.js
//   ③ ポータル外          : このファイルをゲームに同梱して <script src="./hi-game-lang.js">
//   ⚠️ このファイルに export を書かないのは①③のためです（module でも classic でも読める）。
//      hi-game-shot.js / hi-game-rtc.js が module 専用なのは、あちらが「ポータル内でしか
//      意味がない機能」だから。言語は**ポータル外でも必ず決まらないといけない**ので、
//      1本のファイルがどの読み方でも通るようにしてあります。書き換えないこと。
// ============================================================
(function (global) {
  'use strict';

  var HI = 'lang1';
  var PORTAL_KEY = 'preferred_lang';   // ポータルの正本（読むだけ。書かない）
  var MINE_PREFIX = 'hi_lang:';        // ゲーム内で選んだ記録 {lang, base}

  // ── ストレージ安全層 ───────────────────────────────
  // ⚠️ YouTube Playables は ytgame SDK が localStorage / sessionStorage / indexedDB を
  //    null に固定する(non-configurable)。素の localStorage.getItem は評価時点で即死する
  //    ので、読み書きは必ずここを通す（reference_youtube_playables.md の既知事故）。
  var mem = {};
  function lsGet(k) {
    try { var v = global.localStorage.getItem(k); if (v != null) return v; } catch (_) {}
    return Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : null;
  }
  function lsSet(k, v) {
    mem[k] = v;
    try { global.localStorage.setItem(k, v); } catch (_) {}
  }

  // ── 言語コードの正規化と照合 ───────────────────────
  function norm(v) { return String(v == null ? '' : v).trim().toLowerCase().replace(/_/g, '-'); }

  // langs の中から使えるものを返す。'zh-TW' なら 'zh-tw' 完全一致 → 'zh' の順。無ければ null
  function match(v, langs) {
    var s = norm(v);
    if (!s || !langs || !langs.length) return null;
    for (var i = 0; i < langs.length; i++) if (norm(langs[i]) === s) return langs[i];
    var base = s.split('-')[0];
    for (var j = 0; j < langs.length; j++) if (norm(langs[j]).split('-')[0] === base) return langs[j];
    return null;
  }
  function english(langs) { return match('en', langs) || langs[0]; }

  // 「はっきり指定された言語」の解決。持っていなければ**英語で確定**して、
  // navigator.language には落とさない。これが今回の要望そのもの。
  function explicit(v, langs) { return v ? (match(v, langs) || english(langs)) : null; }

  // ── 言語の出どころ ────────────────────────────────
  // ⚠️ 2つのクエリを役割で分ける。
  //    ?lang= … 人が手で打つ強制指定（QA・不具合報告・招待リンク）。最優先。
  //    ?hl=   … ラッパーやプラットフォームが自動で撒く「種」。preferred_lang と同格＝
  //             ゲーム内で選び直したらそちらが勝つ。同じ ?lang= に撒くと、ゲーム内の
  //             選択が永久に無視される（URL が常に最優先なので）。
  function q(name) {
    try { return new global.URLSearchParams(global.location.search).get(name); } catch (_) { return null; }
  }
  function urlLang() { return q('lang'); }
  function urlSeed() { return q('hl'); }

  var pushed = null;   // 親(ポータル)から postMessage で届いた値

  function hostLang(c) {
    if (pushed) return pushed;                       // ① 親からの明示 push（storage が死んでいても効く）
    var p = lsGet(PORTAL_KEY);                       // ② ポータルの localStorage（同一オリジンの iframe）
    if (p) return p;
    var seed = urlSeed();                            // ③ ラッパー/プラットフォームが撒いた ?hl=
    if (seed) return seed;
    try { if (c && typeof c.host === 'function') { var h = c.host(); if (h) return h; } } catch (_) {}
    try {                                            // ③ 埋め込み先プラットフォーム（Playgama 等）
      var b = global.bridge;
      if (b && b.platform && b.platform.language) return b.platform.language;
    } catch (_) {}
    return null;
  }

  // ゲーム内セレクタで選んだ記録。base = そのとき Web 側で選ばれていた言語
  function readMine(c) {
    var raw = lsGet(MINE_PREFIX + c.id);
    if (raw) {
      try {
        var o = JSON.parse(raw);
        if (o && o.lang) return { lang: o.lang, base: o.base == null ? null : norm(o.base) };
      } catch (_) {}
    }
    // 既存ゲームの古いキー（spades_lang / logos66_lang / cm_lang / cc_lang …）。
    // base が分からない＝「Web設定より前の選択」とみなし、Web を優先させる（下の resolve 参照）
    if (c.legacyKey) { var old = lsGet(c.legacyKey); if (old) return { lang: old, base: null }; }
    return null;
  }

  // ── 決定（同期・これ1つが唯一の決め所）──────────────
  function resolve(c) {
    var langs = c.langs;

    // ① URL の ?lang=（ポータル外・QA・Playgama のリロード往復・招待リンク）
    var u = explicit(urlLang(), langs);
    if (u) return u;

    var host = hostLang(c);
    var mine = readMine(c);

    // ② Web(ポータル/プラットフォーム)の設定がある
    if (host) {
      // ゲーム内で選んだときの Web 設定と今の Web 設定が同じなら、その選択を尊重する。
      // Web 側が変わった瞬間は Web が勝つ（＝「Webの設定に同期」を満たす）
      if (mine && mine.base && mine.base === norm(host)) {
        var kept = match(mine.lang, langs);
        if (kept) return kept;
      }
      return explicit(host, langs);   // ★ 持っていない言語は英語。navigator には落とさない
    }

    // ③ ポータル外で、自分で選んだ記録がある
    if (mine) { var m = match(mine.lang, langs); if (m) return m; }

    // ④ ブラウザの言語（ここは「推測」なので、当たらなければ次へ落ちてよい）
    var navs = [];
    try { if (global.navigator) { navs = (global.navigator.languages || []).slice(); if (global.navigator.language) navs.push(global.navigator.language); } } catch (_) {}
    for (var i = 0; i < navs.length; i++) { var n = match(navs[i], langs); if (n) return n; }

    // ⑤ 何も分からなければ英語
    return english(langs);
  }

  // ── 状態と通知 ────────────────────────────────────
  var cfg = null, current = null, subs = [], wired = false;

  function apply(code, why) {
    if (!cfg) return current;
    var next = match(code, cfg.langs) || english(cfg.langs);
    if (next === current) return current;
    current = next;
    setHtmlLang();
    for (var i = 0; i < subs.length; i++) { try { subs[i](current, why); } catch (_) {} }
    return current;
  }
  function setHtmlLang() {
    if (!cfg || cfg.setHtmlLang === false) return;
    try { global.document.documentElement.lang = current; } catch (_) {}
  }

  // Web 側の値が届いたとき（storage / postMessage）。
  // ⚠️ ここでは ?lang= を見ない。人がポータルで切り替えた操作のほうが新しいから。
  function fromHost(v) {
    if (!cfg) { pushed = v || pushed; return; }
    // ⚠️ 値が消えた（ログアウト・別タブでの削除）ときは英語で固定せず、決め直す。
    //    ここで english() を返すと、ポータル外の人が navigator 由来で使えていた言語を失う。
    if (!v) { pushed = null; apply(resolve(cfg), 'portal'); return; }
    pushed = String(v);
    var mine = readMine(cfg);
    if (mine && mine.base && mine.base === norm(v)) { apply(mine.lang, 'portal'); return; }
    apply(explicit(v, cfg.langs) || english(cfg.langs), 'portal');
  }

  function wire() {
    if (wired) return; wired = true;

    // ① 同一オリジンの iframe なら、親(ポータル)の localStorage 書き込みがここに届く。
    //    ⚠️ storage は「書いた document 自身」には飛ばない。将来ゲームを iframe 無しで
    //       同じ document に載せると無音で効かなくなるので、②と二重化してある。
    try {
      global.addEventListener('storage', function (e) {
        if (!e || e.key !== PORTAL_KEY) return;
        fromHost(e.newValue);
      });
    } catch (_) {}

    // ② ポータルと**同じ document**に載っているゲーム（YUUGURE のように iframe を使わない
    //    構成）向け。storage は自分の document には飛ばず、親も自分自身なので postMessage も
    //    来ない。この場合だけ js/i18n.js の CustomEvent が直接届く。
    try {
      global.addEventListener('langchange', function (e) {
        var v = e && e.detail && e.detail.lang;
        if (v) fromHost(v);
      });
    } catch (_) {}

    // ③ 親からの明示 push。storage が使えない環境と、読み込み順の取りこぼしの保険。
    try {
      global.addEventListener('message', function (e) {
        // ⚠️ 出どころ検証。無いと、埋め込み先の別サイトや同一ページの他スクリプトから
        //    表示言語を差し替えられる（hi-game-shot.js / hi-game-rtc.js と同じ作法）
        if (e.origin !== global.location.origin || e.source !== global.parent) return;
        var m = e.data;
        if (!m || m.hi !== HI || m.ev !== 'set' || typeof m.lang !== 'string') return;
        fromHost(m.lang);
      });
    } catch (_) {}
  }

  // 親に「言語ちょうだい」と名乗る。ポータル外なら返事が来ないだけ（無害）。
  // 親側(js/game-lang-bridge.js)は load 時・langchange 時にも push してくるので、
  // どちらが先に立ち上がっても取りこぼさない。
  function hello() {
    var say = function () {
      try {
        if (global.parent && global.parent !== global) {
          // ⚠️ langs と live を必ず載せる。ポータルはこれを見て「この作品は英語のみです」と
          //    出す。出さないと、韓国語を選んでいるのに英語が出る理由がユーザーに分からない。
          //    live:false なら親は自動で読み込み直さない（対局や部屋が落ちるため）。
          global.parent.postMessage({
            hi: HI, ev: 'ready', lang: current,
            langs: cfg ? cfg.langs.slice() : [], live: !!(cfg && cfg.live)
          }, global.location.origin);
        }
      } catch (_) {}
    };
    say();
    try { global.setTimeout(say, 1500); } catch (_) {}   // 親のブリッジが module で後発のとき用
  }

  var HiLang = {
    /**
     * 起動時に1回。使うべき言語コードを **同期で** 返す。
     * @param {{id?:string, langs:string[], onChange?:function, legacyKey?:string,
     *          host?:function, setHtmlLang?:boolean}|string[]} opts
     *        langs だけの配列を直接渡してもよい（HiLang.init(['en','ja'])）
     * @returns {string} langs のどれか（決められなければ 'en'）
     */
    init: function (opts) {
      var o = Array.isArray(opts) ? { langs: opts } : (opts || {});
      var langs = (o.langs && o.langs.length) ? o.langs.slice() : ['en'];
      cfg = {
        id: o.id || 'game',
        langs: langs,
        legacyKey: o.legacyKey || null,
        host: typeof o.host === 'function' ? o.host : null,
        setHtmlLang: o.setHtmlLang,
        // live: 起動後に言語を差し替えても画面が正しく作り直せるか。
        // ⚠️ 既定は false（安全側）。true にするのは「切替で全画面を描き直せる」と
        //    確認したゲームだけ。false のゲームには親が『次回の読み込みから』と出す。
        live: o.live === true
      };
      if (typeof o.onChange === 'function') subs.push(o.onChange);
      current = resolve(cfg);
      setHtmlLang();
      wire();
      hello();
      return current;
    },

    /** 副作用なしで「使うべき言語」だけ知りたいとき（保存も購読もしない） */
    pick: function (langs, opts) {
      var o = opts || {};
      return resolve({
        id: o.id || '-', langs: (langs && langs.length) ? langs : ['en'],
        legacyKey: o.legacyKey || null, host: typeof o.host === 'function' ? o.host : null
      });
    },

    /** いまの言語 */
    get: function () { return current || (cfg ? english(cfg.langs) : 'en'); },

    /** 変化の購読。戻り値は解除関数（hi-game-rtc.js の onState と同じ作法） */
    onChange: function (fn) {
      subs.push(fn);
      return function () { var i = subs.indexOf(fn); if (i >= 0) subs.splice(i, 1); };
    },

    /**
     * ゲーム内の言語セレクタから呼ぶ。
     * ⚠️ ポータルの preferred_lang は書かない（ゲームがサイト全体の設定を乗っ取らない）。
     * 未対応コードでも黙って no-op にせず英語に落とす（現行ゲームの事故パターン封じ）。
     */
    set: function (code) {
      if (!cfg) return 'en';
      var next = match(code, cfg.langs) || english(cfg.langs);
      var base = hostLang(cfg);
      lsSet(MINE_PREFIX + cfg.id, JSON.stringify({ lang: next, base: base ? norm(base) : null }));
      if (cfg.legacyKey) lsSet(cfg.legacyKey, next);   // 既存キーも書いておく（旧版と行き来しても壊れない）
      return apply(next, 'game');
    },

    /** このゲームが持つ言語の一覧（セレクタを組むとき用） */
    langs: function () { return cfg ? cfg.langs.slice() : []; },

    /** 照合規則（ゲーム側でも同じ規則を使えるように公開）。無ければ null */
    match: function (v, langs) { return match(v, langs || (cfg ? cfg.langs : ['en'])); },

    version: '1.0.0'
  };

  global.HiLang = global.HiLang || HiLang;
})(typeof window !== 'undefined' ? window : globalThis);
