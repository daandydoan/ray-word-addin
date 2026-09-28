import base64, pathlib

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT = pathlib.Path(__file__).resolve().parent / "ray-word-addin-mock.html"

def data_uri(name):
    b = (ASSETS / name).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(b).decode()

RAY = data_uri("ray-avatar.svg")
WORDMARK = data_uri("tenderfy-wordmark.svg")

CSS = r"""
:root {
  --ground: #F4F1EC; --ink: #14211D; --ink-2: #33423E; --dim: #6B7975; --line: #E6ECEA;
  --acc: #1D9E75; --acc-deep: #0F7355; --acc-tint: rgba(29,158,117,.08); --amber: #F2C46D;
  --word-chrome: #F3F2F1; --word-line: #E1DFDD; --word-blue: #185ABD;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--ground); }
body { font-family: 'Outfit', system-ui, -apple-system, sans-serif; color: var(--ink); padding: 48px 24px 120px; }
.head { max-width: 1180px; margin: 0 auto 40px; }
.head .eyebrow { display: inline-flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--acc-deep); background: #E4F1EC; border-radius: 999px; padding: 6px 12px; }
.head .eyebrow::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--acc); }
.head h1 { font-size: 34px; font-weight: 700; letter-spacing: -.02em; margin: 14px 0 8px; font-style: italic; }
.head h1 em { font-style: italic; color: var(--acc-deep); }
.head p { font-size: 15px; line-height: 1.55; color: #4A5754; margin: 0; max-width: 68ch; }
.head p b { color: var(--ink); }

.frame { max-width: 1180px; margin: 0 auto 64px; }
.frame-head { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
.frame-head .num { font-family: ui-monospace, Menlo, monospace; font-size: 11px; font-weight: 700; letter-spacing: .08em; color: var(--acc); text-transform: uppercase; }
.frame-head h2 { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: -.01em; font-style: italic; }
.frame-head .brief { width: 100%; font-size: 13.5px; line-height: 1.5; color: #4A5754; margin: 2px 0 0; max-width: 80ch; }
.frame-head .brief b { color: var(--ink); font-weight: 600; }

/* ===== the Word window ===== */
.win { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 30px 70px -30px rgba(15,26,23,.35), 0 0 0 1px rgba(15,26,23,.06); }
.titlebar { display: flex; align-items: center; gap: 14px; padding: 9px 14px; background: var(--word-chrome); border-bottom: 1px solid var(--word-line); font-size: 12px; color: #323130; }
.lights { display: flex; gap: 6px; }
.lights i { width: 11px; height: 11px; border-radius: 50%; background: #E1DFDD; }
.lights i:nth-child(1) { background: #FF5F57; } .lights i:nth-child(2) { background: #FEBC2E; } .lights i:nth-child(3) { background: #28C840; }
.docname { display: flex; align-items: center; gap: 8px; margin: 0 auto; font-weight: 500; }
.docname .ms { font-size: 16px; color: var(--word-blue); }
.docname small { color: #605E5C; font-weight: 400; }
.docname small::before { content: '·'; margin: 0 6px; }
.presence { display: flex; align-items: center; }
.av { width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font-size: 9.5px; font-weight: 700; color: #fff; border: 2px solid #fff; margin-left: -6px; }
.av.a1 { background: #38988A; } .av.a2 { background: #5C6BC0; } .av.a3 { background: #EF6C00; } .av.a4 { background: #6D4C41; }
.presence .av:first-child { margin-left: 0; }
.tabs { display: flex; align-items: center; gap: 2px; padding: 4px 12px 0; background: var(--word-chrome); font-size: 12.5px; color: #323130; }
.tabs span { padding: 7px 10px 8px; border-radius: 6px 6px 0 0; }
.tabs span.on { background: #fff; color: var(--acc-deep); font-weight: 600; box-shadow: inset 0 -2px 0 var(--acc); position: relative; }
.tabs span.on .dot { position: absolute; top: 6px; right: 4px; width: 7px; height: 7px; border-radius: 50%; background: #D93B3B; border: 1.5px solid #fff; }
.ribbon { display: flex; align-items: stretch; gap: 4px; padding: 8px 12px; border-bottom: 1px solid var(--word-line); background: #fff; }
.rb { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; min-width: 62px; padding: 6px 8px; border-radius: 6px; font-size: 10.5px; color: #323130; }
.rb .ms { font-size: 22px; color: var(--acc-deep); }
.rb.pri { background: var(--acc-tint); }
.rb b { font-weight: 500; }
.rb-sep { width: 1px; background: var(--word-line); margin: 2px 6px; }
.rb-group { display: flex; flex-direction: column; justify-content: flex-end; }
.rb-group .lbl { font-size: 9.5px; color: #8A8886; text-align: center; margin-top: 2px; }
.rb-group .row { display: flex; }
.body { display: grid; grid-template-columns: minmax(0, 1fr) 340px; background: #E9E9E7; }
.canvas { padding: 26px 28px 34px; overflow: hidden; }
.page { background: #fff; width: min(680px, 100%); margin: 0 auto; padding: 48px 56px 40px; box-shadow: 0 2px 10px rgba(0,0,0,.08); font-family: 'Outfit', system-ui, sans-serif; color: #1F2B28; min-height: 560px; position: relative; }
.page .crumb { font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-bottom: 8px; }
.page h3 { font-size: 20px; margin: 0 0 4px; letter-spacing: -.01em; }
.page .sub { font-size: 12.5px; color: var(--dim); margin: 0 0 22px; }
.q { position: relative; margin: 0 0 18px; padding-left: 0; }
.q .qh { display: flex; align-items: baseline; gap: 10px; font-size: 13px; font-weight: 600; margin-bottom: 6px; }
.q .qh .n { font-family: ui-monospace, Menlo, monospace; font-size: 11px; color: var(--acc-deep); background: #E4F1EC; border-radius: 4px; padding: 2px 6px; }
.q .a { font-size: 12.5px; line-height: 1.55; color: #33423E; }
.q .a p { margin: 0 0 6px; }
.ln { display: block; height: 7px; border-radius: 4px; background: rgba(15,26,23,.09); margin: 0 0 7px; }
.ln.w90 { width: 90%; } .ln.w70 { width: 70%; } .ln.w80 { width: 80%; } .ln.w50 { width: 50%; } .ln.w60 { width: 60%; }
.ins { background: var(--acc-tint); border-left: 3px solid var(--acc); border-radius: 0 8px 8px 0; padding: 8px 10px; }
.ins .tag { display: inline-flex; align-items: center; gap: 5px; font-size: 10px; font-weight: 600; color: var(--acc-deep); margin-bottom: 4px; }
.ins .tag::before { content: ''; width: 12px; height: 10px; background: url("__RAY__") center / contain no-repeat; }
.ins .tag small { font-weight: 500; color: var(--dim); }
.slot { border: 1.5px dashed #C9D4D0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: var(--dim); display: flex; align-items: center; gap: 8px; min-height: 40px; }
.slot.target { border-color: var(--acc); background: var(--acc-tint); color: var(--acc-deep); }
.caret { display: inline-block; width: 1.5px; height: 14px; background: #1F2B28; animation: caret 1s steps(2) infinite; vertical-align: -3px; }
@keyframes caret { 50% { opacity: 0; } }
.chip { display: inline-flex; align-items: center; gap: 5px; font-size: 10px; font-weight: 600; border-radius: 999px; padding: 3px 8px; background: #EEF2F0; color: var(--ink-2); }
.chip .av { width: 14px; height: 14px; font-size: 7px; border: 0; margin: 0; }
.chip.warm { background: #FFF3DF; color: #7A4B00; }
.chip.live { background: #E6F0FF; color: #1C4B9B; }
.chip.live::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: #2F78C2; animation: pulse 1.4s ease-in-out infinite; }
@keyframes pulse { 50% { opacity: .3; } }
/* presence / assignment / comment chips sit between the question and its answer,
   inside the page — hanging them off the page edge clipped them */
.q { display: flex; flex-direction: column; }
.q .qh { order: 0; }
.q .side { order: 1; align-self: flex-start; margin: -2px 0 7px; white-space: nowrap; }
.q .a, .q .slot { order: 2; }
.qtag { position: absolute; left: -46px; top: 2px; font-family: ui-monospace, Menlo, monospace; font-size: 9.5px; font-weight: 700; color: var(--acc-deep); background: #E4F1EC; border: 1px solid #BFE0D2; border-radius: 4px; padding: 2px 5px; }
.outline-rail { position: absolute; left: 14px; top: 48px; bottom: 40px; width: 2px; background: linear-gradient(to bottom, var(--acc), rgba(29,158,117,.15)); border-radius: 1px; }
.page.mapped { padding-left: 84px; }

/* ===== the task pane (Office chrome) + the Ray panel inside it ===== */
.pane { background: #fff; border-left: 1px solid var(--word-line); display: flex; flex-direction: column; min-height: 0; }
.pane-head { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--word-line); font-size: 12px; font-weight: 600; color: #323130; background: var(--word-chrome); }
.pane-head img { height: 14px; }
.pane-head .ms { font-size: 18px; color: #605E5C; margin-left: auto; }
.pane-head .bell { position: relative; margin-left: auto; }
.pane-head .bell .ms { margin: 0; }
.pane-head .bell b { position: absolute; top: -5px; right: -7px; min-width: 15px; height: 15px; border-radius: 999px; background: #D93B3B; color: #fff; font-size: 9px; font-weight: 700; display: grid; place-items: center; padding: 0 4px; border: 1.5px solid #fff; }
.pane-head .bell + .ms { margin-left: 0; }

/* the Ray panel — the film's light tokens, verbatim */
.raypanel { display: flex; flex-direction: column; flex: 1; min-height: 0; background: #fff; color: #33423E; --acc: #1D9E75; --dim: #6B7975; --ink-2: #33423E; --line: #E6ECEA; font-size: 12px; }
.rp-head { display: flex; align-items: center; gap: 8px; padding: 10px 12px; border-bottom: 1px solid #EEF2F0; font-size: 12px; font-weight: 600; color: #1F2B28; }
.rp-back { width: 7px; height: 7px; border-left: 1.5px solid #6B7975; border-bottom: 1.5px solid #6B7975; transform: rotate(45deg); margin-right: 4px; }
.rp-title { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rp-beta { font-style: normal; font-size: 8.5px; font-weight: 700; letter-spacing: .12em; background: #F2C46D; color: #2B2B2B; border-radius: 3px; padding: 2px 5px; text-transform: uppercase; }
.rp-dots { width: 14px; height: 3px; background: radial-gradient(circle, #6B7975 1px, transparent 1.4px) 0 0 / 5px 3px; }
.rail-body { padding: 12px 14px 10px; display: flex; flex-direction: column; gap: 9px; flex: 1; min-height: 0; }
.rail-you { align-self: flex-end; max-width: 92%; font-size: 11px; line-height: 1.35; color: #1F2B28; background: #E9EFEC; border-radius: 9px 9px 2px 9px; padding: 6px 9px; }
.rp-ray { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #6B7975; }
.rp-ray img { width: 16px; height: 14px; }
.rh-s { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #6B7975; margin: -2px 0 0; }
.rh-s .chev { width: 6px; height: 6px; border-top: 1.5px solid #6B7975; border-right: 1.5px solid #6B7975; transform: rotate(45deg); }
.rh-s.open .chev { transform: rotate(135deg); margin-top: -3px; }
.rail-work { display: flex; flex-direction: column; gap: 5px; }
.rail-work.folded { display: none; }
.work { display: grid; grid-template-columns: 12px auto minmax(0, 1fr); align-items: center; gap: 7px; font-size: 11px; line-height: 1.25; color: #4A5754; }
.work i { width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid #C9D4D0; position: relative; }
.work.done { color: #6B7975; }
.work.done i { background: #1D9E75; border-color: #1D9E75; }
.work.done i::after { content: ''; position: absolute; left: 2.5px; top: 1px; width: 3px; height: 5px; border: solid #fff; border-width: 0 1.5px 1.5px 0; transform: rotate(45deg); }
.work.live i { border-color: #1D9E75; animation: v4pulse 1.1s ease-in-out infinite; }
@keyframes v4pulse { 50% { box-shadow: 0 0 0 3px rgba(29,158,117,.18); } }
.work code { font-family: ui-monospace, Menlo, monospace; font-size: 10.5px; color: #1F2B28; }
.work span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rail-offer { border: 1px solid #DCE5E1; border-radius: 9px; padding: 9px 10px; }
.rail-offer p { margin: 0; font-size: 11.5px; line-height: 1.35; color: #1F2B28; }
.rail-offer p b { color: #0F7355; }
.rail-offer.ask { border-color: rgba(29,158,117,.5); background: rgba(29,158,117,.06); }
.rail-offer.status { border-color: #DCE5E1; background: #F7FAF8; }
.acts { display: flex; gap: 7px; margin-top: 9px; flex-wrap: wrap; }
.rail-btn { border-radius: 999px; padding: 5px 12px; font-size: 11.5px; font-weight: 600; background: #1D9E75; color: #fff; white-space: nowrap; }
.rail-btn.ghost { background: #fff; color: #33423E; border: 1px solid #D7DEDB; }
.rail-btn.next { animation: pressGo 2.2s ease-in-out 1.1s infinite; }
@keyframes pressGo { 0%,100% { box-shadow: 0 0 0 0 rgba(29,158,117,.35); } 40% { box-shadow: 0 0 0 6px rgba(29,158,117,0); } }
.srcs { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
.srcs b { font-weight: 500; font-size: 9.5px; color: #33423E; background: #EEF2F0; border-radius: 999px; padding: 3px 8px; white-space: nowrap; }
.srcs b::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #1D9E75; margin-right: 5px; vertical-align: 1px; }
.ins-list { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }
.ins-row { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 7px 8px; border: 1px solid #E6ECEA; border-radius: 8px; font-size: 11px; }
.ins-row .n { font-family: ui-monospace, Menlo, monospace; font-size: 10px; font-weight: 700; color: #0F7355; }
.ins-row .t { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #1F2B28; }
.ins-row small { display: block; font-size: 9.5px; color: #6B7975; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ins-row.done { background: #F7FAF8; }
.ins-row.done .st { font-size: 10px; color: #0F7355; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.ins-row.done .st::before { content: ''; width: 10px; height: 10px; border-radius: 50%; background: #1D9E75; }
.ins-row .rail-btn { padding: 4px 10px; font-size: 10.5px; }
.ins-row.queued { opacity: .6; }
.note { font-size: 10.5px; line-height: 1.4; color: #6B7975; padding: 8px 10px; border-radius: 8px; background: #F7FAF8; border: 1px dashed #DCE5E1; }
.note b { color: #33423E; font-weight: 600; }
.assign { border: 1px solid #DCE5E1; border-radius: 9px; overflow: hidden; }
.assign .k { font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; padding: 7px 10px 4px; }
.assign .r { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 8px; padding: 7px 10px; border-top: 1px solid #EEF2F0; font-size: 11px; color: #1F2B28; }
.assign .r .t small { display: block; font-size: 9.5px; color: #6B7975; }
.assign .r .n { font-family: ui-monospace, Menlo, monospace; font-size: 10px; font-weight: 700; color: #0F7355; }
.assign .r .when { font-size: 9.5px; color: #6B7975; white-space: nowrap; }
.rp-next { display: flex; position: relative; align-items: center; gap: 8px; margin-top: 2px; padding: 8px 10px 12px; border: 1px solid #DCE5E1; border-radius: 10px; font-size: 11px; color: #33423E; background: #FBFCFB; }
.rp-arrow { width: 8px; height: 8px; border-top: 1.5px solid #1D9E75; border-right: 1.5px solid #1D9E75; transform: rotate(45deg); flex: none; }
.rp-next .t { flex: 1; min-width: 0; }
.rp-next b { color: #1F2B28; }
.rp-go { background: #1D9E75; color: #fff; border-radius: 999px; padding: 4px 11px; font-size: 11px; font-weight: 600; white-space: nowrap; }
.rp-go.off { background: #E6ECEA; color: #6B7975; }
.rp-meter { position: absolute; left: 10px; right: 10px; bottom: 4px; height: 2px; background: #E6ECEA; border-radius: 1px; overflow: hidden; }
.rp-meter i { display: block; height: 100%; background: #1D9E75; }
.rp-foot { border-top: 1px solid #EEF2F0; padding: 8px 12px 12px; margin-top: auto; }
.rp-ref { display: flex; flex-wrap: wrap; gap: 5px; align-items: center; margin-bottom: 8px; }
.rp-ref span { width: 100%; font-size: 8.5px; letter-spacing: .12em; text-transform: uppercase; color: #6B7975; }
.rp-ref b { font-weight: 500; font-size: 9.5px; color: #33423E; background: #EEF2F0; border-radius: 999px; padding: 3px 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 62%; }
.rp-ref .add { background: transparent; border: 1px dashed #C9D4D0; color: #6B7975; }
.rp-composer { display: flex; align-items: center; gap: 8px; background: #F2F5F4; border-radius: 10px; padding: 8px 10px; font-size: 11px; color: #6B7975; }
.rp-att, .rp-clip { width: 11px; height: 11px; border: 1.5px solid #8A9793; border-radius: 3px; flex: none; }
.rp-input { flex: 1; min-height: 1.2em; color: #1F2B28; }
.rp-input:empty::before { content: attr(data-ph); color: #6B7975; }
.rp-send { width: 20px; height: 20px; border-radius: 50%; background: #1D9E75; position: relative; flex: none; }
.rp-send::after { content: ''; position: absolute; left: 7px; top: 5px; width: 5px; height: 5px; border-top: 1.5px solid #fff; border-left: 1.5px solid #fff; transform: rotate(45deg); }
.ray-empty { display: flex; flex-direction: column; gap: 6px; padding: 6px 0 4px; }
.ray-halo { width: 34px; height: 34px; border-radius: 50%; background: radial-gradient(circle, rgba(29,158,117,.28), rgba(29,158,117,.05) 70%); display: grid; place-items: center; margin-bottom: 6px; }
.ray-halo img { width: 22px; }
.ray-empty h3 { margin: 0; font-size: 14px; color: #1F2B28; }
.ray-empty p { margin: 0 0 6px; font-size: 11.5px; line-height: 1.45; color: #4A5754; }
.ray-starter { background: #F2F5F4; color: #1F2B28; border: 1px solid #E6ECEA; border-radius: 9px; padding: 8px 10px; font-size: 11px; line-height: 1.35; }

/* ===== roadmap strip (from the update — not in-product UI) ===== */
.road { max-width: 1180px; margin: 0 auto; }
.road .lbl { font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-bottom: 12px; }
.road .lbl b { color: var(--ink); }
.road-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; }
.road .rp-next { margin: 0; padding: 12px 12px 16px; background: #fff; }
.road .rp-next .t b { display: block; margin-bottom: 2px; }
.road .rp-next .t small { font-size: 10.5px; color: var(--dim); line-height: 1.35; display: block; }
.road .rp-next.gone { opacity: .55; text-decoration: none; }
.road .rp-next.gone .rp-arrow { border-color: #B8C4C0; }

@media (max-width: 900px) {
  body { padding: 28px 16px 80px; }
  .body { grid-template-columns: 1fr; }
  .pane { border-left: 0; border-top: 1px solid var(--word-line); }
  .canvas { padding: 16px; }
  .page { padding: 28px 22px 26px; min-height: 0; }
  .page.mapped { padding-left: 22px; }
  .qtag { position: static; display: inline-block; margin-bottom: 4px; }
  .outline-rail { display: none; }
  .q .side { position: static; transform: none; display: block; margin-top: 4px; }
  .ribbon { overflow-x: auto; }
  .tabs { overflow-x: auto; }
  .road-grid { grid-template-columns: 1fr; }
}
"""

