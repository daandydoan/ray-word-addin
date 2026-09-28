import base64, pathlib, re

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
EXTRACTS = pathlib.Path(__file__).resolve().parent
OUT = EXTRACTS / "ray-word-addin-interactive-b.html"

def data_uri(name):
    return "data:image/svg+xml;base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()
RAY = data_uri("ray-avatar.svg"); WORDMARK = data_uri("tenderfy-wordmark.svg")

src = (EXTRACTS / "ray-word-addin-mock.build.py").read_text(encoding="utf-8")
BASE_CSS = re.search(r'CSS = r"""(.*?)"""', src, re.S).group(1).replace("__RAY__", RAY)

EXTRA_CSS = r"""
.frame { margin-bottom: 28px; }
.guide { max-width: 1180px; margin: 0 auto 16px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.guide .lbl { font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-right: 4px; }
.guide .g { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; color: var(--ink-2); background: #fff; border: 1px solid #DCE5E1; border-radius: 999px; padding: 5px 11px 5px 7px; cursor: pointer; }
.guide .g i { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid #C9D4D0; position: relative; flex: none; }
.guide .g.done { border-color: #BFE0D2; background: #EAF5F0; }
.guide .g.done i { background: #1D9E75; border-color: #1D9E75; }
.guide .g.done i::after { content: ''; position: absolute; left: 4px; top: 1.5px; width: 3.5px; height: 7px; border: solid #fff; border-width: 0 1.5px 1.5px 0; transform: rotate(45deg); }
.guide .reset { margin-left: auto; font-size: 12px; color: var(--dim); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.guide .alt { font-size: 12px; color: var(--acc-deep); text-decoration: underline; text-underline-offset: 3px; }
.win { user-select: none; position: relative; }
.rb { cursor: pointer; } .rb:hover { background: #F2F5F4; } .rb.pri { background: var(--acc-tint); }

/* ===== the Ray bar: workflow across the top of the document ===== */
.raybar { display: flex; align-items: center; gap: 12px; padding: 8px 16px; background: #fff; border-bottom: 1px solid var(--word-line); font-size: 12px; }
.raybar .who { display: flex; align-items: center; gap: 7px; font-weight: 600; color: #1F2B28; }
.raybar .who img { width: 20px; height: 17px; }
.raybar .who em { font-style: normal; font-size: 8.5px; font-weight: 700; letter-spacing: .12em; background: #F2C46D; color: #2B2B2B; border-radius: 3px; padding: 2px 5px; text-transform: uppercase; }
.steps { display: flex; gap: 4px; flex: 1; }
.step { display: flex; align-items: center; gap: 7px; padding: 6px 10px; border-radius: 8px; border: 1px solid #E6ECEA; background: #FBFCFB; color: #6B7975; font-size: 11px; font-weight: 600; cursor: pointer; transition: background .15s, border-color .15s; }
.step:hover { border-color: #C9D4D0; }
.step i { width: 16px; height: 16px; border-radius: 50%; border: 1.5px solid #C9D4D0; display: grid; place-items: center; font-size: 9px; font-style: normal; color: #6B7975; }
.step.on { border-color: #1D9E75; color: #0F7355; background: rgba(29,158,117,.06); }
.step.on i { border-color: #1D9E75; color: #1D9E75; }
.step.done i { background: #1D9E75; border-color: #1D9E75; color: #fff; }
.step small { font-weight: 400; color: #6B7975; }
.step .bar { width: 46px; height: 3px; background: #E6ECEA; border-radius: 2px; overflow: hidden; }
.step .bar i { display: block; height: 100%; width: 0; border: 0; border-radius: 0; background: #1D9E75; transition: width .5s ease; }
.team { display: flex; align-items: center; gap: 8px; }
.team .presence .av { width: 22px; height: 22px; font-size: 9px; }
.bell { position: relative; cursor: pointer; }
.bell .ms { font-size: 20px; color: #605E5C; }
.bell b { position: absolute; top: -5px; right: -7px; min-width: 15px; height: 15px; border-radius: 999px; background: #D93B3B; color: #fff; font-size: 9px; font-weight: 700; display: grid; place-items: center; padding: 0 4px; border: 1.5px solid #fff; }
.bell b:empty { display: none; }

/* ===== document with a comment margin ===== */
.body { display: block; height: 660px; position: relative; }
.canvas { height: 100%; overflow: auto; padding: 26px 0 120px; }
.sheetwrap { display: grid; grid-template-columns: minmax(0, 1fr) 250px; gap: 0; width: min(1000px, 100%); margin: 0 auto; align-items: start; }
.page { width: 100%; margin: 0; min-height: 720px; padding: 48px 56px 60px; position: relative; }
.margin { position: relative; padding: 8px 12px 0 16px; }
.balloon { background: #fff; border: 1px solid #E6ECEA; border-radius: 10px; padding: 8px 10px; font-size: 11px; color: #1F2B28; box-shadow: 0 8px 20px -14px rgba(15,26,23,.4); margin-bottom: 10px; position: relative; animation: insIn .3s ease both; }
.balloon .h { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-weight: 600; }
.balloon .h .av { width: 18px; height: 18px; font-size: 8px; border: 0; margin: 0; }
.balloon .h small { margin-left: auto; font-weight: 400; color: #6B7975; }
.balloon .h .ray { width: 16px; height: 14px; }
.balloon p { margin: 0; line-height: 1.4; color: #33423E; }
.balloon .qref { font-family: ui-monospace, Menlo, monospace; font-size: 10px; font-weight: 700; color: #0F7355; }
.balloon .acts { margin-top: 7px; gap: 5px; }
.balloon .rail-btn { padding: 4px 10px; font-size: 10.5px; cursor: pointer; }
.balloon.live { border-color: #BFD3F0; }
.balloon.ray { border-color: rgba(29,158,117,.45); background: rgba(29,158,117,.05); }
.balloon.warm { border-color: #F2D9A6; }
.margin .k { font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; margin: 4px 0 8px; }
.margin .mute { font-size: 10.5px; color: #6B7975; }

/* questions with a gutter owner */
.q { position: relative; padding-left: 0; }
.own { position: absolute; left: -44px; top: 0; cursor: pointer; }
.own .av { width: 26px; height: 26px; font-size: 9.5px; border: 2px solid #fff; box-shadow: 0 0 0 1px #E6ECEA; margin: 0; }
.own .add { width: 26px; height: 26px; border-radius: 50%; border: 1.5px dashed #C9D4D0; display: grid; place-items: center; color: #9AA8A3; font-size: 16px; background: #fff; }
.own:hover .add { border-color: #1D9E75; color: #1D9E75; }
.pop { position: absolute; left: 0; top: 30px; z-index: 4; background: #fff; border: 1px solid #DCE5E1; border-radius: 9px; padding: 8px; display: none; gap: 6px; box-shadow: 0 12px 30px -14px rgba(15,26,23,.4); }
.pop.on { display: flex; }
.pop .p { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; border: 1px solid #DCE5E1; border-radius: 999px; padding: 3px 9px 3px 4px; cursor: pointer; white-space: nowrap; }
.pop .p:hover { background: #F2F5F4; }
.pop .p .av { width: 18px; height: 18px; font-size: 8px; border: 0; margin: 0; box-shadow: none; }
.q .qh { cursor: pointer; }
.q .qh:hover .n { background: #D2ECE2; }

/* ghost drafts inline, accept in place */
.ghost { border: 1.5px dashed #9DC9B8; border-radius: 8px; padding: 9px 12px; background: rgba(29,158,117,.04); position: relative; animation: insIn .35s ease both; }
.ghost p { margin: 0 0 8px; font-size: 12.5px; line-height: 1.55; color: #3E5A52; font-style: italic; }
.ghost .gh { display: flex; align-items: center; gap: 6px; font-size: 10px; color: #0F7355; font-weight: 600; margin-bottom: 5px; }
.ghost .gh img { width: 12px; height: 10px; }
.ghost .gh small { font-weight: 500; color: #6B7975; }
.ghost .gh .kb { margin-left: auto; font-family: ui-monospace, Menlo, monospace; font-size: 9.5px; color: #6B7975; border: 1px solid #DCE5E1; border-radius: 4px; padding: 1px 5px; background: #fff; }
.ghost .ga { display: flex; gap: 6px; }
.ghost .rail-btn { padding: 4px 11px; font-size: 10.5px; cursor: pointer; }
.q.next .ghost { border-style: solid; border-color: #1D9E75; box-shadow: 0 0 0 4px rgba(29,158,117,.12); }
.fields { border: 1px solid #E6ECEA; border-radius: 8px; padding: 10px 12px; margin: 0 0 18px; }
.fields .k { font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.fields .k .chip { margin-left: auto; }
.frow { display: grid; grid-template-columns: 150px 1fr; gap: 10px; font-size: 12px; padding: 4px 0; border-top: 1px solid #F0F3F1; align-items: center; }
.frow:first-of-type { border-top: 0; }
.frow span { color: var(--dim); }
.frow b { font-weight: 500; color: #1F2B28; }
.frow .empty { display: inline-block; width: 60%; height: 8px; border-radius: 4px; border: 1.5px dashed #C9D4D0; }
.frow.filled b { background: var(--acc-tint); border-radius: 4px; padding: 1px 6px; animation: insIn .4s ease both; }
.frow.ghosted b { font-style: italic; color: #3E5A52; background: rgba(29,158,117,.06); border-radius: 4px; padding: 1px 6px; }
.fields .ga { display: flex; gap: 6px; margin-top: 8px; }
.fields .rail-btn { padding: 4px 11px; font-size: 10.5px; cursor: pointer; }

/* focus mode: the question expands inside the page */
.page.focus .q:not(.focused), .page.focus .fields, .page.focus .crumb, .page.focus .sub { display: none; }
.page.focus h3 { font-size: 13px; color: var(--dim); }
.page.focus .q.focused .qh { font-size: 17px; margin-bottom: 14px; }
.page.focus .q.focused .own { display: none; }
.focus-top { display: none; align-items: center; gap: 8px; font-size: 11px; color: var(--dim); margin: 0 0 14px; }
.page.focus .focus-top { display: flex; }
.focus-top .back { display: inline-flex; align-items: center; gap: 4px; color: #0F7355; font-weight: 600; cursor: pointer; }
.focus-top .wc { margin-left: auto; }
.ed-text { outline: none; font-size: 14px; line-height: 1.7; color: #1F2B28; min-height: 300px; }
.ed-text p { margin: 0 0 12px; }
.ed-text .new { background: var(--acc-tint); border-radius: 3px; animation: insIn .4s ease both; }
.focus-foot { display: none; gap: 8px; align-items: center; margin-top: 18px; padding-top: 14px; border-top: 1px solid #E6ECEA; }
.page.focus .focus-foot { display: flex; }
.focus-foot .srcs { margin: 0; flex: 1; }
.focus-foot .rail-btn { cursor: pointer; }
/* the library drawer slides up under the page */
.drawer { position: absolute; left: 0; right: 0; bottom: 0; background: #fff; border-top: 1px solid var(--word-line); box-shadow: 0 -20px 40px -30px rgba(15,26,23,.5); transform: translateY(100%); transition: transform .28s cubic-bezier(.2,.8,.2,1); z-index: 6; }
.drawer.on { transform: none; }
.drawer .dh { display: flex; align-items: center; gap: 10px; padding: 10px 20px; border-bottom: 1px solid #EEF2F0; font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); }
.drawer .dh .lib-s { margin: 0 0 0 auto; width: 240px; }
.drawer .dh .ms.close { font-size: 18px; cursor: pointer; }
.drawer .db { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; padding: 12px 20px 16px; }
.lib-s { font-size: 11px; color: var(--dim); background: #F7FAF8; border: 1px solid #DCE5E1; border-radius: 8px; padding: 6px 9px; display: flex; gap: 6px; align-items: center; }
.lib-s .ms { font-size: 15px; }
.lib-i { background: #fff; border: 1px solid #E6ECEA; border-radius: 9px; padding: 8px 10px; font-size: 11px; cursor: pointer; transition: border-color .15s, transform .15s; }
.lib-i:hover { border-color: #1D9E75; transform: translateY(-1px); }
.lib-i b { display: block; font-weight: 600; color: #1F2B28; margin-bottom: 2px; }
.lib-i small { color: var(--dim); display: block; line-height: 1.35; }
.lib-i em { font-style: normal; font-size: 9.5px; color: #0F7355; background: #E4F1EC; border-radius: 4px; padding: 1px 5px; margin-top: 5px; display: inline-block; }
.drawer-tab { position: absolute; left: 50%; bottom: 74px; transform: translateX(-50%); display: none; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 600; color: #0F7355; background: #fff; border: 1px solid #BFE0D2; border-radius: 999px; padding: 6px 12px; cursor: pointer; z-index: 5; box-shadow: 0 10px 24px -14px rgba(15,26,23,.5); }
.drawer-tab.on { display: inline-flex; }
.drawer-tab .ms { font-size: 16px; }

/* floating composer pill over the document */
.ask { position: absolute; left: 50%; bottom: 18px; transform: translateX(-50%); width: min(560px, 92%); z-index: 5; display: flex; align-items: center; gap: 8px; background: #fff; border: 1px solid #DCE5E1; border-radius: 999px; padding: 8px 8px 8px 12px; box-shadow: 0 18px 40px -18px rgba(15,26,23,.45); font-size: 12px; color: #6B7975; }
.ask img { width: 18px; height: 15px; }
.ask .rp-input { flex: 1; min-height: 1.2em; color: #1F2B28; outline: none; }
.ask .rp-input:empty::before { content: attr(data-ph); color: #6B7975; }
.ask .rp-send { width: 24px; height: 24px; cursor: pointer; }
.ask .rp-send::after { left: 9px; top: 7px; }
.ask .chips { display: flex; gap: 4px; }
.ask .chips b { font-weight: 500; font-size: 9.5px; color: #33423E; background: #EEF2F0; border-radius: 999px; padding: 3px 8px; white-space: nowrap; }
/* Ray's reply appears as a toast card above the pill */
.reply { position: absolute; left: 50%; bottom: 70px; transform: translateX(-50%); width: min(560px, 92%); z-index: 5; background: #fff; border: 1px solid rgba(29,158,117,.45); border-radius: 12px; padding: 10px 12px; font-size: 11.5px; color: #1F2B28; box-shadow: 0 18px 40px -18px rgba(15,26,23,.45); display: none; animation: insIn .3s ease both; }
.reply.on { display: block; }
.reply .rp-ray { margin-bottom: 4px; }
.reply .rh-s { display: flex; gap: 5px; align-items: center; font-size: 11px; color: #6B7975; cursor: pointer; margin-bottom: 4px; }
.reply .rail-work { margin-bottom: 6px; }
.reply .rail-work.folded { display: none; }
.reply p { margin: 0; line-height: 1.4; }
.reply p b { color: #0F7355; }
.reply .acts { margin-top: 8px; }
.reply .rail-btn { cursor: pointer; }
.reply .x { position: absolute; right: 8px; top: 8px; font-size: 16px; color: #9AA8A3; cursor: pointer; }
.toast { position: fixed; left: 50%; bottom: 28px; transform: translate(-50%, 20px); background: #1F2B28; color: #fff; font-size: 12.5px; padding: 9px 14px; border-radius: 999px; opacity: 0; transition: opacity .25s, transform .25s; pointer-events: none; z-index: 9; }
.toast.on { opacity: 1; transform: translate(-50%, 0); }
.ins { animation: insIn .5s ease both; }
@keyframes insIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.qtag, .outline-rail { display: none; }
.page.mapped .qtag, .page.mapped .outline-rail { display: block; }
.slot { cursor: pointer; }
@media (max-width: 900px) { .sheetwrap { grid-template-columns: 1fr; } .margin { display: none; } .page { padding: 28px 22px 60px 50px; } .own { left: -36px; } .drawer .db { grid-template-columns: 1fr 1fr; } .steps { overflow-x: auto; } }
"""

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ray for Word · B</title>
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
  <span class="eyebrow">RayAI expansion · Word add-in · version B — document-native</span>
  <h1>Ray, <em>in the page, not beside it.</em></h1>
  <p>The alternate take on the 25 Sep scrum. No side pane: Ray is a <b>workflow bar</b> across the top of the document, drafts arrive as <b>ghost text inside each answer</b> you accept in place (Tab, Tab, Tab), a question <b>expands within the page</b> with the response library as a bottom drawer, owners sit in the <b>gutter</b>, and activity lives in <b>Word-style margin balloons</b>. Same tokens, same rows, same buttons as version A.</p>
