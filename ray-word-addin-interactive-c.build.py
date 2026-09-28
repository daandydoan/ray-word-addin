import base64, pathlib, re

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
EXTRACTS = pathlib.Path(__file__).resolve().parent
OUT = EXTRACTS / "ray-word-addin-interactive-c.html"

def data_uri(name):
    return "data:image/svg+xml;base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()
RAY = data_uri("ray-avatar.svg"); WORDMARK = data_uri("tenderfy-wordmark.svg")

src_a = (EXTRACTS / "ray-word-addin-mock.build.py").read_text(encoding="utf-8")
BASE_CSS = re.search(r'CSS = r"""(.*?)"""', src_a, re.S).group(1).replace("__RAY__", RAY)
src_i = (EXTRACTS / "ray-word-addin-interactive.build.py").read_text(encoding="utf-8")
A_CSS = re.search(r'EXTRA_CSS = r"""(.*?)"""', src_i, re.S).group(1)

C_CSS = r"""
/* ===== version C: worklist pane with tabs, and a wide mode ===== */
.body { grid-template-columns: minmax(0,1fr) 360px; transition: grid-template-columns .28s cubic-bezier(.2,.8,.2,1); }
.body.wide { grid-template-columns: minmax(0,1fr) 62%; }
.pane-head .ms.wide { cursor: pointer; margin-left: 0; }
.pane-head .ms.wide.on { color: #0F7355; }
.ptabs { display: flex; border-bottom: 1px solid #EEF2F0; padding: 0 8px; }
.ptab { flex: 1; text-align: center; padding: 9px 4px 8px; font-size: 11px; font-weight: 600; color: #6B7975; cursor: pointer; position: relative; }
.ptab.on { color: #0F7355; box-shadow: inset 0 -2px 0 #1D9E75; }
.ptab b { display: inline-grid; place-items: center; min-width: 15px; height: 15px; border-radius: 999px; background: #EEF2F0; color: #33423E; font-size: 9px; font-weight: 700; padding: 0 4px; margin-left: 4px; vertical-align: 1px; }
.ptab b.hot { background: #D93B3B; color: #fff; }
.pbody { flex: 1; min-height: 0; overflow: auto; padding: 10px 12px 12px; display: flex; flex-direction: column; gap: 8px; }
.phases { padding: 0; }
.filters { display: flex; gap: 5px; }
.fl { font-size: 10.5px; font-weight: 600; color: #6B7975; border: 1px solid #E6ECEA; border-radius: 999px; padding: 3px 9px; cursor: pointer; background: #fff; }
.fl.on { color: #0F7355; border-color: #BFE0D2; background: #EAF5F0; }
.fl b { font-weight: 500; color: #9AA8A3; margin-left: 3px; }
.wl { display: flex; flex-direction: column; gap: 6px; }
.wr { display: grid; grid-template-columns: 8px auto minmax(0,1fr) auto auto; align-items: center; gap: 8px; padding: 8px 9px; border: 1px solid #E6ECEA; border-radius: 9px; background: #fff; font-size: 11px; cursor: pointer; transition: border-color .15s, background .15s; }
.wr:hover { border-color: #C9D4D0; }
.wr.cur { border-color: #1D9E75; background: rgba(29,158,117,.05); }
.wr .st { width: 8px; height: 8px; border-radius: 50%; background: #DCE5E1; }
.wr.open .st { background: #E0A32E; }
.wr.ready .st { background: #2F78C2; animation: pulse 1.4s ease-in-out infinite; }
.wr.done .st { background: #1D9E75; }
.wr.gap .st { background: #D93B3B; }
.wr .n { font-family: ui-monospace, Menlo, monospace; font-size: 10px; font-weight: 700; color: #0F7355; }
.wr .t { min-width: 0; color: #1F2B28; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wr .t small { display: block; font-weight: 400; font-size: 9.5px; color: #6B7975; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wr .av { width: 20px; height: 20px; font-size: 8px; border: 0; margin: 0; }
.wr .noav { width: 20px; height: 20px; border-radius: 50%; border: 1.5px dashed #C9D4D0; }
.wr .rail-btn { padding: 4px 10px; font-size: 10.5px; cursor: pointer; }
.wr.sched { grid-template-columns: 8px auto minmax(0,1fr) auto; background: #F7FAF8; }
.wr .trace { grid-column: 1 / -1; display: flex; flex-direction: column; gap: 4px; padding-top: 4px; }
.bulk { display: flex; gap: 6px; flex-wrap: wrap; }
.bulk .rail-btn { cursor: pointer; }
.bulk .rail-btn.dis { opacity: .45; pointer-events: none; }
.hint { font-size: 10.5px; color: #6B7975; line-height: 1.4; }
/* editor inside the pane (wide mode) */
.ped { display: grid; grid-template-columns: minmax(0,1fr) 220px; gap: 12px; flex: 1; min-height: 0; }
.ped.nolib { grid-template-columns: 1fr; }
.ped .ed { display: flex; flex-direction: column; min-height: 0; border: 1px solid #E6ECEA; border-radius: 10px; overflow: hidden; }
.ped .ed-top { padding: 10px 14px; }
.ped .ed-tools { padding: 6px 14px; }
.ped .ed-body { padding: 18px 24px; }
.ped .ed-text { font-size: 13.5px; }
.ped .ed-foot { padding: 8px 14px; }
.ped .lib { border: 1px solid #E6ECEA; border-radius: 10px; background: #F7FAF8; display: flex; flex-direction: column; min-height: 0; overflow: auto; }
.narrow-note { border: 1px dashed #DCE5E1; border-radius: 9px; padding: 9px 10px; font-size: 10.5px; color: #6B7975; line-height: 1.4; }
.narrow-note b { color: #33423E; }
.narrow-note .rail-btn { margin-top: 6px; cursor: pointer; }
/* team tab */
.team-row { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 7px 9px; border: 1px solid #E6ECEA; border-radius: 9px; font-size: 11px; }
.team-row .av { width: 24px; height: 24px; font-size: 9px; border: 0; margin: 0; }
.team-row .t small { display: block; font-size: 9.5px; color: #6B7975; }
.team-row .load { display: flex; gap: 3px; }
.team-row .load i { width: 14px; height: 6px; border-radius: 3px; background: #E6ECEA; }
.team-row .load i.on { background: #1D9E75; }
.assign-row { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 6px 9px; border: 1px solid #E6ECEA; border-radius: 9px; font-size: 11px; }
.assign-row .who { display: flex; gap: 3px; }
.assign-row .who .av { width: 20px; height: 20px; font-size: 8px; border: 1.5px solid #fff; margin: 0; cursor: pointer; opacity: .4; }
.assign-row .who .av.sel { opacity: 1; box-shadow: 0 0 0 2px #1D9E75; }
.assign-row .who .av:hover { opacity: 1; }
.act { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 7px 9px; border: 1px solid #E6ECEA; border-radius: 9px; font-size: 11px; }
.act .av { width: 20px; height: 20px; font-size: 8px; border: 0; margin: 0; }
.act .t small { display: block; font-size: 9.5px; color: #6B7975; }
.act .rail-btn { padding: 4px 10px; font-size: 10.5px; cursor: pointer; }
.act.new { border-color: rgba(29,158,117,.45); background: rgba(29,158,117,.05); }
.k { font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; margin: 4px 0 0; }
/* ray tab */
.rail-body { padding: 0; }
.lib-i { margin: 0 0 8px; }
.pbody .lib-s { margin: 0 0 8px; }
.lib-i.dis { opacity: .55; cursor: default; }
@media (max-width: 900px) { .body.wide { grid-template-columns: 1fr; } .ped { grid-template-columns: 1fr; } .ped .lib { display: none; } }
"""

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ray for Word · C</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0,0">
<style>
.ms {{ font-family: 'Material Symbols Outlined'; font-weight: normal; font-style: normal; line-height: 1; letter-spacing: normal; text-transform: none; display: inline-block; white-space: nowrap; direction: ltr; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; }}
{BASE_CSS}
{A_CSS}
{C_CSS}
</style></head>
<body>
<header class="head">
  <span class="eyebrow">RayAI expansion · Word add-in · version C — the worklist pane</span>
  <h1>Ray, <em>as the list of what’s left.</em></h1>
  <p>Third take on the 25 Sep scrum, still entirely in the side pane. The pane opens on a <b>worklist</b> — every question as a row with status, owner and one action — not a conversation. Tabs give the same pane <b>Ray</b> (chat and reasoning), <b>Library</b> and <b>Team</b> without stealing space from each other. For long answers the pane <b>widens</b> into an editor with the library beside it — the task pane grows, nothing floats over Word. Same tokens as A and B.</p>
