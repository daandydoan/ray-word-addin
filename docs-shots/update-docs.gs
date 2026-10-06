// Ray for Word docs, 7 Oct 2026 update. Run main() once. Safe to re-run: every edit checks before it changes.
// DOCS (id map) is defined by the caller, which keeps doc ids out of this public file
const FILE = 'https://www.figma.com/design/yTjFH7kFIb9jbQs19JiPc5';
const SHOT = { "H01": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/H01.png?v=3", "H04": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/H04.png?v=3", "H06": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/H06.png?v=4", "H07": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/H07.png?v=4", "E01": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E01.png?v=3", "E02": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E02.png?v=3", "E03": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E03.png?v=3", "E04": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E04.png?v=3", "E07": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E07.png?v=4", "E08": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E08.png?v=3", "E09": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E09.png?v=4", "E27": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E27.png?v=3", "E34": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E34.png?v=4", "E41": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E41.png?v=3", "E46": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E46.png?v=4", "E48": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E48.png?v=4", "E50": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E50.png?v=3", "E51": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E51.png?v=3", "E52": "https://raw.githubusercontent.com/daandydoan/ray-word-addin/main/docs-shots/E52.png?v=3"}; // code -> fresh Figma screenshot URL of the frame's pane
const NODE = { E50: '71-17198', E51: '71-17726', E52: '76-12816' };
const QS_CAP = { '1. Pick your tender': 'H01', '2. Ray fills the document': 'H07' };
const CHANGES = '7 Oct 2026: step 4 shows which page Ray is reading and can no longer be stopped (RW-07, RW-47, UC-05 retired); Q&A is read-only during the run; the File Manager has file-type tabs; Just chat with Ray skips filling (RW-57, E50, E51); Figma links open in Dev Mode.';
const LOG = [];

function main() {
  for (const [k, id] of Object.entries(DOCS)) {
    const doc = DocumentApp.openById(id), b = doc.getBody(), n0 = LOG.length;
    devLinks(b, k);
    shots(b, k);
    ({ stories, uc, spec, guide, qs })[k](b);
    if (k !== 'qs') e52(b, k);
    if (k !== 'qs') control(b);
    doc.saveAndClose();
    Logger.log(k + ': ' + LOG.slice(n0).join(' | '));
  }
  return LOG.filter(x => /MISS/.test(x));
}

/* ---------- helpers ---------- */
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const dev = u => !u || !/figma\.com\/design\//.test(u) || /[?&]m=dev\b/.test(u) ? u : u + (u.includes('?') ? '&' : '?') + 'm=dev';
function rep(b, find, to) {
  // skip when already applied: the old text is gone, or the new text contains it and is already there
  const hasFind = b.findText(esc(find)), hasTo = b.findText(esc(to));
  if (!hasFind) { if (!hasTo) LOG.push('MISS ' + find.slice(0, 50)); return; }
  if (hasTo && to.includes(find)) return;
  b.replaceText(esc(find), to.replace(/\$/g, '\\$')); LOG.push('rep');
}
function para(b, text) { const r = b.findText(esc(text)); if (!r) return null; let e = r.getElement(); while (e && e.getType() !== DocumentApp.ElementType.PARAGRAPH && e.getType() !== DocumentApp.ElementType.LIST_ITEM) e = e.getParent(); return e; }
function setTxt(el, t, kw, keepBold) { const tx = el.editAsText(); tx.setText(t); if (!keepBold) tx.setBold(false); tx.setLinkUrl(null); if (kw) for (const w of kw) { const i = t.indexOf(w); if (i >= 0) tx.setBold(i, i + w.length - 1, true); } return el; }
// copy the paragraph or list item holding `anchor`, put it after, give it new text (first word bold if bold=true)
function addAfter(b, anchor, text, guard, bold) {
  if (b.findText(esc(guard || text.slice(0, 40)))) return;
  const p = para(b, anchor); if (!p) { LOG.push('MISS anchor ' + anchor.slice(0, 40)); return; }
  const parent = p.getParent(), c = p.copy(), i = parent.getChildIndex(p);
  setTxt(c, text, bold ? [text.split(/\s/)[0]] : null);
  if (p.getType() === DocumentApp.ElementType.LIST_ITEM) parent.insertListItem(i + 1, c); else parent.insertParagraph(i + 1, c);
  LOG.push('add');
}
function drop(b, text) { const p = para(b, text); if (p) { p.removeFromParent(); LOG.push('drop'); } }
function rowOf(b, first) { // table row whose first cell text is exactly `first`
  for (const t of b.getTables()) for (let r = 0; r < t.getNumRows(); r++) { const row = t.getRow(r); if (row.getNumCells() && row.getCell(0).getText().trim() === first) return row; }
  return null;
}
function setRow(b, first, cells) { const row = rowOf(b, first); if (!row) { LOG.push('MISS row ' + first); return; } cells.forEach((v, i) => { if (v != null && row.getCell(i).getText() !== v) { const tx = row.getCell(i).editAsText(); tx.setText(v); tx.setBold(false); } }); LOG.push('row'); }
function addRowAfter(b, after, cells, link) {
  if (rowOf(b, cells[0])) return; const row = rowOf(b, after); if (!row) { LOG.push('MISS row ' + after); return; }
  const t = row.getParent(), nr = t.insertTableRow(t.getChildIndex(row) + 1, row.copy());
  cells.forEach((v, i) => { const tx = nr.getCell(i).editAsText(); tx.setText(v); tx.setBold(false); tx.setLinkUrl(null); });
  if (link) nr.getCell(0).editAsText().setLinkUrl(link); LOG.push('addrow');
}
function dropRow(b, first) { const row = rowOf(b, first); if (row) { row.removeFromParent(); LOG.push('droprow'); } }