def av(initials, cls):
    return f'<span class="av {cls}">{initials}</span>'

def titlebar(extra_presence=""):
    return f'''
  <div class="titlebar">
    <span class="lights"><i></i><i></i><i></i></span>
    <span class="docname"><span class="ms">description</span>Northside School Upgrade – Tender Response.docx <small>Saved to SharePoint</small></span>
    <span class="presence">{av("DD","a1")}{av("MW","a2")}{extra_presence}</span>
  </div>'''

def tabs(dot=False):
    d = '<i class="dot"></i>' if dot else ''
    return f'''
  <div class="tabs"><span>Home</span><span>Insert</span><span>Layout</span><span>References</span><span>Review</span><span>View</span><span class="on">Tenderfy Ray{d}</span></div>'''

def ribbon(active="ask"):
    def rb(icon, label, key):
        return f'<div class="rb{" pri" if key == active else ""}"><span class="ms">{icon}</span><b>{label}</b></div>'
    return f'''
  <div class="ribbon">
    <div class="rb-group"><div class="row">{rb("smart_toy","Open Ray","open")}{rb("help","Ask about<br>document","ask")}</div><div class="lbl">Ray</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">{rb("text_select_move_forward_character","Insert<br>at cursor","cursor")}{rb("playlist_add","Insert<br>all answers","all")}</div><div class="lbl">Answers</div></div>
    <div class="rb-sep"></div>
    <div class="rb-group"><div class="row">{rb("assignment_ind","Assign<br>question","assign")}{rb("sync","Sync<br>SharePoint","sync")}{rb("notifications","Activity","activity")}</div><div class="lbl">Team</div></div>
  </div>'''

