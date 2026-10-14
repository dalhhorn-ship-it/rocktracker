# Architecture

Owner: `architect`. Status: v1 for M1, 14 Oct 2026. Contract: `schema/workbook.schema.json` (version 1.0.0, schema format 2). Decisions: `docs/DECISIONS.md` 0002 to 0009.

## In one paragraph

Leads type only on their own rock tab. Every rock tab has the same fixed layout. Five read only consolidated sheets each hold one Excel 365 formula that stacks the matching block of every rock tab between `RockTemplate` and `RocksEnd` (a 3D `VSTACK` plus `FILTER`). The portal and the email read only those five sheets and the lookups. A scheduled Office Script appends the Rocks and Epics rows to two snapshot tables every Monday, which is the history.

## Data model

```
 rock tab (one per rock, typed by the lead)            consolidated sheet (formula, read only)
 ┌──────────────────────────────────────┐
 │ row 2 hidden strip: profile, update, │ ──3D VSTACK──▶ Rocks       (PK RockID)
 │ signals as one row                   │                  ▲
 │ 3 Epics block      (15 slots)        │ ──3D VSTACK──▶ Epics       (PK EpicKey,    FK RockID)
 │ 4 Risks block      (10 slots)        │ ──3D VSTACK──▶ Risks       (PK RiskKey,    FK RockID)
 │ 5 Call outs block  (8 slots)         │ ──3D VSTACK──▶ CallOuts    (PK CallOutKey, FK RockID)
 │ 6 Decisions block  (25 slots)        │ ──3D VSTACK──▶ Decisions   (PK DecisionKey,FK RockID)
 └──────────────────────────────────────┘
                     snapshot.ts (Monday, or button) ──▶ RockSnapshots (PK SnapshotID = date|RockID)
                                                      ──▶ EpicSnapshots (PK SnapshotID = date|EpicKey)
 lkp_People, lkp_ValueChains, lkp_Steercos (owner)       dropdowns on rock tabs, NextSteerco
 lkp_State, lkp_EpicStatus, lkp_LeadStatus, lkp_Commitment, lkp_Level, lkp_OpenClosed, lkp_YesNo, lkp_DecisionState (fixed)
```

One line per table:

| Sheet | Kind | One row per | Key | Read by |
| :--- | :--- | :--- | :--- | :--- |
| Rocks | consolidated | rock tab with a Rock ID | RockID | tabs 1, 2; email header, portfolio table, per rock section |
| Epics | consolidated | epic of an active rock | EpicKey (R03-E04) | tabs 2 (counts), 3; email development update and epic tables |
| Risks | consolidated | risk of an active rock | RiskKey | tabs 1 (top risks), 4; email key risks |
| CallOuts | consolidated | call out of an active rock | CallOutKey | tab 1; email key call outs |
| Decisions | consolidated | decision of any rock, requested or decided | DecisionKey | tabs 1, 3.1, 5; email key call outs |
| RockSnapshots | history (Table) | active rock per snapshot day | date\|RockID | M3 look back |
| EpicSnapshots | history (Table) | epic per snapshot day | date\|EpicKey | M3 look back |
| lkp_* | lookup (Table) | allowed value | Value (Name, Date) | dropdowns, portal colours |

Sheet order in the workbook: About, RockTemplate, rock tabs, RocksEnd, Rocks, Epics, Risks, CallOuts, Decisions, RockSnapshots, EpicSnapshots, lookups.

## Rock tab layout

Columns: A key (narrow, grey), B labels and titles (wide), C values, D onward block columns. No merged cells; long text overflows to the right.

| Rows | Section | Who | Content |
| :--- | :--- | :--- | :--- |
| 1 | Title | formula | Rock ID · Rock name |
| 2 (hidden) | Strip | formula | the Rocks row: profile, update and signals in Rocks column order |
| 3 | Guide | static | the 7 minute order of work |
| 5 to 10 | 1 Update | lead | Update date, State, Main message, Positions planned, Positions filled |
| 12 to 21 | 2 Signals | formula | Days since update, Data signal, Check the call, committed y, slipped x, on plan, delivered, open High risks, High risks without action |
| 23 to 39 | 3 Epics | lead | 15 slots: Title, ADO id, Commitment, Planned, Forecast, Lead status, Comment, KR link; then grey Status, Slip weeks, In window, Overdue, RockID, Rock, GPM |
| 41 to 52 | 4 Risks | lead | 10 slots: Title, Likelihood, Impact, Key action, Action owner, Status, Top risk; then grey Score, High, Needs action, RockID, Rock, GPM |
| 54 to 63 | 5 Call outs | lead | 8 slots: Text, Date, Status; then grey RockID, Rock, GPM |
| 65 to 91 | 6 Decisions | lead | 25 slots: Decision, Steerco, Decide by, Choice point, Options, Outcome, Owner, Follow up; then grey State, Due at next steerco, Open follow up, RockID, Rock, GPM |
| 93 to 102 | 7 Rock profile | owner | Rock ID, name, value chain, lead, GPM, Active, purpose, goals, delivers |

