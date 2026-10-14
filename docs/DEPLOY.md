# Deployment and handoff

Owner: `developer` (filled in by `/handoff`). The factory delivers the workbook;
the portal is built by the product owner in Microsoft Copilot Cowork.

## 1. The package
`/handoff` builds `dist/<title>/` and `dist/<title>.zip` with the workbook, `README.md`,
`PORTAL_BUILD.md`, `preview.html` and `DESIGN_SYSTEM.md`. The package README has the
step by step instructions for the product owner; this file is the record on the repo side.

| Version | Date | Tests | Location | Notes |
| :--- | :--- | :--- | :--- | :--- |

## 2. Deploy the workbook to the shared drive
1. Upload the workbook from the package to: (SharePoint site, Teams channel or OneDrive folder)
2. Keep the file name stable; the portal and links point at it.
3. Permissions: editors (who), readers (who). Keep the editor group small.
4. Turn on version history (default on SharePoint) so mistakes can be rolled back.
5. Enter or paste the first real data, then open the About sheet and check the row counts.

## 3. Build the portal in Copilot Cowork
1. Open Copilot Cowork and point it at the deployed workbook (not a local copy).
2. Attach `PORTAL_BUILD.md` and `preview.html` from the package and ask Cowork to
   build the portal described in PORTAL_BUILD.md.
3. Compare with `preview.html` and walk the checklist in section 6 of `PORTAL_BUILD.md`.
4. Note anything Cowork could not do in `docs/TECH_DEBT.md` and in "Lessons learned".

## 4. Changing the structure later
The live workbook holds real data, so never replace it with a fresh build.
1. Change the schema in this repo (architect), rebuild and test as usual.
2. Download the live workbook, then run `/handoff "<downloaded file>"`
   (or `python3 scripts/build_handoff.py --from "<downloaded file>"`).
3. Read the warnings: columns that no longer exist are listed, not silently copied.
4. Upload the migrated file as a new version of the same file, at a quiet moment.
5. Regenerate the portal in Copilot Cowork if tabs, KPIs or columns changed.
