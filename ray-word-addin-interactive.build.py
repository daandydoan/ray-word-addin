import base64, pathlib, re

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
EXTRACTS = pathlib.Path(__file__).resolve().parent
OUT = EXTRACTS / "ray-word-addin-interactive.html"

def data_uri(name):
    return "data:image/svg+xml;base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()
RAY = data_uri("ray-avatar.svg"); WORDMARK = data_uri("tenderfy-wordmark.svg")

# reuse the static mock's stylesheet verbatim, then layer the interactive bits on top
src = (EXTRACTS / "ray-word-addin-mock.build.py").read_text(encoding="utf-8")
BASE_CSS = re.search(r'CSS = r"""(.*?)"""', src, re.S).group(1).replace("__RAY__", RAY)

EXTRA_CSS = r"""
.frame { margin-bottom: 28px; }
.guide { max-width: 1180px; margin: 0 auto 16px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.guide .lbl { font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-right: 4px; }
.guide .g { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; color: var(--ink-2); background: #fff; border: 1px solid #DCE5E1; border-radius: 999px; padding: 5px 11px 5px 7px; cursor: pointer; transition: background .2s, border-color .2s; }
.guide .g i { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid #C9D4D0; position: relative; flex: none; }
.guide .g.done { border-color: #BFE0D2; background: #EAF5F0; }
.guide .g.done i { background: #1D9E75; border-color: #1D9E75; }
.guide .g.done i::after { content: ''; position: absolute; left: 4px; top: 1.5px; width: 3.5px; height: 7px; border: solid #fff; border-width: 0 1.5px 1.5px 0; transform: rotate(45deg); }
.guide .reset { margin-left: auto; font-size: 12px; color: var(--dim); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.win { user-select: none; }
.body { height: 640px; }
.canvas { overflow: auto; height: 100%; }
.pane { height: 100%; }
.rail-body { overflow: auto; }
.rb { cursor: pointer; transition: background .15s; }
.rb:hover { background: #F2F5F4; }
.rb.pri { background: var(--acc-tint); }
.rb.dis { opacity: .4; pointer-events: none; }
.rb { position: relative; }
.rb .cnt { position: absolute; top: 4px; right: 10px; min-width: 15px; height: 15px; border-radius: 999px; background: #D93B3B; color: #fff; font-size: 9px; font-weight: 700; display: grid; place-items: center; padding: 0 4px; }
.slot { cursor: text; transition: border-color .2s, background .2s; }
.slot:hover { border-color: #9DB5AC; }
.q.cur .slot { border-color: var(--acc); background: var(--acc-tint); color: var(--acc-deep); }
.ins { animation: insIn .5s ease both; }
@keyframes insIn { from { opacity: 0; transform: translateY(6px); background: rgba(29,158,117,.28); } to { opacity: 1; transform: none; } }
.qtag, .outline-rail { display: none; }
.page.mapped .qtag, .page.mapped .outline-rail { display: block; }
.page.mapped .qtag { animation: insIn .4s ease both; }
.rail-btn { cursor: pointer; transition: transform .12s ease, filter .12s ease; }
.rail-btn:active { transform: scale(.93); filter: brightness(.9); }
.rail-btn.dis { opacity: .45; pointer-events: none; }
.rh-s { cursor: pointer; }
.rh-s .chev { transition: transform .2s; }
.work.hidden { display: none; }
.work { animation: insIn .3s ease both; }
.ray-starter { cursor: pointer; transition: background .15s, border-color .15s; }
.ray-starter:hover { background: #E9EFEC; border-color: #C9D4D0; }
.rp-composer { cursor: text; }
.rp-input { outline: none; }
.rp-input.typing::after { content: ''; display: inline-block; width: 1px; height: 1em; background: #1D9E75; margin-left: 1px; vertical-align: -2px; animation: caret 1s steps(2) infinite; }
.rp-send { cursor: pointer; }
.rp-go { cursor: pointer; }
.pane-head .bell { cursor: pointer; }
.pane-head .bell b:empty { display: none; }
.rail-entry { display: flex; flex-direction: column; gap: 8px; }
.assign .r .rail-btn { cursor: pointer; }
.picker { border: 1px solid #DCE5E1; border-radius: 9px; padding: 8px 10px; }
.picker .k { font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; margin-bottom: 6px; }
.picker .ppl { display: flex; gap: 6px; flex-wrap: wrap; }
.picker .p { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; border: 1px solid #DCE5E1; border-radius: 999px; padding: 3px 9px 3px 4px; cursor: pointer; background: #fff; }
.picker .p:hover { background: #F2F5F4; }
.picker .p .av { width: 18px; height: 18px; font-size: 8px; border: 0; margin: 0; }
.toast { position: fixed; left: 50%; bottom: 28px; transform: translate(-50%, 20px); background: #1F2B28; color: #fff; font-size: 12.5px; padding: 9px 14px; border-radius: 999px; opacity: 0; transition: opacity .25s, transform .25s; pointer-events: none; z-index: 9; }
.toast.on { opacity: 1; transform: translate(-50%, 0); }
.q .side { animation: insIn .3s ease both; }
.chip.warm { cursor: default; }
.gap { border-left-color: #E0A32E; background: #FFF8EA; }
.gap .tag { color: #7A4B00; }
.gap .tag::before { display: none; }
/* two-phase stepper under the panel head */
.phases { display: flex; gap: 6px; padding: 8px 12px 0; }
.ph { flex: 1; display: flex; align-items: center; gap: 6px; font-size: 10px; font-weight: 600; color: #6B7975; padding: 5px 8px; border: 1px solid #E6ECEA; border-radius: 8px; background: #FBFCFB; }
.ph i { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid #C9D4D0; display: grid; place-items: center; font-size: 8px; font-style: normal; color: #6B7975; flex: none; }
.ph.on { border-color: #1D9E75; color: #0F7355; background: rgba(29,158,117,.06); }
.ph.on i { border-color: #1D9E75; color: #1D9E75; }
.ph.done i { background: #1D9E75; border-color: #1D9E75; color: #fff; }
.ph small { font-weight: 400; color: #6B7975; margin-left: auto; white-space: nowrap; }
/* standard fields block on the page (phase 1 target) */
.fields { border: 1px solid #E6ECEA; border-radius: 8px; padding: 10px 12px; margin: 0 0 18px; }
.fields .k { font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.fields .k .chip { margin-left: auto; }
.frow { display: grid; grid-template-columns: 150px 1fr; gap: 10px; font-size: 12px; padding: 4px 0; border-top: 1px solid #F0F3F1; align-items: center; }
.frow:first-of-type { border-top: 0; }
.frow span { color: var(--dim); }
.frow b { font-weight: 500; color: #1F2B28; }
.frow .empty { display: inline-block; width: 60%; height: 8px; border-radius: 4px; border: 1.5px dashed #C9D4D0; }
.frow.filled b { background: var(--acc-tint); border-radius: 4px; padding: 1px 6px; animation: insIn .4s ease both; }
/* assignment sheet */
.sheet { border: 1px solid #DCE5E1; border-radius: 9px; overflow: hidden; }
.sheet .k { font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; padding: 7px 10px 5px; display: flex; flex-wrap: wrap; gap: 2px 8px; }
.sheet .k b { width: 100%; color: #33423E; font-weight: 500; letter-spacing: 0; text-transform: none; font-size: 10px; }
.sheet .r { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 6px 10px; border-top: 1px solid #EEF2F0; font-size: 11px; color: #1F2B28; }
.sheet .r.cur { background: rgba(29,158,117,.06); }
.sheet .r .n { font-family: ui-monospace, Menlo, monospace; font-size: 10px; font-weight: 700; color: #0F7355; }
.sheet .r .t { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sheet .r .t small { display: block; font-size: 9.5px; color: #6B7975; }
.sheet .who { display: flex; gap: 3px; }
.sheet .who .av { width: 20px; height: 20px; font-size: 8px; border: 1.5px solid #fff; margin: 0; cursor: pointer; opacity: .45; transition: opacity .15s, transform .15s; }
.sheet .who .av:hover { opacity: 1; transform: scale(1.1); }
.sheet .who .av.sel { opacity: 1; box-shadow: 0 0 0 2px #1D9E75; }
.sheet .load { display: flex; gap: 8px; padding: 7px 10px; border-top: 1px solid #EEF2F0; font-size: 10px; color: #6B7975; flex-wrap: wrap; }
.sheet .load b { color: #33423E; font-weight: 500; }
/* full-screen answering view */
.fs { position: absolute; inset: 0; background: #fff; display: none; grid-template-columns: 240px minmax(0,1fr); z-index: 5; }
.fs.on { display: grid; animation: insIn .25s ease both; }
.fs .lib { border-right: 1px solid var(--word-line); background: #F7FAF8; display: flex; flex-direction: column; min-height: 0; transition: width .2s; }
.fs.libhid { grid-template-columns: 44px minmax(0,1fr); }
.fs.libhid .lib > *:not(.lib-h) { display: none; }
.fs.libhid .lib-h span { display: none; }
.lib-h { display: flex; align-items: center; gap: 8px; padding: 12px 12px 8px; font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); }
.lib-h .ms { font-size: 18px; color: var(--dim); cursor: pointer; margin-left: auto; }
.lib-s { margin: 0 12px 8px; font-size: 11px; color: var(--dim); background: #fff; border: 1px solid #DCE5E1; border-radius: 8px; padding: 6px 9px; display: flex; gap: 6px; align-items: center; }
.lib-s .ms { font-size: 15px; }
.lib-i { margin: 0 12px 8px; background: #fff; border: 1px solid #E6ECEA; border-radius: 9px; padding: 8px 10px; font-size: 11px; cursor: pointer; transition: border-color .15s, transform .15s; }
.lib-i:hover { border-color: #1D9E75; transform: translateY(-1px); }
.lib-i b { display: block; font-weight: 600; color: #1F2B28; margin-bottom: 2px; }
.lib-i small { color: var(--dim); display: block; line-height: 1.35; }
.lib-i em { font-style: normal; font-size: 9.5px; color: #0F7355; background: #E4F1EC; border-radius: 4px; padding: 1px 5px; margin-top: 5px; display: inline-block; }
.fs .ed { display: flex; flex-direction: column; min-height: 0; }
.ed-top { display: flex; align-items: center; gap: 10px; padding: 12px 20px; border-bottom: 1px solid var(--word-line); font-size: 12px; }
.ed-top .n { font-family: ui-monospace, Menlo, monospace; font-size: 11px; font-weight: 700; color: #0F7355; background: #E4F1EC; border-radius: 4px; padding: 2px 6px; }
.ed-top .t { font-weight: 600; color: #1F2B28; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
.ed-top .wc { font-size: 10.5px; color: var(--dim); white-space: nowrap; }
.ed-top .ms { font-size: 20px; color: var(--dim); cursor: pointer; }
.ed-tools { display: flex; gap: 2px; padding: 6px 20px; border-bottom: 1px solid var(--word-line); }
.ed-tools .ms { font-size: 18px; color: #605E5C; padding: 4px 6px; border-radius: 4px; }
.ed-tools .sep { width: 1px; background: var(--word-line); margin: 2px 6px; }
.ed-body { flex: 1; overflow: auto; padding: 28px 48px; }
.ed-body h4 { font-size: 15px; margin: 0 0 14px; color: #1F2B28; }
.ed-text { outline: none; font-size: 14px; line-height: 1.7; color: #1F2B28; max-width: 70ch; min-height: 240px; }
.ed-text p { margin: 0 0 12px; }
.ed-text .new { background: var(--acc-tint); border-radius: 3px; animation: insIn .4s ease both; }
.ed-foot { display: flex; align-items: center; gap: 8px; padding: 10px 20px; border-top: 1px solid var(--word-line); background: #FBFCFB; }
.ed-foot .srcs { margin: 0; flex: 1; }
.ed-foot .rail-btn { font-size: 12px; padding: 7px 14px; }
.ins-row .ms, .rail-offer .ms.exp { font-size: 16px; color: var(--dim); cursor: pointer; vertical-align: middle; }
.rail-offer .exp { display: inline-flex; align-items: center; gap: 4px; font-size: 10.5px; color: #6B7975; cursor: pointer; margin-left: auto; }
.rail-offer .exp .ms { font-size: 15px; }
.acts .exp { margin-left: auto; }
.body { position: relative; }
@media (max-width: 900px) { .body { height: auto; } .canvas { height: auto; max-height: 520px; } .pane { height: auto; } .rail-body { max-height: 460px; } .fs { grid-template-columns: 1fr; } .fs .lib { display: none; } .frow { grid-template-columns: 1fr; } }
"""

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ray for Word</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0,0">
<style>
.ms {{ font-family: 'Material Symbols Outlined'; font-weight: normal; font-style: normal; line-height: 1; letter-spacing: normal; text-transform: none; display: inline-block; white-space: nowrap; direction: ltr; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; }}
{BASE_CSS}
{EXTRA_CSS}
</style></head>
<body>
<header class="head">
  <span class="eyebrow">RayAI expansion · Microsoft Word add-in · interactive</span>
  <h1>Ray, <em>inside the document.</em></h1>
  <p>A working mock of the Word add-in, adjusted to the 25 Sep design scrum: a <b>two-phase flow</b> (autofill the standard fields first, then draft and finalise the rest), <b>question assignment</b> that holds up for a 30-person team, and a <b>full-screen answering view</b> with the response library moved to the side instead of a tiny modal. Everything here is simulated; nothing is stored.</p>
