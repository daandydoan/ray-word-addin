# Ray for Word — C4 design (28 Sep 2026)

C3 rethought against what a Word add-in can really do (MS Learn, checked 28 Sep
2026). The four usability problems in the 25 Sep scrum notes drive the
structure; each section names the surface that solves it and the fallback.

## Surfaces C4 uses

| Surface | Used for | Availability |
|---|---|---|
| Task pane, 320px | Worklist, progress, chat tab, team tab | Everywhere |
| `taskpane.setWidth()` to 50% of window | **Wide mode**: editor + library side by side | Win 2507+, Mac 16.100.4+. Web: silently no-ops (bug), iPad: none |
| Dialog window (`displayDialogAsync`, 90%) | Same editor when wide mode is unavailable | Everywhere. Dialog can't call Word API: text goes back to the pane by message, pane inserts |
| Content controls, tagged `ray/q/<id>` and `ray/field/<key>` | Every answer slot and standard field; owner + status stored in the tag | Everywhere |
| Track Changes | Ray's drafts land as tracked insertions; review = Word's Review tab | Everywhere |
| Ribbon tab "Tenderfy Ray" | Fill fields · Draft all · Insert next · Assign · Check criteria · Open Ray | Everywhere except iPad |
| Right-click context menu | "Assign this question…", "Draft with Ray", "Add to library" on a question | Win/Mac/web |
| Keyboard shortcuts | Ctrl+Alt+R open Ray · Ctrl+Alt+I insert next ready · Ctrl+Alt+E edit current | Win 2408+, Mac 16.88+, web only when focus is in the document |
| Document settings / custom XML | Slot map, phase state, assignment snapshot travel with the file | Everywhere |

Not used, still impossible: anything drawn on the page (B's ghost text,
gutter owners, balloons). Track Changes is the honest replacement.

## 1 · "Tiny modal" for long answers

**Rule: the pane never edits a four-page answer. Word does.**

- Row action on an open question = **Draft**. Ray drafts into the pane as a
  preview (first ~6 lines, word count, refs). Two buttons: **Insert** and
  **Edit first**.
- **Insert** writes the draft into the question's content control as a
  tracked insertion and selects it (`contentControl.select()`), so the user is
  already editing in Word at full page width. The pane switches to a compact
  **context card** for that control: criterion, refs, library matches, and
  **Re-draft** / **Shorten** / **Ask Ray about this**. Editing the control
  updates the row status live via `onDataChanged`.
- **Edit first** opens the editor:
  - Desktop: `setWidth(min(50% window, 720))`. Layout is two columns: editor
    (flex 1) + library (240px, searchable, click to insert at caret). Toolbar is
    B / I / list + overflow. Closing restores the previous width. This is the
    "full-screen view with the library relocated" Tom asked for, inside the
    pane.
  - Web / iPad / when `setWidth` doesn't take (measure `innerWidth` after
    calling it): same editor HTML in a **dialog** at 90%. On Save the dialog
    `messageParent`s the HTML; the pane inserts.
- Library never replaces the editor body. It is a column (wide) or a bottom
  drawer that pushes the body up (narrow), body stays visible.
- Editor body scrolls internally; toolbar and Insert are sticky. (C3 let the
  body grow past the pane at 630 words.)

## 2 · Two phases the solo user understands

- Persistent two-step strip at the top of the pane, never a toast:
  `① Fill standard fields 0/6  ② Draft answers 0/5`. Current step highlighted.
- **No second document.** Autofill fills the open document's field controls.
  Copy on first open: "Ray reads this document in place — nothing is copied."
