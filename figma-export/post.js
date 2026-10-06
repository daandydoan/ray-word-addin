// post.js: raw DOM trees (states/*.json) -> build plan (plan/*.json)
//  1. infer auto layout from geometry for every container the DOM didn't give us flex for
//  2. tag colours that equal a CSS custom property (become Figma variables)
//  3. tag text runs with a text-style key (frequent combos become Figma text styles)
//  4. pull repeated elements out as component variants; screens reference them as instances
const fs = require('fs');
const SRC = fs.readFileSync(__dirname + '/../ray-word-addin-interactive-c4.src.html', 'utf8');
fs.mkdirSync(__dirname + '/plan', { recursive: true });

/* ---------- tokens ---------- */
const hex = h => { h = h.replace('#', ''); if (h.length === 3) h = h.split('').map(c => c + c).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255); };
const TOK = []; // {name, css, rgba}
const seen = new Set();
for (const m of SRC.matchAll(/--([a-z0-9-]+):\s*([^;}]+)/gi)) {
  const [, k, v] = m; if (seen.has(k)) continue;
  let c = null;
  if (/^#[0-9a-f]{3,6}$/i.test(v.trim())) c = [...hex(v.trim()), 1];
  const rm = v.match(/^rgba?\(([^)]+)\)$/); if (rm) { const p = rm[1].split(/[\s,]+/).map(parseFloat); c = [p[0] / 255, p[1] / 255, p[2] / 255, p.length > 3 ? p[3] : 1]; }
  if (!c) continue;
  if (k === 'rowbg') continue; // redefined per context; not a single token
  seen.add(k);
  const name = k.startsWith('r-') ? 'pane/' + k.slice(2) : k.startsWith('w') ? 'word/' + k.slice(1) : k.startsWith('trk') ? 'track/' + (k === 'trk' ? 'insert' : 'delete') : 'brand/' + k;
  TOK.push({ name, css: '--' + k, rgba: c.map(x => Math.round(x * 1000) / 1000) });
}
const tokOf = c => { if (!c) return null; const t = TOK.find(t => t.rgba.every((v, i) => Math.abs(v - c[i]) < 0.004)); return t ? t.name : null; };

