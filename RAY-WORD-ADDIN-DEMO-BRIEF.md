# Ray for Word — feature brief from the first demo video (24 Sep 2026)

Source: `E:\Tenderfy\word_plugins_first_demo.mp4` (22:31, Shivam demoing the
live add-in to Tom Blake; recorded for Daniel via Asana TND-113 "Designs Agent
Ray in Word and Excel"). Frames + Whisper transcript in the session scratchpad.

## What the built add-in looks like today

Task pane "Tenderfy Ray", ~330px, Tenderfy wordmark, sign-out icon. Three tabs:
**Ask Ray · Responses · Q&A**. Under the tabs a context block:
`Tender · Folder · Document`. Document opened from the platform carries
metadata (tender id, folder, doc) so the pane remembers login + context; a
document opened outside Tenderfy shows **Choose a tender** (searchable list),
uploads the doc into that tender, then analysis starts.

## Feature inventory

| # | Feature | State in demo (Shivam's words) | How it should be shown |
|---|---|---|---|
| 1 | **Q&A tab: Extracted Questions** — pane parses the open doc (OOXML, no bookmarks) into question cards: title, Table badge, answer box prefilled from Response Library, word count, copy, `Mark as Ready`, `Generate with AI`, `Assign User`, `Mark as "Not a Question"`. Header "139 Questions Extracted"; sub-tabs **Assigned Questions (0) · All Questions**; button **Fill document**. Progress state "Analysing the document… 1/8 sections · 8 questions found". Checkbox questions render as `☐ Checked` toggles; Yes/No as radio pair. | Parsing done. Insert from a card **not implemented**. Generate with AI is "simple GPT, not Agent Ray", partial. Assigned tab empty, linking flaky. | This is the worklist. Keep cards, but add an **Insert** per card and **Insert next** at the bottom; status glyph per card; collapse by section; scope the 139 into sections with counts. Generate with AI → route through Agent Ray with tender context. |
| 2 | **Fill document** — writes every prefilled answer via OOXML node walk. | Works, but produces a **new downloaded file** ("Filled 67 — downloaded"), not the open doc. Accuracy "much better than Syncfusion"; never corrupts. | Tom: must fill the **open** document. Show as step ① of the phase strip; review-then-write list of matched values; result lands in place as tracked changes. |
| 3 | **Ask Ray tab** — chat with history / new chat, "Thinking… N steps" collapsible (`read_open_document`, `find_answer_from_library`), streamed answer, **Insert into document** button, "Inserted ✓" badge. Demo: "let me know the ABN" → inserted; "answers for all 1.1" → 10-step, full field list, inserted as one block at the cursor. | Works. Insert only at cursor; the 1.1 block landed in one cell as a wall of text. | Chat stays a tab, not the default. Insert targets a tagged content control, never the cursor; multi-field answers insert field-by-field. Keep collapsed thinking + streaming (already agreed 24 Aug). |
| 4 | **Responses tab** — Response Library browser: search, `Default Responses` / `About` chips, accordion entries (Postal Address, Public Liability…, policies), `+` to add. Click an entry → inserts at cursor. | Works, cursor-bound. | Becomes the library column/drawer inside the editor and a "tap to add to 3.4" list; entries insert into the active question, not the cursor. |
| 5 | **Cursor-bound insertion** (everything above). | Tom's #1 ask: "insert insert insert, cursor knows where to go". Shivam: "one more button and it inserts into the right place — can do." | Content-control slot per question (`ray/q/<id>`); Insert next walks the list. This is the insertion contract in C4 §4. |
| 6 | **Assign User** on a card + Assigned Questions tab + notification icon. | "In progress"; not working; icon planned. | Owner in control tag; Mine filter; Team tab; right-click assign. Tom's open question: how does the assignee's answer get back if not on SharePoint → state it: solo = Word, team = SharePoint co-authoring. |
| 7 | **Track Changes** for Ray's inserts. | Tom asked; Shivam: "we need to enable it — can be done." | Default on for every Ray write. Review tab = accept/reject. |
| 8 | **Autofill** (standard fields). | Partial; also creates a new doc. | Merge into Fill document step ①; no separate feature. |
| 9 | **Tick boxes** (Yes/No, ☐ lists). | Renders and (claims) writes; Tom: test squares/triangles/non-standard glyphs. | Show as choice chips on the card; QA list item. |
| 10 | **Context persistence** — metadata written on platform download; history + login remembered on reopen. | Works. | Keep; show the Tender/Folder/Document block; "Choose a tender" for foreign docs. |
| 11 | **SharePoint co-authoring** | Same plugin; untested. | Team story depends on it; QA item. |
| 12 | **Excel** | Not started; "logic too different". | Out of scope for Word release. |
| 13 | **Platform side** — remove the web Q&A mode (Syncfusion) for uploaded schedules; keep Syncfusion only for Tenderfy-built docs; users download → work in Word → upload back. | Tom's direction. | Landing/product copy: "Upload it, download it, complete it in Word." |

## Tom's asks, verbatim intent

1. "Insert insert insert — you don't want to manually move the cursor."
2. Assigning questions out, and the Assigned tab so you see yours on open.
3. Fill the open document, not a new one (user-flow problem, "that's the design").
4. Track changes visible in Word.
5. Generate with AI must be Agent Ray with this tender's context.
6. Test complex schedules and odd tick boxes; never corrupt the document.
7. Daniel: design the UI + QA flow for all of the above; first release "end of next week".

## Gaps vs the C4 design note

C4 already covers 1–5 and 7. Add: tick-box card type (9), the "Choose a
tender" onboarding state (10), and the platform copy change (13). Drop C4's
assumption that autofill is a separate feature — in the build it is the same
Fill document pass.