</header>

<div class="guide" id="guide">
  <span class="lbl">Try</span>
  <span class="g" data-g="autofill" data-do="autofill"><i></i>Phase 1 · Autofill standard fields</span>
  <span class="g" data-g="insert" data-do="rest"><i></i>Phase 2 · Draft, insert, insert</span>
  <span class="g" data-g="expand" data-do="expandcur"><i></i>Answer full-screen</span>
  <span class="g" data-g="assign" data-do="assign"><i></i>Assign across the team</span>
  <span class="g" data-g="map" data-do="map"><i></i>Map the document (XML)</span>
  <span class="g" data-g="activity" data-do="activity"><i></i>SharePoint activity</span>
  <span class="reset" id="reset">Reset</span>
</div>

<section class="frame">
<div class="win">
  <div class="titlebar">
    <span class="lights"><i></i><i></i><i></i></span>
    <span class="docname"><span class="ms">description</span>Northside School Upgrade – Tender Response.docx <small id="savestate">Saved to SharePoint</small></span>
    <span class="presence" id="presence"><span class="av a1">DD</span><span class="av a2">MW</span></span>
  </div>
  <div class="tabs"><span>Home</span><span>Insert</span><span>Layout</span><span>References</span><span>Review</span><span>View</span><span class="on">Tenderfy Ray<i class="dot" id="tabdot" style="display:none"></i></span></div>
  <div class="ribbon">
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="toggle"><span class="ms">smart_toy</span><b>Open Ray</b></div>
      <div class="rb" data-do="ask"><span class="ms">help</span><b>Ask about<br>document</b></div>
    </div><div class="lbl">Ray</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="autofill"><span class="ms">auto_fix_high</span><b>Autofill<br>fields</b></div>
      <div class="rb" data-do="cursor"><span class="ms">text_select_move_forward_character</span><b>Insert<br>at cursor</b></div>
      <div class="rb" data-do="rest"><span class="ms">playlist_add</span><b>Insert<br>all answers</b></div>
      <div class="rb" data-do="expandcur"><span class="ms">open_in_full</span><b>Answer<br>full-screen</b></div>
    </div><div class="lbl">Answers</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="assign"><span class="ms">assignment_ind</span><b>Assign<br>question</b></div>
      <div class="rb" data-do="sync"><span class="ms">sync</span><b>Sync<br>SharePoint</b></div>
      <div class="rb" data-do="activity"><span class="ms">notifications</span><b>Activity</b><span class="cnt" id="ribcnt"></span></div>
    </div><div class="lbl">Team</div></div>
  </div>
  <div class="body">
    <div class="canvas"><div class="page" id="page">
      <div class="crumb">Schedule 3 · Returnable schedules</div>
      <h3>Section 3 — Methodology</h3>
      <p class="sub">Responses to the Principal’s evaluation criteria · Northside School Upgrade · RFT 2026-114</p>
      <i class="outline-rail"></i>
      <div id="fields"></div>
      <div id="qs"></div>
    </div></div>
    <div class="fs" id="fs"></div>
    <div class="pane" id="pane">
      <div class="pane-head"><img src="{WORDMARK}" alt="Tenderfy"> Ray <span class="bell" data-do="activity"><span class="ms">notifications</span><b id="bell"></b></span><span class="ms" data-do="toggle">close</span></div>
      <div class="raypanel">
        <div class="rp-head"><i class="rp-back"></i><span class="rp-title">Northside School Upgrade</span><em class="rp-beta">Beta</em><i class="rp-dots"></i></div>
        <div class="phases" id="phases"></div>
        <div class="rail-body" id="rail"></div>
        <div class="rp-foot"><div class="rp-ref" id="refs"></div>
          <div class="rp-composer" id="composer"><i class="rp-att"></i><span class="rp-input" id="input" contenteditable="true" data-ph="Reply to Ray…"></span><i class="rp-clip"></i><i class="rp-send" id="send"></i></div></div>
      </div>
    </div>
  </div>
