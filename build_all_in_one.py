import html, pathlib
E = pathlib.Path(__file__).resolve().parent
V = [('c3','C3','Worklist pane · after council','ray-word-addin-interactive-c3.html','Recommended'),
     ('c2','C2','Worklist pane · compacted','ray-word-addin-interactive-c2.html','Reviewed r1'),
     ('c','C','Worklist pane','ray-word-addin-interactive-c.html','Superseded'),
     ('a','A','Conversation pane','ray-word-addin-interactive.html','Alternate'),
     ('b','B','Document-native (reference)','ray-word-addin-interactive-b.html','Outside constraint'),
     ('m','Static','Five states, one document','ray-word-addin-mock.html','Reference')]
tabs = ''.join(f'<button class="t" data-v="{k}"><b>{lab}</b><span>{d}</span><em>{tag}</em></button>' for k,lab,d,f,tag in V)
frames = ''.join(f'<iframe id="f-{k}" title="{lab} · {d}" srcdoc="{html.escape((E/f).read_text(encoding="utf-8"), quote=True)}" loading="lazy"></iframe>' for k,lab,d,f,tag in V)
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ray for Word · all versions</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap">
<style>html,body{{margin:0;height:100%;background:#F4F1EC;font-family:Outfit,system-ui,sans-serif;color:#14211D}}body{{display:flex;flex-direction:column}}header{{display:flex;align-items:center;gap:10px;padding:10px 16px;background:#fff;border-bottom:1px solid #DCE5E1;flex-wrap:wrap}}header .ey{{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0F7355;background:#E4F1EC;border-radius:999px;padding:5px 10px;white-space:nowrap}}header h1{{font-size:15px;font-style:italic;margin:0 12px 0 0;letter-spacing:-.01em}}.tabs{{display:flex;gap:4px;flex-wrap:wrap}}.t{{font:inherit;text-align:left;background:#fff;border:1px solid #DCE5E1;border-radius:10px;padding:6px 10px;cursor:pointer;display:grid;grid-template-columns:auto auto;gap:0 8px;align-items:center}}.t b{{font-size:12px;font-style:italic;color:#14211D}}.t em{{font-style:normal;font-size:9.5px;font-weight:600;color:#33423E;background:#EEF2F0;border-radius:999px;padding:2px 7px;grid-row:span 2}}.t span{{font-size:10.5px;color:#6B7975;grid-column:1}}.t.on{{border-color:#1D9E75;background:#EAF5F0}}.t.on em{{background:#1D9E75;color:#fff}}main{{flex:1;min-height:0;position:relative}}iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;display:none;background:#F4F1EC}}iframe.on{{display:block}}</style></head><body>
<header><span class="ey">RayAI · Word add-in</span><h1>Ray for Word, every version</h1><div class="tabs">{tabs}</div></header><main>{frames}</main>
<script>const tabs=[...document.querySelectorAll('.t')];function show(v){{tabs.forEach(t=>t.classList.toggle('on',t.dataset.v===v));document.querySelectorAll('iframe').forEach(f=>f.classList.toggle('on',f.id==='f-'+v));location.hash=v;}}tabs.forEach(t=>t.onclick=()=>show(t.dataset.v));show((location.hash||'#c3').slice(1));</script></body></html>'''
(E/'ray-word-addin-all-in-one.html').write_text(out, encoding='utf-8'); print('wrote all-in-one', len(out))