</header>

<div class="guide" id="guide">
  <span class="lbl">Try</span>
  <span class="g" data-g="autofill" data-do="autofill"><i></i>Autofill (ghost → accept)</span>
  <span class="g" data-g="draft" data-do="draft"><i></i>Draft all · accept, accept, accept</span>
  <span class="g" data-g="focus" data-do="focuscur"><i></i>Expand a question in-page</span>
  <span class="g" data-g="assign" data-do="assignhint"><i></i>Owners in the gutter</span>
  <span class="g" data-g="map" data-do="map"><i></i>Map the document (XML)</span>
  <span class="g" data-g="activity" data-do="activity"><i></i>Margin activity</span>
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
      <div class="rb" data-do="autofill"><span class="ms">auto_fix_high</span><b>Autofill<br>fields</b></div>
      <div class="rb" data-do="draft"><span class="ms">auto_awesome</span><b>Draft all<br>open answers</b></div>
      <div class="rb" data-do="acceptnext"><span class="ms">keyboard_tab</span><b>Accept<br>next</b></div>
      <div class="rb" data-do="focuscur"><span class="ms">open_in_full</span><b>Expand<br>question</b></div>
    </div><div class="lbl">Answers</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">
      <div class="rb" data-do="assignhint"><span class="ms">assignment_ind</span><b>Assign<br>owners</b></div>
      <div class="rb" data-do="sync"><span class="ms">sync</span><b>Sync<br>SharePoint</b></div>
      <div class="rb" data-do="review"><span class="ms">fact_check</span><b>Check<br>criteria</b></div>
    </div><div class="lbl">Team</div></div>
  </div>
  <div class="raybar">
    <span class="who"><img src="{RAY}" alt="">Ray <em>Beta</em></span>
    <div class="steps" id="steps"></div>
    <div class="team"><span class="presence" id="teamav"></span><span class="bell" data-do="activity"><span class="ms">notifications</span><b id="bell"></b></span></div>
  </div>
  <div class="body">
    <div class="canvas" id="canvas"><div class="sheetwrap">
      <div class="page" id="page">
        <div class="focus-top" id="focustop"></div>
        <div class="crumb">Schedule 3 · Returnable schedules</div>
        <h3>Section 3 — Methodology</h3>
        <p class="sub">Responses to the Principal’s evaluation criteria · Northside School Upgrade · RFT 2026-114</p>
        <i class="outline-rail"></i>
        <div id="fields"></div>
        <div id="qs"></div>
      </div>
      <div class="margin" id="margin"></div>
    </div></div>
    <span class="drawer-tab" id="drawertab" data-do="drawer"><span class="ms">library_books</span>Response library</span>
    <div class="drawer" id="drawer"></div>
    <div class="reply" id="reply"></div>
    <div class="ask" id="ask"><img src="{RAY}" alt=""><span class="rp-input" id="input" contenteditable="true" data-ph="Ask Ray about this document…"></span><span class="chips" id="askchips"></span><i class="rp-send" id="send"></i></div>
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
const ghosts = () => S.qs.filter(x => !x.a && S.ghost[x.id]);
const sleep = ms => new Promise(r => setTimeout(r, ms));
function toast(m) {{ const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('on'), 2200); }}
function mark(g) {{ S.guide[g] = true; document.querySelectorAll('.guide .g').forEach(el => el.classList.toggle('done', !!S.guide[el.dataset.g])); }}
function fresh() {{
  S = {{ qs: Q0(), cur: '3.2', ghost: {{}}, fieldsGhost: false, mapped: false, focus: null, drawer: false,
        fields: [ ['Tenderer name', 'Northside Constructions Pty Ltd'], ['ABN', '61 204 118 337'], ['Registered address', '14 Grove Street, Northside VIC 3070'],
                  ['Public liability insurance', '$20M · QBE · expires 30 Jun 2027'], ['Workers compensation', 'WorkSafe VIC · policy 88-1120-4'], ['Quality system', 'ISO 9001:2015 · cert. 2025-1183'] ].map(([k,v]) => ({{ k, v, filled: false }})),
        assigned: {{ '3.4': ['MW','Daniel','due Friday'] }}, editing: {{ '3.1':'MW' }}, comments: {{ '3.5':'TB' }}, unread: 3, busy: false, guide: {{}},
        balloons: [] }};
  S.balloons = [
    {{ id:'b1', kind:'live', who:'MW', q:'3.1', text:'is editing this answer — rewrote the gate sequence.', when:'now' }},
    {{ id:'b2', kind:'warm', who:'DD', q:'3.4', text:'assigned this question to you · due Friday.', when:'2 h', acts:[['draft','Draft it'],['focus','Open']] }},
    {{ id:'b3', kind:'', who:'TB', q:'3.5', text:'“Add the noise monitoring clause?”', when:'1 h', acts:[['review','Check criteria']] }},
  ];
  $('#reply').className = 'reply'; $('#drawer').className = 'drawer'; $('#drawertab').className = 'drawer-tab';
  renderAll();
}}
function renderAll() {{ renderSteps(); renderFields(); renderDoc(); renderMargin(); renderTeam(); renderChips(); }}
function renderSteps() {{
  const f = S.fields.filter(x => x.filled).length, e = empties().length, asg = S.qs.filter(x => S.assigned[x.id]).length;
  const s1 = f === 6 ? 'done' : 'on', s2 = e === 0 ? 'done' : (f === 6 ? 'on' : ''), s3 = asg === 5 ? 'done' : '', s4 = S.qs.some(x => x.checked) ? 'done' : '';
  $('#steps').innerHTML = `
    <div class="step ${{s1}}" data-do="autofill"><i>${{s1==='done'?'✓':'1'}}</i>Autofill <small>${{f}}/6</small><span class="bar"><i style="width:${{f/6*100}}%"></i></span></div>
    <div class="step ${{s2}}" data-do="draft"><i>${{s2==='done'?'✓':'2'}}</i>Draft &amp; accept <small>${{5-e}}/5</small><span class="bar"><i style="width:${{(5-e)/5*100}}%"></i></span></div>
    <div class="step ${{s3}}" data-do="assignhint"><i>${{s3==='done'?'✓':'3'}}</i>Owners <small>${{asg}}/5</small></div>
    <div class="step ${{s4}}" data-do="review"><i>${{s4==='done'?'✓':'4'}}</i>Check criteria</div>`;
}}
function renderTeam() {{
  const load = Object.keys(PEOPLE).map(k => Object.values(S.assigned).filter(v => v[0]===k).length);
  $('#teamav').innerHTML = Object.keys(PEOPLE).map((k,i) => `<span class="av ${{PEOPLE[k][1]}}" title="${{PEOPLE[k][0]}} · ${{load[i]}} question${{load[i]===1?'':'s'}}">${{k}}</span>`).join('');
  $('#bell').textContent = S.unread || '';
}}
function renderChips() {{
  const e = empties().length;
  $('#askchips').innerHTML = e ? `<b data-do="draft">Draft ${{e}} open</b><b data-do="map">Map</b>` : `<b data-do="review">Check criteria</b>`;
}}
function renderFields() {{
  const f = S.fields.filter(x => x.filled).length, g = S.fieldsGhost;
  $('#fields').innerHTML = `<div class="fields"><div class="k">Schedule 1 · Tenderer details ${{f === 6 ? `<span class="chip">6 of 6 autofilled by Ray</span>` : g ? `<span class="chip">6 matched from company profile — review</span>` : `<span class="chip warm">6 standard fields empty</span>`}}</div>
    ${{S.fields.map(x => `<div class="frow${{x.filled?' filled':(g?' ghosted':'')}}"><span>${{x.k}}</span>${{x.filled||g ? `<b>${{x.v}}</b>` : '<i class="empty"></i>'}}</div>`).join('')}}
    ${{g && f < 6 ? `<div class="ga"><span class="rail-btn" data-do="acceptfields">Accept all 6</span><span class="rail-btn ghost" data-do="autofill">Re-match</span></div>` : ''}}</div>`;
}}
function renderDoc() {{
  const page = $('#page'); page.classList.toggle('mapped', S.mapped); page.classList.toggle('focus', !!S.focus);
  const nextGhost = ghosts()[0];
  $('#qs').innerHTML = S.qs.map(x => {{
    const own = S.assigned[x.id] ? `<span class="own" data-do="ownpop" data-q="${{x.id}}" title="Owner · ${{PEOPLE[S.assigned[x.id][0]][0]}}">${{AV(S.assigned[x.id][0])}}<span class="pop" id="pop-${{x.id}}"></span></span>` : `<span class="own" data-do="ownpop" data-q="${{x.id}}" title="Assign an owner"><span class="add"><span class="ms">person_add</span></span><span class="pop" id="pop-${{x.id}}"></span></span>`;
    let body;
    if (S.focus === x.id) body = `<div class="ed-text" id="edtext" contenteditable="true">${{(x.a || x.d) ? `<p>${{x.a || x.d}}</p>` : '<p><br></p>'}}</div>
        <div class="focus-foot"><div class="srcs">${{(x.src||[]).map(s => `<b>${{s}}</b>`).join('')}}</div><span class="rail-btn ghost" data-do="drawer">Response library</span><span class="rail-btn" data-do="focusdone">${{x.a ? 'Update answer' : 'Insert answer'}}</span></div>`;
    else if (x.a && x.by === 'ray') body = `<div class="a ins"><span class="tag">Inserted by Ray <small>· from ${{x.src.length}} sources · just now</small></span><p>${{x.a}}</p></div>`;
    else if (x.a) body = `<div class="a${{x.flag?' ins gap':''}}">${{x.flag?`<span class="tag">Gap flagged by Ray <small>· ${{x.gap}}</small></span>`:''}}<p>${{x.a}}</p></div>`;
    else if (S.ghost[x.id]) body = `<div class="ghost"><div class="gh"><img src="${{RAY}}" alt="">Ray’s draft <small>· ${{x.src[0].split(' ·')[0]}}</small>${{nextGhost && nextGhost.id === x.id ? '<span class="kb">Tab · accept</span>' : ''}}</div><p>${{x.d}}</p>
        <div class="ga"><span class="rail-btn" data-do="accept" data-q="${{x.id}}">Accept</span><span class="rail-btn ghost" data-do="focus" data-q="${{x.id}}">Edit</span><span class="rail-btn ghost" data-do="skip" data-q="${{x.id}}">Skip</span></div></div>`;
    else body = `<div class="slot" data-do="ask" data-q="${{x.id}}">${{S.mapped ? 'Answer slot detected · empty' : 'Not answered yet'}} — click to ask Ray</div>`;
    const cls = ['q', S.focus === x.id ? 'focused' : '', nextGhost && nextGhost.id === x.id ? 'next' : ''].join(' ');
    return `<div class="${{cls}}" data-q="${{x.id}}">${{own}}<span class="qtag">Q${{x.id}}</span><div class="qh" data-do="focus" data-q="${{x.id}}"><span class="n">${{x.id}}</span>${{x.t}}</div>${{body}}</div>`;
  }}).join('');
  if (S.focus) {{ const x = q(S.focus); $('#focustop').innerHTML = `<span class="back" data-do="focusdone"><span class="ms" style="font-size:16px">arrow_back</span>Back to Section 3</span><span>Answering ${{x.id}} in place — the page is the editor</span><span class="wc" id="wc"></span>`; const ed = $('#edtext'); ed.addEventListener('input', wc); wc(); setTimeout(() => ed.focus(), 40); $('#drawertab').classList.add('on'); }}
  else {{ $('#drawertab').classList.remove('on'); $('#drawer').classList.remove('on'); }}
}}
function wc() {{ const t = ($('#edtext')?.innerText || '').trim(); const n = t ? t.split(/\\s+/).length : 0; const el = $('#wc'); if (el) el.textContent = `${{n}} words · ~${{Math.max(1, Math.round(n/300))}} page${{n>300?'s':''}}`; }}
function renderMargin() {{
  const bs = S.balloons.map(b => `<div class="balloon ${{b.kind}}"><div class="h">${{b.who==='RAY' ? `<img class="ray" src="${{RAY}}" alt="">Ray` : `${{AV(b.who)}}${{PEOPLE[b.who][0]}}`}}<small>${{b.when}}</small></div>
      <p><span class="qref">${{b.q}}</span> ${{b.text}}</p>${{b.acts ? `<div class="acts">${{b.acts.map(a => `<span class="rail-btn ${{a[0]==='focus'||a[0]==='review'?'ghost':''}}" data-do="${{a[0]}}" data-q="${{b.q}}">${{a[1]}}</span>`).join('')}}</div>` : ''}}</div>`).join('');
  $('#margin').innerHTML = `<div class="k">Activity · SharePoint</div>${{bs || '<p class="mute">Nothing new since you were last here.</p>'}}`;
}}
// ---------- Ray's reply card ----------
async function think(steps, secs, html) {{
  const r = $('#reply'); r.className = 'reply on';
  r.innerHTML = `<span class="ms x" data-do="replyclose">close</span><div class="rp-ray"><img src="${{RAY}}" alt=""><span>Ray</span></div><div class="rh-s"><i class="chev"></i><span class="lbl">Working…</span></div><div class="rail-work"></div>`;
  const work = r.querySelector('.rail-work');
  for (const [code, note] of steps) {{ work.insertAdjacentHTML('beforeend', `<div class="work live"><i></i><code>${{code}}</code><span>${{note}}</span></div>`); await sleep(380); work.lastElementChild.classList.replace('live', 'done'); }}
  const h = r.querySelector('.rh-s'); h.querySelector('.lbl').textContent = `Thought for ${{secs}}s · ${{steps.length}} steps`; work.classList.add('folded');
  h.onclick = () => work.classList.toggle('folded');
  if (html) r.insertAdjacentHTML('beforeend', html);
}}
function replyClose() {{ $('#reply').className = 'reply'; }}
// ---------- flows ----------
async function autofill() {{
  if (S.busy) return; S.busy = true; mark('autofill');
  await think([['read_document_xml','Schedule 1 · 6 standard fields found'],['read_company_profile','Northside Constructions · profile current'],['match_fields','6 / 6 matched · shown in place for review']], '1.2',
    `<p><b>6 fields matched.</b> They’re shown in Schedule 1 as ghost values — accept them there, or re-match. Nothing leaves this document.</p><div class="acts"><span class="rail-btn" data-do="acceptfields">Accept all 6</span></div>`);
  S.fieldsGhost = true; renderFields(); $('#fields').scrollIntoView({{ behavior:'smooth', block:'start' }}); S.busy = false;
}}
async function acceptFields() {{ replyClose(); for (const x of S.fields) {{ x.filled = true; renderFields(); await sleep(140); }} renderSteps(); toast('Schedule 1 filled — phase 2: draft the open answers'); }}
async function draft() {{
  if (S.busy) return; const e = empties(); if (!e.length) {{ toast('Nothing open in Section 3'); return; }}
  S.busy = true; mark('draft');
  const steps = [['read_document_xml','Schedule 3 · 14 questions found'],['outline_document',`${{e.length}} open answer slots in Section 3`]]; e.forEach(x => steps.push(['search_company_knowledge', `${{x.id}} · ${{x.src[0].split(' ·')[0]}}`])); steps.push(['draft_answers', `${{e.length}} drafts placed in the page as ghost text`]);
  await think(steps, '3.1', `<p><b>${{e.length}} drafts are in the page.</b> Each sits in its own slot as ghost text — <b>Tab</b> accepts the highlighted one and moves on. Accept, accept, accept.</p><div class="acts"><span class="rail-btn" data-do="acceptnext">Accept next</span><span class="rail-btn ghost" data-do="acceptall">Accept all</span></div>`);
  e.forEach(x => S.ghost[x.id] = true); renderDoc(); const first = $('.q.next'); first && first.scrollIntoView({{ behavior:'smooth', block:'center' }}); S.busy = false;
}}
function accept(qid) {{
  const x = q(qid); if (!x || x.a) return; x.a = x.d; x.by = 'ray'; delete S.ghost[x.id];
  renderDoc(); renderSteps(); renderChips();
  $('#savestate').textContent = 'Saving…'; setTimeout(() => $('#savestate').textContent = 'Saved to SharePoint', 900);
  const n = ghosts()[0]; if (n) {{ const el = document.querySelector(`.q[data-q="${{n.id}}"]`); el && el.scrollIntoView({{ behavior:'smooth', block:'center' }}); toast(`${{x.id}} accepted · Tab for ${{n.id}}`); }} else {{ toast(`${{x.id}} accepted${{empties().length ? '' : ' · Section 3 complete'}}`); if (!empties().length) replyClose(); }}
}}
function acceptNext() {{ const n = ghosts()[0]; if (n) accept(n.id); else if (empties().length) draft(); else toast('Section 3 is complete'); }}
async function acceptAll() {{ for (const g of ghosts()) {{ accept(g.id); await sleep(500); }} }}
function skip(qid) {{ delete S.ghost[qid]; renderDoc(); toast(`${{qid}} skipped — still open`); }}
function focus(qid) {{ const x = q(qid || S.cur); if (!x) return; S.cur = x.id; S.focus = x.id; delete S.ghost[x.id]; mark('focus'); replyClose(); renderDoc(); $('#canvas').scrollTo({{ top: 0 }}); }}
function focusDone(save) {{ const x = q(S.focus); const t = ($('#edtext')?.innerText || '').trim(); if (save !== false && t && t !== (x.a || x.d)) {{ x.d = t; if (x.a) {{ x.a = t; x.by = 'ray'; }} }} if (save === 'insert' && !x.a && t) {{ x.d = t; x.a = t; x.by = 'ray'; }} S.focus = null; S.drawer = false; renderDoc(); renderSteps(); renderChips(); }}
function drawer() {{ const d = $('#drawer'); const on = !d.classList.contains('on'); d.classList.toggle('on', on); if (on) d.innerHTML = `<div class="dh"><span class="ms">library_books</span>Response library <span class="lib-s"><span class="ms">search</span>Search 1,240 assets…</span><span class="ms close" data-do="drawer">close</span></div><div class="db">${{LIB.map((l,i) => `<div class="lib-i" data-do="libins" data-i="${{i}}"><b>${{l[0]}}</b><small>${{l[1]}}</small><em>${{l[2]}}</em></div>`).join('')}}</div>`; }}
function libInsert(i) {{ const ed = $('#edtext'); if (!ed) return; ed.insertAdjacentHTML('beforeend', `<p class="new">${{LIB[i][3]}}</p>`); wc(); toast(`Added from ${{LIB[i][0].split(' ·')[0]}}`); }}
function ownPop(qid) {{ document.querySelectorAll('.pop.on').forEach(p => p.classList.remove('on')); const p = document.getElementById('pop-' + qid); p.innerHTML = Object.keys(PEOPLE).map(k => `<span class="p" data-do="own" data-q="${{qid}}" data-who="${{k}}">${{AV(k)}}${{PEOPLE[k][0]}}</span>`).join('') + (S.assigned[qid] ? `<span class="p" data-do="unown" data-q="${{qid}}">Clear</span>` : ''); p.classList.add('on'); mark('assign'); }}
function own(qid, who) {{ S.assigned[qid] = [who, 'you', 'due Fri']; if (who === 'DD') {{ S.unread += 1; S.balloons.unshift({{ id:'b'+Date.now(), kind:'warm', who:'DD', q:qid, text:'assigned to you · due Friday.', when:'now', acts:[['draft','Draft it']] }}); }} renderAll(); toast(`${{qid}} → ${{PEOPLE[who][0]}}`); }}
function unown(qid) {{ delete S.assigned[qid]; renderAll(); }}
function assignHint() {{ mark('assign'); const open = S.qs.find(x => !S.assigned[x.id]); if (open) {{ const el = document.querySelector(`.q[data-q="${{open.id}}"]`); el && el.scrollIntoView({{ behavior:'smooth', block:'center' }}); setTimeout(() => ownPop(open.id), 400); }} else toast('Every question has an owner'); }}
async function map() {{
  if (S.busy) return; S.busy = true; mark('map');
  await think([['open_document_xml','word/document.xml · 48 KB · no bookmarks needed'],['outline_document',`5 sections · 14 questions · ${{empties().length}} empty answer slots`],['map_answer_slots','14 / 14 matched by heading + numbering'],['validate_structure','styles, tables, numbering untouched']], '2.1',
    `<p><b>Document map ready.</b> Ray reads and writes the document’s own XML, so answers land inside the real paragraphs. No bookmarks, no Syncfusion, nothing rewritten around them.</p><div class="srcs"><b>XML-native</b><b>No bookmarks</b><b>No corruption risk</b></div>`);
  S.mapped = true; renderDoc(); S.busy = false;
}}
function activity() {{ mark('activity'); S.unread = 0; renderTeam(); $('#margin').scrollIntoView({{ behavior:'smooth', block:'start' }}); const first = $('.balloon'); if (first) {{ first.style.boxShadow = '0 0 0 3px rgba(29,158,117,.25)'; setTimeout(() => first.style.boxShadow = '', 1200); }} }}
async function sync() {{ $('#savestate').textContent = 'Syncing…'; await sleep(700); const t = S.qs.find(x => x.a && x.id !== '3.1') || q('3.1'); S.editing = {{}}; S.editing[t.id] = 'TB'; S.unread += 1; if (!$('#presence .a3')) $('#presence').insertAdjacentHTML('beforeend', AV('TB')); S.balloons.unshift({{ id:'b'+Date.now(), kind:'live', who:'TB', q:t.id, text:'opened the document and is editing this answer.', when:'now' }}); $('#savestate').textContent = 'Saved to SharePoint'; renderMargin(); renderTeam(); toast('Change arrived from SharePoint'); }}
async function review() {{
  if (S.busy) return; S.busy = true; const answered = S.qs.filter(x => x.a);
  await think([['read_criteria','criteria 3(a)–3(e) · weights loaded'], ...answered.map(x => ['check_answer', `${{x.id}} · ${{x.id==='3.5' ? 'gap: noise monitoring' : 'meets criterion'}}`])], '2.6',
    `<p><b>${{answered.length}} answers checked · 1 gap.</b> 3.5 has controls but no monitoring — criterion 3(e) scores “monitoring and response”. Tom’s comment asks for the same thing.</p><div class="acts"><span class="rail-btn" data-do="fixgap">Add monitoring clause</span></div>`);
  S.qs.forEach(x => x.checked = !!x.a); const g = q('3.5'); g.flag = true; renderDoc(); renderSteps(); document.querySelector('.q[data-q="3.5"]').scrollIntoView({{ behavior:'smooth', block:'center' }}); S.busy = false;
}}
function fixGap() {{ const g = q('3.5'); if (!g.flag) return; g.a += ' Noise will be monitored at the school boundary with a logging meter; readings above the EPA limit stop the work until the source is controlled.'; g.flag = false; g.by = 'ray'; g.src = ['Noise management procedure','Northside RFT · criterion 3(e)']; S.balloons = S.balloons.filter(b => b.q !== '3.5'); S.balloons.unshift({{ id:'b'+Date.now(), kind:'ray', who:'RAY', q:'3.5', text:'monitoring clause added — Tom’s comment resolved.', when:'now' }}); replyClose(); renderAll(); toast('3.5 updated · comment resolved'); }}
async function ask(qid) {{
  if (S.busy) return; S.busy = true; const x = q(qid || S.cur); S.cur = x.id;
  await think([['read_question', `${{x.id}} · ${{x.short.toLowerCase()}}`],['search_company_knowledge', `3 matches · ${{x.src[0].split(' ·')[0]}} strongest`],['draft_answer', `${{x.d.split(' ').length}} words · aligned to criterion`]], '1.4',
    `<p><b>${{x.why}}</b> The draft is in the page under ${{x.id}} — accept it there, edit it in place, or skip.</p>`);
  S.ghost[x.id] = true; renderDoc(); document.querySelector(`.q[data-q="${{x.id}}"]`).scrollIntoView({{ behavior:'smooth', block:'center' }}); S.busy = false;
}}
async function typed(text) {{
  const t = text.trim().toLowerCase(); if (!t) return;
  if (/autofill|abn|standard fields|company profile/.test(t)) return autofill();
  if (/map|parse|structure|xml/.test(t)) return map();
  if (/assign|owner/.test(t)) return assignHint();
  if (/expand|full|focus|open/.test(t)) return focus(S.cur);
  if (/changed|since|activity|comment/.test(t)) return activity();
  if (/rest|all|section|open|draft/.test(t)) return draft();
  if (/check|criteria|review|gap/.test(t)) return review();
  const m = t.match(/3\\.[1-5]/); if (m) S.cur = m[0]; else {{ const e = empties()[0]; if (e) S.cur = e.id; }}
  return ask(S.cur);
}}
document.addEventListener('click', e => {{
  const el = e.target.closest('[data-do]');
  if (!e.target.closest('.own')) document.querySelectorAll('.pop.on').forEach(p => p.classList.remove('on'));
  if (!el) return; const d = el.dataset.do, qid = el.dataset.q;
  ({{ autofill, acceptfields: acceptFields, draft, accept: () => accept(qid), acceptnext: acceptNext, acceptall: acceptAll, skip: () => skip(qid),
     focus: () => focus(qid), focuscur: () => focus(S.cur), focusdone: () => focusDone(el.classList.contains('rail-btn') ? 'insert' : true), drawer, libins: () => libInsert(+el.dataset.i),
     ownpop: () => ownPop(qid), own: () => own(qid, el.dataset.who), unown: () => unown(qid), assignhint: assignHint,
     map, activity, sync, review, fixgap: fixGap, ask: () => ask(qid), replyclose: replyClose }})[d]?.();
}});
document.addEventListener('keydown', e => {{
  if (e.key === 'Tab' && !S.focus && ghosts().length) {{ e.preventDefault(); acceptNext(); }}
  if (e.key === 'Escape') {{ if (S.focus) focusDone(true); replyClose(); }}
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
