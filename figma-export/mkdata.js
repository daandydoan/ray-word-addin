// mkdata.js: plan/*.json -> upload payloads in out/
const fs = require('fs'); const P = __dirname + '/plan/'; fs.mkdirSync(__dirname + '/out', { recursive: true });
const W = (f, o) => fs.writeFileSync(__dirname + '/out/' + f, JSON.stringify(o));
const tok = JSON.parse(fs.readFileSync(P + 'tokens.json'));
W('tokens.json', { kind: 'tokens', tokens: tok.tokens, styles: tok.styles });
W('components.json', { kind: 'components', sets: JSON.parse(fs.readFileSync(P + 'components.json')) });
const NAMES = {
  H01: ['Ask Ray / Fill this document / 1 Choose the tender'], H02: ['Ask Ray / Fill this document / 2 Choose where to upload'], H03: ['Ask Ray / Fill this document / 3 Add reference documents'],
  H04: ['Ask Ray / File Manager / Files selected'], H05: ['Ask Ray / Fill this document / 3 References chosen'], H06: ['Ask Ray / Fill this document / 4 Analysing and filling'],
  H07: ['Ask Ray / Fill this document / Finished'], H08: ['Q&A list / All questions / Review in Q&A'], H09: ['Q&A list / All questions / Needs Review drafts'],
  H10: ['Question card / Needs Review draft / Default'], H11: ['Question card / 4.1 Local employment / Empty'], H12: ['Question card / 4.1 Local employment / Answer written'],
  H13: ['Question card / Next question / After Put in document & next'], H14: ['Q&A list / All questions / Back from the card'],
  E01: ['Ask Ray / Choose the tender / Search', 'H01'], E02: ['Ask Ray / Choose the tender / No match', 'H01'],
  E03: ['Ask Ray / File Manager / Folder filter', 'H04'], E04: ['Ask Ray / File Manager / Search', 'H04'],
  E05: ['Ask Ray / Fill this document / Paused', 'H06'], E06: ['Ask Ray / Fill this document / Undone', 'H06'], E07: ['Ask Ray / Fill this document / Reopened mid-run', 'H06'], E08: ['Q&A list / All questions / Answering while Ray works', 'H06'],
  E09: ['Ask Ray / Fill this document / Protected document', 'H07'], E34: ['Ask Ray / Conversation / Chat unlocked', 'H07'],
  E10: ['Q&A list / Inline answer / Typing short', 'H08'], E11: ['Q&A list / Inline answer / Getting long', 'H08'], E12: ['Q&A list / Inline answer / Draft kept', 'H08'], E13: ['Q&A list / All questions / Back to pill', 'H08'],
  E14: ['Q&A list / All questions / Assigned to teammate', 'H09'], E16: ['Q&A list / All questions / Status filter · Needs Review', 'H09'], E17: ['Q&A list / All questions / Status filter · Open', 'H09'],
  E15: ['Question card / 3.2 Stock holdings / Response Library answer', 'H10'],
  E18: ['Q&A list / Assigned / Default', 'H14'], E19: ['Q&A list / All questions / Filter by person', 'H14'], E20: ['Header / Notifications / Open', 'H14'], E21: ['Header / More menu / Open', 'H14'], E22: ['Header / Keyboard shortcuts / Sheet', 'H14'], E23: ['Header / Changelog / Sheet', 'H14'],
  E24: ['Question card / 6.1 Pricing basis / Open', 'H11'], E25: ['Question card / 6.1 Pricing basis / Assign menu', 'H11'], E33: ['Question card / 1.1 Legal company name / First in queue', 'H11'],
  E26: ['Question card / 6.1 Pricing basis / Ray · Draft from a file', 'H12'], E27: ['Question card / 6.1 Pricing basis / Ray · File Manager', 'H12'], E28: ['Question card / 6.1 Pricing basis / Ray · Drafting', 'H12'], E29: ['Question card / 6.1 Pricing basis / Ray · Reply', 'H12'],
  E30: ['Question card / 6.1 Pricing basis / Ray · Use this answer', 'H13'], E31: ['Question card / 6.1 Pricing basis / Full screen', 'H13'], E32: ['Q&A list / Not a Question / Dismissed', 'H13'],
  E35: ['Q&A list / Missed question / Right-click menu', 'H08'], E36: ['Q&A list / Missed question / Added as Needs Review', 'H08'],
  E37: ["Q&A list / Protected document / Couldn't insert rows", 'H07'], E38: ['Ask Ray / Choose the tender / No tenders', 'H01'],
  E39: ['Ask Ray / Choose the tender / Loading', 'H01'], E40: ['Ask Ray / Choose where to upload / No folders', 'H02'], E41: ['Ask Ray / File Manager / Empty', 'H04'],
  E42: ['Ask Ray / Add reference documents / Unsupported file', 'H03'], E43: ['Ask Ray / Fill this document / Upload failed', 'H06'],
  E44: ['Ask Ray / Fill this document / Library unreachable', 'H06'], E45: ['Ask Ray / Fill this document / Connection lost', 'H06'],
  E46: ['Ask Ray / Fill this document / No questions found', 'H07'], E47: ["Q&A list / Inline answer / Couldn't insert", 'H08'],
  E48: ["Ask Ray / Conversation / Ray can't answer", 'H07'], E49: ['Header / Session expired / Sheet', 'H14'],
};
const OLD = { H01: '18:8546', H02: '18:9046', H03: '18:9546', H04: '18:10032', H05: '18:10745', H06: '18:11371', H07: '18:11983', H08: '18:12544', H09: '18:13106', H10: '18:13669', H11: '18:14285', H12: '18:14849', H13: '18:15411', H14: '18:16023',
  E01: '18:16639', E02: '18:17333', E03: '18:17830', E04: '18:18449', E05: '18:19070', E06: '18:19680', E07: '18:20291', E08: '18:20910', E09: '18:21539', E10: '18:22104', E11: '18:22701', E12: '18:23260', E13: '18:23841', E14: '18:24417', E15: '18:24937', E16: '18:25497', E17: '18:7925', E18: '18:26103', E19: '18:26722', E20: '18:27329', E21: '18:27930', E22: '18:28565', E23: '32:26203', E24: '32:26766', E25: '32:27332', E26: '32:27970',
  E27: '35:21310', E28: '35:21999', E29: '35:22573', E30: '35:23167', E31: '35:23730', E32: '35:24263', E33: '35:24868', E34: '35:25430', E35: '50:5774', E36: '50:6453', E37: '50:7112', E38: '50:7738',
  E39: '58:6257', E40: '58:6800', E41: '58:7339', E42: '58:7946', E43: '58:8501', E44: '58:9065', E45: '58:9629', E46: '58:10199', E47: '58:10763', E48: '58:11420', E49: '58:12059' };
const pos = {}, stack = {};
for (const [id, [, br]] of Object.entries(NAMES)) {
  if (!br) pos[id] = { x: (+id.slice(1) - 1) * 1640, y: 0 };
  else { const j = stack[br] = (stack[br] || 0) + 1; pos[id] = { x: (+br.slice(1) - 1) * 1640, y: j * 1140 + 160 }; }
}
for (const id of Object.keys(NAMES)) W(id + '.json', { kind: 'screens', screens: [{ id, target: OLD[id], name: NAMES[id][0], x: pos[id].x, y: pos[id].y, tree: JSON.parse(fs.readFileSync(P + id + '.json')) }] });
fs.writeFileSync(__dirname + '/out/names.json', JSON.stringify({ NAMES, pos }));
console.log('ok', Object.keys(NAMES).length);
