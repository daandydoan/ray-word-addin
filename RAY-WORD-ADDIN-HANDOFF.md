# Ray for Word — session handoff (28 Sep 2026)

Design track for the RayAI expansion as a **Microsoft Word add-in**. Everything
below is mock/prototype work in plain HTML — nothing has been built in Office.js
yet. Read the "Council findings" and "Plugin can / cannot" sections before
proposing anything new; they set the constraints the next design has to respect.

## The brief (two sources)

1. **Developer update (video, mid-Sep):** a Word add-in with a Q&A task pane
   using company knowledge; insertion currently needs the cursor placed by
   hand, target is an "insert, insert, insert" sequential flow; parsing moved
   from Syncfusion bookmarks (corrupted formatting) to XML operations; wants
   notification icons for assigned questions/changes with SharePoint carrying
   multi-author history; Word first, Excel next, template builder pending a new
   developer; first Word release targeted "end of next week" from the update.
2. **Agent Ray design scrum, 25 Sep 2026** (Tom Blake, Daniel Doan; Gemini
   notes: https://docs.google.com/document/d/1YQ-2mO4R3LtejjciQLZstGe6meq-4-0nzhmcBskOx_0/):
   - **Two-phase workflow**: autofill standard fields (ABN, address, company
     name, policies, insurances) first, then draft/finalise the rest. Today
     autofill via "Shivven" creates a *new* document — users must understand
     they autofill first, then finish in the new file.
   - **Small teams** (Victoria EIWA type): minimal manual entry, autofill.
     **Large teams** (Bilby, ~30 people): assign specific questions to people.
   - **Tiny modal is the pain**: long answers (hundreds of words, up to 4
     pages) need a full-screen-like view; relocate the response library to
     free space.
   - Actions: Daniel to draft UI (full-screen answering, repositioned
     library), finish the video and page that morning, Word plugin in the
     afternoon.
   - **Hard constraint given later by Daniel: everything must live in the
     side panel.** (Version B was built before this and is reference only.)

## What exists (all in `tenderfy-landing/extracts/`)

Every mock is a self-contained HTML file built by a sibling `*.build.py`
(run `python3 <file>.build.py` from anywhere; it reads `../assets` SVGs and
the static mock's CSS and writes the HTML). All use the film's light Ray-panel
tokens: Outfit, teal `#1D9E75` / `#0F7355`, `.rp-*` panel rows, chips, buttons.

| File | What | Status |
|---|---|---|
| `ray-word-addin-mock.html` | Static: five states of the pane on one document + roadmap strip | First pass from the dev update |
| `ray-word-addin-interactive.html` | **A** — conversation-first pane: phase stepper, full-screen overlay editor with library rail, assignment sheet | Alternate |
| `ray-word-addin-interactive-b.html` | **B** — document-native: workflow bar, ghost drafts accepted in place (Tab), in-page focus, gutter owners, margin balloons | Reference only — violates side-panel constraint |
| `ray-word-addin-interactive-c.html` | **C** — worklist pane: question rows, tabs Ray/Library/Team, "wide mode" | Superseded (wide mode infeasible) |
| `ray-word-addin-interactive-c2.html` | **C2** — C compacted: one strip, single-line rows by collapsible section, in-place preview, one contextual action, refs in composer, keyboard | Council round 1 |
| `ray-word-addin-interactive-c3.html` | **C3** — C2 + council items 1–4 (below) | **Current / recommended**; council round 2 done |
| `ray-word-addin-all-in-one.html` | All six above embedded in one file with a tab bar (`#c3`, `#a` … hash selects) | Share this one |

Local demo server: `.claude/launch.json` has a `mocks` config (port 4180)
serving a scratchpad mirror of `extracts/` with `index.html`. The preview
sandbox on this Mac cannot read `~/Documents`, so re-copy files into the
mirror after edits (see memory `mac-preview-server-documents`).

## Design decisions already made (don't relitigate without new input)

- **Worklist over conversation** as the pane's default (C family): the list of
  what's left is the primary object; chat is a tab. Reason: large teams work a
  list; solo users want the next button, not a conversation.
- **Density is right; legibility is the tax.** C2's compaction (one strip,
  single-line rows, folded sections, one contextual action, refs in composer)
  survived two council rounds. What didn't: colour-only status and hover-only
  labels (fixed in C3), and any assumption of horizontal room.
- **No wide mode.** A task pane cannot resize itself. Long answers open a
  full-height editor *inside* the pane with a Library toggle and an honest
  "drag the pane's edge" note (C3).
- **Two phases are surfaced, not enforced**: progress line shows fields and
  answers; the bottom action chains Autofill → Draft when nobody else is
  assigned.
- **Assignment v2 is deferred** (scope call with Tom/Shivam) — see council.

## Council findings (four lenses: Office add-in engineer, 30-person bid manager, solo subbie owner, dense-UI designer)

**Round 1 on C2 → applied in C3 (items 1–4):**
1. Status dot → 12px glyph per state (ring open / half ready / ✓ done / ! gap).
2. Row action shows its word on the selected/hovered row.
3. Wide mode removed → in-pane full-height editor + Library toggle + drag tip.
4. Chained "Autofill & draft all · one press" when solo.
5. *Deferred:* assignment v2 (assign-by-section, due dates, overdue, diffs).

**Round 2 on C3 → open, ranked cheapest-first:**
1. "One press" **over-promises**: `autoDraft` drafts but never inserts. Either
   chain insert (with undo) or rename to "…then insert".
2. Label-on-current-row **relocated** the problem: invisible to touch, still
   icon-only on unselected rows, and the pill widening shifts the grid.
   → Always-visible 10.5px label on every row.
3. `solo` rule is all-or-nothing: one assigned question hides bulk actions for
   the rest. → Scope bulk actions to *unassigned*; same rule gives "assign
   filtered to X" — the bid manager's minimum to survive one tender.
4. In-pane editor kept 680px-era padding and an 8-icon toolbar with no reflow;
   swapping the body for the library loses the user's place. → Reflow for
   340px, toolbar collapsed to B/I/list + overflow, library as bottom half,
   keep "3.4 · 2 of 5 open" in the strip.
5. "Ready" half-moon glyph reads as a smudge → distinct ▶ glyph.
6. **Still unmodelled, both rounds** (the real work): insertion is narrative —
   `insert()` sets a string; nothing targets a paragraph/content control or
   handles a conflict with a live co-author edit. And trust on the row:
   "Answered" conflates a teammate's text with Ray's; "changed since you last
   looked" only exists in the Team tab.

## What a Word add-in can and cannot do (why the constraints exist)

An add-in is a sandboxed web page in an iframe beside the document, talking to
Word only through Office.js.

**Can:** read/write paragraphs, ranges, headings, tables, content controls,
styles, lists; insert text/HTML/raw OOXML at a range; search; read tracked
changes and comments (newer API sets); anchor "answer slots" durably with
tagged **content controls**; add ribbon buttons, a task pane, a **dialog**
(separate pop-up window — the only escape from pane width), context-menu items;
call its own backend over HTTPS; SSO via Microsoft identity, then Graph/
SharePoint for presence and history; react to open/selection events; store
small per-document state (settings / custom XML parts) so slot maps and
assignments travel with the file.

**Cannot:** resize or move the task pane, overlay the page, or render in the
canvas; own editing (pane text is not Word text until inserted; no true WYSIWYG
of Word formatting in the pane); replace Word's comments/presence/save; hold a
co-authoring lock or resolve a merge; read the file system or other documents;
run or notify while Word is closed; guarantee parity across Windows/Mac/Online
without targeting the common API subset; take single-key shortcuts while focus
is in the document.

**Initial issues this creates for Ray:** the tiny-modal problem is structural;
insertion/slot-finding is the whole risk (content controls are the sensible
answer); co-authoring conflicts aren't Ray's to resolve; distribution needs
centralised deployment or AppSource and an IT conversation at a 30-person
firm; notifications outside Word belong to SharePoint/Teams/email.

## Suggested next moves

1. Apply round-2 items 1–5 to C3 (contained, ~1 hour) → C4.
2. Take item 6 to the scrum: (a) insertion contract — content-control-tagged
   slots, insert against a paragraph id, explicit branch for track-changes /
   co-author conflict; (b) assignment v2 scope; (c) notification story outside
   Word. These decide the real build, not the mock.
3. Then a thin Office.js spike: manifest + task pane that reads headings,
   tags slots with content controls, inserts one answer. That validates the
   one thing the mocks can't.

## Related memory (this Mac)

`tenderfy-ray-phase1` (the Ray panel prototype these tokens come from),
`tenderfy-ray-syncup-decisions`, `tenderfy-live-wordpress-site` (unrelated
live-site track), `mac-preview-server-documents`.