/* ---------- 1. auto layout inference ---------- */
const EPS = 1.2;
function infer(n) {
  if (n.t !== 'F' || !n.ch) return;
  n.ch.forEach(infer);
  if (n.al) { // from CSS flex: just decide hugging on the main axis
    return;
  }
  const kids = n.ch.filter(k => !k.abs && !k.rot);
  if (!kids.length) return;
  // scrolled container: children sit at a scroll offset auto layout can't express, keep it absolute
  if (n.clip === 2 && kids.some(k => k.y < -1 || k.x < -1 || k.y + k.h > n.h + 1 || k.x + k.w > n.w + 1)) return;
  const col = arrange(n, kids, 'V'), row = col ? null : arrange(n, kids, 'H');
  const lay = col || row; if (!lay) return;
  n.ch = [...lay.kids, ...n.ch.filter(k => k.abs || k.rot).map(k => (k.abs = 1, k))];
  n.al = lay.al;
}
function arrange(n, kids, d) {
  const V = d === 'V', A = V ? 'y' : 'x', S = V ? 'h' : 'w', B = V ? 'x' : 'y', T = V ? 'w' : 'h';
  const k = [...kids].sort((a, b) => a[A] - b[A]);
  for (let i = 1; i < k.length; i++) if (k[i][A] < k[i - 1][A] + k[i - 1][S] - EPS) return null; // overlap on main axis
  if (k.length > 1 && !V) { // a row must share a band vertically
    const top = Math.max(...k.map(c => c.y)), bot = Math.min(...k.map(c => c.y + c.h)); if (bot < top - EPS) return null;
  }
  const padA = Math.max(0, k[0][A]), padZ = Math.max(0, n[S] - (k[k.length - 1][A] + k[k.length - 1][S]));
  const padB1 = Math.max(0, Math.min(...k.map(c => c[B]))), padB2 = Math.max(0, n[T] - Math.max(...k.map(c => c[B] + c[T])));
  const inner = n[T] - padB1 - padB2;
  // cross-axis alignment per child
  const cls = k.map(c => {
    const off = c[B] - padB1, end = n[T] - padB2 - (c[B] + c[T]);
    if (Math.abs(off) < EPS && Math.abs(end) < EPS) return 'S';
    if (V && c.t === 'T' && !isIcon(c) && Math.abs(off) < EPS) return 'S'; // block text flows full width
    if (Math.abs(off) < EPS) return 'MIN'; if (Math.abs(end) < EPS) return 'MAX';
    if (Math.abs(off - end) < EPS) return 'CENTER'; return 'X';
  });
  const tally = {}; cls.forEach(c => { if (c !== 'S' && c !== 'X') tally[c] = (tally[c] || 0) + 1; });
  const ai = Object.keys(tally).sort((a, b) => tally[b] - tally[a])[0] || 'MIN';
  // main-axis gaps; one dominant gap in a row = pushed apart (margin-left:auto / space-between)
  const gaps = k.slice(1).map((c, i) => c[A] - (k[i][A] + k[i][S]));
  let spacing = gaps.length ? Math.max(0, Math.min(...gaps)) : 0;
  let groups = null;
  if (!V && gaps.length) {
    const big = Math.max(...gaps), bi = gaps.indexOf(big), rest = gaps.filter((_, i) => i !== bi);
    if (big > 20 && (!rest.length || big > 3 * Math.max(...rest, 1)) && padZ < 24) groups = [k.slice(0, bi + 1), k.slice(bi + 1)];
  }
  const place = (list, sp) => { const bef = list.map((c, i) => i === 0 ? 0 : c[A] - (list[i - 1][A] + list[i - 1][S]) - sp); return list.map((c, i) => {
    let before = bef[i];
    const ci = cls[k.indexOf(c)], mis = ci !== 'S' && ci !== ai;
    if (before <= 3 && !mis) { if (ci === 'S') c.st = 1; return c; }
    // a margin auto layout can't express: transparent wrapper spanning the cross axis carries it as padding
    const w = { t: 'F', n: 'offset', ch: [c] };
    if (before <= 3) before = 0;
    w[A] = c[A] - before; w[S] = c[S] + before; w[B] = padB1; w[T] = inner; w.st = 1;
    const inAi = ci === 'S' || ci === 'X' ? 'MIN' : ci, cross = ci === 'X' ? Math.max(0, c[B] - padB1) : 0;
    c[A] = before > EPS ? before : 0; c[B] = c[B] - padB1; if (ci === 'S') c.st = 1;
    w.al = { d, gap: 0, pad: V ? [r1(c[A]), 0, 0, r1(cross)] : [r1(cross), 0, 0, r1(c[A])], jc: 'MIN', ai: inAi, hug: 0, hp: 1 };
    return w;
  }); };
  let out, al;
  if (groups) {
    const mk = (g) => { if (g.length === 1) return g[0]; const gg = g.slice(1).map((c, i) => c.x - (g[i].x + g[i].w)); const sp = Math.max(0, Math.min(...gg));
      const x = g[0].x, y = Math.min(...g.map(c => c.y)), w = g[g.length - 1].x + g[g.length - 1].w - x, h = Math.max(...g.map(c => c.y + c.h)) - y;
      const grp = { t: 'F', n: 'group', x, y, w, h, ch: g };
      const inner = place(g, sp); grp.ch = inner; inner.forEach(c => { if (!c.al || c.n !== 'offset') { c.x -= x; c.y -= y; } else { c.x -= x; c.y -= y; } });
      grp.al = { d: 'H', gap: sp, pad: [0, 0, 0, 0], jc: 'MIN', ai, hug: 1 }; return grp; };
    out = [mk(groups[0]), mk(groups[1])];
    al = { d, gap: 0, pad: [padB1, padZ, padB2, padA].map(r1), jc: 'SPACE_BETWEEN', ai, hug: 0 };
  } else {
    out = place(k, spacing);
    const ctr = !V && Math.abs(padA - padZ) < 2.5 && padA > 8;
    const pad = V ? [ctr ? 0 : padA, padB2, ctr ? 0 : padZ, padB1] : [padB1, ctr ? 0 : padZ, padB2, ctr ? 0 : padA];
    al = { d, gap: r1(spacing), pad: pad.map(r1), jc: ctr ? 'CENTER' : 'MIN', ai, hug: 0 };
    // hug the main axis unless the box is clearly taller/wider than its content (fixed or flex-grown)
    if (!ctr && !n.clip && padZ <= Math.max(padA, 0) + EPS + 1) al.hp = 1;
  }
  // stretch-to-fill on the cross axis for children spanning the full inner size
  out.forEach(c => { if (c.st && c.t === 'T') { if (V && !isIcon(c)) c.fw = 1; else delete c.st; } });
  return { kids: out, al };
}
const r1 = x => Math.round(x * 10) / 10;
const isIcon = n => n.t === 'T' && n.s.every(s => s[1][0] === 'ICON');

