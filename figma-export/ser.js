// In-page DOM → compact layer tree. Injected via CDP; call window.__ser(rootEl, extraEls[]).
// Node shapes: F=frame, T=text, S=svg, I=component instance slot. Coords are relative to the parent node.
window.__ser = function (root, extras = [], comps = {}) {
  const R0 = root.getBoundingClientRect();
  const r3 = n => Math.round(n * 1000) / 1000, r1 = n => Math.round(n * 10) / 10;
  const col = c => {
    const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat); const a = p.length > 3 ? p[3] : 1;
    return a === 0 ? null : [r3(p[0] / 255), r3(p[1] / 255), r3(p[2] / 255), r3(a)];
  };
  const splitTop = s => { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '(') d++; if (ch === ')') d--; if (ch === ',' && !d) { out.push(cur.trim()); cur = ''; } else cur += ch; } if (cur.trim()) out.push(cur.trim()); return out; };
  const grad = s => {
    const m = s && s.match(/^linear-gradient\((.*)\)$/); if (!m) return null;
    const parts = splitTop(m[1]); let ang = 180;
    if (/deg$/.test(parts[0])) ang = parseFloat(parts.shift());
    else if (/^to /.test(parts[0])) { ang = { 'to right': 90, 'to left': 270, 'to bottom': 180, 'to top': 0 }[parts.shift()] ?? 180; }
    const stops = parts.map((p, i, a) => { const c = col(p) || [0, 0, 0, 0]; const pm = p.match(/\)\s*([\d.]+)%/); return [c, pm ? +pm[1] / 100 : null]; });
    stops.forEach((s, i, a) => { if (s[1] == null) s[1] = a.length > 1 ? i / (a.length - 1) : 0; });
    return { ang, stops: stops.map(([c, p]) => [c || [0, 0, 0, 0], r3(p)]) };
  };
  const shadow = s => {
    if (!s || s === 'none') return null;
    return splitTop(s).filter(x => !/inset/.test(x)).map(x => { const c = col(x); const n = x.replace(/rgba?\([^)]*\)/, '').trim().split(/\s+/).map(parseFloat); return c ? [n[0] || 0, n[1] || 0, n[2] || 0, n[3] || 0, c] : null; }).filter(Boolean);
  };
  const fam = (f, w) => {
    f = f.split(',')[0].replace(/['"]/g, '').trim();
    if (/Material Symbols/.test(f)) return 'ICON';
    if (/Outfit/i.test(f)) return 'Outfit';
    if (/Segoe/i.test(f)) return 'Noto Sans';
    if (/Times/i.test(f)) return 'Tinos';
    if (/Georgia/i.test(f)) return 'Gelasio';
    if (/mono|Menlo/i.test(f)) return 'Roboto Mono';
    return 'Outfit';
  };
  const boxOf = cs => {
    const o = {};
    const bg = col(cs.backgroundColor); if (bg) o.bg = bg;
    const g = grad(cs.backgroundImage); if (g) o.gr = g;
    const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => cs['border' + s + 'Style'] === 'none' ? 0 : parseFloat(cs['border' + s + 'Width']) || 0);
    if (bw.some(Boolean)) {
      const i = bw.findIndex(Boolean), side = ['Top', 'Right', 'Bottom', 'Left'][i]; const c = col(cs['border' + side + 'Color']);
      if (c) { o.bd = { w: bw, c }; if (cs['border' + side + 'Style'] === 'dashed') o.bd.dash = 1; }
    }
    const sh = shadow(cs.boxShadow); if (sh && sh.length) o.sh = sh;
    return o;
  };
  const radius = (cs, w, h) => {
    const v = ['TopLeft', 'TopRight', 'BottomRight', 'BottomLeft'].map(k => { const s = cs['border' + k + 'Radius'].split(' ')[0]; return s.endsWith('%') ? parseFloat(s) / 100 * Math.min(w, h) : parseFloat(s) || 0; }).map(r1);
    return v.some(Boolean) ? (v.every(x => x === v[0]) ? v[0] : v) : 0;
  };
  const hasBox = (cs) => { const b = boxOf(cs); return !!(b.bg || b.gr || b.bd || b.sh) || ['Top', 'Right', 'Bottom', 'Left'].some(s => parseFloat(cs['padding' + s]) > 0); };
  const visible = cs => cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.01;
  const rotOf = cs => { const t = cs.transform; if (!t || t === 'none') return 0; const m = t.match(/matrix\(([^)]+)\)/); if (!m) return 0; const [a, b] = m[1].split(',').map(parseFloat); return r1(Math.atan2(b, a) * 180 / Math.PI); };
  const txtStyle = (cs) => {
    const w = +cs.fontWeight || 400, f = fam(cs.fontFamily, w);
    const dec = /underline/.test(cs.textDecorationLine) ? 'U' : /line-through/.test(cs.textDecorationLine) ? 'S' : '';
    const bgc = col(cs.backgroundColor);
    return [f, w, cs.fontStyle === 'italic' ? 1 : 0, r1(parseFloat(cs.fontSize)), col(cs.color) || [0, 0, 0, 1], dec, cs.textTransform === 'uppercase' ? 'UP' : '', bgc];
  };
  const inter = (a, b) => !b || (a.right > b.left && a.left < b.right && a.bottom > b.top && a.top < b.bottom);
  const clipOf = (r, c) => !c ? r : { left: Math.max(r.left, c.left), top: Math.max(r.top, c.top), right: Math.min(r.right, c.right), bottom: Math.min(r.bottom, c.bottom) };
  const nameOf = el => (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '') || el.tagName.toLowerCase();

  // is every descendant inline text without its own box?
  const inlineOnly = el => {
    for (const c of el.childNodes) {
      if (c.nodeType === 3) continue; if (c.nodeType !== 1) continue;
      const cs = getComputedStyle(c); if (!visible(cs)) continue;
      if (c.tagName === 'BR') continue;
      if (cs.display !== 'inline' || hasBox(cs) || /^(IMG|svg|INPUT|SELECT|TEXTAREA)$/i.test(c.tagName) || pseudo(c).length) return false;
      if (!inlineOnly(c)) return false;
    }
    return true;
  };
  const segsOf = (el, ws) => {
    const segs = [];
    const walk = (n) => {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) { const cs = getComputedStyle(c.parentElement); segs.push([c.data, txtStyle(cs)]); }
        else if (c.nodeType === 1) { const cs = getComputedStyle(c); if (!visible(cs)) continue; if (c.tagName === 'BR') { segs.push(['\n', txtStyle(cs), 1]); continue; } walk(c); }
      }
    };
    walk(el);
    // collapse whitespace like the browser (unless pre)
    const pre = /pre/.test(ws);
    let prevSpace = true; const out = [];
    for (let [t, st, br] of segs) {
      if (!pre && !br) { t = t.replace(/[\t\r\n ]+/g, ' '); if (prevSpace) t = t.replace(/^ /, ''); }
      if (!t) continue; prevSpace = /[ \n]$/.test(t); if (st[0] === 'ICON') st = st.slice(); out.push([t, st]);
    }
    if (out.length && !pre) { const l = out[out.length - 1]; l[0] = l[0].replace(/ $/, ''); if (!l[0]) out.pop(); }
    if (out.length) out[0][0] = out[0][0].replace(/^\n+/, '');
    return out.filter(s => s[0]);
  };
  const textNode = (segs, cs, rect, parentRect, extra = {}) => {
    const lh = cs.lineHeight === 'normal' ? null : r1(parseFloat(cs.lineHeight));
    const fs = parseFloat(cs.fontSize); const lhp = lh || fs * 1.25;
    const mh = extra._mh != null ? extra._mh : rect.height; delete extra._mh;
    const multi = mh > lhp * 1.6 || segs.some(s => s[0].includes('\n'));
    const o = { t: 'T', x: r1(rect.left - parentRect.left), y: r1(rect.top - parentRect.top), w: r1(rect.width), h: r1(rect.height), s: segs, lh, ls: cs.letterSpacing === 'normal' ? 0 : r1(parseFloat(cs.letterSpacing)), ta: { center: 'CENTER', right: 'RIGHT', end: 'RIGHT', justify: 'JUSTIFIED' }[cs.textAlign] || 'LEFT' };
    if (multi || o.ta !== 'LEFT') o.fw = 1; // fixed width
    if (!multi) o.sl = 1;
    const clamp = +cs.webkitLineClamp || 0; if (clamp) { o.ml = clamp; o.fw = 1; }
    if (cs.textOverflow === 'ellipsis' && cs.whiteSpace === 'nowrap') { o.ml = 1; o.fw = 1; }
    if (+cs.opacity < 1) o.op = r3(+cs.opacity);
    return Object.assign(o, extra);
  };

  // ::before / ::after
  function pseudo(el) {
    const out = [];
    for (const p of ['::before', '::after']) {
      const cs = getComputedStyle(el, p); if (!cs.content || cs.content === 'none' || cs.content === 'normal' || !visible(cs)) continue;
      let txt = cs.content; const am = txt.match(/^attr\(([^)]+)\)$/);
      txt = am ? (el.getAttribute(am[1]) || '') : txt.replace(/^["']|["']$/g, '');
      out.push({ p, cs, txt });
    }
    return out;
  }
  const pseudoNodes = (el, rect) => {
    const res = [];
    for (const { p, cs, txt } of pseudo(el)) {
      const w = parseFloat(cs.width) || 0, h = parseFloat(cs.height) || 0;
      const box = boxOf(cs); const rot = rotOf(cs);
      const ecs = getComputedStyle(el);
      let x, y;
      if (cs.position === 'absolute') {
        const bl = parseFloat(ecs.borderLeftWidth) || 0, bt = parseFloat(ecs.borderTopWidth) || 0;
        const L = parseFloat(cs.left), T = parseFloat(cs.top), Rr = parseFloat(cs.right), B = parseFloat(cs.bottom);
        const ww = w || (!isNaN(L) && !isNaN(Rr) ? rect.width - L - Rr : 0), hh = h || (!isNaN(T) && !isNaN(B) ? rect.height - T - B : 0);
        x = bl + (!isNaN(L) ? L : rect.width - ww - (Rr || 0)); y = bt + (!isNaN(T) ? T : rect.height - hh - (B || 0));
        if (cs.left === '50%' || /%/.test(cs.left)) x = bl + rect.width * parseFloat(cs.left) / 100;
        if (txt) { res.push(Object.assign(textNode([[txt, txtStyle(cs)]], cs, { left: rect.left + x, top: rect.top + y, width: 0, height: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3 }, rect), box, { n: p, pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].map(parseFloat), fw: 0 })); continue; }
        res.push(Object.assign({ t: 'F', n: p, x: r1(x), y: r1(y), w: r1(ww), h: r1(hh), r: radius(cs, ww, hh), rot }, box)); continue;
      }
      if (txt) { // placeholder text: sits at the element's content box
        const pl = parseFloat(ecs.paddingLeft) + parseFloat(ecs.borderLeftWidth), pt = parseFloat(ecs.paddingTop) + parseFloat(ecs.borderTopWidth);
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3;
        res.push(Object.assign(textNode([[txt, txtStyle(cs)]], cs, { left: rect.left + pl, top: rect.top + pt, width: Math.max(0, rect.width - pl - parseFloat(ecs.paddingRight)), height: lh }, rect), { n: p + ' placeholder' })); continue;
      }
      if (!w && !h && !box.bd) continue;
      const bw = box.bd ? box.bd.w : [0, 0, 0, 0];
      const ww = w + bw[1] + bw[3], hh = h + bw[0] + bw[2];
      res.push(Object.assign({ t: 'F', n: p, x: r1((rect.width - ww) / 2), y: r1((rect.height - hh) / 2), w: r1(ww), h: r1(hh), r: radius(cs, ww, hh), rot }, box));
    }
    return res;
  };

  function el2node(el, parentRect, clip, cull = true) {
    const cs = getComputedStyle(el); if (!visible(cs)) return null;
    if (el.matches('.demoscan,.demo,.grip')) return null;
    let rect = el.getBoundingClientRect();
    const rot = rotOf(cs);
    if (rot) { const cw = el.offsetWidth, chh = el.offsetHeight, cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2; rect = { left: cx - cw / 2, top: cy - chh / 2, width: cw, height: chh, right: cx + cw / 2, bottom: cy + chh / 2 }; }
    if (cull && !inter(rect, clip)) return null; // only cull at a scroll/clip boundary, never inside a partly visible element
    for (const [sel, k] of Object.entries(comps)) if (el.matches(sel)) return { t: 'I', k, x: r1(rect.left - parentRect.left), y: r1(rect.top - parentRect.top), w: r1(rect.width), h: r1(rect.height) };
    const pos = { x: r1(rect.left - parentRect.left), y: r1(rect.top - parentRect.top), w: r1(rect.width), h: r1(rect.height) };
    if (rect.width < 0.5 && rect.height < 0.5 && !el.children.length) return null;
    const tag = el.tagName;
    if (tag === 'IMG') {
      const src = el.getAttribute('src') || '';
      if (src.startsWith('data:image/svg+xml')) { let svg = src.includes('base64,') ? atob(src.split('base64,')[1]) : decodeURIComponent(src.split(',').slice(1).join(',')); return Object.assign({ t: 'S', n: el.alt || 'image', svg, r: radius(cs, rect.width, rect.height) }, pos); }
      return Object.assign({ t: 'F', n: 'img', bg: [0.85, 0.87, 0.86, 1] }, pos);
    }
    if (tag.toLowerCase() === 'svg') {
      const c = el.cloneNode(true); c.setAttribute('width', rect.width); c.setAttribute('height', rect.height);
      c.querySelectorAll('*').forEach(n => { const s = getComputedStyle(n); if (n.getAttribute('fill') === 'currentColor') n.setAttribute('fill', s.color); if (n.getAttribute('stroke') === 'currentColor') n.setAttribute('stroke', s.color); });
      if (c.getAttribute('fill') === 'currentColor') c.setAttribute('fill', cs.color);
      return Object.assign({ t: 'S', n: 'svg', svg: c.outerHTML }, pos);
    }
    if (tag === 'SELECT') { // render the closed select as a box + its selected label
      const n = Object.assign({ t: 'F', n: nameOf(el), r: radius(cs, rect.width, rect.height), ch: [] }, pos, boxOf(cs));
      const lab = el.options[el.selectedIndex]?.text || ''; const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
      n.ch.push(textNode([[lab, txtStyle(cs)]], cs, { left: rect.left + pl, top: rect.top + (rect.height - parseFloat(cs.fontSize) * 1.3) / 2, width: rect.width - pl, height: parseFloat(cs.fontSize) * 1.3 }, rect, { fw: 0 }));
      n.ch.push(textNode([['expand_more', ['ICON', 400, 0, 14, col(cs.color) || [0, 0, 0, 1], '', '']]], cs, { left: rect.right - 18, top: rect.top + (rect.height - 14) / 2, width: 14, height: 14 }, rect, { fw: 0, lh: 14, ta: 'LEFT' }));
      return n;
    }
    if (tag === 'INPUT') {
      const n = Object.assign({ t: 'F', n: nameOf(el), r: radius(cs, rect.width, rect.height), ch: [] }, pos, boxOf(cs));
      const v = el.value || el.placeholder || ''; const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
      const st = txtStyle(cs); if (!el.value) st[4] = col(getComputedStyle(el, '::placeholder').color) || [0.42, 0.47, 0.46, 1];
      if (v) n.ch.push(textNode([[v, st]], cs, { left: rect.left + pl, top: rect.top + (rect.height - parseFloat(cs.fontSize) * 1.3) / 2, width: rect.width - pl * 2, height: parseFloat(cs.fontSize) * 1.3 }, rect, { fw: 0 }));
      return n;
    }
    const box = boxOf(cs);
    const deco = !!(box.bg || box.gr || box.bd || box.sh);
    const ps = pseudoNodes(el, rect);
    const hasText = /\S/.test(el.textContent);
    // pure text element with no decoration → a single TEXT layer
    const padded = ['Top', 'Right', 'Bottom', 'Left'].some(x => parseFloat(cs['padding' + x]) > 0) && cs.display !== 'inline';
    if (hasText && !deco && !padded && !ps.length && inlineOnly(el) && cs.display !== 'flex' && cs.display !== 'inline-flex' && cs.display !== 'grid') {
      const segs = segsOf(el, cs.whiteSpace); if (!segs.length) return null;
      const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth), pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth), pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
      const tr = { left: rect.left + pl, top: rect.top + pt, width: rect.width - pl - pr, height: rect.height - pt - pb };
      const rg0 = document.createRange(); rg0.selectNodeContents(el);
      return Object.assign(textNode(segs, cs, tr, parentRect, { _mh: rg0.getBoundingClientRect().height }), { n: nameOf(el) });
    }
    const node = Object.assign({ t: 'F', n: nameOf(el), r: radius(cs, rect.width, rect.height), ch: [] }, pos, box);
    if (rot) node.rot = rot;
    if (+cs.opacity < 1) node.op = r3(+cs.opacity);
    let myClip = clip;
    if (cs.overflow !== 'visible' || cs.overflowX !== 'visible' || cs.overflowY !== 'visible') { node.clip = /auto|scroll/.test(cs.overflowY + cs.overflowX) ? 2 : 1; myClip = clipOf(rect, clip); }
    if (hasText && inlineOnly(el) && !ps.length && cs.display !== 'flex' && cs.display !== 'inline-flex') {
      const segs = segsOf(el, cs.whiteSpace);
      const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth), pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth), pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
      if (segs.length) {
        const rg = document.createRange(); rg.selectNodeContents(el); const rr = rg.getBoundingClientRect();
        const tn = Object.assign(textNode(segs, cs, { left: rect.left + pl, top: rect.top + pt, width: rect.width - pl - pr, height: rect.height - pt - pb }, rect, { _mh: rr.height }), { n: 'text' });
        if (tn.sl && rr.width) { // single line in a box: auto layout keeps it placed when edited
          const dx = (rr.left + rr.width / 2) - (rect.left + rect.width / 2), dy = (rr.top + rr.height / 2) - (rect.top + rect.height / 2);
          const jc = Math.abs(dx) < 1.5 ? 'CENTER' : dx < 0 ? 'MIN' : 'MAX', ai = Math.abs(dy) < 1.5 ? 'CENTER' : 'MIN';
          node.al = { d: 'H', gap: 0, pad: [ai === 'MIN' ? r1(rr.top - rect.top) : 0, jc === 'MAX' ? r1(rect.right - rr.right) : 0, 0, jc === 'MIN' ? r1(rr.left - rect.left) : 0], jc, ai, hug: 0 };
          // box is exactly text + padding → hug it, so editing the label resizes the box like the browser would
          if (Math.abs(rr.left - (rect.left + pl)) < 1.5 && Math.abs((rect.right - pr) - rr.right) < 1.5 && Math.abs(rr.top - (rect.top + pt)) < 2.5)
            node.al = { d: 'H', gap: 0, pad: [pt, pr, pb, pl].map(r1), jc: 'MIN', ai: 'CENTER', hug: 1 };
          tn.fw = 0; delete tn.ml; if (cs.textOverflow === 'ellipsis') { tn.fw = 1; tn.ml = 1; tn.grow = 1; }
        }
        node.ch.push(tn);
      }
      return node;
    }
    ps.forEach(p => p.abs = 1); node.ch.push(...ps.filter(p => p.n.startsWith('::before')));
    const flowKids = [];
    for (const c of el.childNodes) {
      if (c.nodeType === 3) {
        if (!/\S/.test(c.data)) continue;
        const rg = document.createRange(); rg.selectNodeContents(c); const rr = rg.getBoundingClientRect(); if (!rr.width || (node.clip && !inter(rr, myClip))) continue;
        let t = c.data.replace(/\s+/g, ' ').trim(); if (!t) continue;
        const tn = textNode([[t, txtStyle(cs)]], cs, rr, rect, { n: 'text' }); tn.fw = rr.height > (parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.25) * 1.6 ? 1 : 0;
        node.ch.push(tn); flowKids.push(tn);
      } else if (c.nodeType === 1) {
        const k = el2node(c, rect, myClip, !!node.clip); if (!k) continue;
        const ccs = getComputedStyle(c);
        if (ccs.position === 'absolute' || ccs.position === 'fixed') k.abs = 1;
        else { flowKids.push(k); k._m = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(ccs['margin' + s]) || 0); k._g = +ccs.flexGrow || 0; k._as = ccs.alignSelf; }
        node.ch.push(k);
      }
    }
    node.ch.push(...ps.filter(p => p.n.startsWith('::after')));
    // flexbox → auto layout, only when the measured positions agree
    if ((cs.display === 'flex' || cs.display === 'inline-flex') && cs.flexWrap === 'nowrap' && /^(row|column)$/.test(cs.flexDirection) && flowKids.length && !ps.some(p => !p.abs)) {
      const H = cs.flexDirection === 'row';
      const pad = ['Top', 'Right', 'Bottom', 'Left'].map(s => r1((parseFloat(cs['padding' + s]) || 0) + (parseFloat(cs['border' + s + 'Width']) || 0)));
      const gap = r1(parseFloat(H ? cs.columnGap : cs.rowGap) || 0);
      const jc = { 'flex-start': 'MIN', normal: 'MIN', start: 'MIN', center: 'CENTER', 'flex-end': 'MAX', end: 'MAX', 'space-between': 'SPACE_BETWEEN' }[cs.justifyContent];
      const ai = { center: 'CENTER', 'flex-end': 'MAX', end: 'MAX', 'flex-start': 'MIN', start: 'MIN', stretch: 'MIN', normal: 'MIN', baseline: 'BASELINE' }[cs.alignItems];
      let ok = jc && ai && flowKids.every(k => !k._m || k._m.every(m => Math.abs(m) < 1.5));
      if (ok && jc !== 'SPACE_BETWEEN') { // verify main-axis packing
        const a = H ? 'x' : 'y', s = H ? 'w' : 'h'; const total = flowKids.reduce((t, k) => t + k[s], 0) + gap * (flowKids.length - 1);
        let p = jc === 'MIN' ? pad[H ? 3 : 0] : jc === 'MAX' ? node[s] - pad[H ? 1 : 2] - total : (node[s] - total) / 2 + (pad[H ? 3 : 0] - pad[H ? 1 : 2]) / 2;
        for (const k of flowKids) { if (Math.abs(k[a] - p) > 2) { ok = false; break; } p += k[s] + gap; }
      }
      if (ok) {
        node.al = { d: H ? 'H' : 'V', gap: jc === 'SPACE_BETWEEN' ? 0 : gap, pad, jc, ai, hug: cs.display === 'inline-flex' ? 1 : 0 };
        for (const k of flowKids) { if (k._g) k.grow = 1; if ((cs.alignItems === 'stretch' || cs.alignItems === 'normal') && (!k._as || k._as === 'auto') && k.t === 'F') k.st = 1; }
      }
    }
    for (const k of flowKids) { delete k._m; delete k._g; delete k._as; }
    if (!node.ch.length) delete node.ch;
    return node;
  }
  const tree = el2node(root, { left: R0.left, top: R0.top }, null);
  tree.x = 0; tree.y = 0;
  for (const e of extras) { const n = el2node(e, R0, null); if (n) { n.abs = 1; (tree.ch ||= []).push(n); } }
  return tree;
};
