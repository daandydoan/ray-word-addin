// Runs inside use_figma via new Function('figma','D','O', code). ASCII only.
// D.kind: 'tokens' | 'components' | 'screens'
// O: { page, vars:{name:id}, styles:{key:id}, comps:{variantKey:componentId} }
const STY = {
  Outfit: w => ({ 100: 'Thin', 200: 'ExtraLight', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black' })[Math.round(w / 100) * 100] || 'Regular',
  'Noto Sans': (w, i) => (w >= 650 ? 'Bold' : w >= 550 ? 'SemiBold' : w >= 450 ? 'Medium' : i ? '' : 'Regular') + (i ? (w >= 450 ? ' Italic' : 'Italic') : ''),
  Tinos: (w, i) => w >= 600 ? (i ? 'Bold Italic' : 'Bold') : (i ? 'Italic' : 'Regular'),
  Gelasio: (w, i) => (w >= 650 ? 'Bold' : w >= 550 ? 'SemiBold' : w >= 450 ? 'Medium' : i ? '' : 'Regular') + (i ? (w >= 450 ? ' Italic' : 'Italic') : ''),
  'Roboto Mono': (w, i) => (w >= 650 ? 'Bold' : w >= 550 ? 'SemiBold' : w >= 450 ? 'Medium' : i ? '' : 'Regular') + (i ? (w >= 450 ? ' Italic' : 'Italic') : ''),
  ICON: w => w >= 650 ? 'Bold' : w >= 550 ? 'SemiBold' : w >= 450 ? 'Medium' : 'Regular',
};
const fontOf = st => { const f = st[0]; return { family: f === 'ICON' ? 'Material Symbols Rounded' : f, style: STY[f] ? STY[f](st[1], st[2]) : 'Regular' }; };
const rgb = c => ({ r: c[0], g: c[1], b: c[2] });

const VARS = {};
for (const k in (O.vars || {})) VARS[k] = await figma.variables.getVariableByIdAsync(O.vars[k]);
const COMP = {};
for (const k in (O.comps || {})) COMP[k] = await figma.getNodeByIdAsync(O.comps[k]);
const solid = (c, tok) => {
  const p = { type: 'SOLID', color: rgb(c), opacity: c[3] };
  return tok && VARS[tok] ? figma.variables.setBoundVariableForPaint(p, 'color', VARS[tok]) : p;
};

/* ---------------- tokens: variables + text styles ---------------- */
if (D.kind === 'tokens') {
  const col = figma.variables.createVariableCollection('Ray C4 tokens');
  const mode = col.modes[0].modeId; col.renameMode(mode, 'Light');
  const vars = {};
  for (const t of D.tokens) {
    const v = figma.variables.createVariable(t.name, col, 'COLOR');
    v.setValueForMode(mode, { r: t.rgba[0], g: t.rgba[1], b: t.rgba[2], a: t.rgba[3] });
    v.scopes = ['ALL_FILLS', 'STROKE_COLOR', 'EFFECT_COLOR']; v.description = t.css; vars[t.name] = v.id;
  }
  const pw = figma.variables.createVariable('pane/width', col, 'FLOAT'); pw.setValueForMode(mode, 340); pw.scopes = ['WIDTH_HEIGHT']; pw.description = '--pw'; vars['pane/width'] = pw.id;
  const styles = {};
  const fonts = new Map(D.styles.map(s => { const [f, w, i] = s.key.split('|'); const fo = fontOf([f === 'Icon' ? 'ICON' : f, +w, +i]); return [fo.family + fo.style, fo]; }));
  await Promise.all([...fonts.values()].map(f => figma.loadFontAsync(f)));
  for (const s of D.styles) {
    const [f, w, i, size, lh, ls] = s.key.split('|');
    const st = figma.createTextStyle(); st.name = s.name;
    st.fontName = fontOf([f === 'Icon' ? 'ICON' : f, +w, +i]); st.fontSize = +size;
    st.lineHeight = lh === 'auto' ? { unit: 'AUTO' } : { unit: 'PIXELS', value: +lh };
    if (+ls) st.letterSpacing = { unit: 'PIXELS', value: +ls };
    styles[s.key] = st.id;
  }
  return { vars, styles };
}

/* ---------------- layer builder ---------------- */
const fk = new Map();
const scanFonts = n => { const add = s => { const f = fontOf(s[1]); fk.set(f.family + '|' + f.style, f); }; if (n.t === 'T') n.s.forEach(add); if (n.texts) n.texts.forEach(t => t.s.forEach(add)); (n.ch || []).forEach(scanFonts); };
const roots = D.kind === 'components' ? D.sets.flatMap(s => s.variants.map(v => v.tree)) : D.screens.map(s => s.tree);
roots.forEach(scanFonts);
await Promise.all([...fk.values()].map(f => figma.loadFontAsync(f)));
const page = await figma.getNodeByIdAsync(O.page);
if (figma.currentPage !== page) await figma.setCurrentPageAsync(page);

const later = [];
function paintBox(f, n) {
  const fills = [];
  if (n.bg) fills.push(solid(n.bg, n.bgt));
  if (n.gr) {
    const t = n.gr.ang * Math.PI / 180 - Math.PI / 2, c = Math.cos(t), s = Math.sin(t);
    fills.push({ type: 'GRADIENT_LINEAR', gradientTransform: [[c, s, 0.5 - 0.5 * c - 0.5 * s], [-s, c, 0.5 + 0.5 * s - 0.5 * c]], gradientStops: n.gr.stops.map(([col, p]) => ({ position: Math.min(1, Math.max(0, p)), color: { r: col[0], g: col[1], b: col[2], a: col[3] } })) });
  }
  f.fills = fills;
  if (n.bd) {
    f.strokes = [solid(n.bd.c, n.bd.t)]; f.strokeAlign = 'INSIDE';
    const [t, r, b, l] = n.bd.w;
    if (t === r && r === b && b === l) f.strokeWeight = t; else { f.strokeTopWeight = t; f.strokeRightWeight = r; f.strokeBottomWeight = b; f.strokeLeftWeight = l; }
    if (n.bd.dash) f.dashPattern = [3, 2];
  }
  if (n.r) { if (Array.isArray(n.r)) { [f.topLeftRadius, f.topRightRadius, f.bottomRightRadius, f.bottomLeftRadius] = n.r; } else f.cornerRadius = n.r; }
  if (n.sh) f.effects = n.sh.map(([x, y, bl, sp, c]) => ({ type: 'DROP_SHADOW', color: { r: c[0], g: c[1], b: c[2], a: c[3] }, offset: { x, y }, radius: bl, spread: sp, visible: true, blendMode: 'NORMAL' }));
}
function applySegs(t, segs, setChars) {
  const text = segs.map(s => s[0]).join('');
  if (setChars) { t.fontName = fontOf(segs[0][1]); t.characters = text; }
  let i = 0;
  for (const [str, st] of segs) {
    const a = i, b = i + str.length; i = b; if (a === b) continue;
    t.setRangeFontName(a, b, fontOf(st));
    t.setRangeFontSize(a, b, Math.max(1, st[3]));
    t.setRangeFills(a, b, [solid(st[4], st[8])]);
    t.setRangeTextDecoration(a, b, st[5] === 'U' ? 'UNDERLINE' : st[5] === 'S' ? 'STRIKETHROUGH' : 'NONE');
    t.setRangeTextCase(a, b, st[6] === 'UP' ? 'UPPER' : 'ORIGINAL');
    const sid = O.styles && O.styles[st[9]];
    if (sid) later.push(async () => { await t.setRangeTextStyleIdAsync(a, b, sid); t.setRangeTextDecoration(a, b, st[5] === 'U' ? 'UNDERLINE' : st[5] === 'S' ? 'STRIKETHROUGH' : 'NONE'); t.setRangeTextCase(a, b, st[6] === 'UP' ? 'UPPER' : 'ORIGINAL'); });
  }
  return text;
}
function mkText(n) {
  const t = figma.createText();
  const text = applySegs(t, n.s, true);
  t.lineHeight = n.lh ? { unit: 'PIXELS', value: n.lh } : { unit: 'AUTO' };
  if (n.ls) t.letterSpacing = { unit: 'PIXELS', value: n.ls };
  t.textAlignHorizontal = n.ta || 'LEFT';
  if (n.op) t.opacity = n.op;
  t.name = (n.n && n.n !== 'text' ? n.n + ' ' : '') + text.slice(0, 40);
  return t;
}
function sizeText(t, n, flow) {
  if (n.s.every(s => s[1][0] === 'ICON')) { t.textAutoResize = 'WIDTH_AND_HEIGHT'; return; }
  if (n.sl && !n.ml && !n.st) { t.textAutoResize = 'WIDTH_AND_HEIGHT'; if (flow) return; const dw = n.w - t.width; if (n.ta === 'CENTER') n.x += dw / 2; else if (n.ta === 'RIGHT') n.x += dw; return; }
  if (n.fw || n.st) { const sl = n.ml ? 0 : 1; t.resize(Math.max(1, n.w + sl), Math.max(1, t.height)); t.textAutoResize = 'HEIGHT'; if (n.ml) { t.textTruncation = 'ENDING'; t.maxLines = n.ml; } if (!flow) { if (n.ta === 'RIGHT') n.x -= sl; else if (n.ta === 'CENTER') n.x -= sl / 2; } }
  else t.textAutoResize = 'WIDTH_AND_HEIGHT';
}
function place(node, n) {
  if (n.rot) {
    const th = n.rot * Math.PI / 180, c = Math.cos(th), s = Math.sin(th), w = node.width, h = node.height;
    const cx = n.x + n.w / 2, cy = n.y + n.h / 2;
    node.relativeTransform = [[c, -s, cx - (c * w / 2 - s * h / 2)], [s, c, cy - (s * w / 2 + c * h / 2)]];
  } else { node.x = n.x; node.y = n.y; }
}
let count = 0; const misses = [];
function instance(n) {
  const comp = COMP[n.k]; if (!comp) { misses.push(n.k); return null; }
  const inst = comp.createInstance();
  const ts = inst.findAll(x => x.type === 'TEXT');
  if (ts.length === n.texts.length) n.texts.forEach((tx, i) => { const t = ts[i]; const want = tx.s.map(s => s[0]).join(''); if (t.characters !== want) { applySegs(t, tx.s, true); if (t.textAutoResize === 'HEIGHT') n._wrap = 1; } });
  else misses.push(n.k + ' texts ' + ts.length + '/' + n.texts.length);
  return inst;
}
function build(n, parent, parentAL) {
  let node;
  if (n.t === 'T' && n.sl && !n.ml && (n.ta || 'LEFT') === 'LEFT') { n.st = 0; n.fw = 0; } // one line in the browser stays one line here
  if (n.t === 'I') { node = instance(n); if (!node) return null; }
  else if (n.t === 'S') {
    try { node = figma.createNodeFromSvg(n.svg); } catch (e) { node = figma.createFrame(); node.fills = [solid([0.85, 0.87, 0.86, 1])]; }
    node.name = n.n || 'svg';
    node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    if (n.r) { node.cornerRadius = n.r; node.clipsContent = true; }
  } else if (n.t === 'T') {
    node = mkText(n);
    if (n.bg || n.bd || n.pad) { // text with its own box (content-control title tab)
      const f = figma.createAutoLayout('HORIZONTAL'); f.name = n.n || 'label'; paintBox(f, n);
      [f.paddingTop, f.paddingRight, f.paddingBottom, f.paddingLeft] = n.pad || [0, 0, 0, 0];
      f.appendChild(node); node.textAutoResize = 'WIDTH_AND_HEIGHT';
      parent.appendChild(f); count++;
      if (parentAL) f.layoutPositioning = 'ABSOLUTE'; f.x = n.x; f.y = n.y;
      return f;
    }
  } else {
    node = figma.createFrame();
    node.name = n.n || 'frame';
    node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    paintBox(node, n);
    node.clipsContent = !!n.clip;
    if (n.op) node.opacity = n.op;
    if (n.al) {
      const a = n.al;
      node.layoutMode = a.d === 'H' ? 'HORIZONTAL' : 'VERTICAL';
      [node.paddingTop, node.paddingRight, node.paddingBottom, node.paddingLeft] = a.pad;
      if (a.jc === 'SPACE_BETWEEN') node.primaryAxisAlignItems = 'SPACE_BETWEEN'; else { node.primaryAxisAlignItems = a.jc; node.itemSpacing = a.gap; }
      node.counterAxisAlignItems = a.ai === 'BASELINE' && a.d !== 'H' ? 'MIN' : a.ai;
      node.primaryAxisSizingMode = 'FIXED'; node.counterAxisSizingMode = 'FIXED';
      node.resize(Math.max(0.01, n.w), Math.max(0.01, n.h));
    }
  }
  parent.appendChild(node); count++;
  if (n.t === 'T') sizeText(node, n, parentAL && !n.abs);
  if (parentAL) {
    if (n.abs || n.rot) { node.layoutPositioning = 'ABSOLUTE'; place(node, n); }
    else {
      if (n.grow) node.layoutGrow = 1;
      if (n.st) node.layoutAlign = 'STRETCH';
      if (n.t === 'T' && (!n.fw || (n.sl && !n.ml)) && !n.grow && !n.st) node.layoutSizingHorizontal = 'HUG';
    }
  } else place(node, n);
  if (n.t === 'I' && !n.st && !n.grow) {
    // keep the instance at its rendered size on axes the component doesn't hug
    const L = node.layoutMode, hugW = L === 'HORIZONTAL' ? node.primaryAxisSizingMode === 'AUTO' : L === 'VERTICAL' ? node.counterAxisSizingMode === 'AUTO' : false;
    const hugH = L === 'VERTICAL' ? node.primaryAxisSizingMode === 'AUTO' : L === 'HORIZONTAL' ? node.counterAxisSizingMode === 'AUTO' : false;
    if (!hugW && Math.abs(node.width - n.w) > 1) node.resize(n.w, node.height);
    if (L !== 'NONE' && n._wrap) { /* hugged below */ }
    else if (!hugH && Math.abs(node.height - n.h) > 1) node.resize(node.width, n.h);
  }
  if (n.t === 'I' && n._wrap && node.layoutMode !== 'NONE') { /* overridden wrapping text may need more lines than the master */ if (node.layoutMode === 'VERTICAL') node.primaryAxisSizingMode = 'AUTO'; else node.counterAxisSizingMode = 'AUTO'; }
  if (n.ch && n.t === 'F') for (const c of n.ch) build(c, node, !!n.al);
  if (n.al && n.al.hug) { node.primaryAxisSizingMode = 'AUTO'; node.counterAxisSizingMode = 'AUTO'; }
  else if (n.al && n.al.hp) node.primaryAxisSizingMode = 'AUTO';
  return node;
}

/* ---------------- components ---------------- */
if (D.kind === 'components') {
  const out = {}; const sets = [];
  let y = O.y || 0;
  for (const s of D.sets) {
    const made = s.variants.map(v => {
      const f = build(Object.assign({}, v.tree, { x: 0, y: 0 }), page, false);
      const c = figma.createComponentFromNode(f); c.name = 'Variant=' + v.label.replace(/[=,]/g, ' '); out[v.key] = c.id; return c;
    });
    const set = figma.combineAsVariants(made, page);
    set.name = s.set;
    set.layoutMode = 'HORIZONTAL'; set.layoutWrap = 'WRAP'; set.itemSpacing = 24; set.counterAxisSpacing = 24;
    set.paddingTop = set.paddingBottom = set.paddingLeft = set.paddingRight = 24;
    set.primaryAxisSizingMode = 'FIXED'; set.counterAxisSizingMode = 'AUTO';
    set.resize(Math.max(400, Math.min(1600, made.reduce((a, c) => a + c.width + 24, 48))), 100); set.counterAxisSizingMode = 'AUTO';
    set.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }]; set.strokes = [{ type: 'SOLID', color: { r: 0.592, g: 0.278, b: 1 } }]; set.dashPattern = [6, 4];
    set.x = O.x || 0; set.y = y; y += set.height + 120;
    sets.push(set.id);
  }
  await Promise.all(later.map(f => f()));
  return { comps: out, sets, nextY: y, misses };
}

