---
description: Build the standard handoff package (workbook, README, PORTAL_BUILD.md for Copilot Cowork)
model: sonnet
---

Prepare the handoff. The factory delivers the Excel backend; I build the portal myself in
Copilot Cowork after the workbook is deployed on the shared drive.

1. Bump `version` in `schema/workbook.schema.json` if the structure changed since the last
   handoff. Set `deploy_location` there if I have told you where the workbook will live.
2. Regenerate the preview: `python3 scripts/render_preview.py`.
3. Build the package (it runs all tests first and stops if any fail):
   `python3 scripts/build_handoff.py`. If I give a downloaded live workbook in the arguments,
   add `--from "<file>"` and show me any migration warnings.
4. Read the generated `README.md` and `PORTAL_BUILD.md` once as if you were me and as if you
   were Copilot Cowork. If anything is unclear, fix the generator, not the output.
5. Add a line to the deployment log in `docs/DEPLOY.md` (version, date, test summary).
6. Run the `reviewer` on the package (spec coverage, workbook usability for editors, safety).
7. Commit, then tell me where the package and zip are and the next 3 steps.

$ARGUMENTS
