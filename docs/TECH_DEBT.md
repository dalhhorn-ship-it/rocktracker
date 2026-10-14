# Tech Debt Overview

Owner: `developer`. Updated after every task. Entries TD01 to TD08 recorded by the architect at design time (review round 1, 14 Oct 2026).

Open: 8 (high 1, medium 4, low 3). Resolved: 0.

## Open

| ID | Description | Impact | Effort | Proposed fix | Added |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TD01 | 3D reference inside VSTACK and dynamic array metadata written by openpyxl are unverified in Excel for the web (DECISIONS 0002, 0003) | high | small (spike) | PLAN T05 user check by Thu 15 Oct 12:00; fallbacks A2 `setup.ts`, plan C `consolidate.ts`, plan C2 tab list formula | 14 Oct 2026 |
| TD02 | 25 decision slots per rock and no archive; the decision log fills in about a year (DECISIONS 0004) | medium | medium | M3 T30: archive Decided rows into a history table before the slots run out; About check on slots left | 14 Oct 2026 |
| TD03 | Fixed capacity per rock tab (15 epics, 10 risks, 8 call outs, 25 decisions); more rows need a schema change and a layout migration | medium | medium | M2 T26 layout versioned `--from`; leads reuse slots only for closed items | 14 Oct 2026 |
| TD04 | Snapshot Power Automate flow runs under the director's account; it stops if the account is disabled or loses access (DECISIONS 0007) | medium | small | DEPLOY names a backup owner; move the flow to a service account if the tenant allows; button fallback | 14 Oct 2026 |
| TD05 | The "Save snapshot" button on the About sheet is a manual one off step in Excel; the generator cannot create Office Script buttons | low | small | Steps in DEPLOY and README; checklist item in the deploy test run | 14 Oct 2026 |
| TD06 | Sheet protection has no password: it is a guard rail against inserted rows, not security; any editor can change any rock tab | medium | none in Excel | SharePoint permissions limit editors to leads, GPMs, owner and director; version history as backstop (ARCHITECTURE Permissions) | 14 Oct 2026 |
| TD07 | Slot based keys: a lead who reuses an epic slot for a different epic mixes two epics in EpicSnapshots history (titles are kept) | low | small | Guide rule "a slot is one epic for life"; M3 look back groups by key and title | 14 Oct 2026 |
| TD08 | Excel formulas and the Python mirror (`rock_model.py`) can drift; consolidation cells cannot be recalculated outside Excel | low | small | T09 LibreOffice comparison for all rock tab formulas; one manual Excel check per release in DEPLOY | 14 Oct 2026 |

## Resolved

| ID | Description | Resolved on | How |
| :--- | :--- | :--- | :--- |