- Step ① is **review-then-write** (B's pattern): "6 matched from company
  profile" opens a list of field → value with per-row ✎, then **Fill all 6**.
  Values land in `ray/field/*` controls as tracked insertions.
- Step ② bottom button changes by state:
  - Solo, nothing drafted: **Fill & draft this document** → autofill, draft
    every open question, insert all as tracked changes, then "Review 5 drafts
    in Word's Review tab". One press really ends in the document.
  - Some drafted: **Insert 3 ready**. Some assigned: **Draft my 2**.
- Same two actions exist as ribbon buttons (Fill fields, Draft all), so the
  phases are visible before the pane is even opened.

## 3 · Assignment for a 30-person team

- Owner lives in the control tag (`ray/q/3.4|owner=MW|due=2026-10-03`) plus a
  document-settings snapshot, so it travels with the file and syncs through
  SharePoint co-authoring. No backend needed for the first release; SharePoint
  presence stays the source for "who's in the doc".
- Assign from three places: row menu, **right-click on the question in the
  page**, and **Assign filtered** on the current filter (e.g. "all Section 3
  open → Mia"). Suggest owners from past tenders stays.
- Bulk actions scope to **unassigned + mine**, never hidden because one row is
  someone else's. Assignees open the pane on the **Mine** filter by default.
- Team tab: per-person load, overdue, "changed since you last looked"
  (compare control text hash against the snapshot). Notifications outside
  Word are SharePoint/Teams, stated in the tab, not faked.

## 4 · Direct insertion contract (the first ticket)

- On first open, **Map** runs silently: for each numbered question heading,
  wrap the answer paragraph(s) in a content control tagged `ray/q/<id>`, title
  = question number. Standard fields get `ray/field/<key>`. User never sees the
  word "map" or "XML"; the pane shows "Ray found 12 questions and 6 fields".
- `insert(id, html)`: locate control by tag → `insertHtml(..., 'Replace')`
  with Track Changes on → `select()`. Missing control (user deleted it):
  search the heading text, re-wrap, then insert; if not found, ask "where
  should 3.4 go?" and insert at selection.
- Co-authoring: no lock exists. Tracked insertion + Word's merge is the
  conflict model; the pane shows "Mia changed 3.4 since Ray drafted" from the
  hash and offers Re-draft on top of her text.
- Status per row derives from the control: empty → Open; tracked, unaccepted
  → Ready (▶); accepted text → Answered; owner ≠ me → shows avatar.

## Copy and legibility (carried from council round 2)

- Every row action always labelled (10.5px word under the icon).
- Glyphs: ○ open · ▶ ready · ✓ answered · ! gap.
- No developer vocabulary in the pane: "Map", "XML", "bookmarks", "Syncfusion"
  removed. Empty state explains Ray in one line.
- Keyboard hint reads "↑↓ move · Enter act · Ctrl+Alt+E edit" (single-key
  shortcuts don't reach the document).

## Build order for Shivam

1. Manifest: task pane + ribbon tab + context-menu item + shortcuts + shared
   runtime. Check `TaskPaneApi 1.1` at runtime, not in the manifest.
2. Map + insert (section 4). Ship with just this and the worklist.
3. Fill-then-draft strip and the state-driven bottom button.
4. Wide mode / dialog editor.
5. Assignment in tags + Team tab.

## Revision after the Q&A council (28 Sep 2026)

Superseding §1 above: **there is no in-pane editor, wide mode or dialog.**
Long answers are edited in the page. Ray inserts a draft into the question's
tagged content control as a tracked change and selects it; the pane follows
with the criterion, references, Re-draft, Shorten and Ask Ray. That is the
answer to the "tiny modal / full-screen" ask, and it should be said in the
handover in one line: *the Word page is the full-screen editor.*

Flow as built:
1. Choose a tender (mandatory first screen) → "Reading the document" → lands
   on **Autofill the whole document**: review of matched fields, then one press
   *Fill N fields & generate M drafts*. Fields land in place; drafts go to
   **Ready** and wait to be read. Nothing is inserted unread (Tom's two phases).
2. **Go question by question**: list, Open · Assigned · All (Assigned by
   default when anything open is yours). Row click expands inline; chevron
   opens the card. Open card: Generate with AI (primary), Mark as Ready (reads
   the answer already written in Word, no insert), Assign User, Not a Question.
   Ready card: draft, references, Refine with Ray, Insert into document
   (primary). Drafted card: Accept in Review, Re-draft, Shorten, Ask Ray;
   footer Insert next, or Generate next when nothing is ready.
3. Counts: **Answered = accepted in Word's Review**; inserted-but-unaccepted
   rows read "Drafted · accept in Review".

Build order, revised: the Executor's spike first — wrap three answer cells of
a real Bilby schedule in tagged content controls, turn tracking on, insert,
read back, edit as a second user, detect the author. Owners and due dates go
in document settings keyed by question id (tags cap at ~64 chars). Context
menu labels are static in the manifest ("Assign to…", "Generate with AI"); the
handler reads the selection's control. Gate every insert on "all controls
written" after the reading step. Unmodelled and to specify: partial-batch
rollback when an insert fails mid-run, and two assignees autofilling the same
file at once.

## Revision after the whole-feature and Assign councils (28 Sep 2026)

Applied to the mock in full, no release split:
- **Autofill document fills fields again.** The Autofill screen lists the
  standard fields first (matched value and source, filled ones ticked), then
  the open questions. One press writes the fields in place as tracked changes,
  then drafts the questions for reading. Nothing is inserted unread.
- **Track Changes is not optional.** The ribbon toggle is gone; every Ray
  write is tracked, and the status derivation depends on it.
- **Vocabulary.** "Ready · in the pane" → "Draft ready". "Drafted · accept in
  Review" → "In document · needs accepting". "Accept in Review" → "Accept in
  Word". Batch insert says up front that every draft becomes a tracked change
  to accept or reject in Word's Review tab.
- **Folder defaults to Default.** Choose a tender goes straight to reading; the
  reading screen shows "Saving to <tender> · Default · Change folder".
- **Assign User:** the one dropdown now carries a real due date (native date
  input) and an optional note. A section header has an assign icon that
  assigns every open question in the section. The menu states the rule:
  stored in the question's tag, syncs because the file is on SharePoint.
- **Assignee side:** the card shows who assigned it, the due date and the note,
  with **Hand back** for questions assigned to you.
- **Team:** Changelog half removed (fiction until identity is real). The tab
  is Assignments only, with the SharePoint rule as a footer line.

Not changed, by decision: tick-box question types (Daniel: ignore the
checkbox mention), a 139-question data set (the mock stays at 9 so the demo
reads), demo data (drafts are already about the tenderer's own company).
