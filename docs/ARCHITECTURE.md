# Architecture

Owner: `architect`. Status: v2 for change request 1, 14 Oct 2026. Contract: `schema/workbook.schema.json` (version 2.1.0, schema format 2; v1.0.0 kept in `schema/history/`). Decisions: `docs/DECISIONS.md` 0002 to 0017.

## In one paragraph

Leads type only on their own rock tab. Every rock tab has the same fixed layout. Six read only consolidated sheets each hold one Excel 365 formula that stacks the matching block of every rock tab between `RockTemplate` and `RocksEnd` (a 3D `VSTACK` plus `FILTER`). The portal and the email read only those six sheets and the lookups. A scheduled Office Script appends the Rocks and Milestones rows to two snapshot tables every Monday, which is the history.

## Data model

```
 rock tab (one per rock, typed by the lead)            consolidated sheet (formula, read only)
 ┌──────────────────────────────────────┐
 │ row 2 hidden strip: profile, update, │ ──3D VSTACK──▶ Rocks       (PK RockID)
 │ key points, signals as one row       │                  ▲
 │ 3 Milestones block (15 slots)        │ ──3D VSTACK──▶ Milestones  (PK MilestoneKey, FK RockID)
 │ 4 Risks block      (10 slots)        │ ──3D VSTACK──▶ Risks       (PK RiskKey,      FK RockID)
 │ 5 Call outs block  (8 slots)         │ ──3D VSTACK──▶ CallOuts    (PK CallOutKey,   FK RockID)
 │ 6 Decisions block  (25 slots)        │ ──3D VSTACK──▶ Decisions   (PK DecisionKey,  FK RockID)
 │ 8 Teams block      (5 slots)         │ ──3D VSTACK──▶ Teams       (PK TeamKey,      FK RockID)
 └──────────────────────────────────────┘
                     snapshot.ts (Monday, or button) ──▶ RockSnapshots      (PK SnapshotID = date|RockID)
                                                      ──▶ MilestoneSnapshots (PK SnapshotID = date|MilestoneKey)
 lkp_People, lkp_ValueChains, lkp_Steercos (owner)       dropdowns on rock tabs, NextSteerco
 lkp_State, lkp_MilestoneStatus, lkp_LeadStatus, lkp_Commitment, lkp_Level, lkp_OpenClosed, lkp_YesNo, lkp_DecisionState (fixed)
```

One line per table:

| Sheet | Kind | One row per | Key | Read by |
| :--- | :--- | :--- | :--- | :--- |
| Rocks | consolidated | rock tab with a Rock ID | RockID | tabs 1 (message, key points), 2; email header, portfolio table, per rock section |
| Milestones | consolidated | milestone of an active rock | MilestoneKey (R03-M04) | tabs 2 (counts), 3 (timeline, filter, pop up); email development update and milestone tables |
| Risks | consolidated | risk of an active rock | RiskKey | tab 4; email key risks |
| CallOuts | consolidated | call out of an active rock | CallOutKey | tab 1; email key call outs |
| Decisions | consolidated | decision of any rock, requested or decided | DecisionKey | tabs 1 (RequestNo 1 to 5), 3.1, 5; email key call outs |
| Teams | consolidated | team of an active rock | TeamKey (R03-T02) | tab 2 resourcing; email per rock resourcing |
| RockSnapshots | history (Table) | active rock per snapshot day | date\|RockID | M3 look back |
| MilestoneSnapshots | history (Table) | milestone per snapshot day | date\|MilestoneKey | M3 look back by MC quarter |
| lkp_* | lookup (Table) | allowed value | Value (Name, Date) | dropdowns, portal colours |

Sheet order in the workbook: About, RockTemplate, rock tabs, RocksEnd, Rocks, Milestones, Risks, CallOuts, Decisions, Teams, RockSnapshots, MilestoneSnapshots, lookups.

## Rock tab layout

Columns: A key (narrow, grey), B labels and titles (wide), C values, D onward block columns. No merged cells; long text overflows to the right.

