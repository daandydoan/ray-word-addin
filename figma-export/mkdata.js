// mkdata.js: plan/*.json -> upload payloads in out/
const fs = require('fs'); const P = __dirname + '/plan/'; fs.mkdirSync(__dirname + '/out', { recursive: true });
const W = (f, o) => fs.writeFileSync(__dirname + '/out/' + f, JSON.stringify(o));
const tok = JSON.parse(fs.readFileSync(P + 'tokens.json'));
W('tokens.json', { kind: 'tokens', tokens: tok.tokens, styles: tok.styles });
W('components.json', { kind: 'components', sets: JSON.parse(fs.readFileSync(P + 'components.json')) });
const NAMES = {
  H01: ['Setup / Choose a tender / Default'], H02: ['Setup / Choose a folder / Default'], H03: ['Setup / Reading the document / In progress'],
  H04: ['Q&A list / All questions / Ray scanning'], H05: ['Q&A list / All questions / Analysis finished'], H06: ['Q&A list / All questions / Open questions'],
  H07: ['Question card / 3.7 Product substitution / Empty'], H08: ['Question card / 3.7 Product substitution / Answer written'], H09: ['Question card / 4.1 Local employment / After Insert & next'],
  H10: ['Q&A list / All questions / Inserted'], H11: ['Question card / 3.2 Stock holdings / Autofilled'], H12: ['Question card / 3.2 Stock holdings / Edited'],
  H13: ['Q&A list / All questions / Drafts ready'], H14: ['Q&A list / All questions / Applied'],
  E01: ['Q&A list / All questions / Answering during scan', 'H04'], E02: ['Question card / 2.3 Similar contracts / Ray analysing', 'H04'],
  E03: ['Q&A list / All questions / No library match', 'H06'], E04: ['Q&A list / Inline answer / Typing short', 'H06'], E05: ['Q&A list / Inline answer / Getting long', 'H06'],
  E06: ['Q&A list / Inline answer / Draft kept', 'H06'], E07: ['Q&A list / All questions / Assigned to teammate', 'H06'],
  E08: ['Q&A list / All questions / Edited by teammate', 'H10'], E09: ['Question card / 3.1 Delivery lead times / Edited by teammate', 'H10'], E10: ['Q&A list / All questions / Show more expanded', 'H10'],
  E11: ['Question card / 7.4 Professional indemnity / Empty', 'H07'], E12: ['Question card / 7.4 Professional indemnity / Assign menu', 'H07'], E13: ['Question card / 7.4 Professional indemnity / Generate from a file', 'H07'],
  E14: ['Question card / 7.4 Professional indemnity / Ray generating', 'H08'], E15: ['Question card / 7.4 Professional indemnity / Draft ready', 'H08'], E16: ['Question card / 7.4 Professional indemnity / Full-screen dialog', 'H08'],
  E17: ['Q&A list / Not a Question / Dismissed', 'H07'], E18: ['Q&A list / Assigned / Default', 'H05'], E19: ['Q&A list / All questions / Filter by person', 'H05'],
  E20: ['Q&A list / All questions / Status filter empty', 'H05'], E21: ['Header / Notifications / Open', 'H05'], E22: ['Question card / 1.1 Legal company name / First in queue', 'H07'],
};
const pos = {}, stack = {};
for (const [id, [, br]] of Object.entries(NAMES)) {
  if (!br) pos[id] = { x: (+id.slice(1) - 1) * 1640, y: 0 };
  else { const j = stack[br] = (stack[br] || 0) + 1; pos[id] = { x: (+br.slice(1) - 1) * 1640, y: j * 1140 + 160 }; }
}
for (const id of Object.keys(NAMES)) W(id + '.json', { kind: 'screens', screens: [{ id, name: NAMES[id][0], x: pos[id].x, y: pos[id].y, tree: JSON.parse(fs.readFileSync(P + id + '.json')) }] });
fs.writeFileSync(__dirname + '/out/names.json', JSON.stringify({ NAMES, pos }));
console.log('ok', Object.keys(NAMES).length);
