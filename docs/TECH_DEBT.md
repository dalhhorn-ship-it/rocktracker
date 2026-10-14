# Tech Debt Overview

Owner: `developer`. Updated after every task. Entries TD01 to TD08 recorded by the architect at design time (review round 1, 14 Oct 2026).

Open: 17 (high 1, medium 6, low 10). Resolved: 2.

## Open

| ID | Description | Impact | Effort | Proposed fix | Added |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TD09 | Dynamic array metadata (`cm`, `xl/metadata.xml`) is patched into the xlsx by `mark_dynamic_arrays` from knowledge of the file format; tests prove structure and LibreOffice opening, not Excel behaviour. T07 now reuses the helper for the five consolidated sheets; `scripts/build_spike.py` stays as the throwaway spike file | medium | small | Keep the spike result in DECISIONS after the user check (Thu 15 Oct 12:00); delete `build_spike.py` once the path is settled | 14 Oct 2026 |
| TD01 | 3D reference inside VSTACK and dynamic array metadata written by openpyxl are unverified in Excel for the web (DECISIONS 0002, 0003) | high | small (spike) | PLAN T05 user check by Thu 15 Oct 12:00; fallbacks A2 `setup.ts`, plan C `consolidate.ts`, plan C2 tab list formula | 14 Oct 2026 |
| TD02 | 25 decision slots per rock and no archive; the decision log fills in about a year (DECISIONS 0004) | medium | medium | M3 T30: archive Decided rows into a history table before the slots run out; About check on slots left | 14 Oct 2026 |
| TD03 | Fixed capacity per rock tab (15 epics, 10 risks, 8 call outs, 25 decisions); more rows need a schema change and a layout migration | medium | medium | M2 T26 layout versioned `--from`; leads reuse slots only for closed items | 14 Oct 2026 |
| TD04 | Snapshot Power Automate flow runs under the director's account; it stops if the account is disabled or loses access (DECISIONS 0007) | medium | small | DEPLOY names a backup owner; move the flow to a service account if the tenant allows; button fallback | 14 Oct 2026 |
| TD05 | The "Save snapshot" button on the About sheet is a manual one off step in Excel; the generator cannot create Office Script buttons | low | small | Steps in DEPLOY and README; checklist item in the deploy test run | 14 Oct 2026 |
| TD06 | Sheet protection has no password: it is a guard rail against inserted rows, not security; any editor can change any rock tab | medium | none in Excel | SharePoint permissions limit editors to leads, GPMs, owner and director; version history as backstop (ARCHITECTURE Permissions) | 14 Oct 2026 |
| TD07 | Slot based keys: a lead who reuses an epic slot for a different epic mixes two epics in EpicSnapshots history (titles are kept) | low | small | Guide rule "a slot is one epic for life"; M3 look back groups by key and title | 14 Oct 2026 |
| TD08 | Excel formulas and the Python mirror (`rock_model.py`) can drift; consolidation cells cannot be recalculated outside Excel | low | small | T09 LibreOffice comparison for all rock tab formulas; one manual Excel check per release in DEPLOY | 14 Oct 2026 |
| TD10 | `snapshot.ts` is verified only by `tsc` against a minimal declaration file and by the Python mirror; the Office Scripts runtime (addRows, protect/unprotect, used range of the spills, serial dates) is untested | low | small | One manual run in the real workbook per release (DEPLOY section 6, steps A3 and B5); run the script inside the deploy test run | 14 Oct 2026 |
| TD11 | `data/sample.json` is hand generated and snapshot rows are computed with a small status function that duplicates the schema rules. The T07 builder now reads the new shape (rocks with block lists, lookups, snapshots) | low | S | T08 `rock_model.py` recomputes snapshot rows and a test compares them with the stored ones | 14 Oct 2026 |
| TD13 | `rock_model.py` raises on a Likelihood, Impact or State value outside the lookups where Excel would show an error value; dropdowns prevent it in the workbook | low | S | Decide in review whether the mirror should return "" instead | 14 Oct 2026 |
| TD14 | Excel only behaviour that nothing here can check: ANCHORARRAY (`Rocks!$A$2#`) inside the duplicate Rock ID conditional format, defined names as dropdown sources written without a leading equals sign, the warning style steerco dropdown, 3D `VSTACK` itself (TD01), pink conditional formats using `start_color` and `end_color`, protection options on rock tabs after Duplicate | medium | S | Part of the user spike and deploy test run: open the deployment file in Excel for the web, duplicate RockTemplate, type a duplicate Rock ID, pick an unlisted steerco date, press Save snapshot; add results to DEPLOY | 14 Oct 2026 |
| TD16 | `--from` migration reads rock tabs by the current schema layout (cell addresses), with no layout version stored on the tab; a future layout change would copy the wrong cells | low | M | M2 T26: store the layout version in a hidden cell on every rock tab and read old layouts from `schema/history/` (see TD03) | 14 Oct 2026 |
| TD17 | Dropdown lists are fixed ranges (lookup rows 2 to 200), so Excel shows blank entries at the end of every list; consolidated and history sheets only format the first 2000 rows | low | S | Switch the defined names to table structured references once the T05 spike confirms Excel accepts them in validation | 14 Oct 2026 |
| TD18 | About checks that read the consolidated sheets (`INDEX(Rocks!$A$2#,,n)` with UNIQUE and FILTER) are written by `check_formula` but never evaluated: LibreOffice cannot calculate the 3D VSTACK, so the tests only prove the formulas are present and that the standalone check calculates | low | S | Add the About checks to the Excel for the web spike and deploy test run (TD14); expect 0 on the sample except rock count | 14 Oct 2026 |
| TD19 | `tests/test_recalc.py` (T09) cannot freeze TODAY() in LibreOffice, so it compares with the model at the machine date; a test run across midnight or a changed date rule could differ. Earlier sample snapshots (before the latest) cannot be recomputed from today's rock tabs, so they get a consistency check only (TD11 is covered for the latest snapshot) | low | small | Install `faketime` in CI and freeze to the sample date; or regenerate older snapshots from dated rock data | 14 Oct 2026 |

## Resolved

| ID | Description | Resolved on | How |
| :--- | :--- | :--- | :--- |
| TD12 | `rock_model.py` loader `rocks_from_workbook` was tested only on a minimal workbook | 14 Oct 2026 | T07: the `rows` fixture in `tests/conftest.py` now loads the generated sample workbook with it and `tests/test_workbook.py` checks the result against the schema |
| TD15 | About sheet was minimal | 14 Oct 2026 | T11: `build_about` now writes checks, update guide, add and close rock steps, rules and definitions from `about` in the schema, in both the sample and deployment workbook; `tests/test_about.py` |