</header>

<div class="guide" id="guide">
  <span class="lbl">Try</span>
  <span class="g" data-g="autofill" data-do="autofill"><i></i>Autofill Schedule 1</span>
  <span class="g" data-g="draft" data-do="draftall"><i></i>Draft all · insert from the list</span>
  <span class="g" data-g="wide" data-do="widecur"><i></i>Wide mode · edit in the pane</span>
  <span class="g" data-g="team" data-do="tabteam"><i></i>Team tab · owners &amp; activity</span>
  <span class="g" data-g="map" data-do="map"><i></i>Map the document (XML)</span>
  <span class="g" data-g="ray" data-do="tabray"><i></i>Ask Ray</span>
  <span class="reset" id="reset">Reset</span>
</div>

<section class="frame">
<div class="win">
  <div class="titlebar">
    <span class="lights"><i></i><i></i><i></i></span>
    <span class="docname"><span class="ms">description</span>Northside School Upgrade – Tender Response.docx <small id="savestate">Saved to SharePoint</small></span>
    <span class="presence" id="presence"><span class="av a1">DD</span><span class="av a2">MW</span></span>
  </div>
  <div class="tabs"><span>Home</span><span>Insert</span><span>Layout</span><span>References</span><span>Review</span><span>View</span><span class="on">Tenderfy Ray</span></div>
  <div class="ribbon">
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="tabq"><span class="ms">checklist</span><b>Questions</b></div>
      <div class="rb" data-do="autofill"><span class="ms">auto_fix_high</span><b>Autofill<br>fields</b></div>
      <div class="rb" data-do="draftall"><span class="ms">auto_awesome</span><b>Draft all<br>open</b></div>
      <div class="rb" data-do="widecur"><span class="ms">width_wide</span><b>Wide<br>mode</b></div>
    </div><div class="lbl">Answers</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="tabteam"><span class="ms">group</span><b>Team</b></div>
      <div class="rb" data-do="sync"><span class="ms">sync</span><b>Sync<br>SharePoint</b></div>
      <div class="rb" data-do="review"><span class="ms">fact_check</span><b>Check<br>criteria</b></div>
    </div><div class="lbl">Team</div></div>
  </div>
  <div class="body" id="body">
    <div class="canvas" id="canvas"><div class="page" id="page">
      <div class="crumb">Schedule 3 · Returnable schedules</div>
      <h3>Section 3 — Methodology</h3>
      <p class="sub">Responses to the Principal’s evaluation criteria · Northside School Upgrade · RFT 2026-114</p>
      <i class="outline-rail"></i>
      <div id="fields"></div>
      <div id="qs"></div>
    </div></div>
    <div class="pane" id="pane">
      <div class="pane-head"><img src="{WORDMARK}" alt="Tenderfy"> Ray <span class="ms wide" id="widebtn" data-do="wide" title="Wide mode">width_wide</span><span class="ms">close</span></div>
      <div class="raypanel">
        <div class="ptabs" id="ptabs"></div>
        <div class="pbody" id="pbody"></div>
        <div class="rp-foot"><div class="rp-ref" id="refs"></div>
          <div class="rp-composer" id="composer"><i class="rp-att"></i><span class="rp-input" id="input" contenteditable="true" data-ph="Ask Ray…"></span><i class="rp-clip"></i><i class="rp-send" id="send"></i></div></div>
      </div>
    </div>
  </div>
