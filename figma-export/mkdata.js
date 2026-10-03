// mkdata.js: plan/*.json -> upload payloads in out/
const fs = require('fs'); const P = __dirname + '/plan/'; fs.mkdirSync(__dirname + '/out', { recursive: true });
const W = (f, o) => fs.writeFileSync(__dirname + '/out/' + f, JSON.stringify(o));
const tok = JSON.parse(fs.readFileSync(P + 'tokens.json'));
W('tokens.json', { kind: 'tokens', tokens: tok.tokens, styles: tok.styles });
W('components.json', { kind: 'components', sets: JSON.parse(fs.readFileSync(P + 'components.json')) });
const NAMES = {
  H01: ['Setup / Choose a tender / Default'], H02: ['Setup / Choose a folder / Default'], H03: ['Setup / Reading the document / In progress'],
  H04: ['Q&A list / All questions / Ray scanning'], H05: ['Q&A list / All questions / Analysis finished'], H06: ['Q&A list / All questions / Open and AI drafts'],
  H07: ['Question card / 4.1 Local employment / Empty'], H08: ['Question card / 4.1 Local employment / Answer written'], H09: ['Question card / 4.3 Indigenous participation / After Put in document & next'],
  H10: ['Q&A list / All questions / Inserted'], H11: ['Question card / 3.2 Stock holdings / Response Library answer'], H12: ['Question card / 3.2 Stock holdings / Edited'],
  H13: ['Q&A list / All questions / Drafts ready'], H14: ['Q&A list / All questions / Applied'],
  E01: ['Q&A list / All questions / Answering during scan', 'H04'], E02: ['Question card / 2.3 Similar contracts / Ray analysing', 'H04'],
  E03: ['Q&A list / All questions / AI generated drafts', 'H06'], E04: ['Q&A list / Inline answer / Typing short', 'H06'], E05: ['Q&A list / Inline answer / Getting long', 'H06'],
  E06: ['Q&A list / Inline answer / Draft kept', 'H06'], E07: ['Q&A list / All questions / Assigned to teammate', 'H06'],
  E08: ['Q&A list / All questions / Edited by teammate', 'H10'], E09: ['Question card / 3.1 Delivery lead times / Edited by teammate', 'H10'], E10: ['Q&A list / All questions / Show more expanded', 'H10'],
  E11: ['Question card / 6.1 Pricing basis / Open', 'H07'], E12: ['Question card / 6.1 Pricing basis / Assign menu', 'H07'], E13: ['Question card / 6.1 Pricing basis / Ray · Draft from a file', 'H07'],
  E14: ['Question card / 6.1 Pricing basis / Ray · Drafting', 'H08'], E15: ['Question card / 6.1 Pricing basis / Ray · Reply', 'H08'], E16: ['Question card / 6.1 Pricing basis / Full screen', 'H08'],
  E17: ['Q&A list / Not a Question / Dismissed', 'H07'], E18: ['Q&A list / Assigned / Default', 'H05'], E19: ['Q&A list / All questions / Filter by person', 'H05'],
  E20: ['Q&A list / All questions / Status filter · Open', 'H05'], E21: ['Header / Notifications / Open', 'H05'], E22: ['Question card / 1.1 Legal company name / First in queue', 'H07'],
  E23: ['Question card / 6.1 Pricing basis / Ray · Use this answer', 'H08'], E24: ['Question card / 6.1 Pricing basis / Full screen · Ray', 'H08'],
  E25: ['Ask Ray / Conversation / Follow-up', 'H05'], E26: ['Question card / 7.4 Professional indemnity / AI generated draft', 'H06'],
};
const OLD = { H01: '18:8546', H02: '18:9046', H03: '18:9546', H04: '18:10032', H05: '18:10745', H06: '18:11371', H07: '18:11983', H08: '18:12544', H09: '18:13106', H10: '18:13669', H11: '18:14285', H12: '18:14849', H13: '18:15411', H14: '18:16023',
  E01: '18:16639', E02: '18:17333', E03: '18:17830', E04: '18:18449', E05: '18:19070', E06: '18:19680', E07: '18:20291', E08: '18:20910', E09: '18:21539', E10: '18:22104', E11: '18:22701', E12: '18:23260', E13: '18:23841', E14: '18:24417', E15: '18:24937', E16: '18:25497', E17: '18:7925', E18: '18:26103', E19: '18:26722', E20: '18:27329', E21: '18:27930', E22: '18:28565' };
const pos = {}, stack = {};
for (const [id, [, br]] of Object.entries(NAMES)) {
  if (!br) pos[id] = { x: (+id.slice(1) - 1) * 1640, y: 0 };
  else { const j = stack[br] = (stack[br] || 0) + 1; pos[id] = { x: (+br.slice(1) - 1) * 1640, y: j * 1140 + 160 }; }
}
for (const id of Object.keys(NAMES)) W(id + '.json', { kind: 'screens', screens: [{ id, target: OLD[id], name: NAMES[id][0], x: pos[id].x, y: pos[id].y, tree: JSON.parse(fs.readFileSync(P + id + '.json')) }] });
fs.writeFileSync(__dirname + '/out/names.json', JSON.stringify({ NAMES, pos }));
console.log('ok', Object.keys(NAMES).length);
