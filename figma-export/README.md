# figma-export

Rebuilds the C4 mock as editable Figma layers (file `yTjFH7kFIb9jbQs19JiPc5`).

1. `node capture.js` — headless Chrome drives the mock through every state (1440×900) and serializes the live DOM to `states/*.json`.
2. `node post.js` — infers auto layout, tags CSS-token colours and text styles, extracts component variants → `plan/`.
3. `node mkdata.js` — frame names / positions → `out/*.json`; `node pack.js <json> <png>` wraps each payload in a PNG.
4. Upload the PNGs with the Figma MCP `upload_assets`, then run `builder.js` inside `use_figma` (it reads its payload back from the image bytes).