Block column order on the rock tab equals the column order of the consolidated sheet, so the stack needs no reordering. Exact rows and formulas are in `rock_tab` of the schema; the generator never hard codes them.

Guard rails: sheet protection without password (entry cells unlocked, no row insert or delete), dropdowns from `lst_lkp_*` names (Decisions.SteercoDate as a warning, not a stop, so a lead can enter a steerco not listed yet), date validation, a pink Rock ID when another tab uses the same ID, pink highlight for empty required cells on rows that have a title, and a pink row when a block row has data but no title (it would be invisible to the portal).

## Consolidation

`Epics!A2` (same pattern for Risks, CallOuts, Decisions):

```
=LET(d,VSTACK(RockTemplate:RocksEnd!$A$25:$P$39),k,CHOOSECOLS(d,1),
     f,FILTER(d,ISTEXT(k)*(k<>""),""),IF(f=0,"",f))
```

`Rocks!A2` stacks row 2 of every rock tab without the zero wrap. Rules:
* A row reaches the portal only when its key is text: title present, Rock ID present, rock Active (decisions also when inactive).
* Empty cells come through VSTACK as 0; list blocks turn 0 back into blank. The Rocks strip returns "" itself, so real zero counts survive.
* RockTemplate is the first sheet of the 3D range and contributes nothing (no Rock ID). RocksEnd is empty in all ranges.
* Rock tab names are free: no formula refers to them. Renaming RockTemplate or RocksEnd is safe (Excel updates the reference); moving or deleting them is not.
* Spill cells take the number format of the target cells, so the generator formats date columns on the consolidated sheets.
* Generator detail: dynamic array functions are written with `_xlfn.` prefixes (`_xlfn.LET`, `_xlpm.` parameters, `_xlfn.VSTACK`, `_xlfn._xlws.FILTER`, `_xlfn.CHOOSECOLS`, `_xlfn.MINIFS`) and the anchor cell gets dynamic array cell metadata; fallback `scripts/office/setup.ts`.
* If Excel rejects the 3D reference inside VSTACK (go or no go Thu 15 Oct 12:00), plan C in DECISIONS 0002 applies: `consolidate.ts` rebuilds five real Tables from the rock tabs every 30 minutes, with the same sheet and column names, so the portal and email contract does not change.

## Computed rules

All in the schema (`excel` plus `rule`), mirrored in `scripts/rock_model.py`. Named formulas: HighRiskMin 6, StaleDays 14, QuarterStart, QuarterEnd, WindowStart (quarter start), WindowEnd (end of next quarter), NextSteerco (first lkp_Steercos date on or after today).

| Rule | Definition |
| :--- | :--- |
| Epic Status | first match: Lead status Delivered; Lead status On hold; commitment not Committed gives Not committed; forecast later than planned gives Slipped; Lead status On watch; else On plan. Empty forecast means on the planned date |
| SlipWeeks | (forecast minus planned) / 7, one decimal, Slipped only |
| InWindow | planned or forecast date between WindowStart and WindowEnd |
| Overdue | committed, not Delivered or On hold, forecast (or planned) before today |
| Risk Score, High | likelihood times impact (1 to 3 each); High when 6 or more |
| NeedsAction | High, not Closed, key action or action owner empty |
| Epics x of y | y EpicsCommitted = committed and in window; x EpicsSlipped = Slipped and in window; EpicsOnPlan = On plan, On watch or Delivered (tab 3 spotlight, so delivering never lowers the ratio); EpicsDelivered |
| Positions x of y | PositionsFilled of PositionsPlanned, both typed |
| Update age, Stale | today minus update date; Stale when empty or over 14 days |
| Data signal | Off track: a Slipped epic planned this quarter is forecast after quarter end; At risk: slipped x > 0 or a High risk without action; else On track |
| CheckCall | data signal worse than the lead's State (order On track, At risk, Off track) |
| DecisionState | Requested until Outcome is filled in, then Decided |
| DueNextSteerco | Requested and (raised for the next steerco or decide by on or before it) |
| OpenFollowUp | Decided and FollowUp not Closed; empty FollowUp counts as Open (tab 5 spotlight) |