def pane_head(bell=None):
    b = f'<span class="bell"><span class="ms">notifications</span><b>{bell}</b></span><span class="ms">close</span>' if bell else '<span class="ms">close</span>'
    return f'<div class="pane-head"><img src="{WORDMARK}" alt="Tenderfy"> Ray {b}</div>'

RP_HEAD = '<div class="rp-head"><i class="rp-back"></i><span class="rp-title">Northside School Upgrade</span><em class="rp-beta">Beta</em><i class="rp-dots"></i></div>'
RP_RAY = f'<div class="rp-ray"><img src="{RAY}" alt=""><span>Ray</span></div>'
def foot(refs):
    chips = "".join(f"<b>{r}</b>" for r in refs)
    return f'''<div class="rp-foot"><div class="rp-ref"><span>Reference</span>{chips}<b class="add">+ Add</b></div>
      <div class="rp-composer"><i class="rp-att"></i><span class="rp-input" data-ph="Reply to Ray…"></span><i class="rp-clip"></i><i class="rp-send"></i></div></div>'''

# ---------- document states ----------
Q31_DONE = '''
<div class="q"><div class="qh"><span class="n">3.1</span>Describe your approach to site establishment and hoarding.</div>
  <div class="a"><p>Site establishment will follow our standard three-stage sequence: perimeter hoarding to the Grove Street frontage, temporary services connection, and a single controlled gate on the northern boundary away from the school entrance.</p><i class="ln w70"></i></div></div>'''