| Rows | Section | Who | Content |
| :--- | :--- | :--- | :--- |
| 1 | Title | formula | Rock ID · Rock name |
| 2 (hidden) | Strip | formula | the Rocks row: profile, update, key points and signals in Rocks column order |
| 3 | Guide | static | the 7 minute order of work |
| 5 to 17 | 1 Update and steerco message | lead, plus grey lines | 6 Update date, 7 State, 8 Main message, 9 to 11 key risks or attention points 1 to 3; grey: 12 open decision requests count, 13 to 17 decision requested 1 to 5 (from section 6) |
| 19 to 33 | 2 Signals | formula | 20 days since update, 21 data signal, 22 check the call, 23 outlook quarters, 24 committed y, 25 slipped x, 26 on plan, 27 delivered, 28 overdue, 29 open High risks, 30 High risks without action, 31 positions budgeted, 32 positions actual, 33 fill % |
| 35 to 51 | 3 Milestones | lead | 15 slots (rows 37 to 51): Title, Owner, Commitment, Start, Planned, Forecast, Actual, Lead status, Comment, KR link, ADO id, ADO link, Description, Detail 1 to 3; then grey Status, Slip weeks, Timeline date, MC quarter, In outlook, Visible, Overdue, RockID, Rock, GPM (columns A to AA) |
| 53 to 64 | 4 Risks | lead | 10 slots (55 to 64): Title, Likelihood, Impact, Key action, Action owner, Status; then grey Score, High, Needs action, RockID, Rock, GPM |
| 66 to 75 | 5 Call outs | lead | 8 slots (68 to 75): Text, Date, Status; then grey RockID, Rock, GPM |
| 77 to 103 | 6 Decisions | lead | 25 slots (79 to 103): Decision (one line), Steerco, Decide by, Choice point, Options, Outcome, Owner, Follow up; then grey State, Open request no., Due at next steerco, Open follow up, RockID, Rock, GPM |
| 105 to 114 | 7 Rock profile | owner | 106 Rock ID, name, value chain, lead, GPM, 111 Active, purpose, goals, 114 delivers |
| 116 to 122 | 8 Teams | lead | 5 slots (118 to 122): Team, Team lead, Budgeted, Actual; then grey Fill %, RockID, Rock, GPM |

Block column order on the rock tab equals the column order of the consolidated sheet, so the stack needs no reordering. Exact rows and formulas are in `rock_tab` of the schema; the generator never hard codes them.