Blank safety: every calculated cell returns "" when its row has no key, wraps dates in `N()` so an empty date is 0, and never divides by an empty value. Empty Status on risks and call outs, and empty FollowUp on decided decisions, counts as Open.

About sheet checks (schema `about.checks`): rock tabs found, duplicate rock IDs, next steerco date missing, and choice point mismatches in both directions between epic Commitment and open choice point decisions. The Decisions row is authoritative for tab 3.1; the epic Commitment drives the roadmap colour on tab 3.

## History

`scripts/office/snapshot.ts`: reads the Rocks and Epics spills, keeps active rocks, appends to `tbl_RockSnapshots` and `tbl_EpicSnapshots`, skips keys already present for today (pressing twice is harmless), unprotects and reprotects the two sheets. Scheduled by a Power Automate flow (Recurrence, Monday 06:00, action "Run script" on the SharePoint file), owned by the director. Fallback: the same script behind a "Save snapshot" button on the About sheet, pressed by the GPM before steerco. Volume at 15 rocks: about 800 rock rows and 6,000 epic rows a year.

## How the portal and the email consume the data (brief)

* The portal (later phase, spec in `portal/portal.spec.json`) reads only Rocks, Epics, Risks, CallOuts, Decisions and the lookups, never rock tabs. Every tab filters on Rocks.Active = Yes and can filter on RockID or GPM, present on every row. Tab 1 reads a rock header (RockName, Lead, GPM, ValueChain, Purpose, Goals, Delivers) when filtered to one rock, Rocks.MainMessage, Risks TopRisk, CallOuts, Decisions Requested; tab 2 Rocks state and signals; tab 3 Epics in window; tab 3.1 Decisions with ChoicePoint Yes and Requested; tab 4 Risks by Likelihood and Impact; tab 5 Decisions Decided. Spotlights rely on precomputed flags (DueNextSteerco, NeedsAction, OpenFollowUp, State, EpicsOnPlan of EpicsCommitted) so Cowork needs no date logic.
* The email (M2) reads the same five sheets: header from Rocks and lkp_People.Role; portfolio table from Rocks; call outs from Decisions Requested, Epics Overdue, CallOuts open; development update from Epics Status counts, Delivered with forecast in the last 14 days, mean SlipWeeks; risks from Risks Top or High; per rock section opens with RockName, ValueChain, Purpose, Goals and Delivers, then state, resourcing, headline and the epic table from Epics. Mechanism decided in T21.

## Upkeep per role mapped to fields

| Role | Fields they touch | When |
| :--- | :--- | :--- |
| Lead | Section 1 (UpdateDate, State, MainMessage, PositionsPlanned, PositionsFilled); Epics ForecastDate, Comment, LeadStatus where they moved; Risks rows that changed; CallOuts; Decisions (raise; after steerco Outcome, Owner, FollowUp, and Commitment and PlannedDate on epics) | every one or two weeks, 7 minutes |
| GPM | none in steady state; presses Save snapshot only if the flow is off | before steerco |
| Workbook owner | Section 7 profile of new rocks, Active = No to close, lkp_People, lkp_ValueChains, lkp_Steercos | quarterly |
| Director | Power Automate flow (one off) | deploy |
| Executives | nothing | |

## Permissions

SharePoint site: edit for leads, GPMs, workbook owner and director; read for executives. Excel cannot restrict editing per tab per person; protection is a guard rail and version history is the backstop. Staffing is counts only and people are named at role level.

## Data flows and refresh

Lead edits rock tab, formulas recalculate at once, consolidated sheets update, the portal shows it on its next refresh. Monday 06:00 the flow appends snapshots. No copy step anywhere.

## Limits

* Capacity per rock: 15 epics, 10 risks, 8 call outs, 25 decisions. Up to about 30 rock tabs is fine for the formulas; PRD assumes 15.
* Concurrency: co-authoring merges per cell; two leads on different tabs never collide. Avoid anything that locks the file: no Power Query, no macros, no external links.
* Requires Excel 365 (web or current desktop) for dynamic arrays. Older desktop Excel shows the consolidated sheets as errors.
* Office Scripts and Power Automate must be allowed by the tenant; if not, history falls back to the button.

## Evolving the schema safely

* Rename nothing that is an identifier: consolidated sheet and column names, RockTemplate, RocksEnd, named formulas, lookup names.
* Adding a column to a block or moving a section changes cell addresses on every rock tab: schema version bump, rebuild, and `--from` migration that reads the old layout by the old schema version and writes the new one. From M2 the generator stores the layout version on each rock tab (hidden cell) and keeps old schemas in `schema/history/`.
* Adding a consolidated column is safe for the portal only when appended at the end of a block.
* Every change: schema first, then generator, tests, DECISIONS entry with migration note.