Q32_EMPTY_CURSOR = '''
<div class="q"><div class="qh"><span class="n">3.2</span>Describe how you will manage disruption during school drop-off and pick-up.</div>
  <div class="slot target"><span class="caret"></span>Cursor placed here — ready for Ray’s answer</div></div>'''

Q32_INSERTED = '''
<div class="q"><div class="qh"><span class="n">3.2</span>Describe how you will manage disruption during school drop-off and pick-up.</div>
  <div class="a ins"><span class="tag">Inserted by Ray <small>· from 2 sources · 9:42am</small></span>
  <p>No deliveries, concrete pours or crane lifts will be scheduled between 8:00–9:15am and 2:45–3:45pm on school days. A dedicated traffic controller will hold the Grove Street gate closed during these windows, with the site supervisor as the single point of contact for the school office.</p></div></div>'''

Q33_TARGET = '''
<div class="q"><div class="qh"><span class="n">3.3</span>Outline your communication plan with the school and neighbouring residents.</div>
  <div class="slot target"><span class="caret"></span>Next — Ray inserts here on the next click</div></div>'''

Q33_EMPTY = '''
<div class="q"><div class="qh"><span class="n">3.3</span>Outline your communication plan with the school and neighbouring residents.</div>
  <div class="slot">Not answered yet</div></div>'''

