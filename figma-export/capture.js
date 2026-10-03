// Drives the C4 mock (Ask Ray workflow) through every state and serializes each to states/<id>.json (+ reference png)
const open = require('./cdp'), fs = require('fs');
const URL = 'file:///C:/Users/tieun/ray-word-addin/ray-word-addin-interactive-c4.html';
fs.mkdirSync(__dirname + '/states', { recursive: true });
const only = process.argv[2] ? process.argv[2].split(',') : null;
const meta = [];
const HELP = `
window.$c=s=>{const e=document.querySelector(s);if(!e)throw new Error('missing '+s);e.click();};
window.$type=(s,t)=>{const e=document.querySelector(s);if(!e)throw new Error('missing '+s);e.focus();e.innerText=t;e.dispatchEvent(new Event('input',{bubbles:true}));};
window.$val=(s,t)=>{const e=document.querySelector(s);if(!e)throw new Error('missing '+s);e.focus();e.value=t;e.dispatchEvent(new Event('input',{bubbles:true}));};
window.$see=s=>{const e=document.querySelector(s);if(!e)throw new Error('missing '+s);toTop(e,false);};
window.$top=()=>{const p=document.querySelector('.pbody');if(p)p.scrollTop=0;};
window.$sel=(id,v)=>{const e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('change',{bubbles:true}));};
window.$key=(k,o={})=>(document.activeElement||document).dispatchEvent(new KeyboardEvent('keydown',Object.assign({key:k,bubbles:true},o)));
window.$nr=()=>document.querySelector('.pbody .wr .atag.ai').closest('.wr').dataset.q;
document.head.insertAdjacentHTML('beforeend','<style>*,*::before,*::after{animation:none!important;transition:none!important}</style>');1`;