Guard rails: sheet protection without password (entry cells unlocked, no row insert or delete), dropdowns from `lst_lkp_*` names (Decisions.SteercoDate as a warning, not a stop), date validation, whole number validation on Budgeted and Actual, URL validation on ADOLink (`format: url`: empty or starts with https://), a pink Rock ID when another tab uses the same ID, pink highlight for empty required cells on rows that have a title, and a pink row when a block row has data but no title. Columns with `number_format` (FillPct 0%, SlipWeeks 0.0) are formatted on the rock tab and the consolidated sheet.

## Consolidation

`Milestones!A2` (same pattern for Risks, CallOuts, Decisions, Teams):

```
=LET(d,VSTACK(RockTemplate:RocksEnd!$A$37:$AA$51),k,CHOOSECOLS(d,1),
     f,FILTER(d,ISTEXT(k)*(k<>""),""),IF(f=0,"",f))
```

`Rocks!A2` stacks row 2 of every rock tab without the zero wrap. Rules:
* A row reaches the portal only when its key is text: title present, Rock ID present, rock Active (decisions also when inactive).
* Empty cells come through VSTACK as 0; list blocks turn 0 back into blank. A real 0 in Teams Budgeted, Actual or FillPct also shows blank; the portal treats a blank count as 0. The Rocks strip returns "" itself, so real zero counts and totals survive.
* RockTemplate is the first sheet of the 3D range and contributes nothing (no Rock ID). RocksEnd is empty in all ranges.
* Rock tab names are free: no formula refers to them. Renaming RockTemplate or RocksEnd is safe (Excel updates the reference); moving or deleting them is not.
* Spill cells take the number format of the target cells, so the generator formats date and number columns on the consolidated sheets.
* Generator detail: dynamic array functions are written with `_xlfn.` prefixes and the anchor cell gets dynamic array cell metadata; fallback `scripts/office/setup.ts`.
* Plan C (DECISIONS 0002) still applies if Excel rejects the 3D reference; it now rebuilds six Tables.

## Computed rules

All in the schema (`excel` plus `rule`), mirrored in `scripts/rock_model.py`. Named formulas: HighRiskMin 6, StaleDays 14, MCQuarterStart (first day of the current quarter), MCQuarterEnd, OutlookEnd (last day of the next quarter), CurrentMCQuarter and NextMCQuarter (labels), NextSteerco.

| Rule | Definition |
| :--- | :--- |
| MC quarter label | shift the date back 3 months, then `"MC"&RIGHT(YEAR(d),2)&"Q"&INT((MONTH(d)+2)/3)`: Oct 2026 MC26Q3, Jan 2027 MC26Q4, Apr 2027 MC27Q1. Locale safe (no TEXT year codes) |
| Milestone Status | first match: Lead status Completed gives Completed; Lead status On hold; commitment not Committed gives Not committed; forecast later than planned gives Slipped; Lead status On watch; else On plan. Empty forecast means on the planned date |
| SlipWeeks | (forecast minus planned) / 7, one decimal, Slipped only |
| TimelineDate | actual, else forecast, else planned; empty when none. ActualDate is recorded, optional, and does not set the status |
| MCQuarter | MC quarter of TimelineDate; empty when no date |
| InOutlook | planned or timeline date between MCQuarterStart and OutlookEnd (counts and data signal) |
| Visible | Completed: hidden when the actual date (or, when empty, the planned date) is before today, else InOutlook. Not Completed: shown when InOutlook, undated, or date passed (overdue). Roadmap reads Visible Yes |
| Overdue | committed, not Completed or On hold, timeline date before today |
| Risk Score, High | likelihood times impact (1 to 3 each); High when 6 or more |
| NeedsAction | High, not Closed, key action or action owner empty |
| Milestones x of y | y MilestonesCommitted = committed and InOutlook; x MilestonesSlipped = Slipped and InOutlook; MilestonesOnPlan = On plan, On watch or Completed; MilestonesCompleted; MilestonesOverdue = Overdue, any quarter |
| Positions | PositionsBudgeted and PositionsActual = sums over keyed Teams rows; FillPct = actual / budgeted, empty when budgeted is 0; per team FillPct the same |
| Update age, Stale | today minus update date; Stale when empty or over 14 days |
| Data signal | Off track: a Slipped milestone planned this MC quarter is forecast after its end; At risk: slipped x, overdue or High risks without action above 0; else On track |
| CheckCall | data signal worse than the lead's State (order On track, At risk, Off track) |
| DecisionState | Requested until Outcome is filled in, then Decided |
| RequestNo | position of a Requested row among the rock's Requested rows by slot; section 1 lines and tab 1 show 1 to 5 |
| DueNextSteerco | Requested and (raised for the next steerco or decide by on or before it) |
| OpenFollowUp | Decided and FollowUp not Closed; empty FollowUp counts as Open (tab 5 spotlight) |

Blank safety: every calculated cell returns "" when its row has no key, wraps dates in `N()` so an empty date is 0, and never divides by an empty value. Empty Status on risks and call outs, and empty FollowUp on decided decisions, counts as Open. Rock tab formulas avoid LET, FILTER and other functions LibreOffice 24.2 lacks (RequestNo uses SUMPRODUCT, the section 1 lines INDEX and MATCH), so the recalc test covers them.

About sheet checks (schema `about.checks`): rock tabs found, duplicate rock IDs, next steerco date missing, choice point mismatches in both directions, Completed milestones without an Actual date (warning), open requests beyond the 5 the portal shows.

## Decision log (DECISIONS 0012)

One table does request, outcome and log. The lead types a request once, as one line, in section 6 (Decision, Steerco, Decide by, and for a choice point Choice point Yes and Options). Section 1 shows the first 5 open requests as grey lines at once, and tab 1 reads Decisions with RequestNo 1 to 5. After steerco the lead fills Outcome, Owner and Follow up on the same row; DecisionState turns Decided and the row appears on tab 5. Tab 3.1 reads ChoicePoint Yes and Requested. Nothing is copied, cleared or typed twice; the log is live.

## History

`scripts/office/snapshot.ts`: reads the Rocks and Milestones spills, keeps active rocks, appends to `tbl_RockSnapshots` and `tbl_MilestoneSnapshots`, skips keys already present for today (pressing twice is harmless), unprotects and reprotects the two sheets. Copies MilestonesCommitted, MilestonesSlipped, MilestonesCompleted, PositionsBudgeted, PositionsActual for rocks; ActualDate and MCQuarter for milestones. Scheduled by a Power Automate flow (Recurrence, Monday 06:00), owned by the director; fallback a "Save snapshot" button. Volume at 15 rocks: about 800 rock rows and 6,000 milestone rows a year.

## How the portal and the email consume the data (brief)

* The portal reads only Rocks, Milestones, Risks, CallOuts, Decisions, Teams and the lookups, never rock tabs. One tab per section in steerco order: 1, 2, 3, 3.1, 4, 5, full list. Every tab filters on Rocks.Active = Yes and can filter on RockID or GPM, present on every row. Light and dark mode from the same tokens (DECISIONS 0016).
  * Tab 1: rock header (RockName, Lead, GPM, ValueChain, Purpose, Goals, Delivers) when filtered to one rock; Rocks.MainMessage; Rocks.Attention1 to 3; Decisions Requested with RequestNo 1 to 5 (DueNextSteerco first); CallOuts open.
  * Tab 2: Rocks State, DataSignal, CheckCall, Milestones x of y, MilestonesOverdue, OpenHighRisks, PositionsActual of PositionsBudgeted and FillPct; Teams list per rock.
  * Tab 3: Milestones with Visible Yes; filter on MCQuarter, default Rocks.CurrentMCQuarter and NextMCQuarter; timeline at TimelineDate with planned to forecast slip lines; undated in "Not dated yet"; Overdue marked; pop up with Owner, Description, StartDate, PlannedDate, ForecastDate, Status (Completed in the done stage colour), Detail1 to 3 and ADOLink when present.
  * Tab 3.1: Decisions with ChoicePoint Yes and Requested. Tab 4: Risks by Likelihood and Impact. Tab 5: Decisions Decided.
  * Spotlights rely on precomputed flags (DueNextSteerco, NeedsAction, OpenFollowUp, State, MilestonesOnPlan of MilestonesCommitted) so Cowork needs no date logic.
* The email (M2) reads the same six sheets: header from Rocks and lkp_People.Role; portfolio table from Rocks (milestones slipped x of y, positions actual of budgeted); call outs from Decisions Requested, Milestones Overdue, CallOuts open; development update from Milestones Status counts, releases = Completed milestones with ActualDate in the last 14 days, mean SlipWeeks; key risks from Rocks.Attention1 to 3 and High risks; per rock section with Teams and the milestone table. Mechanism decided in T21.

## Upkeep per role mapped to fields

| Role | Fields they touch | When |
| :--- | :--- | :--- |
| Lead | Section 1 (UpdateDate, State, MainMessage, Attention1 to 3); Milestones ForecastDate, Comment, LeadStatus (Completed, On hold, On watch) and ActualDate where they moved; Risks rows that changed; CallOuts; Decisions (raise; after steerco Outcome, Owner, FollowUp, and Commitment and PlannedDate on milestones); Teams when positions change | every one or two weeks, 7 minutes |
| Lead (one off per milestone) | Owner, StartDate, Description, Detail1 to 3, ADO id and link | when a milestone is added; part of the first load |
| GPM | none in steady state; presses Save snapshot only if the flow is off | before steerco |
| Workbook owner | Section 7 profile of new rocks, Active = No to close, lkp_People, lkp_ValueChains, lkp_Steercos | quarterly |
| Director | Power Automate flow (one off) | deploy |
| Executives | nothing | |

## Permissions

SharePoint site: edit for leads, GPMs, workbook owner and director; read for executives. Excel cannot restrict editing per tab per person; protection is a guard rail and version history is the backstop. Staffing is counts per team only and people are named at role level (team lead names only, no HR detail).

## Data flows and refresh

Lead edits rock tab, formulas recalculate at once, consolidated sheets update, the portal shows it on its next refresh. Monday 06:00 the flow appends snapshots. No copy step anywhere.

## Limits

* Capacity per rock: 15 milestones, 10 risks, 8 call outs, 25 decisions, 5 teams. Up to about 30 rock tabs is fine for the formulas; PRD assumes 15.
* Concurrency: co-authoring merges per cell; two leads on different tabs never collide. Avoid anything that locks the file: no Power Query, no macros, no external links.
* Requires Excel 365 (web or current desktop) for dynamic arrays. Older desktop Excel shows the consolidated sheets as errors.
* Office Scripts and Power Automate must be allowed by the tenant; if not, history falls back to the button.

## Evolving the schema safely

* Rename nothing that is an identifier: consolidated sheet and column names, RockTemplate, RocksEnd, named formulas, lookup names. Change request 1 renamed Epic to Milestone before any deployment, the last free rename.
* Adding a column to a block or moving a section changes cell addresses on every rock tab: schema version bump, keep the old schema in `schema/history/`, rebuild, and `--from` migration that reads the old layout by its schema version and writes the new one (schema `migration` describes the mapping).
* Adding a consolidated column is safe for the portal only when appended at the end of a block.
* Every change: schema first, then generator, tests, DECISIONS entry with migration note.