Q34_QUEUED = '''
<div class="q"><div class="qh"><span class="n">3.4</span>Detail your traffic management approach for the Grove Street frontage.</div>
  <div class="slot">Queued — answer 3 of 3</div></div>'''

Q34_ASSIGNED = '''
<div class="q"><div class="qh"><span class="n">3.4</span>Detail your traffic management approach for the Grove Street frontage.</div>
  <div class="slot">Not answered yet</div>
  <span class="side"><span class="chip warm">''' + av("MW","a2") + '''Assigned to Mia · due Fri</span></span></div>'''

Q35_SKEL = '''
<div class="q"><div class="qh"><span class="n">3.5</span>Describe your environmental controls for dust and noise.</div>
  <div class="a"><i class="ln w90"></i><i class="ln w80"></i><i class="ln w50"></i></div></div>'''

def page(body, cls=""):
    return f'''<div class="canvas"><div class="page {cls}">
    <div class="crumb">Schedule 3 · Returnable schedules</div>
    <h3>Section 3 — Methodology</h3>
    <p class="sub">Responses to the Principal’s evaluation criteria · Northside School Upgrade · RFT 2026-114</p>
    {body}
  </div></div>'''

# ---------- frames ----------
def frame(num, title, brief, window):
    return f'''
<section class="frame">
  <div class="frame-head"><span class="num">{num}</span><h2>{title}</h2><p class="brief">{brief}</p></div>
  {window}
</section>'''