</div>
</section>
<div class="toast" id="toast"></div>

<script>
const RAY = "{RAY}";
const PEOPLE = {{ DD: ['Daniel','a1'], MW: ['Mia','a2'], TB: ['Tom','a3'] }};
const AV = (k, cls) => `<span class="av ${{PEOPLE[k][1]}} ${{cls||''}}">${{k}}</span>`;
const LIB = [
  ['Disruption Management Plan · Riverside Primary', 'School-hour no-work windows, gate control, single school contact.', 'Won · 2025', 'A dedicated traffic controller will hold the gate closed during school drop-off and pick-up windows, with the site supervisor as the single point of contact for the school office.'],
  ['Communications register · Riverside Primary', 'Fortnightly notices, 48-hour out-of-hours notice, published site number.', 'Won · 2025', 'A fortnightly works notice will go to the school office and neighbouring residents, with 48 hours’ notice for any out-of-hours work.'],
  ['Grove Street TMP · draft v2', 'AS 1742.3, one lane each way, heavy vehicles 9:30–2:30, no reversing.', 'Draft', 'Heavy vehicle movements are restricted to 9:30am–2:30pm and marshalled from the northern gate; no vehicles will reverse onto the carriageway.'],
  ['Noise management procedure', 'Boundary logging meter, EPA limits, stop-work trigger.', 'Policy', 'Noise will be monitored at the school boundary with a logging meter; readings above the EPA limit stop the work until the source is controlled.'],
];
const Q0 = () => [
  {{ id:'3.1', short:'Site establishment', t:'Describe your approach to site establishment and hoarding.', a:'Site establishment will follow our standard three-stage sequence: perimeter hoarding to the Grove Street frontage, temporary services connection, and a single controlled gate on the northern boundary away from the school entrance.', by:null, src:[] }},
  {{ id:'3.2', short:'School drop-off and pick-up', t:'Describe how you will manage disruption during school drop-off and pick-up.', a:null, d:'No deliveries, concrete pours or crane lifts will be scheduled between 8:00–9:15am and 2:45–3:45pm on school days. A dedicated traffic controller will hold the Grove Street gate closed during these windows, with the site supervisor as the single point of contact for the school office.', src:['Disruption Management Plan · Riverside Primary','Northside RFT · criterion 3(b)'], why:'They want windows, not intentions — the criterion scores named no-work periods and a single school contact.' }},
  {{ id:'3.3', short:'Communication plan', t:'Outline your communication plan with the school and neighbouring residents.', a:null, d:'A fortnightly works notice will go to the school office and letterboxed to Grove and Elm Street residents, with a 48-hour notice for any out-of-hours work. The site supervisor’s direct number is published on the hoarding and in every notice.', src:['Communications register · Riverside Primary','Northside RFT · criterion 3(c)'], why:'The criterion asks for a named channel and a notice period; both come from the Riverside comms register.' }},
  {{ id:'3.4', short:'Traffic management', t:'Detail your traffic management approach for the Grove Street frontage.', a:null, d:'A Traffic Management Plan certified to AS 1742.3 will maintain one lane in each direction on Grove Street at all times. Heavy vehicle movements are restricted to 9:30am–2:30pm, marshalled from the northern gate, and no vehicles will reverse onto the carriageway.', src:['Grove Street TMP · draft v2','Northside RFT · criterion 3(d)'], why:'Criterion 3(d) scores lane retention and school-hour restrictions; the draft TMP already has both.' }},
  {{ id:'3.5', short:'Dust and noise', t:'Describe your environmental controls for dust and noise.', a:'Dust will be controlled by water cart during earthworks and a wheel-wash at the gate. Noisy works are restricted to 7:00am–5:00pm Monday to Friday, with residents notified 48 hours ahead of any exception.', by:null, src:[], gap:'No noise monitoring clause — criterion 3(e) scores monitoring and response.' }},
];
let S;
const $ = s => document.querySelector(s);
const q = id => S.qs.find(x => x.id === id);
const empties = () => S.qs.filter(x => !x.a);
const sleep = ms => new Promise(r => setTimeout(r, ms));
function toast(m) {{ const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('on'), 2200); }}
function mark(g) {{ S.guide[g] = true; document.querySelectorAll('.guide .g').forEach(el => el.classList.toggle('done', !!S.guide[el.dataset.g])); }}
function fresh() {{
  S = {{ qs: Q0(), cur: '3.2', tab: 'q', filter: 'all', wide: false, edit: null, mapped: false, ready: {{}}, tracing: {{}}, busy: false, guide: {{}},
        fields: [ ['Tenderer name', 'Northside Constructions Pty Ltd'], ['ABN', '61 204 118 337'], ['Registered address', '14 Grove Street, Northside VIC 3070'], ['Public liability insurance', '$20M · QBE · expires 30 Jun 2027'], ['Workers compensation', 'WorkSafe VIC · policy 88-1120-4'], ['Quality system', 'ISO 9001:2015 · cert. 2025-1183'] ].map(([k,v]) => ({{ k, v, filled: false }})),
        assigned: {{ '3.4': ['MW','Daniel','due Friday'] }}, editing: {{ '3.1':'MW' }}, comments: {{ '3.5':'TB' }}, unread: 3,
        acts: [ {{ who:'MW', q:'3.1', text:'Edited · rewrote the gate sequence', when:'12 min', live:true }}, {{ who:'DD', q:'3.4', text:'Assigned to you · due Friday', when:'2 h', act:['draft','Draft'] }}, {{ who:'TB', q:'3.5', text:'Comment · “Add the noise monitoring clause?”', when:'1 h', act:['review','Check'] }} ],
        chat: [] }};
  setWide(false, true); renderAll();
}}
function renderAll() {{ renderDoc(); renderPane(); renderRefs(); }}
function renderRefs() {{ const refs = ['Tender Response.docx', 'Company knowledge'].concat(S.mapped ? ['Document map'] : []); $('#refs').innerHTML = '<span>Reference</span>' + refs.map(r => `<b>${{r}}</b>`).join('') + '<b class="add">+ Add</b>'; }}
function renderFields() {{
  const f = S.fields.filter(x => x.filled).length;
  $('#fields').innerHTML = `<div class="fields"><div class="k">Schedule 1 · Tenderer details ${{f ? `<span class="chip">${{f}} of 6 autofilled by Ray</span>` : `<span class="chip warm">6 standard fields empty</span>`}}</div>
    ${{S.fields.map(x => `<div class="frow${{x.filled?' filled':''}}"><span>${{x.k}}</span>${{x.filled ? `<b>${{x.v}}</b>` : '<i class="empty"></i>'}}</div>`).join('')}}</div>`;
}}
function renderDoc() {{
  renderFields();
  $('#page').classList.toggle('mapped', S.mapped);
  $('#qs').innerHTML = S.qs.map(x => {{
    let side = '';
    if (S.editing[x.id]) side += `<span class="chip live">${{AV(S.editing[x.id])}}${{PEOPLE[S.editing[x.id]][0]}} is editing</span> `;
    if (S.assigned[x.id]) side += `<span class="chip warm">${{AV(S.assigned[x.id][0])}}Assigned to ${{PEOPLE[S.assigned[x.id][0]][0]}} · ${{S.assigned[x.id][2]}}</span> `;
    if (S.comments[x.id]) side += `<span class="chip">${{AV(S.comments[x.id])}}1 comment</span>`;
    let body;
    if (x.a && x.by === 'ray') body = `<div class="a ins"><span class="tag">Inserted by Ray <small>· from ${{x.src.length}} sources · just now</small></span><p>${{x.a}}</p></div>`;
    else if (x.a) body = `<div class="a${{x.flag?' ins gap':''}}">${{x.flag?`<span class="tag">Gap flagged by Ray <small>· ${{x.gap}}</small></span>`:''}}<p>${{x.a}}</p></div>`;
    else body = `<div class="slot${{S.cur===x.id?' target':''}}" data-do="select" data-q="${{x.id}}">${{S.cur===x.id ? '<span class="caret"></span>' : ''}}${{S.ready[x.id] ? 'Ready — insert from the list' : (S.mapped ? 'Answer slot detected · empty' : 'Not answered yet')}}</div>`;
    return `<div class="q${{S.cur===x.id?' cur':''}}" data-q="${{x.id}}"><span class="qtag">Q${{x.id}}</span><div class="qh" data-do="select" data-q="${{x.id}}"><span class="n">${{x.id}}</span>${{x.t}}</div>${{side?`<span class="side">${{side}}</span>`:''}}${{body}}</div>`;
  }}).join('');
}}
// ---------- pane ----------
function renderPane() {{
  const open = empties().length, mine = S.qs.filter(x => S.assigned[x.id] && S.assigned[x.id][0]==='DD' && !x.a).length;
  $('#ptabs').innerHTML = [['q', `Questions<b>${{open}}</b>`], ['ray', 'Ray'], ['lib', 'Library'], ['team', `Team${{S.unread ? `<b class="hot">${{S.unread}}</b>` : ''}}`]].map(([k, l]) => `<span class="ptab${{S.tab===k?' on':''}}" data-do="tab" data-tab="${{k}}">${{l}}</span>`).join('');
  const b = $('#pbody');
  if (S.edit) return renderEditor(b);
  if (S.tab === 'q') return renderList(b, open, mine);
  if (S.tab === 'ray') return renderRay(b);
  if (S.tab === 'lib') return renderLib(b);
  if (S.tab === 'team') return renderTeam(b);
}}
function statusOf(x) {{ if (x.flag) return ['gap', 'Gap flagged']; if (x.a) return ['done', x.by === 'ray' ? 'Inserted by Ray' : 'Answered']; if (S.ready[x.id]) return ['ready', 'Draft ready']; return ['open', 'Open']; }}
function renderList(b, open, mine) {{
  const f = S.fields.filter(x => x.filled).length;
  const rows = S.qs.filter(x => S.filter === 'all' || (S.filter === 'open' && !x.a) || (S.filter === 'mine' && S.assigned[x.id] && S.assigned[x.id][0]==='DD')).map(x => {{
    const [st, lbl] = statusOf(x); const own = S.assigned[x.id] ? AV(S.assigned[x.id][0]) : '<span class="noav" title="No owner"></span>';
    const act = x.flag ? `<span class="rail-btn" data-do="fixgap">Fix</span>` : x.a ? `<span class="rail-btn ghost" data-do="edit" data-q="${{x.id}}">Edit</span>` : S.ready[x.id] ? `<span class="rail-btn next" data-do="insert" data-q="${{x.id}}">Insert</span>` : `<span class="rail-btn ghost" data-do="draft" data-q="${{x.id}}">Draft</span>`;
    const trace = S.tracing[x.id] ? `<div class="trace" id="trace-${{x.id}}"></div>` : '';
    return `<div class="wr ${{st}}${{S.cur===x.id?' cur':''}}" data-do="select" data-q="${{x.id}}"><i class="st"></i><span class="n">${{x.id}}</span><span class="t">${{x.short}}<small>${{lbl}}${{S.assigned[x.id] ? ' · ' + PEOPLE[S.assigned[x.id][0]][0] : ''}}${{S.comments[x.id] ? ' · 1 comment' : ''}}</small></span>${{own}}${{act}}${{trace}}</div>`;
  }}).join('');
  b.innerHTML = `<div class="phases"><div class="ph ${{f===6?'done':'on'}}" data-do="autofill"><i>${{f===6?'✓':'1'}}</i>Autofill<small>${{f}}/6</small></div><div class="ph ${{open===0?'done':(f===6?'on':'')}}" data-do="draftall"><i>${{open===0?'✓':'2'}}</i>Draft &amp; finalise<small>${{5-open}}/5</small></div></div>
    <div class="filters"><span class="fl${{S.filter==='all'?' on':''}}" data-do="filter" data-f="all">All<b>5</b></span><span class="fl${{S.filter==='open'?' on':''}}" data-do="filter" data-f="open">Open<b>${{open}}</b></span><span class="fl${{S.filter==='mine'?' on':''}}" data-do="filter" data-f="mine">Mine<b>${{mine}}</b></span></div>
    <div class="wl"><div class="wr sched ${{f===6?'done':'open'}}" data-do="autofill"><i class="st"></i><span class="n">S1</span><span class="t">Tenderer details<small>${{f}} of 6 standard fields · company profile</small></span>${{f===6 ? '<span class="rail-btn ghost dis">Done</span>' : '<span class="rail-btn ghost">Autofill</span>'}}</div>${{rows}}</div>
    <div class="bulk"><span class="rail-btn${{open?'':' dis'}}" data-do="draftall">Draft all open</span><span class="rail-btn ghost${{Object.keys(S.ready).length?'':' dis'}}" data-do="insertall">Insert all ready</span><span class="rail-btn ghost" data-do="map">Map document</span></div>
    <div class="hint">Click a row to jump to it in the document. <b>Draft</b> works in the row; <b>Insert</b> writes it into the slot. Long answers: switch to wide mode and the row becomes an editor here.</div>`;
}}
function renderRay(b) {{
  b.innerHTML = `<div class="rail-body" id="rail">${{S.chat.length ? S.chat.join('') : `<div class="ray-empty"><span class="ray-halo"><img src="${{RAY}}" alt=""></span><h3>Ask Ray about this document</h3><p>The list on the Questions tab is what Ray is tracking. Ask about a question, the buyer, or what changed — the answer lands here, the action lands in the list.</p>
    <div class="ray-starter" data-do="ask" data-q="3.2">What does the buyer actually want for 3.2?</div><div class="ray-starter" data-do="review">Check every answer against the evaluation criteria.</div><div class="ray-starter" data-do="tabteam">What changed since yesterday?</div></div>`}}</div>`;
  b.scrollTop = b.scrollHeight;
}}
function renderLib(b) {{
  const target = S.edit ? q(S.edit) : null;
  b.innerHTML = `<div class="lib-s"><span class="ms">search</span>Search 1,240 assets…</div><div class="hint" style="margin-bottom:4px">${{S.edit ? `Click an entry to add it to <b>${{S.edit}}</b>.` : 'Open a question in wide mode to add from here, or drag into the document.'}}</div>` + LIB.map((l,i) => `<div class="lib-i${{S.edit?'':' dis'}}" data-do="libins" data-i="${{i}}"><b>${{l[0]}}</b><small>${{l[1]}}</small><em>${{l[2]}}</em></div>`).join('');
}}
function renderTeam(b) {{
  mark('team'); const people = Object.keys(PEOPLE);
  const team = people.map(k => {{ const n = Object.values(S.assigned).filter(v => v[0]===k).length; return `<div class="team-row">${{AV(k)}}<span class="t">${{PEOPLE[k][0]}}<small>${{n}} question${{n===1?'':'s'}}${{Object.values(S.editing).includes(k) ? ' · editing now' : ''}}</small></span><span class="load">${{[0,1,2].map(i => `<i class="${{i<n?'on':''}}"></i>`).join('')}}</span></div>`; }}).join('');
  const rows = S.qs.map(x => `<div class="assign-row"><span class="n" style="font-family:ui-monospace,Menlo,monospace;font-size:10px;font-weight:700;color:#0F7355">${{x.id}}</span><span class="t" style="min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${{x.short}}</span><span class="who">${{people.map(k => `<span class="av ${{PEOPLE[k][1]}}${{S.assigned[x.id]&&S.assigned[x.id][0]===k?' sel':''}}" data-do="own" data-q="${{x.id}}" data-who="${{k}}" title="${{PEOPLE[k][0]}}">${{k}}</span>`).join('')}}</span></div>`).join('');
  const acts = S.acts.map((a, i) => `<div class="act${{i < S.unread ? ' new' : ''}}">${{AV(a.who)}}<span class="t"><span class="n" style="font-family:ui-monospace,Menlo,monospace;font-size:10px;font-weight:700;color:#0F7355">${{a.q}}</span> ${{a.text}}<small>${{PEOPLE[a.who][0]}} · ${{a.when}}${{a.live?' · SharePoint':''}}</small></span>${{a.act ? `<span class="rail-btn ${{a.act[0]==='review'?'ghost':''}}" data-do="${{a.act[0]}}" data-q="${{a.q}}">${{a.act[1]}}</span>` : ''}}</div>`).join('');
  b.innerHTML = `<div class="k">Owners · Section 3</div>${{rows}}<div class="bulk"><span class="rail-btn ghost" data-do="assignauto">Suggest owners from past tenders</span></div><div class="k">Load</div>${{team}}<div class="k">Activity · SharePoint</div>${{acts}}`;
  S.unread = 0; $('#ptabs').innerHTML = $('#ptabs').innerHTML.replace(/<b class="hot">\\d+<\\/b>/, '');
}}
// ---------- editor in the pane (wide mode) ----------
function setWide(on, silent) {{ S.wide = on; $('#body').classList.toggle('wide', on); $('#widebtn').classList.toggle('on', on); $('#widebtn').textContent = on ? 'width_normal' : 'width_wide'; if (!silent && on) mark('wide'); }}
function renderEditor(b) {{
  const x = q(S.edit); const text = x.a || x.d || '';
  b.innerHTML = `<div class="ped${{S.wide?'':' nolib'}}"><div class="ed"><div class="ed-top"><span class="n">${{x.id}}</span><span class="t">${{x.t}}</span><span class="wc" id="wc"></span><span class="ms" data-do="editclose">close</span></div>
      <div class="ed-tools"><span class="ms">format_bold</span><span class="ms">format_italic</span><span class="ms">format_underlined</span><span class="sep"></span><span class="ms">format_list_bulleted</span><span class="ms">format_list_numbered</span><span class="sep"></span><span class="ms">table</span><span class="ms">link</span></div>
      <div class="ed-body"><div class="ed-text" id="edtext" contenteditable="true">${{text ? `<p>${{text}}</p>` : '<p><br></p>'}}</div></div>
      <div class="ed-foot"><div class="srcs">${{(x.src||[]).map(s => `<b>${{s}}</b>`).join('')}}</div><span class="rail-btn ghost" data-do="editclose">Close</span><span class="rail-btn" data-do="editinsert">${{x.a ? 'Update in document' : 'Insert into document'}}</span></div></div>
    ${{S.wide ? `<div class="lib"><div class="lib-h"><span>Response library</span></div><div class="lib-s"><span class="ms">search</span>Search…</div>${{LIB.map((l,i) => `<div class="lib-i" data-do="libins" data-i="${{i}}"><b>${{l[0]}}</b><small>${{l[1]}}</small><em>${{l[2]}}</em></div>`).join('')}}</div>` : ''}}</div>
    ${{S.wide ? '' : `<div class="narrow-note"><b>Long answer?</b> Widen the pane and this editor gets the response library beside it — the pane grows, nothing floats over Word.<br><span class="rail-btn ghost" data-do="wide">Wide mode</span></div>`}}`;
  wc(); const ed = $('#edtext'); ed.addEventListener('input', wc); setTimeout(() => ed.focus(), 40);
}}
function wc() {{ const t = ($('#edtext')?.innerText || '').trim(); const n = t ? t.split(/\\s+/).length : 0; const el = $('#wc'); if (el) el.textContent = `${{n}} words · ~${{Math.max(1, Math.round(n/300))}} page${{n>300?'s':''}}`; }}
function edit(qid) {{ S.edit = qid || S.cur; S.cur = S.edit; renderDoc(); renderPane(); }}
function editClose() {{ const x = q(S.edit); const t = ($('#edtext')?.innerText || '').trim(); if (x && t && t !== (x.a || x.d)) {{ x.d = t; if (x.a) {{ x.a = t; x.by = 'ray'; }} }} S.edit = null; renderAll(); }}
function editInsert() {{ const x = q(S.edit); const t = ($('#edtext')?.innerText || '').trim(); if (!t) return; x.d = t; if (x.a) {{ x.a = t; x.by = 'ray'; S.edit = null; renderAll(); toast(`${{x.id}} updated`); }} else {{ S.ready[x.id] = true; S.edit = null; insert(x.id); }} }}
function libInsert(i) {{ const ed = $('#edtext'); if (!ed) {{ toast('Open a question in wide mode first'); return; }} ed.insertAdjacentHTML('beforeend', `<p class="new">${{LIB[i][3]}}</p>`); wc(); toast(`Added from ${{LIB[i][0].split(' ·')[0]}}`); }}
function wideCur() {{ setWide(true); edit(S.cur); }}
// ---------- flows ----------
async function traceIn(container, steps) {{ for (const [code, note] of steps) {{ container.insertAdjacentHTML('beforeend', `<div class="work live"><i></i><code>${{code}}</code><span>${{note}}</span></div>`); await sleep(330); container.lastElementChild.classList.replace('live','done'); }} }}
async function draft(qid) {{
  const x = q(qid); if (!x || x.a || S.ready[x.id] || S.tracing[x.id]) return; S.cur = x.id; S.tracing[x.id] = true; S.tab = 'q'; S.filter = S.filter === 'mine' && !(S.assigned[x.id] && S.assigned[x.id][0]==='DD') ? 'all' : S.filter; renderAll();
  const c = document.getElementById('trace-' + x.id); if (c) await traceIn(c, [['read_question', `${{x.short.toLowerCase()}}`],['search_company_knowledge', `3 matches · ${{x.src[0].split(' ·')[0]}}`],['draft_answer', `${{x.d.split(' ').length}} words · aligned to criterion`]]);
  delete S.tracing[x.id]; S.ready[x.id] = true; renderAll(); mark('draft');
}}
async function draftAll() {{ mark('draft'); for (const x of empties()) if (!S.ready[x.id]) await draft(x.id); }}
function insert(qid) {{ const x = q(qid); if (!x || x.a) return; x.a = x.d; x.by = 'ray'; delete S.ready[x.id]; const e = empties(); S.cur = e.length ? e[0].id : x.id; renderAll(); const el = document.querySelector(`.q[data-q="${{x.id}}"]`); el && el.scrollIntoView({{ behavior:'smooth', block:'center' }}); $('#savestate').textContent = 'Saving…'; setTimeout(() => $('#savestate').textContent = 'Saved to SharePoint', 900); toast(`Inserted into ${{x.id}}${{e.length ? ` · ${{e.length}} open` : ' · Section 3 complete'}}`); }}
async function insertAll() {{ for (const id of Object.keys(S.ready)) {{ insert(id); await sleep(500); }} }}
async function autofill() {{
  if (S.busy || S.fields.every(x => x.filled)) return; S.busy = true; mark('autofill'); S.tab = 'q'; S.edit = null; renderPane();
  const row = document.querySelector('.wr.sched'); row.insertAdjacentHTML('beforeend', '<div class="trace" id="trace-s1"></div>');
  await traceIn(document.getElementById('trace-s1'), [['read_company_profile','Northside Constructions · current'],['match_fields','6 / 6 · ABN, address, insurances, quality'],['write_fields','written in place · no new document']]);
  for (const x of S.fields) {{ x.filled = true; renderFields(); await sleep(200); }}
  $('#fields').scrollIntoView({{ behavior:'smooth', block:'start' }}); renderAll(); toast('Schedule 1 filled — phase 2: draft the open questions'); S.busy = false;
}}
async function map() {{ if (S.busy) return; S.busy = true; mark('map'); S.tab = 'ray'; pushRay('Map this document.'); await rayThink([['open_document_xml','word/document.xml · 48 KB · no bookmarks needed'],['outline_document',`5 sections · 14 questions · ${{empties().length}} empty slots`],['map_answer_slots','14 / 14 matched by heading + numbering'],['validate_structure','styles, tables, numbering untouched']], '2.1', `<div class="rail-offer status"><p><b>Document map ready.</b> Ray reads and writes the document’s own XML — answers land inside the real paragraphs. No bookmarks, no Syncfusion, nothing rewritten around them.</p><div class="srcs"><b>XML-native</b><b>No bookmarks</b><b>No corruption risk</b></div></div>`); S.mapped = true; renderAll(); S.busy = false; }}
function pushRay(text) {{ S.chat.push(`<div class="rail-you">${{text}}</div>`); S.tab = 'ray'; renderPane(); }}
async function rayThink(steps, secs, html) {{
  S.tab = 'ray'; renderPane(); const id = 'e' + Date.now();
  $('#rail').insertAdjacentHTML('beforeend', `<div class="rail-entry" id="${{id}}"><div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div><div class="rh-s open"><i class="chev"></i><span class="lbl">Working…</span></div><div class="rail-work"></div></div>`);
  const entry = document.getElementById(id); await traceIn(entry.querySelector('.rail-work'), steps);
  entry.querySelector('.rh-s .lbl').textContent = `Thought for ${{secs}}s · ${{steps.length}} steps`; entry.querySelector('.rh-s').classList.remove('open'); entry.querySelector('.rail-work').classList.add('folded');
  entry.insertAdjacentHTML('beforeend', html); S.chat.push(entry.outerHTML); $('#pbody').scrollTop = 1e6;
}}
async function ask(qid) {{ if (S.busy) return; S.busy = true; mark('ray'); const x = q(qid || S.cur); S.cur = x.id; pushRay(`What is the buyer actually asking for in ${{x.id}}?`); await rayThink([['read_question', `${{x.id}} · ${{x.short.toLowerCase()}}`],['search_company_knowledge', `3 matches · ${{x.src && x.src[0] ? x.src[0].split(' ·')[0] : 'company profile'}}`],['draft_answer', 'aligned to criterion']], '1.4', `<div class="rail-offer ask"><p><b>${{x.why || 'Already answered.'}}</b> ${{x.a ? 'The answer is in the document.' : 'The draft is ready in the Questions list — insert it from there, or open it wide to edit.'}}</p><div class="acts">${{x.a ? '' : `<span class="rail-btn" data-do="insert" data-q="${{x.id}}">Insert</span>`}}<span class="rail-btn ghost" data-do="widecur">Open wide</span></div></div>`); if (!x.a) S.ready[x.id] = true; renderDoc(); S.busy = false; }}
async function review() {{ if (S.busy) return; S.busy = true; const answered = S.qs.filter(x => x.a); pushRay('Check every answer against the evaluation criteria.'); await rayThink([['read_criteria','criteria 3(a)–3(e) · weights loaded'], ...answered.map(x => ['check_answer', `${{x.id}} · ${{x.id==='3.5'?'gap: noise monitoring':'meets criterion'}}`])], '2.6', `<div class="rail-offer ask"><p><b>${{answered.length}} answers checked · 1 gap.</b> 3.5 has controls but no monitoring — criterion 3(e) scores “monitoring and response”. Tom’s comment asks for the same thing.</p><div class="acts"><span class="rail-btn" data-do="fixgap">Add monitoring clause</span></div></div>`); q('3.5').flag = true; renderDoc(); S.busy = false; }}
function fixGap() {{ const g = q('3.5'); if (!g.flag) return; g.a += ' Noise will be monitored at the school boundary with a logging meter; readings above the EPA limit stop the work until the source is controlled.'; g.flag = false; g.by = 'ray'; g.src = ['Noise management procedure','Northside RFT · criterion 3(e)']; delete S.comments['3.5']; S.acts = S.acts.filter(a => a.q !== '3.5'); S.tab = 'q'; renderAll(); toast('3.5 updated · comment resolved'); }}
function own(qid, who) {{ S.assigned[qid] = [who, 'you', 'due Fri']; if (who === 'DD') {{ S.acts.unshift({{ who:'DD', q:qid, text:'Assigned to you · due Friday', when:'now', act:['draft','Draft'] }}); }} renderAll(); toast(`${{qid}} → ${{PEOPLE[who][0]}}`); }}
function assignAuto() {{ const pick = {{ '3.1':'DD', '3.2':'MW', '3.3':'MW', '3.4':'TB', '3.5':'TB' }}; S.qs.forEach(x => {{ if (!x.a) S.assigned[x.id] = [pick[x.id], 'Ray', 'due Fri']; }}); renderAll(); toast('Owners suggested from who wrote these last time'); }}
async function sync() {{ $('#savestate').textContent = 'Syncing…'; await sleep(700); const t = S.qs.find(x => x.a && x.id !== '3.1') || q('3.1'); S.editing = {{}}; S.editing[t.id] = 'TB'; S.unread += 1; S.acts.unshift({{ who:'TB', q:t.id, text:'Opened the document · editing now', when:'now', live:true }}); if (!$('#presence .a3')) $('#presence').insertAdjacentHTML('beforeend', AV('TB')); $('#savestate').textContent = 'Saved to SharePoint'; renderAll(); toast('Change arrived from SharePoint'); }}
function select(qid) {{ S.cur = qid; renderDoc(); if (S.tab === 'q' && !S.edit) renderPane(); const el = document.querySelector(`.q[data-q="${{qid}}"]`); el && el.scrollIntoView({{ behavior:'smooth', block:'center' }}); }}
async function typed(text) {{ const t = text.trim().toLowerCase(); if (!t) return; if (/autofill|abn|standard fields/.test(t)) return autofill(); if (/map|xml|parse/.test(t)) return map(); if (/assign|owner|team|changed|since/.test(t)) {{ S.tab = 'team'; return renderPane(); }} if (/wide|expand|edit/.test(t)) return wideCur(); if (/rest|all|draft/.test(t)) return draftAll(); if (/check|criteria|review/.test(t)) return review(); const m = t.match(/3\\.[1-5]/); if (m) S.cur = m[0]; return ask(S.cur); }}
document.addEventListener('click', e => {{
  const el = e.target.closest('[data-do]'); if (!el) return; const d = el.dataset.do, qid = el.dataset.q;
  if (d === 'select' && e.target.closest('.rail-btn')) return;
  ({{ tab: () => {{ S.tab = el.dataset.tab; S.edit = null; renderPane(); }}, tabq: () => {{ S.tab='q'; S.edit=null; renderPane(); }}, tabray: () => {{ S.tab='ray'; S.edit=null; mark('ray'); renderPane(); }}, tabteam: () => {{ S.tab='team'; S.edit=null; renderPane(); }},
     filter: () => {{ S.filter = el.dataset.f; renderPane(); }}, select: () => select(qid), draft: () => draft(qid), draftall: draftAll, insert: () => insert(qid), insertall: insertAll,
     autofill, map, edit: () => edit(qid), editclose: editClose, editinsert: editInsert, libins: () => libInsert(+el.dataset.i), wide: () => {{ setWide(!S.wide); if (S.edit) renderPane(); }}, widecur: wideCur,
     own: () => own(qid, el.dataset.who), assignauto: assignAuto, sync, review, fixgap: fixGap, ask: () => ask(qid) }})[d]?.();
}});
const inp = $('#input');
inp.addEventListener('keydown', e => {{ if (e.key === 'Enter') {{ e.preventDefault(); const v = inp.textContent; inp.textContent = ''; typed(v); }} }});
$('#send').onclick = () => {{ const v = inp.textContent; inp.textContent = ''; typed(v); }};
$('#reset').onclick = fresh;
fresh();
</script>
</body></html>'''

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT, len(HTML))