</div>
</section>

<section class="road">
  <div class="lbl"><b>Roadmap</b> · from the update — not in-product UI</div>
  <div class="road-grid">
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Word add-in</b><small>First release · end of next week. Q&amp;A pane, insert at cursor, XML parsing.</small></span><span class="rp-go">Now</span><i class="rp-meter"><i style="width:78%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Insert, insert, insert</b><small>Sequential insertion into the next empty slot — the flow after cursor placement.</small></span><span class="rp-go off">Next</span><i class="rp-meter"><i style="width:20%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Excel add-in</b><small>Starts once the Word add-in ships. Same panel, same knowledge.</small></span><span class="rp-go off">After</span><i class="rp-meter"><i style="width:0%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Template builder</b><small>Complex module · a new developer may join, pending technical interview.</small></span><span class="rp-go off">Pending</span><i class="rp-meter"><i style="width:0%"></i></i></div>
  </div>
</section>
<div class="toast" id="toast"></div>

<script>
const RAY = "{RAY}";
const PEOPLE = {{ DD: ['Daniel','a1'], MW: ['Mia','a2'], TB: ['Tom','a3'] }};
const AV = (k, cls) => `<span class="av ${{PEOPLE[k][1]}} ${{cls||''}}">${{k}}</span>`;
const Q0 = () => [
  {{ id:'3.1', t:'Describe your approach to site establishment and hoarding.', a:'Site establishment will follow our standard three-stage sequence: perimeter hoarding to the Grove Street frontage, temporary services connection, and a single controlled gate on the northern boundary away from the school entrance.', by:null }},
  {{ id:'3.2', t:'Describe how you will manage disruption during school drop-off and pick-up.', a:null, d:'No deliveries, concrete pours or crane lifts will be scheduled between 8:00–9:15am and 2:45–3:45pm on school days. A dedicated traffic controller will hold the Grove Street gate closed during these windows, with the site supervisor as the single point of contact for the school office.', src:['Disruption Management Plan · Riverside Primary','Northside RFT · criterion 3(b)'], why:'They want windows, not intentions. The criterion scores named no-work periods and a single school contact. Drafted from your Riverside Primary plan, with the times swapped for Northside’s bell schedule.', short:'School drop-off and pick-up', srcshort:'Riverside disruption plan' }},
  {{ id:'3.3', t:'Outline your communication plan with the school and neighbouring residents.', a:null, d:'A fortnightly works notice will go to the school office and letterboxed to Grove and Elm Street residents, with a 48-hour notice for any out-of-hours work. The site supervisor’s direct number is published on the hoarding and in every notice.', src:['Communications register · Riverside Primary','Northside RFT · criterion 3(c)'], why:'The criterion asks for a named channel and a notice period. Both come straight from the Riverside comms register; the residents’ streets are Northside’s.', short:'Communication plan', srcshort:'Riverside comms register' }},
  {{ id:'3.4', t:'Detail your traffic management approach for the Grove Street frontage.', a:null, d:'A Traffic Management Plan certified to AS 1742.3 will maintain one lane in each direction on Grove Street at all times. Heavy vehicle movements are restricted to 9:30am–2:30pm, marshalled from the northern gate, and no vehicles will reverse onto the carriageway.', src:['Grove Street TMP · draft v2','Northside RFT · criterion 3(d)'], why:'Criterion 3(d) scores lane retention and school-hour restrictions. The draft TMP already has both; the reversing clause comes from the Riverside audit finding.', short:'Traffic management', srcshort:'Grove Street TMP' }},
  {{ id:'3.5', t:'Describe your environmental controls for dust and noise.', a:'Dust will be controlled by water cart during earthworks and a wheel-wash at the gate. Noisy works are restricted to 7:00am–5:00pm Monday to Friday, with residents notified 48 hours ahead of any exception.', by:null, gap:'No noise monitoring clause — Tom’s comment on 3.5 asks for one.' }},
];
let S;
function fresh() {{
  S = {{ qs: Q0(), cur: '3.2', open: true, mapped: false, queue: null, ready: {{}}, done: {{}},
        assigned: {{ '3.4': ['MW','Daniel','due Friday'] }}, editing: {{ '3.1':'MW' }}, comments: {{ '3.5':'TB' }},
        unread: 3, log: [], busy: false, guide: {{}}, phase: 1,
        fields: [ ['Tenderer name', 'Northside Constructions Pty Ltd'], ['ABN', '61 204 118 337'], ['Registered address', '14 Grove Street, Northside VIC 3070'],
                  ['Public liability insurance', '$20M · QBE · expires 30 Jun 2027'], ['Workers compensation', 'WorkSafe VIC · policy 88-1120-4'], ['Quality system', 'ISO 9001:2015 · cert. 2025-1183'] ].map(([k,v]) => ({{ k, v, filled: false }})) }};
  document.getElementById('rail').innerHTML = '';
  document.getElementById('fs').className = 'fs';
  S.log = [];
  renderDoc(); renderRefs(); renderBell(); renderGuide(); renderPhases();
  emptyState();
}}
function renderPhases() {{
  const f = S.fields.filter(x => x.filled).length, e = empties().length;
  const p1 = f === S.fields.length ? 'done' : (S.phase === 1 ? 'on' : ''), p2 = e === 0 ? 'done' : (S.phase === 2 ? 'on' : '');
  $('#phases').innerHTML = `<div class="ph ${{p1}}" data-do="autofill"><i>${{p1==='done'?'✓':'1'}}</i>Autofill<small>${{f}}/${{S.fields.length}} fields</small></div>
    <div class="ph ${{p2}}" data-do="rest"><i>${{p2==='done'?'✓':'2'}}</i>Draft &amp; finalise<small>${{5-e}}/5 answers</small></div>`;
}}
function renderFields() {{
  const f = S.fields.filter(x => x.filled).length;
  $('#fields').innerHTML = `<div class="fields"><div class="k">Schedule 1 · Tenderer details ${{f ? `<span class="chip">${{f}} of ${{S.fields.length}} autofilled by Ray</span>` : `<span class="chip warm">${{S.fields.length}} standard fields empty</span>`}}</div>
    ${{S.fields.map(x => `<div class="frow${{x.filled?' filled':''}}"><span>${{x.k}}</span>${{x.filled ? `<b>${{x.v}}</b>` : '<i class="empty"></i>'}}</div>`).join('')}}</div>`;
}}
async function autofill() {{
  if (S.busy) return; S.busy = true; mark('autofill'); S.phase = 1; renderPhases();
  you('Autofill the standard fields from our company profile.');
  const e = await think([
    ['read_document_xml', 'Schedule 1 · 6 standard fields found'],
    ['read_company_profile', 'Northside Constructions · profile current'],
    ['match_fields', '6 / 6 matched · ABN, address, insurances, quality'],
    ['write_fields', 'written in place · no new document created']], '1.2');
  for (const x of S.fields) {{ x.filled = true; renderFields(); await sleep(260); }}
  renderPhases();
  $('#fields').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  offer(e, `<div class="rail-offer status"><p><b>Phase 1 done — 6 fields filled in this document.</b> No second document to go and find: the routine information (ABN, address, insurances, quality system) is written straight into Schedule 1. ${{empties().length}} questions in Section 3 still need drafting.</p>
    <div class="acts"><span class="rail-btn" data-do="phase2">Start phase 2 · Draft &amp; finalise</span><span class="rail-btn ghost" data-do="assign">Assign first</span></div></div>`);
  S.busy = false;
}}
// ---------- full-screen answering ----------
const LIB = [
  ['Disruption Management Plan · Riverside Primary', 'School-hour no-work windows, gate control, single school contact.', 'Won · 2025', 'A dedicated traffic controller will hold the gate closed during school drop-off and pick-up windows, with the site supervisor as the single point of contact for the school office.'],
  ['Communications register · Riverside Primary', 'Fortnightly notices, 48-hour out-of-hours notice, published site number.', 'Won · 2025', 'A fortnightly works notice will go to the school office and neighbouring residents, with 48 hours’ notice for any out-of-hours work.'],
  ['Grove Street TMP · draft v2', 'AS 1742.3, one lane each way, heavy vehicles 9:30–2:30, no reversing.', 'Draft', 'Heavy vehicle movements are restricted to 9:30am–2:30pm and marshalled from the northern gate; no vehicles will reverse onto the carriageway.'],
  ['Noise management procedure', 'Boundary logging meter, EPA limits, stop-work trigger.', 'Policy', 'Noise will be monitored at the school boundary with a logging meter; readings above the EPA limit stop the work until the source is controlled.'],
];
function expand(qid) {{
  const x = q(qid || S.cur); if (!x) return; S.cur = x.id; mark('expand'); renderDoc();
  const text = x.a || x.d || '';
  const fs = $('#fs'); fs.className = 'fs on';
  fs.innerHTML = `<div class="lib"><div class="lib-h"><span>Response library</span><span class="ms" data-do="libtoggle">left_panel_close</span></div>
      <div class="lib-s"><span class="ms">search</span>Search 1,240 assets…</div>
      ${{LIB.map((l, i) => `<div class="lib-i" data-do="libins" data-i="${{i}}"><b>${{l[0]}}</b><small>${{l[1]}}</small><em>${{l[2]}}</em></div>`).join('')}}</div>
    <div class="ed"><div class="ed-top"><span class="n">${{x.id}}</span><span class="t">${{x.t}}</span><span class="wc" id="wc"></span><span class="ms" data-do="fsclose">close_fullscreen</span></div>
      <div class="ed-tools"><span class="ms">format_bold</span><span class="ms">format_italic</span><span class="ms">format_underlined</span><span class="sep"></span><span class="ms">format_list_bulleted</span><span class="ms">format_list_numbered</span><span class="sep"></span><span class="ms">table</span><span class="ms">link</span></div>
      <div class="ed-body"><h4>${{x.t}}</h4><div class="ed-text" id="edtext" contenteditable="true">${{text ? `<p>${{text}}</p>` : '<p><br></p>'}}</div></div>
      <div class="ed-foot"><div class="srcs">${{(x.src||[]).map(s => `<b>${{s}}</b>`).join('')}}</div><span class="rail-btn ghost" data-do="fsclose">Close</span><span class="rail-btn" data-do="fsinsert">${{x.a ? 'Update in document' : 'Insert into document'}}</span></div></div>`;
  wc();
  const ed = $('#edtext'); ed.addEventListener('input', wc); setTimeout(() => ed.focus(), 50);
}}
function wc() {{ const t = ($('#edtext')?.innerText || '').trim(); const n = t ? t.split(/\\s+/).length : 0; const el = $('#wc'); if (el) el.textContent = `${{n}} words · ~${{Math.max(1, Math.round(n/300))}} page${{n>300?'s':''}}`; }}
function libInsert(i) {{ const ed = $('#edtext'); const l = LIB[i]; ed.insertAdjacentHTML('beforeend', `<p class="new">${{l[3]}}</p>`); ed.lastElementChild.scrollIntoView({{ block: 'nearest' }}); wc(); toast(`Added from ${{l[0].split(' ·')[0]}}`); }}
function fsInsert() {{ const x = q(S.cur); const t = ($('#edtext')?.innerText || '').trim(); if (!t) return; x.d = t; if (x.a) {{ x.a = t; x.by = 'ray'; renderDoc(); closeFs(); toast(`${{x.id}} updated in document`); }} else {{ S.ready[x.id] = true; closeFs(); insert(x.id); }} }}
function closeFs() {{ $('#fs').className = 'fs'; }}
// ---------- assignment at team scale ----------
function assignSheet() {{
  mark('assign');
  const people = Object.keys(PEOPLE);
  const rows = S.qs.map(x => `<div class="r${{S.cur===x.id?' cur':''}}"><span class="n">${{x.id}}</span><span class="t">${{x.short || x.t.slice(0,44)}}<small>${{x.a ? 'Answered' : 'Open'}}${{S.assigned[x.id] ? ' · ' + PEOPLE[S.assigned[x.id][0]][0] + ' · ' + S.assigned[x.id][2] : ' · unassigned'}}</small></span>
      <span class="who">${{people.map(k => `<span class="av ${{PEOPLE[k][1]}}${{S.assigned[x.id]&&S.assigned[x.id][0]===k?' sel':''}}" data-do="assignrow" data-q="${{x.id}}" data-who="${{k}}" title="${{PEOPLE[k][0]}}">${{k}}</span>`).join('')}}</span></div>`).join('');
  const load = people.map(k => `<span>${{AV(k)}} <b>${{PEOPLE[k][0]}}</b> · ${{Object.values(S.assigned).filter(v => v[0]===k).length}}</span>`).join('');
  const old = $('#sheet'); if (old) old.closest('.rail-entry').remove();
  rail().insertAdjacentHTML('beforeend', `<div class="rail-entry"><div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div>
    <div class="sheet" id="sheet"><div class="k">Assign Section 3 <b>Bilby-style: 30 people, one owner per question</b></div>${{rows}}<div class="load">${{load}}</div></div>
    <div class="acts"><span class="rail-btn ghost" data-do="assignauto">Suggest owners from past tenders</span></div></div>`);
  scrollRail();
}}
function assignRow(qid, who) {{ S.assigned[qid] = [who, 'you', 'due Fri']; S.unread += who === 'DD' ? 1 : 0; renderBell(); renderDoc(); assignSheet(); toast(`${{qid}} → ${{PEOPLE[who][0]}}`); }}
function assignAuto() {{ const pick = {{ '3.1':'DD', '3.2':'MW', '3.3':'MW', '3.4':'TB', '3.5':'TB' }}; S.qs.forEach(x => {{ if (!x.a) S.assigned[x.id] = [pick[x.id], 'Ray', 'due Fri']; }}); renderDoc(); assignSheet(); rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>Owners suggested from who wrote these answers last time.</b> Everyone gets one notification in Word and on SharePoint; nothing is sent until you confirm.</p></div>`); scrollRail(); }}
const $ = s => document.querySelector(s);
const q = id => S.qs.find(x => x.id === id);
const empties = () => S.qs.filter(x => !x.a);
function toast(m) {{ const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('on'), 2200); }}
function mark(g) {{ S.guide[g] = true; renderGuide(); }}
function renderGuide() {{ document.querySelectorAll('.guide .g').forEach(el => el.classList.toggle('done', !!S.guide[el.dataset.g])); }}
function renderBell() {{
  $('#bell').textContent = S.unread || '';
  $('#ribcnt').textContent = S.unread || '';
  $('#tabdot').style.display = S.unread ? 'block' : 'none';
}}
function renderRefs() {{
  const refs = ['Tender Response.docx', 'Company knowledge'].concat(S.mapped ? ['Document map · 14 questions'] : []);
  $('#refs').innerHTML = '<span>Reference</span>' + refs.map(r => `<b>${{r}}</b>`).join('') + '<b class="add">+ Add</b>';
}}
function renderDoc() {{
  const page = $('#page'); page.classList.toggle('mapped', S.mapped);
  renderFields();
  $('#qs').innerHTML = S.qs.map(x => {{
    let side = '';
    if (S.editing[x.id]) side += `<span class="chip live">${{AV(S.editing[x.id])}}${{PEOPLE[S.editing[x.id]][0]}} is editing</span> `;
    if (S.assigned[x.id]) side += `<span class="chip warm">${{AV(S.assigned[x.id][0])}}Assigned to ${{PEOPLE[S.assigned[x.id][0]][0]}} · ${{S.assigned[x.id][2]}}</span> `;
    if (S.comments[x.id]) side += `<span class="chip">${{AV(S.comments[x.id])}}1 comment</span>`;
    let body;
    if (x.a && x.by === 'ray') body = `<div class="a ins"><span class="tag">Inserted by Ray <small>· from ${{x.src.length}} sources · just now</small></span><p>${{x.a}}</p></div>`;
    else if (x.a) body = `<div class="a${{x.flag?' ins gap':''}}">${{x.flag?'<span class="tag">Gap flagged by Ray <small>· '+x.gap+'</small></span>':''}}<p>${{x.a}}</p></div>`;
    else {{
      const isCur = S.cur === x.id, ready = S.ready[x.id];
      body = `<div class="slot" data-slot="${{x.id}}">${{isCur ? '<span class="caret"></span>' : ''}}${{isCur ? (ready ? 'Cursor here — Ray’s answer is ready to insert' : 'Cursor here — ask Ray, or Insert at cursor') : (S.mapped ? 'Answer slot detected · empty' : 'Not answered yet')}}</div>`;
    }}
    return `<div class="q${{S.cur===x.id?' cur':''}}" data-q="${{x.id}}"><span class="qtag">Q${{x.id}}</span><div class="qh"><span class="n">${{x.id}}</span>${{x.t}}</div>${{side?`<span class="side">${{side}}</span>`:''}}${{body}}</div>`;
  }}).join('');
  document.querySelectorAll('.slot').forEach(el => el.onclick = () => {{ S.cur = el.dataset.slot; renderDoc(); }});
  document.querySelectorAll('.q').forEach(el => el.onclick = e => {{ if (!e.target.closest('.slot')) {{ S.cur = el.dataset.q; renderDoc(); }} }});
}}
// ---------- rail ----------
const rail = () => $('#rail');
function scrollRail() {{ const r = rail(); r.scrollTop = r.scrollHeight; }}
function you(text) {{ rail().insertAdjacentHTML('beforeend', `<div class="rail-you">${{text}}</div>`); scrollRail(); }}
function emptyState() {{
  const n = empties().length;
  rail().insertAdjacentHTML('beforeend', `<div class="rail-entry">
    <div class="ray-empty"><span class="ray-halo"><img src="${{RAY}}" alt=""></span>
      <h3>How can Ray help with this document?</h3>
      <p>Ray has read <b>Tender Response.docx</b> — 6 standard fields empty in Schedule 1, ${{n}} questions open in Section 3 — and has your company profile and knowledge alongside it. Two phases: fill the routine fields first, then draft the rest.</p>
      <div class="ray-starter" data-do="autofill">Autofill the standard fields — ABN, address, insurances — from our company profile.</div>
      <div class="ray-starter" data-do="rest">Then answer the open questions in Section 3 from our Riverside Primary submission.</div>
      <div class="ray-starter" data-do="assign">Assign Section 3 across the team.</div></div>
    ${{nextCard()}}</div>`);
  scrollRail();
}}
function nextCard() {{
  const e = empties(); if (!e.length) return `<div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Section 3 complete</b> · 5 of 5 answered</span><i class="rp-meter"><i style="width:100%"></i></i></div>`;
  const done = 5 - e.length;
  return `<div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Next · ${{done+1}} of 5</b> · ${{e[0].id}} ${{e[0].short || e[0].t.slice(0,32)}}</span><span class="rp-go" data-do="ask" data-q="${{e[0].id}}">Start</span><i class="rp-meter"><i style="width:${{done/5*100}}%"></i></i></div>`;
}}
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function think(steps, secs) {{
  const id = 'e' + Date.now();
  rail().insertAdjacentHTML('beforeend', `<div class="rail-entry" id="${{id}}">
    <div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div>
    <div class="rh-s open"><i class="chev"></i><span class="lbl">Working…</span></div>
    <div class="rail-work"></div></div>`);
  const entry = document.getElementById(id), work = entry.querySelector('.rail-work');
  for (const [code, note] of steps) {{
    work.insertAdjacentHTML('beforeend', `<div class="work live"><i></i><code>${{code}}</code><span>${{note}}</span></div>`);
    scrollRail(); await sleep(420);
    work.lastElementChild.classList.replace('live', 'done');
  }}
  const h = entry.querySelector('.rh-s'); h.querySelector('.lbl').textContent = `Thought for ${{secs}}s · ${{steps.length}} steps`;
  h.classList.remove('open'); work.classList.add('folded');
  h.onclick = () => {{ h.classList.toggle('open'); work.classList.toggle('folded'); }};
  return entry;
}}
function offer(entry, html) {{ entry.insertAdjacentHTML('beforeend', html); scrollRail(); }}
// ---------- flows ----------
async function ask(qid) {{
  if (S.busy) return; S.busy = true; mark('ask');
  const x = q(qid || S.cur); S.cur = x.id; renderDoc();
  you(`What is the buyer actually asking for in ${{x.id}} — and what have we said before?`);
  const e = await think([
    ['read_document_xml', 'Schedule 3 · 14 questions found'],
    ['read_question', `${{x.id}} · ${{x.short.toLowerCase()}}`],
    ['search_company_knowledge', `3 matches · ${{x.srcshort}} strongest`],
    ['draft_answer', `${{x.d.split(' ').length}} words · aligned to criterion`]], '1.4');
  S.ready[x.id] = true; renderDoc();
  offer(e, `<div class="rail-offer ask"><p><b>${{x.why.split('. ')[0]}}.</b> ${{x.why.split('. ').slice(1).join('. ')}}</p>
    <div class="srcs">${{x.src.map(s => `<b>${{s}}</b>`).join('')}}</div>
    <div class="acts"><span class="rail-btn" data-do="insert" data-q="${{x.id}}">Insert at cursor</span><span class="rail-btn ghost" data-do="refine" data-q="${{x.id}}">Refine</span><span class="exp" data-do="expand" data-q="${{x.id}}"><span class="ms">open_in_full</span>Full screen</span></div></div>`);
  S.busy = false;
}}
function insert(qid, fromQueue) {{
  const x = q(qid); if (!x || x.a) return;
  x.a = x.d; x.by = 'ray'; delete S.ready[x.id]; S.done[x.id] = true;
  const e = empties(); S.cur = e.length ? e[0].id : x.id;
  S.phase = 2; renderDoc(); renderPhases();
  const el = document.querySelector(`.q[data-q="${{x.id}}"]`); el && el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  $('#savestate').textContent = 'Saving…'; setTimeout(() => $('#savestate').textContent = 'Saved to SharePoint', 900);
  if (S.queue) renderQueue(); else {{ rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>Inserted into ${{x.id}}.</b> ${{e.length ? `Cursor moved to ${{S.cur}} — ${{e.length}} still empty.` : 'Section 3 is complete.'}}</p></div>${{nextCard()}}`); scrollRail(); }}
  toast(`Inserted into ${{x.id}}${{e.length && S.queue ? ` · next: ${{S.cur}}` : ''}}`);
}}
async function rest() {{
  if (S.busy) return; const e = empties(); if (!e.length) {{ toast('Nothing left to answer in Section 3'); return; }}
  S.busy = true; mark('insert'); S.phase = 2; renderPhases();
  you('Answer the rest of Section 3 from the same sources.');
  const steps = [['read_document_xml', 'Schedule 3 · 14 questions found'], ['outline_document', `${{e.length}} empty answer slots in Section 3`]];
  e.forEach(x => steps.push(['search_company_knowledge', `${{x.id}} · ${{x.srcshort}}`]));
  steps.push(['draft_answers', `${{e.length}} drafts · aligned to criteria 3(b)–3(d)`]);
  const entry = await think(steps, '3.1');
  e.forEach(x => S.ready[x.id] = true); renderDoc();
  S.queue = {{ ids: e.map(x => x.id), entry }};
  entry.insertAdjacentHTML('beforeend', `<div class="rail-offer" id="queue"></div><div class="note"><b>Today:</b> place the cursor, then insert. <b>Next:</b> Ray targets the next empty slot itself — insert, insert, insert.</div>`);
  renderQueue(); S.busy = false;
}}
function renderQueue() {{
  const box = document.getElementById('queue'); if (!box || !S.queue) return;
  const ids = S.queue.ids, left = ids.filter(id => !q(id).a);
  let firstOpen = true;
  box.innerHTML = `<p><b>${{left.length ? `${{left.length}} answer${{left.length>1?'s':''}} ready.` : 'All inserted.'}}</b> ${{left.length ? 'One click each — Ray places every answer in its own slot, in order, so you never hunt for the cursor.' : 'Every answer landed in its own slot, in order.'}}</p>
    <div class="ins-list">${{ids.map(id => {{ const x = q(id); if (x.a) return `<div class="ins-row done"><span class="n">${{id}}</span><span class="t">${{x.short}}<small>Inserted · ${{x.src.length}} sources</small></span><span class="st">Inserted</span></div>`;
      const cls = firstOpen ? 'next' : 'ghost'; const row = `<div class="ins-row${{firstOpen?'':' queued'}}"><span class="n">${{id}}</span><span class="t">${{x.short}}<small>Ready · ${{x.srcshort}}</small></span><span style="display:flex;gap:6px;align-items:center"><span class="ms" data-do="expand" data-q="${{id}}" title="Open full-screen">open_in_full</span><span class="rail-btn ${{cls}}" data-do="insert" data-q="${{id}}">Insert</span></span></div>`; firstOpen = false; return row; }}).join('')}}</div>
    ${{left.length ? `<div class="acts"><span class="rail-btn ghost" data-do="insertall">Insert all ${{left.length===1?'':left.length===2?'both':'three'}}</span><span class="rail-btn ghost" data-do="sources">Review first</span></div>` : nextCard()}}`;
  if (!left.length) S.queue = null;
  scrollRail();
}}
async function insertAll() {{ const ids = (S.queue ? S.queue.ids : empties().map(x=>x.id)).filter(id => !q(id).a); for (const id of ids) {{ insert(id, true); await sleep(650); }} }}
async function map() {{
  if (S.busy) return; S.busy = true; mark('map');
  you('Map this document.');
  const e = await think([
    ['open_document_xml', 'word/document.xml · 48 KB · no bookmarks needed'],
    ['outline_document', '5 sections · 14 questions · ' + empties().length + ' empty answer slots'],
    ['map_answer_slots', '14 / 14 matched by heading + numbering'],
    ['validate_structure', 'styles, tables, numbering untouched']], '2.1');
  S.mapped = true; renderDoc(); renderRefs();
  offer(e, `<div class="rail-offer status"><p><b>Document map ready.</b> Ray reads and writes the document’s own XML — the structure Word itself uses — so answers land inside the real paragraphs, and nothing is rewritten around them.</p>
    <div class="srcs"><b>XML-native</b><b>No bookmarks</b><b>No corruption risk</b></div></div>
    <div class="note">Replaces the Syncfusion bookmark approach — the source of the formatting pain in earlier builds.</div>`);
  S.busy = false;
}}
function activity() {{
  mark('activity'); S.unread = 0; renderBell();
  const mine = Object.entries(S.assigned).filter(([id, v]) => v[0] === 'DD');
  const forYou = [['3.4', 'Traffic management approach', 'Assigned by Daniel · due Friday']];
  rail().insertAdjacentHTML('beforeend', `<div class="rail-entry">
    <div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div>
    <div class="rail-offer status"><p><b>Since you were last here:</b> 3 things changed in this document on SharePoint.</p></div>
    <div class="assign"><div class="k">Assigned to you</div>
      ${{q('3.4').a ? `<div class="r"><span class="n">3.4</span><span class="t">Traffic management approach<small>Answered · assigned by Daniel</small></span><span class="when">done</span></div>` : `<div class="r"><span class="n">3.4</span><span class="t">Traffic management approach<small>Assigned by Daniel · due Friday</small></span><span class="rail-btn" data-do="ask" data-q="3.4">Draft</span></div>`}}</div>
    <div class="assign"><div class="k">Changed on SharePoint</div>
      <div class="r"><span class="n">3.1</span><span class="t">Edited by Mia<small>Rewrote the gate sequence · now editing</small></span><span class="when">12 min</span></div>
      <div class="r"><span class="n">3.5</span><span class="t">Comment from Tom<small>“Add the noise monitoring clause?”</small></span><span class="rail-btn ghost" data-do="review">Check</span></div></div>
    ${{nextCard()}}</div>`);
  scrollRail();
}}
function assignPick() {{
  const x = q(S.cur); if (!x) return;
  rail().insertAdjacentHTML('beforeend', `<div class="rail-entry" id="pick">
    <div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div>
    <div class="picker"><div class="k">Assign ${{x.id}} · ${{x.short || x.t.slice(0,40)}}</div>
      <div class="ppl">${{Object.keys(PEOPLE).map(k => `<span class="p" data-do="assignto" data-who="${{k}}">${{AV(k)}}${{PEOPLE[k][0]}}</span>`).join('')}}</div></div></div>`);
  scrollRail();
}}
function assignTo(who) {{
  const x = q(S.cur); S.assigned[x.id] = [who, 'you', 'due Fri']; mark('assign');
  const p = document.getElementById('pick'); if (p) p.id = '';
  renderDoc();
  rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>${{x.id}} assigned to ${{PEOPLE[who][0]}}.</b> ${{PEOPLE[who][0]}} gets a notification in Word and on SharePoint; the question is flagged in the document.</p></div>`);
  scrollRail(); toast(`${{x.id}} assigned to ${{PEOPLE[who][0]}}`);
}}
async function sync() {{
  $('#savestate').textContent = 'Syncing…'; await sleep(700);
  const target = S.qs.find(x => x.a && !S.editing[x.id] && x.id !== '3.1') || q('3.1');
  S.editing = {{}}; S.editing[target.id] = 'TB'; S.unread += 1; renderBell(); renderDoc();
  if (!$('#presence .a3')) $('#presence').insertAdjacentHTML('beforeend', AV('TB'));
  $('#savestate').textContent = 'Saved to SharePoint';
  rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>SharePoint sync.</b> Tom opened the document and is editing ${{target.id}}. Activity now shows ${{S.unread}} unread.</p></div>`); scrollRail();
  toast('Change arrived from SharePoint');
}}
async function review() {{
  if (S.busy) return; S.busy = true;
  you('Check every answer against the evaluation criteria.');
  const answered = S.qs.filter(x => x.a);
  const e = await think([['read_document_xml', 'Schedule 3 · 14 questions found'], ['read_criteria', 'criteria 3(a)–3(e) · weights loaded'], ...answered.map(x => ['check_answer', `${{x.id}} · ${{x.id==='3.5' ? 'gap: noise monitoring' : 'meets criterion'}}`])], '2.6');
  const g = q('3.5'); g.flag = true; renderDoc();
  offer(e, `<div class="rail-offer ask"><p><b>${{answered.length}} answers checked · 1 gap.</b> 3.5 has controls but no monitoring — criterion 3(e) scores “monitoring and response”. Tom’s comment asks for the same thing.</p>
    <div class="acts"><span class="rail-btn" data-do="fixgap">Add monitoring clause</span><span class="rail-btn ghost" data-do="sources">Show criterion</span></div></div>`);
  S.busy = false;
}}
function fixGap() {{ const g = q('3.5'); if (!g.flag) return; g.a += ' Noise will be monitored at the school boundary with a logging meter; readings above the EPA limit stop the work until the source is controlled.'; g.flag = false; g.by = 'ray'; g.src = ['Noise management procedure', 'Northside RFT · criterion 3(e)']; delete S.comments['3.5']; renderDoc(); rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>Monitoring clause added to 3.5.</b> Tom’s comment is resolved.</p></div>`); scrollRail(); toast('3.5 updated · comment resolved'); }}
function refine(qid) {{ const x = q(qid); rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>Refine ${{x.id}}:</b> tell Ray what to change — shorter, more specific, a different source — in the box below.</p></div>`); scrollRail(); $('#input').focus(); }}
function sources() {{ rail().insertAdjacentHTML('beforeend', `<div class="rail-offer status"><p><b>Sources are company knowledge,</b> read through the same guard as the app: only documents this role can see are ever offered, and every answer names what it drew on.</p></div>`); scrollRail(); }}
function togglePane() {{ S.open = !S.open; $('#pane').style.display = S.open ? '' : 'none'; document.querySelector('.body').style.gridTemplateColumns = S.open ? '' : '1fr'; }}
async function typed(text) {{
  const t = text.trim().toLowerCase(); if (!t) return;
  if (/autofill|auto-fill|abn|standard fields|company profile/.test(t)) return autofill();
  if (/map|parse|structure|xml/.test(t)) return map();
  if (/assign /.test(t + ' ') && !/assigned to me/.test(t)) {{ you(text); return assignSheet(); }}
  if (/full.?screen|expand|open .* editor/.test(t)) return expand(S.cur);
  if (/assigned|changed|since|activity|who/.test(t)) {{ you(text); return activity(); }}
  if (/rest|all|section|empty/.test(t)) return rest();
  if (/check|criteria|review|gap/.test(t)) return review();
  if (/insert/.test(t)) {{ const r = Object.keys(S.ready)[0]; if (r) return insert(r); }}
  const m = t.match(/3\\.[1-5]/); if (m) S.cur = m[0];
  return ask(S.cur);
}}
// ---------- wiring ----------
document.addEventListener('click', e => {{
  const el = e.target.closest('[data-do]'); if (!el) return;
  const d = el.dataset.do, qid = el.dataset.q;
  ({{ ask: () => ask(qid), rest, map, activity, assign: assignSheet, assignrow: () => assignRow(qid, el.dataset.who), assignauto: assignAuto, assignto: () => assignTo(el.dataset.who), sync, review, toggle: togglePane,
     insert: () => insert(qid), insertall: insertAll, cursor: () => {{ const r = S.ready[S.cur]; r ? insert(S.cur) : ask(S.cur); }},
     refine: () => refine(qid), sources, fixgap: fixGap,
     autofill, phase2: () => {{ S.phase = 2; renderPhases(); rest(); }}, expand: () => expand(qid), expandcur: () => expand(S.cur), fsclose: closeFs, fsinsert: fsInsert,
     libins: () => libInsert(+el.dataset.i), libtoggle: () => $('#fs').classList.toggle('libhid') }})[d]?.();
}});
document.addEventListener('dblclick', e => {{ const s = e.target.closest('.slot, .q .a'); if (s) {{ const qq = s.closest('.q'); S.cur = qq.dataset.q; expand(S.cur); }} }});
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeFs(); }});
const inp = $('#input');
inp.addEventListener('focus', () => inp.classList.add('typing')); inp.addEventListener('blur', () => inp.classList.remove('typing'));
inp.addEventListener('keydown', e => {{ if (e.key === 'Enter') {{ e.preventDefault(); const v = inp.textContent; inp.textContent = ''; typed(v); }} }});
$('#send').onclick = () => {{ const v = inp.textContent; inp.textContent = ''; typed(v); }};
$('#composer').onclick = e => {{ if (e.target.id !== 'send') inp.focus(); }};
$('#reset').onclick = fresh;
fresh();
</script>
</body></html>'''

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT, len(HTML))