# 1 — ask about the document
pane1 = f'''
<div class="pane">{pane_head()}
  <div class="raypanel">{RP_HEAD}
    <div class="rail-body">
      <div class="rail-you">What is the buyer actually asking for in 3.2 — and what have we said before?</div>
      {RP_RAY}
      <div class="rh-s"><i class="chev"></i>Thought for 1.4s · 4 steps</div>
      <div class="rail-work">
        <div class="work done"><i></i><code>read_document_xml</code><span>Schedule 3 · 14 questions found</span></div>
        <div class="work done"><i></i><code>read_question</code><span>3.2 · disruption during drop-off / pick-up</span></div>
        <div class="work done"><i></i><code>search_company_knowledge</code><span>3 matches · Riverside Primary 2025 strongest</span></div>
        <div class="work done"><i></i><code>draft_answer</code><span>184 words · aligned to criterion 3(b)</span></div>
      </div>
      <div class="rail-offer ask"><p><b>They want windows, not intentions.</b> The criterion scores named no-work periods and a single school contact. Drafted from your Riverside Primary plan, with the times swapped for Northside’s bell schedule.</p>
        <div class="srcs"><b>Disruption Management Plan · Riverside Primary</b><b>Northside RFT · criterion 3(b)</b></div>
        <div class="acts"><span class="rail-btn">Insert at cursor</span><span class="rail-btn ghost">Refine</span><span class="rail-btn ghost">Show sources</span></div></div>
    </div>
    {foot(["Tender Response.docx", "Company knowledge"])}
  </div></div>'''
win1 = f'<div class="win">{titlebar()}{tabs()}{ribbon("ask")}<div class="body">{page(Q31_DONE + Q32_EMPTY_CURSOR + Q33_EMPTY + Q35_SKEL)}{pane1}</div></div>'

# 2 — insert, insert, insert
pane2 = f'''
<div class="pane">{pane_head()}
  <div class="raypanel">{RP_HEAD}
    <div class="rail-body">
      <div class="rail-you">Answer the rest of Section 3 from the same sources.</div>
      {RP_RAY}
      <div class="rh-s"><i class="chev"></i>Thought for 3.1s · 6 steps</div>
      <div class="rail-offer"><p><b>3 answers ready.</b> One click each — Ray places every answer in its own slot, in order, so you never hunt for the cursor.</p>
        <div class="ins-list">
          <div class="ins-row done"><span class="n">3.2</span><span class="t">School drop-off and pick-up<small>Inserted · 2 sources</small></span><span class="st">Inserted</span></div>
          <div class="ins-row"><span class="n">3.3</span><span class="t">Communication plan<small>Ready · Riverside comms register</small></span><span class="rail-btn next">Insert</span></div>
          <div class="ins-row queued"><span class="n">3.4</span><span class="t">Traffic management<small>Ready · Grove Street TMP</small></span><span class="rail-btn ghost">Insert</span></div>
        </div>
        <div class="acts"><span class="rail-btn ghost">Insert all three</span><span class="rail-btn ghost">Review first</span></div></div>
      <div class="note"><b>Today:</b> place the cursor, then insert. <b>Next:</b> Ray targets the next empty slot itself — insert, insert, insert.</div>
    </div>
    {foot(["Tender Response.docx", "Company knowledge"])}
  </div></div>'''
win2 = f'<div class="win">{titlebar()}{tabs()}{ribbon("all")}<div class="body">{page(Q31_DONE + Q32_INSERTED + Q33_TARGET + Q34_QUEUED)}{pane2}</div></div>'