(async () => {
  const b = await open(URL);
  await b.send('Emulation.setFocusEmulationEnabled', { enabled: true });
  const SER = fs.readFileSync(__dirname + '/ser.js', 'utf8');
  const fresh = async () => { await b.go(URL); await b.ev(SER + ';' + HELP); };
  const until = async (expr, ms = 20000) => { const t = Date.now(); while (Date.now() - t < ms) { if (await b.ev(expr)) return; await b.sleep(100); } throw new Error('timeout ' + expr); };
  const run = async js => { await b.ev(js + ';1'); await b.sleep(250); };
  const snap = async (id, title, note, group) => {
    meta.push({ id, title, note, group });
    if (only && !only.includes(id)) return;
    await b.sleep(150);
    const t = await b.ev(`(()=>{const to=document.querySelector('#toast');return window.__ser(document.querySelector('#win'),to.classList.contains('on')?[to]:[])})()`);
    t.name = id + ' · ' + title;
    fs.writeFileSync(`${__dirname}/states/${id}.json`, JSON.stringify(t));
    await b.shot(`${__dirname}/states/${id}.png`);
    console.log(id, JSON.stringify(t).length);
  };
  const untoast = () => b.ev(`document.querySelector('#toast').classList.remove('on');1`);
  const setup = async () => { await run(`$c('[data-do=wftender][data-i="0"]')`); await run(`$c('[data-do=wffolder][data-f="Default"]')`); };
  const start = async () => { await setup(); await run(`$c('[data-do=wfmock]')`); };
  const done = async () => { await until(`!!ui.scan||ui.run.stage==='done'`); await run(`if(ui.scan)$c('.demoscan')`); await until(`ui.run.stage==='done'`); await untoast(); await run(`renderPane()`); };
  const boot = async () => { await fresh(); await start(); await done(); await run(`$c('[data-do=wfreview]')`); };

  /* ---------- happy flow ---------- */
  await fresh();
  await snap('H01', 'Choose the tender', 'Ray opens in Ask Ray with a pinned "Fill this document" stepper (4 steps). Step 1 asks which Tenderfy tender the document is for; nothing is guessed. Chat stays disabled until the run finishes.', 'happy');
  await run(`$c('[data-do=wftender][data-i="0"]')`);
  await snap('H02', 'Choose where to upload', 'Step 2: the Tenderfy folder this document is uploaded to. Change tender goes back a step.', 'happy');
  await run(`$c('[data-do=wffolder][data-f="Default"]')`);
  await snap('H03', 'Add reference documents', 'Step 3 (optional): extra documents Ray reads when answering. Select File opens the File Manager; Upload File takes one from this computer. Skip moves on.', 'happy');
  await run(`$c('[data-do=wffmopen]')`); await run(`$c('[data-do=wffmpick][data-f="Bilby Capability Statement 2026.pdf"]')`); await run(`$c('[data-do=wffmpick][data-f="ISO 9001 Certificate.pdf"]')`);
  await snap('H04', 'File Manager', 'A modal sheet over the pane: search, collapsible Folders (cards, selected one dark) and Files (one-line rows with a format badge). Close with ×, the backdrop or Esc.', 'happy');
  await run(`$c('[data-do=wffmattach]')`); await run(`$c('[data-do=wfupload]')`); await untoast();
  await snap('H05', 'Reference documents chosen', 'Chosen files list under the card with where they came from; × removes one. The button now reads Continue with 3.', 'happy');
  await run(`$c('[data-do=wfmock]')`); await until(`ui.run.step>=2`, 8000); await untoast();
  await snap('H06', 'Analysing and filling', 'Step 4 starts by itself. "Your choices" sums up the setup while Ray reads, finds questions, matches the Response Library and drafts the rest. Stop pauses; Q&A is usable meanwhile.', 'happy');
  await done();
  await snap('H07', 'Run finished', 'Library matches are in the document as tracked changes; Ray drafts wait as Needs Review; the rest is left for you. Review in Q&A opens the list. Chat unlocks.', 'happy');
  await run(`$c('[data-do=wfreview]')`);
  await snap('H08', 'Review in Q&A', 'Q&A opens on the first question that needs you, highlighted green under a sticky run summary strip (closable).', 'happy');
  await run(`$see('.wr[data-q="'+$nr()+'"]')`);
  await snap('H09', 'Needs Review drafts', 'Ray drafts carry an orange Needs Review tag and a Click to insert pill. Apply to document skips them until someone checks them.', 'happy');
  await run(`$c('.wr[data-q="'+$nr()+'"] .t b')`);
  await snap('H10', 'Question card · Needs Review', 'The card shows the draft in the editor and the Needs Review tag beside the section. Put in document & next inserts it and moves on.', 'happy');
  await run(`$c('[data-do=list]')`); await run(`$c('.wr[data-q="4.1"] .t b')`);
  await snap('H11', 'Question card · empty', 'An open question: full text, the editor with Write manually / Answer with Ray, Put in document & next disabled until there is text.', 'happy');
  await run(`$type('#edbody','We expect to engage four local employees on this contract: two Bundaberg depot staff for receiving and dispatch, one local driver, and a part-time administrator.')`);
  await snap('H12', 'Answer written', 'Typing enables Put in document & next (Ctrl+Enter).', 'happy');
  await run(`$c('#primbtn')`); await untoast();
  await snap('H13', 'Put in document & next', 'The answer goes in as a tracked change and the card moves to the next question still to answer or check.', 'happy');
  await run(`$c('[data-do=list]')`);
  await snap('H14', 'Back in the list', 'Back from the card puts the question you were on at the top, highlighted, with its answer marked Inserted.', 'happy');

  /* ---------- setup edge cases ---------- */
  await fresh();
  await run(`$val('#tsq','north')`);
  await snap('E01', 'Tender search', 'The search box filters tenders live by name or reference.', 'edge');
  await run(`$val('#tsq','zzz')`);
  await snap('E02', 'Tender search · no match', 'No match shows a short note instead of an empty list.', 'edge');
  await fresh(); await setup(); await run(`$c('[data-do=wffmopen]')`); await run(`$c('[data-do=wffmfolder][data-f="Insurance"]')`); await run(`$c('[data-do=wffmpick][data-f="Public Liability.pdf"]')`);
  await snap('E03', 'File Manager · folder', 'Picking a folder card narrows Files to that folder; the selected count sits in the Files header.', 'edge');
  await run(`$c('[data-do=wffmfolder][data-f="All files"]')`); await run(`$val('#fmq','cert')`);
  await snap('E04', 'File Manager · search', 'Search filters files across every folder.', 'edge');

  /* ---------- run edge cases ---------- */
  await fresh(); await start(); await until(`ui.run.step>=1`, 8000); await run(`$c('[data-do=wfstop]')`); await untoast();
  await snap('E05', 'Run paused', 'Stop pauses the run. Carry on picks up; Undo this run takes out everything Ray put in.', 'edge');
  await run(`$c('[data-do=wfundo]')`); await untoast();
  await snap('E06', 'Run undone', 'Nothing from the run is left in the document. Start again reruns with the same choices.', 'edge');
  await fresh(); await start(); await until(`ui.run.step>=2`, 8000); await run(`$c('[data-do=wfresume]')`); await untoast();
  await snap('E07', 'Reopened mid-run', 'Closing and reopening the pane mid-run shows where Ray left off.', 'edge');
  await run(`$c('[data-do=tabq]')`); await run(`$see('.wr[data-q="8.3"]')`); await run(`$type('.wr[data-q="8.3"] .qa .in','No conflicts of interest to declare.')`);
  await snap('E08', 'Answering while Ray works', 'Q&A works during the run. Rows Ray is still on say so; anything you answer first, Ray skips.', 'edge');
  await fresh(); await run(`$c('[data-do=wfprotect]')`); await start(); await done();
  await snap('E09', 'Protected document', 'If Word blocks edits, answers are ready but not written. Copy answers puts them on the clipboard.', 'edge');

  /* ---------- Q&A list ---------- */
  await boot();
  await run(`$see('.wr[data-q="1.8"]')`); await run(`$type('.wr[data-q="1.8"] .qa .in','07 4152 0001')`);
  await snap('E10', 'Quick inline answer', 'A short answer typed into the row. Enter puts it in and jumps to the next open question; Shift+Enter opens the card.', 'edge');
  await run(`$type('.wr[data-q="1.8"] .qa .in','07 4152 0001 (main) and 07 4152 0002 (after hours), both monitored on weekdays from 7am to 5pm AEST.')`);
  await snap('E11', 'Inline answer getting long', 'Past ~85 characters a note suggests the card (Shift+Enter).', 'edge');
  await run(`document.activeElement.blur()`);
  await snap('E12', 'Left mid-typing → draft kept', 'Clicking away keeps the text as a draft with Click to insert; Apply to document puts every draft in at once.', 'edge');
  await run(`ui.cur='5.4';document.querySelectorAll('.wr.cur').forEach(x=>x.classList.remove('cur'));$see('.wr[data-q="5.4"]');document.querySelector('.wr[data-q="5.4"]').classList.add('cur');updFab()`);
  await snap('E13', 'Back to: pill', 'When the question you are working on is off screen, or another row is highlighted, a floating "Back to: …" pill returns you to it.', 'edge');
  await run(`$see('.wr[data-q="5.4"]')`);
  await snap('E14', 'Assigned to someone else', 'Rows assigned to a teammate show their avatar, name and due day. You can still answer.', 'edge');
  await run(`$c('.wr[data-q="3.2"] .t b')`);
  await snap('E15', 'Library answer · card', 'A Response Library answer opens with the text in the editor and the source tag beside the section name.', 'edge');
  await run(`$c('[data-do=list]')`);
  await boot(); await run(`$sel('stfsel','review')`); await run(`$top()`);
  await snap('E16', 'Status filter · Needs Review', 'Needs Review narrows the list to Ray drafts waiting for a check.', 'edge');
  await run(`$sel('stfsel','open')`); await run(`$top()`);
  await snap('E17', 'Status filter · Open', 'Open shows everything not yet in the document.', 'edge');
  await run(`$sel('stfsel','')`); await run(`$c('[data-do=filter][data-f=mine]')`);
  await snap('E18', 'Assigned to me', 'The Assigned switch narrows the list to questions assigned to you.', 'edge');
  await run(`$c('[data-do=filter][data-f=all]')`); await run(`$sel('whosel','MW')`);
  await snap('E19', 'Filter by person', "In All, the person filter shows one teammate's questions across sections.", 'edge');
  await run(`$sel('whosel','')`); await run(`$c('.bell')`);
  await snap('E20', 'Notifications', 'The bell lists the run summary, assignments and teammate answers; clicking one opens that question.', 'edge');
  await run(`document.querySelector('.cmenu')?.remove()`); await run(`$c('[data-do=more]')`);
  await snap('E21', 'More menu', 'The ⋯ menu: Keyboard shortcuts, Changelog and Sign out.', 'edge');
  await run(`$c('[data-do=keys]')`);
  await snap('E22', 'Keyboard shortcuts', 'An in-pane sheet listing list, card and global shortcuts.', 'edge');
  await run(`$c('[data-do=sheetclose]')`); await run(`$c('[data-do=more]')`); await run(`$c('[data-do=changelog]')`);
  await snap('E23', 'Changelog', 'Who changed what in this document, newest first.', 'edge');
  await run(`$c('[data-do=sheetclose]')`);

  /* ---------- question card ---------- */
  await run(`$c('.wr[data-q="6.1"] .t b')`);
  await snap('E24', 'Card for an open question', 'Empty editor, Put in document & next disabled until there is text.', 'edge');
  await run(`$c('.hasg')`);
  await snap('E25', 'Assign from the card header', 'Assign User in the header opens the people menu.', 'edge');
  await run(`document.querySelector('.cmenu')?.remove()`); await run(`$c('.ctabs .ptab[data-k=ray]')`); await run(`$c('.rffile')`);
  await snap('E26', 'Answer with Ray · draft from a file', 'The paperclip opens the same card as the reference step: Select File or Upload File.', 'edge');
  await run(`$c('.genpick [data-do=wffmopen]')`); await run(`$c('[data-do=wffmpick][data-f="TEN3089 Specification.pdf"]')`);
  await snap('E27', 'Draft from files · File Manager', 'The File Manager sheet again; its button reads Draft from files.', 'edge');
  await run(`$c('[data-do=wffmattach]')`); await b.sleep(100);
  await snap('E28', 'Answer with Ray · drafting', 'Ray drafts this question in a per-question conversation.', 'edge');
  await b.sleep(1700);
  await snap('E29', 'Answer with Ray · reply', 'Each reply shows its source, Use this answer, copy, retry and follow-ups.', 'edge');
  await run(`$c('.qthread [data-do=quse]')`);
  await snap('E30', 'Use this answer → editor', 'Use this answer drops the reply into the editor and switches back to Write manually.', 'edge');
  await run(`$c('.ctabrow [data-do=fullscreen]')`); await b.sleep(400);
  await snap('E31', 'Full screen', 'The editor box takes the pane; only the tabs and Put in document & next stay.', 'edge');
  await run(`$c('.ctabrow [data-do=fullscreen]')`); await b.sleep(400);
  await run(`$c('.naq')`); await run(`$c('[data-do=list]')`); await run(`$c('[data-do=sec][data-s="X"]')`); await run(`$see('[data-do=sec][data-s="X"]')`);
  await snap('E32', 'Not a Question', 'Dismissed items leave the queue and the count, and collect in a Not a Question section with Restore.', 'edge');
  await run(`$top()`); await run(`$c('.wr[data-q="1.1"] .t b')`);
  await snap('E33', 'First in the queue', 'Previous Question is disabled on the first item.', 'edge');

  /* ---------- Ask Ray after the run ---------- */
  await run(`$c('[data-do=list]')`); await run(`$c('[data-do=tab][data-tab=ask]')`);
  await run(`$type('#cin','Draft 3.2');document.querySelector('#cin').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}))`); await b.sleep(1800);
  await run(`const p=document.querySelector('.pbody');p.scrollTop=p.scrollHeight`);
  await snap('E34', 'Ask Ray · chat unlocked', 'Once the run is done the composer opens under the run summary for follow-up questions.', 'edge');

  /* ---------- added after the doc council ---------- */
  await boot();
  await run(`const m=document.querySelector('#page .mq');m.scrollIntoView({block:'center'});const r=m.getBoundingClientRect();m.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:r.x+40,clientY:r.y+6}))`);
  await snap('E35', 'Missed question · right-click', 'Ray missed 4.4. Right-click it in the document and choose Add 4.4 as a question.', 'edge');
  await run(`$c('.cmenu [data-do=cm_addq]')`); await run(`$see('.wr[data-q="4.4"]')`);
  await snap('E36', 'Missed question added', '4.4 joins Section 4 in Q&A. Ray drafts it as Needs Review and the run summary counts it.', 'edge');
  await fresh(); await run(`$c('[data-do=wfprotect]')`); await untoast(); await start(); await done(); await run(`$c('[data-do=wfreview]')`);
  await run(`$see('.wr:has(.pst.warn)')`);
  await snap('E37', 'Protected document · rows', "In a protected document each row Ray filled says Couldn't insert, with its own Copy button.", 'edge');
  await fresh(); await run(`$c('[data-do=wfnotenders]')`); await untoast();
  await snap('E38', 'No tenders', 'With no tenders on Tenderfy, step 1 says so and links to Tenderfy to create one.', 'edge');

  /* ---------- failure paths (Demo > Simulate a failure) ---------- */
  const fail = async v => { await run(`$sel('failsel','${v}')`); await untoast(); };
  await fresh(); await fail('slow');
  await snap('E39', 'Loading tenders', 'Tenders load from Tenderfy; placeholder rows show until they arrive.', 'fail');
  await fresh(); await fail('nofolders'); await run(`$c('[data-do=wftender][data-i="0"]')`);
  await snap('E40', 'Tender has no folders', 'Step 2 offers to upload to the tender itself; the team can move it later.', 'fail');
  await fresh(); await fail('nofiles'); await setup(); await run(`$c('[data-do=wffmopen]')`);
  await snap('E41', 'File Manager empty', 'No files yet: the sheet points to Upload File.', 'fail');
  await fresh(); await fail('badfile'); await setup(); await run(`$c('[data-do=wfupload]')`); await untoast();
  await snap('E42', 'Unsupported file', 'A file of the wrong type or size is refused with what is allowed.', 'fail');
  await fresh(); await fail('upload'); await start();
  await snap('E43', 'Upload failed', 'Nothing changes in the document or on Tenderfy. Try again, or choose another folder.', 'fail');
  await fresh(); await fail('library'); await start(); await until(`ui.run.stage==='failed'`);
  await snap('E44', 'Response Library unreachable', 'Ray stops before writing anything. Try again, or answer in Q&A meanwhile.', 'fail');
  await fresh(); await fail('offline'); await start(); await until(`ui.run.stage==='failed'`);
  await snap('E45', 'Connection lost mid-run', 'Says how many answers are already in; Try again carries on from there.', 'fail');
  await fresh(); await fail('noquestions'); await start(); await until(`ui.run.stage==='done'`); await untoast(); await run(`renderPane()`);
  await snap('E46', 'No questions found', 'Points to right-click Add as a question, or choosing another tender.', 'fail');
  await boot(); await fail('insert'); await run(`$see('.wr[data-q="1.8"]')`); await run(`$type('.wr[data-q="1.8"] .qa .in','07 4152 0001')`); await run(`$c('.wr[data-q="1.8"] .qa .go')`); await run(`$see('.wr[data-q="1.8"]')`);
  await snap('E47', "Couldn't insert", 'The answer area was moved or deleted: the row says so and offers Copy.', 'fail');
  await boot(); await fail('chat'); await run(`$c('[data-do=tab][data-tab=ask]')`);
  await run(`$type('#cin','What is our ABN?');document.querySelector('#cin').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}))`); await b.sleep(1800);
  await run(`const p=document.querySelector('.pbody');p.scrollTop=p.scrollHeight`);
  await snap('E48', "Ray can't answer", 'A failed reply says nothing changed and to try again.', 'fail');
  await boot(); await run(`$sel('failsel','session')`); await untoast();
  await snap('E49', 'Session expired', 'A sheet over the pane: sign in again, nothing is lost.', 'fail');

  fs.writeFileSync(__dirname + '/states/meta.json', JSON.stringify(meta, null, 1));
  b.close();
})().catch(e => { console.error(e); process.exit(1); });