// TableCell has no getImages(): walk it for the first inline image
function firstImg(el) { if (el.getType() === DocumentApp.ElementType.INLINE_IMAGE) return el; if (el.getNumChildren) for (let i = 0; i < el.getNumChildren(); i++) { const f = firstImg(el.getChild(i)); if (f) return f; } return null; }

/* ---------- every doc ---------- */
function devLinks(b, k) {
  let n = 0;
  const walk = el => {
    const T = DocumentApp.ElementType;
    if (el.getType() === T.TEXT) {
      const s = el.getText(), idx = el.getTextAttributeIndices();
      for (let i = 0; i < idx.length; i++) { const st = idx[i], en = (i + 1 < idx.length ? idx[i + 1] : s.length) - 1; if (en < st) continue; const u = el.getLinkUrl(st); const d = dev(u); if (d !== u) { el.setLinkUrl(st, en, d); n++; } }
    } else if (el.getType() === T.INLINE_IMAGE) { const u = el.getLinkUrl(), d = dev(u); if (d !== u) { el.setLinkUrl(d); n++; } }
    else if (el.getNumChildren) for (let i = 0; i < el.getNumChildren(); i++) walk(el.getChild(i));
  };
  walk(b); LOG.push('devlinks ' + n);
}
const BLOB = {};
function blob(code) { if (!BLOB[code]) BLOB[code] = UrlFetchApp.fetch(SHOT[code]).getBlob().setName(code + '.png'); return BLOB[code]; }
function swapImg(img, code) {
  const p = img.getParent(), w = img.getWidth(), link = dev(img.getLinkUrl()), i = p.getChildIndex(img);
  const ni = p.insertInlineImage(i, blob(code)); ni.setHeight(Math.round(w * ni.getHeight() / ni.getWidth())).setWidth(w);
  if (link) ni.setLinkUrl(link); img.removeFromParent(); return ni;
}
function shots(b, k) {
  let n = 0;
  for (const img of b.getImages()) {
    let c = img.getParent(); while (c && c.getType() !== DocumentApp.ElementType.TABLE_CELL) c = c.getParent();
    if (!c) continue;
    const txt = c.getText(); let code = (txt.match(/\b([HE]\d\d) in Figma/) || [])[1];
    if (k === 'qs') code = QS_CAP[txt.trim()];
    if (code && SHOT[code]) { swapImg(img, code); n++; }
  }
  LOG.push('shots ' + n);
}
// add a screenshot cell for `code` to the shots row that has a cell for `anchor`
function addShot(b, anchor, code, title) {
  let at = null;
  for (const t of b.getTables()) for (let r = 0; r < t.getNumRows(); r++) for (let i = 0; i < t.getRow(r).getNumCells(); i++) {
    const cell = t.getRow(r).getCell(i), s = cell.getText();
    if (s.includes(code + ' in Figma')) return;
    if (!at && s.includes(anchor + ' in Figma')) at = cell;
  }
  if (!at) { LOG.push('MISS shot ' + anchor); return; }
  const row = at.getParent();
  // drop leftover copies of the anchor cell from an interrupted run
  for (let i = row.getNumCells() - 1; i >= 0; i--) { const c = row.getCell(i); if (c !== at && c.getText().includes(anchor + ' in Figma') && i > row.getChildIndex(at)) { c.removeFromParent(); LOG.push('dedupe'); } }
  const nc = row.appendTableCell(at.copy());
  const img = firstImg(nc); if (img) swapImg(img, code);
  const url = FILE + '?node-id=' + NODE[code] + '&m=dev';
  const r = nc.findText(anchor + ' in Figma.*'); if (r) { const tx = r.getElement().asText(); tx.setLinkUrl(null); tx.setText(code + ' in Figma ' + title); tx.setLinkUrl(0, (code + ' in Figma').length - 1, url); }
  LOG.push('addshot ' + code);
}
function swapShot(b, from, to, title, skip) {
  for (const t of b.getTables()) for (let r = 0; r < t.getNumRows(); r++) {
    const row = t.getRow(r); let rowTxt = ''; for (let i = 0; i < row.getNumCells(); i++) rowTxt += row.getCell(i).getText() + ' / ';
    if (skip && rowTxt.includes(skip + ' in Figma')) continue;
    for (let i = 0; i < row.getNumCells(); i++) { const cell = row.getCell(i); if (!cell.getText().includes(from + ' in Figma')) continue;
      const img = firstImg(cell); if (img) swapImg(img, to);
      const f = cell.findText(from + ' in Figma.*'); if (f) { const tx = f.getElement().asText(); tx.setLinkUrl(null); tx.setText(to + ' in Figma ' + title); tx.setLinkUrl(0, (to + ' in Figma').length - 1, FILE + '?node-id=' + NODE[to] + '&m=dev'); }
      LOG.push('swap ' + from + '>' + to); }
  }
}
// like addShot, but only checks the anchor's own row, so RW-57 gets E52 even though RW-01 already has it
function addShotInRow(b, anchor, code, title) {
  for (const t of b.getTables()) for (let r = 0; r < t.getNumRows(); r++) {
    const row = t.getRow(r); let at = null, has = false;
    for (let i = 0; i < row.getNumCells(); i++) { const s = row.getCell(i).getText(); if (s.includes(code + ' in Figma')) has = true; if (!at && s.includes(anchor + ' in Figma')) at = row.getCell(i); }
    if (!at || has) continue;
    const nc = row.appendTableCell(at.copy()); const img = firstImg(nc); if (img) swapImg(img, code);
    const f = nc.findText(anchor + ' in Figma.*'); if (f) { const tx = f.getElement().asText(); tx.setLinkUrl(null); tx.setText(code + ' in Figma ' + title); tx.setLinkUrl(0, (code + ' in Figma').length - 1, FILE + '?node-id=' + NODE[code] + '&m=dev'); }
    LOG.push('addshot-row ' + code);
  }
}
function e52(b, k) {
  const T = 'Choose the tender: Just chat with Ray';
  swapShot(b, 'E50', 'E52', T, 'E51');
  if (k === 'stories') addShotInRow(b, 'E51', 'E52', T);
}
function control(b) {
  const v = rowOf(b, 'Version'); if (v && v.getCell(1).getText().trim() === '0.2') v.getCell(1).editAsText().setText('0.3');
  const d = rowOf(b, 'Date'); if (d && /3 October 2026/.test(d.getCell(1).getText())) d.getCell(1).editAsText().setText('7 October 2026');
  addRowAfter(b, 'Date', ['Changes in 0.3', CHANGES]);
}
// keep the heading and shots, swap the story or flow text for a retired note
function headingPara(b, text) { let r = b.findText(esc(text)); while (r) { const p = para0(r.getElement()); if (p && p.getType() === DocumentApp.ElementType.PARAGRAPH && p.asParagraph().getHeading() !== DocumentApp.ParagraphHeading.NORMAL) return p; r = b.findText(esc(text), r); } return null; }
function para0(e) { while (e && e.getType() !== DocumentApp.ElementType.PARAGRAPH && e.getType() !== DocumentApp.ElementType.LIST_ITEM) e = e.getParent(); return e; }
function retire(b, heading, note) {
  const h = headingPara(b, heading); if (!h) { LOG.push('MISS retire ' + heading); return; }
  if (!/retired/.test(h.getText())) h.editAsText().appendText(' (retired)');
  const parent = h.getParent(), T = DocumentApp.ElementType; let i = parent.getChildIndex(h) + 1, first = true; const kill = [];
  for (; i < parent.getNumChildren(); i++) {
    const e = parent.getChild(i);
    if (e.getType() === T.PARAGRAPH && e.asParagraph().getHeading() !== DocumentApp.ParagraphHeading.NORMAL) break;
    if (e.getType() === T.LIST_ITEM) { kill.push(e); continue; }
    if (e.getType() === T.PARAGRAPH && e.asParagraph().getText().trim()) { if (first) { setTxt(e, note); first = false; } else kill.push(e); }
  }
  kill.forEach(e => e.removeFromParent()); LOG.push('retire ' + heading.slice(0, 6));
}