# 3 — XML parsing, no bookmarks
def qtag(n): return f'<span class="qtag">Q{n}</span>'
mapped_doc = f'''
<i class="outline-rail"></i>
<div class="q">{qtag("3.1")}<div class="qh"><span class="n">3.1</span>Describe your approach to site establishment and hoarding.</div><div class="a"><i class="ln w90"></i><i class="ln w70"></i></div></div>
<div class="q">{qtag("3.2")}<div class="qh"><span class="n">3.2</span>Describe how you will manage disruption during school drop-off and pick-up.</div><div class="a"><i class="ln w90"></i><i class="ln w80"></i><i class="ln w60"></i></div></div>
<div class="q">{qtag("3.3")}<div class="qh"><span class="n">3.3</span>Outline your communication plan with the school and neighbouring residents.</div><div class="slot">Answer slot detected · empty</div></div>
<div class="q">{qtag("3.4")}<div class="qh"><span class="n">3.4</span>Detail your traffic management approach for the Grove Street frontage.</div><div class="slot">Answer slot detected · empty</div></div>
<div class="q">{qtag("3.5")}<div class="qh"><span class="n">3.5</span>Describe your environmental controls for dust and noise.</div><div class="a"><i class="ln w80"></i><i class="ln w50"></i></div></div>'''
pane3 = f'''
<div class="pane">{pane_head()}
  <div class="raypanel">{RP_HEAD}
    <div class="rail-body">
      <div class="rail-you">Map this document.</div>
      {RP_RAY}
      <div class="rh-s open"><i class="chev"></i>Thought for 2.1s · 4 steps</div>
      <div class="rail-work">
        <div class="work done"><i></i><code>open_document_xml</code><span>word/document.xml · 48 KB · no bookmarks needed</span></div>
        <div class="work done"><i></i><code>outline_document</code><span>5 sections · 14 questions · 9 empty answer slots</span></div>
        <div class="work done"><i></i><code>map_answer_slots</code><span>14 / 14 matched by heading + numbering</span></div>
        <div class="work done"><i></i><code>validate_structure</code><span>styles, tables, numbering untouched</span></div>
      </div>
      <div class="rail-offer status"><p><b>Document map ready.</b> Ray reads and writes the document’s own XML — the structure Word itself uses — so answers land inside the real paragraphs, and nothing is rewritten around them.</p>
        <div class="srcs"><b>XML-native</b><b>No bookmarks</b><b>No corruption risk</b></div></div>
      <div class="note">Replaces the Syncfusion bookmark approach — the source of the formatting pain in earlier builds.</div>
    </div>
    {foot(["Tender Response.docx"])}
  </div></div>'''
win3 = f'<div class="win">{titlebar()}{tabs()}{ribbon("open")}<div class="body">{page(mapped_doc, "mapped")}{pane3}</div></div>'

# 4 — collaboration
collab_doc = f'''
<div class="q"><div class="qh"><span class="n">3.1</span>Describe your approach to site establishment and hoarding.</div>
  <div class="a"><p>Site establishment will follow our standard three-stage sequence: perimeter hoarding to the Grove Street frontage, temporary services connection, and a single controlled gate on the northern boundary.</p></div>
  <span class="side"><span class="chip live">{av("MW","a2")}Mia is editing</span></span></div>
{Q32_INSERTED}
{Q33_EMPTY}
{Q34_ASSIGNED}
<div class="q"><div class="qh"><span class="n">3.5</span>Describe your environmental controls for dust and noise.</div><div class="a"><i class="ln w90"></i><i class="ln w80"></i><i class="ln w50"></i></div>
  <span class="side"><span class="chip">{av("TB","a3")}1 comment</span></span></div>'''
pane4 = f'''
<div class="pane">{pane_head(bell=3)}
  <div class="raypanel">{RP_HEAD}
    <div class="rail-body">
      {RP_RAY}
      <div class="rail-offer status"><p><b>Since you were last here:</b> 3 things changed in this document on SharePoint.</p></div>
      <div class="assign"><div class="k">Assigned to you</div>
        <div class="r"><span class="n">3.4</span><span class="t">Traffic management approach<small>Assigned by Daniel · due Friday</small></span><span class="rail-btn">Draft</span></div></div>
      <div class="assign"><div class="k">Changed on SharePoint</div>
        <div class="r"><span class="n">3.1</span><span class="t">Edited by Mia<small>Rewrote the gate sequence · now editing</small></span><span class="when">12 min</span></div>
        <div class="r"><span class="n">3.5</span><span class="t">Comment from Tom<small>“Add the noise monitoring clause?”</small></span><span class="when">1 hr</span></div></div>
      <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Next · 3.3</b> · Communication plan</span><span class="rp-go">Start</span><i class="rp-meter"><i style="width:43%"></i></i></div>
    </div>
    {foot(["Tender Response.docx", "SharePoint · Northside"])}
  </div></div>'''
win4 = f'<div class="win">{titlebar(av("TB","a3"))}{tabs(dot=True)}{ribbon("activity")}<div class="body">{page(collab_doc)}{pane4}</div></div>'

# 5 — first open / empty state (the hook, in Word)
pane5 = f'''
<div class="pane">{pane_head()}
  <div class="raypanel">{RP_HEAD}
    <div class="rail-body">
      <div class="ray-empty"><span class="ray-halo"><img src="{RAY}" alt=""></span>
        <h3>How can Ray help with this document?</h3>
        <p>Ray has read <b>Tender Response.docx</b> — 14 questions, 9 still empty — and has your company knowledge alongside it.</p>
        <div class="ray-starter">Answer the empty questions in Section 3 from our Riverside Primary submission.</div>
        <div class="ray-starter">Which questions are assigned to me, and what changed since yesterday?</div>
        <div class="ray-starter">Check every answer against the evaluation criteria.</div></div>
      <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Next · 1 of 9</b> · 3.2 School drop-off</span><span class="rp-go">Start</span><i class="rp-meter"><i style="width:0%"></i></i></div>
    </div>
    {foot(["Tender Response.docx", "Company knowledge"])}
  </div></div>'''