/* ---------------- screens ---------------- */
const ids = [];
for (const s of D.screens) {
  let f = build(Object.assign({}, s.tree, { x: 0, y: 0 }), page, false);
  const ex = s.target ? await figma.getNodeByIdAsync(s.target) : null;
  if (ex && ex.type === 'FRAME') { // keep the node id: swap the fresh content into the existing frame
    for (const c of [...ex.children]) c.remove();
    ex.layoutMode = 'NONE'; ex.resize(f.width, f.height);
    ex.fills = f.fills; ex.strokes = f.strokes; ex.effects = f.effects; ex.cornerRadius = f.cornerRadius; ex.clipsContent = f.clipsContent;
    if (f.layoutMode !== 'NONE') { ex.layoutMode = f.layoutMode; for (const k of ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'itemSpacing', 'primaryAxisAlignItems', 'counterAxisAlignItems', 'primaryAxisSizingMode', 'counterAxisSizingMode']) ex[k] = f[k]; }
    for (const c of [...f.children]) ex.appendChild(c);
    f.remove(); f = ex;
  }
  f.name = s.name; f.x = s.x; f.y = s.y; ids.push(f.id);
}
await Promise.all(later.map(f => f()));
// status pill (.wfstat): its ::before/::after lines come through stacked over the pill; put them either side, behind it
for (const id of ids) { const fr = await figma.getNodeByIdAsync(id);
  for (const w of fr.findAll(n => n.type === 'FRAME' && /wfstat/.test(n.name))) {
    const sp = w.children.find(c => c.name === 'span'), b = w.children.find(c => c.name === '::before'), af = w.children.find(c => c.name === '::after');
    if (!sp || !b || !af) continue; const y = Math.round(sp.y + sp.height / 2);
    b.x = 0; b.y = y; b.resize(Math.max(1, sp.x - 8), 1); af.x = sp.x + sp.width + 8; af.y = y; af.resize(Math.max(1, w.width - af.x), 1);
    w.insertChild(0, b); w.insertChild(1, af);
  } }
return { ids, layers: count, misses };
