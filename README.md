# Ray for Word — portable bundle

Start here: `extracts/RAY-WORD-ADDIN-HANDOFF.md` (brief, versions, decisions,
council findings, plugin constraints, next moves).

## Contents
- `extracts/ray-word-addin-*.html` — the mocks (A, B, C, C2, C3, static) and
  `ray-word-addin-all-in-one.html` (every version in one file, tab bar).
- `extracts/*.build.py` — builders; paths are relative, run from anywhere:
  `python3 extracts/ray-word-addin-interactive-c3.build.py`
  (C/C2/C3 builders read the static mock's and A's builder for shared CSS, so
  keep the folder together).
- `extracts/serve.py` + `index.html` — local demo server:
  `python3 extracts/serve.py 4180` → http://localhost:4180
- `assets/` — the two SVGs the builders inline (Ray avatar, wordmark).
- `memory/` — the Claude memory notes referenced by the handoff (copy into
  the new machine's memory folder or paste as context).

Regenerating the all-in-one file after edits: `python3 extracts/build_all_in_one.py`.