Q32_EMPTY = '''
<div class="q"><div class="qh"><span class="n">3.2</span>Describe how you will manage disruption during school drop-off and pick-up.</div>
  <div class="slot">Not answered yet</div></div>'''
Q34_EMPTY = '''
<div class="q"><div class="qh"><span class="n">3.4</span>Detail your traffic management approach for the Grove Street frontage.</div>
  <div class="slot">Not answered yet</div></div>'''
doc5 = page(Q31_DONE + Q32_EMPTY + Q33_EMPTY + Q34_EMPTY + Q35_SKEL)
win5 = f'<div class="win">{titlebar()}{tabs()}{ribbon("open")}<div class="body">{doc5}{pane5}</div></div>'

ROAD = f'''
<section class="road">
  <div class="lbl"><b>Roadmap</b> · from the update — not in-product UI</div>
  <div class="road-grid">
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Word add-in</b><small>First release · end of next week. Q&amp;A pane, insert at cursor, XML parsing.</small></span><span class="rp-go">Now</span><i class="rp-meter"><i style="width:78%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Insert, insert, insert</b><small>Sequential insertion into the next empty slot — the flow after cursor placement.</small></span><span class="rp-go off">Next</span><i class="rp-meter"><i style="width:20%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Excel add-in</b><small>Starts once the Word add-in ships. Same panel, same knowledge.</small></span><span class="rp-go off">After</span><i class="rp-meter"><i style="width:0%"></i></i></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Template builder</b><small>Complex module · a new developer may join, pending technical interview.</small></span><span class="rp-go off">Pending</span><i class="rp-meter"><i style="width:0%"></i></i></div>
  </div>
  <div class="road-grid" style="margin-top:12px;grid-template-columns:repeat(2,minmax(0,1fr))">
    <div class="rp-next gone"><i class="rp-arrow"></i><span class="t"><b>Syncfusion · retired</b><small>Bookmark-based insertion and its formatting limits are out; XML operations replace them.</small></span><span class="rp-go off">Removed</span></div>
    <div class="rp-next"><i class="rp-arrow"></i><span class="t"><b>Collaboration</b><small>Notification icons for assigned questions and changes; SharePoint carries the multi-author change history.</small></span><span class="rp-go off">With Word</span><i class="rp-meter"><i style="width:35%"></i></i></div>
  </div>
</section>'''

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ray for Word</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0,0">
<style>
.ms {{ font-family: 'Material Symbols Outlined'; font-weight: normal; font-style: normal; line-height: 1; letter-spacing: normal; text-transform: none; display: inline-block; white-space: nowrap; direction: ltr; -webkit-font-feature-settings: 'liga'; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; }}
{CSS}
</style></head>
<body>
<header class="head">
  <span class="eyebrow">RayAI expansion · Microsoft Word add-in</span>
  <h1>Ray, <em>inside the document.</em></h1>
  <p>A mock of the Word add-in from the developer update, drawn in the Ray panel language the film and the site already use — same tokens, same rows, same buttons. Five states, one document: <b>Northside School Upgrade – Tender Response.docx</b>, Section 3, nine questions still empty.</p>
</header>

{frame("01 · Ask about the document", "Company knowledge answers the question in front of you",
       "The task pane in Word. You ask about the question under the cursor; Ray reads the document, searches company knowledge, and drafts an answer with its sources shown — ready to insert. <b>From the update:</b> the Q&amp;A panel, driven by company knowledge.", win1)}

{frame("02 · Insert, insert, insert", "One click per answer — Ray places each one in its own slot, in order",
       "Today the cursor has to be placed by hand before an insert. The refined flow: Ray keeps a queue of ready answers, targets the next empty slot itself, and each click drops the next answer into the document sequentially. <b>From the update:</b> the insertion logic and where it is going.", win2)}

{frame("03 · Reads the document’s own XML", "No bookmarks, no corruption — the map is the document’s real structure",
       "Ray opens <code>word/document.xml</code> directly, outlines sections and questions from headings and numbering, and matches every answer slot without planting bookmarks. Writes go into the real paragraphs, so styles, tables and numbering stay untouched. <b>From the update:</b> XML operations replacing the Syncfusion approach.", win3)}

{frame("04 · Working together on one document", "Assigned questions, changes and comments — surfaced where you are",
       "A notification count on the pane, a list of what is assigned to you, and what changed on SharePoint since you last opened the file — who edited which question, who is editing now, and open comments. SharePoint carries the multi-author history; the pane reads it. <b>From the update:</b> notification icons and SharePoint-backed collaboration.", win4)}

{frame("05 · First open", "The same hook as the film, scoped to this document",
       "Ray has already read the file when the pane opens: how many questions, how many are empty, and three starters that map onto the three things above. The <b>Next</b> card walks the empty questions in order. Not from the update directly — it is the entry point the four states above hang off.", win5)}

{ROAD}
</body></html>'''

HTML = HTML.replace("__RAY__", RAY)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT, len(HTML), "bytes")