/* ---------- per doc ---------- */
function common(b) {
  rep(b, 'Answering while Ray works', 'Locked while Ray reads');
  rep(b, 'Fill this document: Paused', 'Fill this document: Paused (retired)');
  rep(b, 'Fill this document: Undone', 'Fill this document: Undone (retired)');
}
function stories(b) {
  common(b);
  rep(b, 'One pass of Analyse and fill: read the document, find the questions, match the library, draft the rest.', 'One pass of Analyse and fill: read the document, find the questions, match the library, draft the rest. Once started it can\'t be stopped; progress shows as the page Ray is reading.');
  addAfter(b, 'returns me to Ask Ray with a "Confirm the tender first" toast', 'And Just chat with Ray, under the list, skips filling and opens the chat (RW-57)', 'Just chat with Ray, under the list', true);
  addShot(b, 'E02', 'E50', 'Conversation: Just chat (no fill)');
  rep(b, 'a collapsible Folders section and a collapsible Files section', 'file-type tabs (All, Resumes, Case Studies, Policies, Insurances, Certifications, Organisation Chart, Others), a collapsible Folders section and a collapsible Files section');
  rep(b, 'folders are same-size cards with file counts; the chosen folder turns dark and narrows the files', 'a tab shows only that type and the folders that hold it; folders are same-size cards with file counts; the chosen folder turns dark and narrows the files further');
  rep(b, 'Watch Ray analyse and fill, without being locked out', 'Watch Ray analyse and fill');
  rep(b, 'so that I know where it is and can keep working.', 'so that I know how far it has got.');
  rep(b, 'Ray lists its steps as they run: reading the document n/8 sections, finding questions, matching the Response Library, drafting the rest', 'a progress bar shows the page Ray is reading, for example "Reading page 6 of 13", with the percent read');
  rep(b, 'Stop sits under the steps with "You can start answering in Q&A."', 'the run cannot be stopped, and Q&A is read-only until it finishes');
  rep(b, 'a "Ray is filling answers · n of 32" card with a progress bar sits above Apply to document', 'a "Ray is reading page n of 13" bar sits above Apply to document, which stays greyed out until the run ends');
  retire(b, 'RW-07 Answer while Ray is still working', 'Retired 7 Oct 2026. Q&A is read-only until Ray finishes reading, so there is nothing to answer during the run (see RW-03).');
  retire(b, 'RW-47 Stop, carry on or undo a run', 'Retired 7 Oct 2026. A run can no longer be stopped, so there is no Paused or Undone state. E05 and E06 stay in Figma, faded. To take an answer out, reject it in Word\'s Review tab.');
  rep(b, 'Whether undo can find every answer the run put in, and what it does to answers the writer has since edited', 'Retired 7 Oct 2026. Runs can no longer be stopped or undone');
  rep(b, 'OQ-7 Undo this run: if the writer has edited an answer the run put in, does undo take their edit out too?', 'OQ-7 Undo this run: closed 7 Oct 2026. RW-47 is retired because a run can no longer be stopped or undone.');
  rep(b, 'opens on the run with "Picking up where I left off · n of 32 done."', 'opens on the run with "Picking up where I left off." and the progress bar keeps its page');
  rep(b, 'the steps continue from there', 'the run continues from there');
  addAfter(b, 'it unlocks as soon as the run finishes', 'And Just chat with Ray in step 1 skips the run and unlocks it straight away (RW-57)', 'skips the run and unlocks it straight away', true);
  newStory(b);
}
function newStory(b) {
  if (b.findText('RW-57 Just chat with Ray')) return;
  const h = headingPara(b, 'RW-52 Chat waits for the run'); if (!h) { LOG.push('MISS RW-52'); return; }
  const parent = h.getParent(), T = DocumentApp.ElementType; let i = parent.getChildIndex(h) + 1; const blk = [h];
  for (; i < parent.getNumChildren(); i++) { const e = parent.getChild(i); if (e.getType() === T.PARAGRAPH && e.asParagraph().getHeading() !== DocumentApp.ParagraphHeading.NORMAL) break; blk.push(e); }
  let at = i;
  const lines = ['RW-57 Just chat with Ray, without filling',
    'As a bid writer, I want to skip filling and go straight to the chat, so that I can ask Ray about a document without running the 4 steps.'];
  const gwt = ['Given step 1 is showing the tender list', 'When I choose Just chat with Ray under the list', 'Then the fill steps go away and the Ask Ray chat opens, ready to type',
    'And Q&A says "Questions show here once Ray fills this document." with a Fill this document button that brings the steps back', 'And the tender rule in RW-01 and the chat rule in RW-52 do not apply while I chat'];
  let li = 0, pi = 0;
  for (const e of blk) {
    const c = e.copy(), t = c.getType();
    if (t === T.PARAGRAPH && c.asParagraph().getHeading() !== DocumentApp.ParagraphHeading.NORMAL) { setTxt(c, lines[0], null, true); parent.insertParagraph(at++, c); }
    else if (t === T.LIST_ITEM) { if (li < gwt.length) { setTxt(c, gwt[li], [gwt[li].split(' ')[0]]); parent.insertListItem(at++, c); li++; } }
    else if (t === T.PARAGRAPH) { const s = c.asParagraph().getText(); if (/^Size/.test(s)) setTxt(c, 'Size S   |   Priority Should', ['Size', 'Priority']); else if (s.trim()) setTxt(c, lines[1], ['As a', 'I want', 'so that']); parent.insertParagraph(at++, c); pi++; }
    else if (t === T.TABLE) { const tb = parent.insertTable(at++, c); const cell = tb.getRow(0).getCell(0); while (tb.getRow(0).getNumCells() > 1) tb.getRow(0).getCell(1).removeFromParent();
      const img = firstImg(cell); if (img) swapImg(img, 'E50'); const r = cell.findText('[HE]\\d\\d in Figma.*'); if (r) { const tx = r.getElement().asText(); tx.setLinkUrl(null); tx.setText('E50 in Figma Conversation: Just chat (no fill)'); tx.setLinkUrl(0, 11, FILE + '?node-id=' + NODE.E50 + '&m=dev'); }
      const c2 = tb.getRow(0).appendTableCell(cell.copy()); const img2 = firstImg(c2); if (img2) swapImg(img2, 'E51'); const r2 = c2.findText('E50 in Figma.*'); if (r2) { const tx = r2.getElement().asText(); tx.setText('E51 in Figma Chat only: Fill this document'); tx.setLinkUrl(0, 11, FILE + '?node-id=' + NODE.E51 + '&m=dev'); } }
  }
  LOG.push('RW-57');
}
function uc(b) {
  common(b);
  rep(b, 'H01, E01, E02, E50, E51', 'H01, E01, E02, E50, E51, E52'); rep(b, 'H01, E01, E02', 'H01, E01, E02, E50, E51, E52');
  addAfter(b, '3a No match: "No tenders match."', '2b Just chat with Ray, under the list (E52), skips filling and opens the chat (E50). Q&A then says questions show once Ray fills the document, with Fill this document to start (E51).', '2b Just chat with Ray');
  rep(b, 'the pane returns to Ask Ray with "Confirm the tender first".', 'the pane returns to Ask Ray with "Confirm the tender first", unless the writer chose Just chat with Ray.');
  // E50 shot added 7 Oct, then swapped to E52 by e52()
  rep(b, 'Select File opens the File Manager sheet: search, Folders, Files.', 'Select File opens the File Manager sheet: search, file-type tabs, Folders, Files.');
  rep(b, '2a A folder card narrows the files. Search covers all folders.', '2a A file-type tab shows only that type and the folders that hold it. A folder card narrows the files further. Search covers the current tab.');
  rep(b, 'Ray shows its steps: read the document, find questions, match the Response Library, draft the rest.', 'A progress bar shows the page Ray is reading, for example "Reading page 6 of 13". The run cannot be stopped.');
  rep(b, '3a The writer opens Q&A during the run: see UC-08.', '3a The writer opens Q&A during the run: the list is read-only until the run ends (UC-08).');
  rep(b, '3b The writer stops the run: see UC-05.', '3b Stopping a run is no longer possible. UC-05 is retired.');
  rep(b, 'Stop, carry on or undo a run', 'Stop, carry on or undo a run (retired)');
  rep(b, 'Stop during step 4', 'None. Retired 7 Oct 2026');
  rep(b, 'Run paused, resumed or undone', 'None. Retired');
  rep(b, 'Status shows Paused and how many answers are in.', 'Retired 7 Oct 2026. A run can no longer be stopped, so there is no Paused or Undone state. E05 and E06 stay in Figma, faded.');
  drop(b, 'Carry on resumes the run.');
  rep(b, '2a Undo this run removes everything the run added. Start again reruns it.', 'None. Retired with UC-05.');
  rep(b, 'Ask Ray shows "Picking up where I left off · n of 32 done."', 'Ask Ray shows "Picking up where I left off." and the progress bar keeps its page.');
  rep(b, '1b Run still going: a progress card sits above Apply to document.', '1b Run still going: the list is read-only and faded, a "Ray is reading page n of 13" bar sits above Apply to document, and Apply to document is greyed out.');
  rep(b, 'Before the run ends, chat is disabled. Hover explains why.', 'Before the run ends, chat is disabled. Hover explains why. Just chat with Ray in step 1 opens it straight away (E50).');
  rep(b, '"I couldn\'t find any questions in this document."', '"I read all 13 pages but couldn\'t find any questions."');
}
function spec(b) {
  common(b);
  rep(b, 'Figma file, 48 frames at 1440 × 900', 'Figma file, 66 frames at 1440 × 900 (E05, E06 retired)'); rep(b, '65 frames at 1440 × 900', '66 frames at 1440 × 900');
  rep(b, 'E01 to E34 are edge cases', 'E01 to E52 are edge cases and failure paths'); rep(b, 'E01 to E51 are edge cases', 'E01 to E52 are edge cases');
  rep(b, 'Shown at 55% opacity and disabled until the run finishes.', 'Shown at 55% opacity and disabled until the run finishes, unless the user chose Just chat with Ray (E50).');
  setRow(b, 'E05', [null, null, null, 'Paused (retired)']); setRow(b, 'E06', [null, null, null, 'Undone (retired)']);
  addRowAfter(b, 'E34', ['E50', 'Ask Ray', 'Conversation', 'Just chat (no fill)', 'H01'], FILE + '?node-id=' + NODE.E50 + '&m=dev');
  addRowAfter(b, 'E50', ['E51', 'Q&A list', 'Chat only', 'Fill this document', 'H01'], FILE + '?node-id=' + NODE.E51 + '&m=dev');
  addRowAfter(b, 'E51', ['E52', 'Ask Ray', 'Choose the tender', 'Just chat with Ray', 'H01'], FILE + '?node-id=' + NODE.E52 + '&m=dev');
  addRowAfter(b, 'Tender rows', ['Just chat with Ray', '"or" divider, then a ghost button with a chat icon, under the tender list', 'Skips filling and opens the chat (E52, then E50). Q&A then says "Questions show here once Ray fills this document." with Fill this document, which brings the steps back (E51)']);
  // E50 shot added 7 Oct, then swapped to E52 by e52()
  setRow(b, 'Status chip', [null, 'Bolt icon and "Reading the document"', 'Static until the run finishes']);
  rep(b, 'Spinner "Working…", then read_document, find_questions, match_library, draft_answers with counts', '"Reading page n of 13", the percent read, and a bar that fills as pages are read');
  rep(b, 'Each step ticks when done', 'The page Ray is reading is the only progress it reports. The run cannot be stopped; Q&A is read-only until it ends (E08)');
  setRow(b, 'Ray steps', ['Progress']);
  dropRow(b, 'Stop');
  setRow(b, 'Paused (E05)', [null, 'Retired 7 Oct 2026. A run can no longer be stopped', 'Frame kept, faded, for reference']);
  setRow(b, 'Undone (E06)', [null, 'Retired 7 Oct 2026. A run can no longer be undone', 'Frame kept, faded, for reference']);
  rep(b, '"Picking up where I left off · n of 32 done." above the steps', '"Picking up where I left off." above the progress bar, which keeps its page');
  rep(b, 'A collapsed line, "Read 8 sections · found 43 questions", then the 4 steps. Then:', 'A line, "Read all 13 pages · found 43 questions". Then:');
  rep(b, 'The collapsed line expands to show Ray\'s thinking', 'Static');
  rep(b, 'Filters files across every folder (E04); folders stay put', 'Filters files in the current tab (E04); folders stay put');
  addRowAfter(b, 'Search files', ['File-type tabs', 'All, Resumes, Case Studies, Policies, Insurances, Certifications, Organisation Chart, Others, each with a count; the row scrolls sideways', 'Click shows only that type and the folders that hold it, and resets the folder to All files. The underline slides to the tab and the content slides the way you moved (E03)']);
  rep(b, 'Collapsible section of same-size cards in two columns: All files 9, Tender documents 2, Insurance 3, Licences 2, Company 2', 'Collapsible section of same-size cards in two columns, only the folders that hold the current tab\'s files. On All: All files 15, Company 7, Tender documents 3, Insurance 3, Licences 2');
  rep(b, 'Ray icon, "Ray is filling answers · n of 32", progress bar', 'Ray icon, "Ray is reading page n of 13", the percent and a progress bar');
  rep(b, 'Shown above Apply to document while the run is going', 'Shown above Apply to document while the run is going. The list is read-only and faded and Apply to document is greyed out until it ends (E08)');
  setRow(b, 'Warning status', [null, null, 'Failure statuses']);
}
function guide(b) {
  common(b);
  rep(b, 'Chat is disabled until the run ends.', 'Chat is disabled until the run ends, unless you choose Just chat with Ray.');
  rep(b, 'Choose the tender. Search by name or reference, then click it.', 'Choose the tender. Search by name or reference, then click it. To skip filling and just ask Ray questions, choose Just chat with Ray under the list.');
  rep(b, 'Pick a folder or search, tick files, choose Attach files.', 'Pick a file-type tab, a folder or search, tick files, choose Attach files.');
  rep(b, 'Analyse and fill. Starts on its own. Ray shows each step as it runs.', 'Analyse and fill. Starts on its own. A bar shows which page Ray is reading, for example page 6 of 13.');
  rep(b, 'You can answer in Q&A. Ray skips what you answer.', 'Q&A is read-only until Ray finishes reading. Answering and Apply to document unlock when the run ends.');
  rep(b, 'Stop pauses. Carry on resumes.', 'The run can\'t be stopped.');
  rep(b, 'Undo this run removes everything the run added. Start again reruns it.', 'To take an answer out, reject it in Word\'s Review tab.');
  rep(b, 'Ray is still on it. You can answer anyway', 'Ray is still on it. You can answer when the run ends');
  rep(b, 'Chat opens after the run. Finish the 4 steps.', 'Chat opens after the run. Or choose Just chat with Ray in step 1 to skip filling.');
  // E50 shot added 7 Oct, then swapped to E52 by e52()
}
function qs(b) {
  rep(b, 'Search by name or reference, then click it.', 'Search by name or reference, then click it. Only want to ask Ray something? Choose Just chat with Ray instead.');
  rep(b, 'puts in your library answers and drafts the rest.', 'puts in your library answers and drafts the rest. A bar shows which page it is on. You can\'t stop it or answer until it finishes.');
}