/* ---------- 2+3. tokens and text styles ---------- */
const STY = {};
const styKey = s => { const fam = s[0] === 'ICON' ? 'Icon' : s[0]; return fam + '|' + s[1] + '|' + s[2] + '|' + s[3]; };
function tag(n, lh) {
  if (n.bg) n.bgt = tokOf(n.bg);
  if (n.bd) n.bd.t = tokOf(n.bd.c);
  if (n.t === 'T') for (const s of n.s) { s[1][8] = tokOf(s[1][4]); const k = styKey(s[1]) + '|' + (n.lh || 'auto') + '|' + (n.ls || 0); s[1][9] = k; STY[k] = (STY[k] || 0) + 1; }
  if (n.texts) n.texts.forEach(t => tag(t));
  (n.ch || []).forEach(c => tag(c));
}

/* ---------- 4. components ---------- */
// [set name, class token, keep size in signature]
const SETS = [
  ['Avatar', 'av', 1], ['Button', 'btn'], ['Pill', 'ins'], ['Tag', 'atag'], ['Section header', 'sec'], ['Select', 'stfsel'],
  ['Segmented control', 'modes'], ['Inline answer', 'qa'], ['Ray box', 'refine'], ['Editor toolbar', 'ed-tools'],
  ['Status dot', 'st'], ['Toast', '#toast'], ['Word / Tabs', 'wtabs', 1], ['Word / Ribbon', 'ribbon', 1], ['Pane / Header', 'tp-head', 1],
];
const classes = n => (n.n || '').split('.').filter(Boolean);
const setOf = n => n.t === 'F' && SETS.find(([, c]) => c.startsWith('#') ? (n.n || '').startsWith(c) : classes(n).includes(c));
const VAR = {}; // sig -> {set, key, name, tree}
const bySet = {};
const strip = (n, keepSize) => {
  const o = {};
  for (const [k, v] of Object.entries(n)) {
    if (['x', 'y', 'abs', 'st', 'fill', 'grow', 'texts', 'name', 'fw', 'sl', 'hp'].includes(k)) continue;
    if ((k === 'w' || k === 'h') && !keepSize && n.t !== 'S') continue;
    if (k === 'w' && n.t === 'T') continue;
    if (k === 'h' && n.t === 'T') continue;
    if (k === 's') { o.s = v.map(s => s[1].slice(0, 8)); continue; }
    if (k === 'ch') { o.ch = v.map(c => strip(c, keepSize)); continue; }
    if (k === 'svg') { o.svg = v.length; continue; }
    if (k === 'n' && n.t === 'T') continue;
    if (k === 'n') { o.n = String(v).replace(/#[^.]*/, ''); continue; }
    if (k === 'al') { o.al = Object.assign({}, v, { pad: v.pad.map(Math.round), gap: Math.round(v.gap) }); continue; }
    o[k] = v;
  }
  return o;
};
const textsOf = (n, out = []) => { if (n.t === 'T') out.push({ s: n.s }); else if (n.t === 'I') out.push(...n.texts); else (n.ch || []).forEach(c => textsOf(c, out)); return out; };
function extract(n, isRoot, ctx = '') {
  const myCtx = classes(n).includes('wr') ? classes(n).filter(c => c !== 'wr' && c !== 'cur').join(' ') : ctx;
  if (n.ch) n.ch = n.ch.map(c => extract(c, false, myCtx));
  const set = !isRoot && setOf(n); if (!set) return n;
  const sig = set[0] + JSON.stringify(strip(n, set[2]));
  let v = VAR[sig];
  if (!v) {
    const list = bySet[set[0]] = bySet[set[0]] || [];
    const extra = classes(n).filter(c => c !== set[1] && !c.startsWith('#'));
    const words = textsOf(n).map(t => t.s.filter(x => x[1][0] !== 'ICON').map(x => x[0]).join('').trim()).filter(Boolean);
    const icons = textsOf(n).map(t => t.s.filter(x => x[1][0] === 'ICON').map(x => x[0]).join('')).filter(Boolean);
    const L = {
      'Status dot': () => myCtx, Toast: () => '', 'Inline answer': () => words[0] === 'Click to answer' ? 'empty' : 'typed',
      'Editor toolbar': () => words.length ? 'word count' : 'no count', Avatar: () => words[0] + ' ' + Math.round(n.w) + 'px',
      Button: () => (words[0] || icons[0] || '').slice(0, 22), Tag: () => words[0], Pill: () => words[0], 'Ray box': () => words[0],
    }[set[0]];
    let label = [extra.filter(c => !['on', 'go', 'filled', 'anl'].includes(c)).join(' '), L ? L() : ''].filter(Boolean).join(' · ') || 'default';
    const same = list.filter(x => x.base === label).length; const base = label; if (same) label += ' ' + (same + 1);
    v = VAR[sig] = { set: set[0], key: 'v' + Object.keys(VAR).length, label, base, tree: JSON.parse(JSON.stringify(n)) };
    v.tree.x = 0; v.tree.y = 0; delete v.tree.abs; delete v.tree.st; delete v.tree.fill; delete v.tree.grow;
    list.push(v);
  }
  return { t: 'I', k: v.key, x: n.x, y: n.y, w: n.w, h: n.h, abs: n.abs, st: n.st, fill: n.fill, grow: n.grow, texts: textsOf(n), set: set[0] };
}

/* ---------- run ---------- */
const meta = JSON.parse(fs.readFileSync(__dirname + '/states/meta.json', 'utf8'));
const screens = {};
for (const m of meta) {
  const t = JSON.parse(fs.readFileSync(`${__dirname}/states/${m.id}.json`, 'utf8'));
  infer(t);
  screens[m.id] = extract(t, true);
}
Object.values(VAR).forEach(v => tag(v.tree));
Object.values(screens).forEach(t => tag(t));
// text styles: combos used 6+ times
const styles = Object.entries(STY).filter(([, c]) => c >= 6).map(([k]) => {
  const [fam, w, it, size, lh, ls] = k.split('|');
  const area = fam === 'Outfit' ? 'Pane' : fam === 'Noto Sans' ? 'Word UI' : fam === 'Tinos' || fam === 'Gelasio' ? 'Document' : fam === 'Icon' ? 'Icon' : 'Mono';
  const wn = { 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold' }[w] || w;
  return { key: k, name: `${area}/${size}${lh !== 'auto' ? '·' + lh : ''} ${wn}${it === '1' ? ' Italic' : ''}${+ls ? ' ls' + ls : ''}` };
});
const names = new Set(); styles.forEach(s => { let n = s.name, i = 2; while (names.has(n)) n = s.name + ' ' + i++; s.name = n; names.add(n); });
fs.writeFileSync(__dirname + '/plan/tokens.json', JSON.stringify({ tokens: TOK, styles }));
const usesI = (n, out = new Set()) => { if (n.t === 'I') out.add(n.set); (n.ch || []).forEach(c => usesI(c, out)); return out; };
let comps = Object.entries(bySet).map(([set, vs]) => ({ set, deps: [...new Set(vs.flatMap(v => [...usesI(v.tree)]))].filter(d => d !== set), variants: vs.map(v => ({ key: v.key, label: v.label, tree: v.tree })) }));
const done = new Set(), ordered = []; while (ordered.length < comps.length) { const nx = comps.filter(c => !done.has(c.set) && c.deps.every(d => done.has(d))); if (!nx.length) throw new Error('cycle'); nx.forEach(c => { done.add(c.set); ordered.push(c); }); } comps = ordered;
fs.writeFileSync(__dirname + '/plan/components.json', JSON.stringify(comps));
for (const [id, t] of Object.entries(screens)) fs.writeFileSync(`${__dirname}/plan/${id}.json`, JSON.stringify(t));
console.log('tokens', TOK.length, 'styles', styles.length, 'sets', comps.map(c => c.set + ':' + c.variants.length).join(', '));
