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

## 6. Weekly snapshot (history): setup for the director, one time, about 10 minutes
The snapshot script `scripts/office/snapshot.ts` appends one row per active rock to `RockSnapshots` and one row per milestone of an active rock to `MilestoneSnapshots` (DECISIONS 0007). Running it twice on the same day adds nothing the second time.

Prerequisite: the tenant allows Office Scripts and Power Automate. If not, use the button route below only.

**A. Add the script to the workbook** (needs Excel for the web or desktop with the Automate tab)
1. Open the deployed workbook from SharePoint in Excel.
2. Automate tab, New Script. Delete the sample code, paste the full contents of `scripts/office/snapshot.ts`, name it `Snapshot`, Save.
3. Press Run once. The message reads "Snapshot yyyy-mm-dd: N rock rows and M milestone rows added." Check that `RockSnapshots` and `MilestoneSnapshots` gained rows. Press Run again: it must say 0 and 0.

**B. Schedule it in Power Automate** (signed in as the director)
1. Go to make.powerautomate.com, Create, Scheduled cloud flow. Name: `Rock Tracker snapshot`.
2. Starting: next Monday 06:00. Repeat every 1 week, On these days: Monday. Set the time zone to the office time zone.
3. Add action: Excel Online (Business), "Run script".
   * Location: SharePoint site that holds the workbook. Document Library: the library. File: the deployed workbook. Script: `Snapshot`.
4. Under the flow settings turn on failure notifications to the director and name a backup owner (share the flow with a second person as co-owner).
5. Save, then Test, Manually. Confirm the run succeeded and that a second test adds nothing.

**C. Fallback: "Save snapshot" button (GPM, before steerco, or if Power Automate is blocked)**
1. On the About sheet select the cell reserved for the button. Automate tab, All Scripts, `Snapshot`, Run. (Excel desktop: Automate, Add button, pick `Snapshot` and place it on the About sheet.)
2. The GPM presses it once before steerco. Pressing twice is harmless.

Not verifiable outside Excel: script run, protection toggling and the flow. Walk the three checks above after every deploy.
