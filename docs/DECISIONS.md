# Decision Log

Owner: `architect`. Newest first.

## 0016 Portal for change request 1: tab per section, milestone pop up, MC quarter filter, dark mode (14 Oct 2026)
* Context: PRD change request 1 item 6. `design/DESIGN_SYSTEM.md` and `design/tokens.css` have no dark mode tokens.
* Decision: the portal has one tab per section in steerco order (1, 2, 3, 3.1, 4, 5, full list). Tab 3 reads Milestones where Visible is Yes, offers a filter on MCQuarter (default CurrentMCQuarter and NextMCQuarter from Rocks) and opens a pop up per milestone (Owner, Description, StartDate, PlannedDate, ForecastDate, Status, Detail1 to Detail3, ADOLink as a link only when it starts with https://). Teams show on tab 2 under the resourcing lens, not as a tab of their own. Dark mode is a second token set under `[data-theme="dark"]` and `prefers-color-scheme: dark`, same names, same hues: crimson stays the only emphasis (lightened to `#E06A93` for contrast), stage colours keep their meaning. Full palette in PLAN T44.
* Consequences: new portal element kinds (pop up, MC quarter filter, theme switch) need generator support in `build_handoff.py` and checks in `test_portal.py`. No schema impact beyond the columns in 0011.

## 0015 Rock tab re layout for schema 2.0.0 (14 Oct 2026)
* Context: new fields in section 1, wider Milestones block, new Teams block. Sections must not overlap; the strip row and the 3D VSTACK pattern stay (0002, 0004).
* Decision: rows 1 title, 2 hidden strip, 3 guide; 5 to 17 section 1 Update and steerco message; 19 to 33 section 2 Signals; 35 to 51 section 3 Milestones (15 slots, columns A to AA); 53 to 64 section 4 Risks (10); 66 to 75 section 5 Call outs (8); 77 to 103 section 6 Decisions (25); 105 to 114 section 7 Rock profile; 116 to 122 section 8 Teams (5). In the Milestones block the cells a lead touches weekly (dates, lead status, comment) sit left of the set up once texts (ADO, description, details).
* Consequences: every cell address on the rock tab moves, so the version is 2.0.0 and v1 is kept in `schema/history/`. Migration note in schema `migration`. No live v1 workbook exists, so `--from` from v1 is a safety net, not a deploy step.

## 0014 Teams replace rock level positions (14 Oct 2026)
* Context: PRD change request 1 item 5.
* Decision: section 8 Teams, a block of 5 slots: TeamName, TeamLead (free text, no lookup, so no admin), Budgeted, Actual, calculated FillPct. Rock totals PositionsBudgeted, PositionsActual and FillPct are calculated in Signals and carried on Rocks; snapshots keep PositionsBudgeted and PositionsActual. A sixth consolidated sheet `Teams` (key RockID-T01) feeds the teams list on tab 2 and the email per rock section. Fill % is stored as a fraction with number format 0%.
* Options: rock totals only (no Teams sheet) was cheaper but tab 2 and the email could not show the team breakdown the user asked for.
* Consequences: a real 0 in Budgeted or Actual shows blank on the Teams sheet (VSTACK zero wrap); the portal reads blank counts as 0. Rock totals on Rocks are exact.

## 0013 Key risks or attention points replace the Top risk flag (14 Oct 2026)
* Context: PRD change request 1 item 4.
* Decision: three typed one line fields Attention1 to Attention3 in section 1, carried on Rocks. Risks.TopRisk is dropped. The lines are free text and not linked to risk rows, because an attention point need not be a risk.
* Consequences: one fewer column per risk; tab 1 and the email key risks read Rocks.Attention1 to 3. `--from` v1 copies the titles of up to 3 open top risks into these lines.

## 0012 Decision log with 5 one line requests: one Decisions table, section 1 shows the first 5 open requests (14 Oct 2026)
* Context: PRD change request 1 item 4: section 1 holds up to 5 one line decision requests, and the decision log (tab 5) and choice points (tab 3.1) must keep working with nothing typed twice.
* Options considered:
  1. Five typed request lines in section 1, each with Outcome and Follow up cells; the weekly snapshot script appends decided lines to a `DecisionLog` history table and the lead then clears the line. Cost: the log lags up to a week; it depends on Power Automate running (a failed flow plus a cleared line loses a decision); a follow up closed after the line is cleared can never be closed in the log, so the tab 5 spotlight goes stale; keys must survive slot reuse; leads must remember a clear rule.
  2. Five typed request lines in section 1 plus the existing Decisions block as the log. Every decision typed twice. Rejected.
  3. Keep the Decisions block (section 6) as the single table for request, outcome and follow up, as approved in M1a. Add a calculated RequestNo (position of a Requested row among the rock's open requests) and five grey lines in section 1 that show the decision text of RequestNo 1 to 5, plus a count of open requests. Tab 1 reads Decisions with RequestNo 1 to 5.
* Decision: option 3. It is the lowest upkeep: each decision is typed once, the outcome goes on the same row, nothing is ever cleared or copied, the log is live, and choice point support (ChoicePoint, Options, DecideBy) for tab 3.1 is unchanged. The 5 cap is enforced by display (section 1, tab 1) plus an About check that counts open requests beyond 5.
* Consequences: the lead types a request in section 6, one screen below section 1, and sees it appear in section 1 at once. The 25 slot limit per rock remains (TD02, M3 archive). If the user insists on typing in section 1 itself, option 1 is the fallback and needs a `DecisionLog` table and snapshot script work.

## 0011 MC quarters, outlook of two quarters, Delivered from the actual date (14 Oct 2026)
* Context: PRD change request 1 items 1 to 3; the user confirmed the outlook is the current plus the next MC quarter and undelivered milestones past their date stay visible as overdue.
* Decision: params `MCQuarterStart`, `MCQuarterEnd`, `OutlookEnd`, `CurrentMCQuarter`, `NextMCQuarter` replace QuarterStart, QuarterEnd, WindowStart and WindowEnd. MC quarters start on calendar quarter days; only the label shifts. Milestones gain calculated columns: `TimelineDate` (actual, else forecast, else planned), `MCQuarter` (`"MC"&RIGHT(YEAR(EDATE(d,-3)),2)&"Q"&INT((MONTH(EDATE(d,-3))+2)/3)`; no `TEXT(…,"yy")` because format codes change with the Excel language), `InOutlook` (planned or timeline date in the outlook; drives the x of y counts and the data signal, so delivering in the quarter never lowers a ratio) and `Visible` (what the roadmap shows: PRD item 3 rule, plus undated milestones for the "Not dated yet" list). Status Delivered now follows from ActualDate only; Delivered leaves `lkp_LeadStatus`, so there is one way to say it. The data signal also turns At risk on an overdue committed milestone (new MilestonesOverdue count). Rocks carries CurrentMCQuarter and NextMCQuarter so the portal needs no date logic.
* Consequences: the six month window language goes everywhere; MilestoneSnapshots adds ActualDate and MCQuarter so the M3 look back groups by MC quarter. A future dated actual date counts as Delivered (guide says type it on delivery).

## 0010 Epic renamed Milestone (14 Oct 2026)
* Context: PRD change request 1 item 1.
* Decision: rename everywhere: section 3 Milestones, consolidated sheet `Milestones`, key `MilestoneKey` = RockID-M plus slot, `MilestoneSnapshots`, `lkp_MilestoneStatus`, signals `Milestones*`. New typed columns Owner, StartDate, ActualDate, ADOLink (optional, validated to start with https://), Description, Detail1 to Detail3. Schema version 2.0.0.
* Consequences: renaming sheets and columns is a breaking change, acceptable now because no workbook is live (T13, T19 open). Every script, test, sample and portal doc that says Epic changes (PLAN T40 to T45). Migration mapping in schema `migration`.

## 0009 Fields added beyond the PRD list, with reasons (14 Oct 2026)
* Context: the PRD allows only fields that feed a tab or the email; additions need a written reason.
* Decision, typed fields: one lookup sheet `lkp_Steercos` (steerco dates, entered once a quarter by the workbook owner). Reason: tab 1 and tab 3.1 spotlights need "the next steerco", and Decisions.SteercoDate becomes a dropdown so tab 5 groups cleanly by steerco.
* Decision, calculated only (nobody types them): row keys (EpicKey, RiskKey, CallOutKey, DecisionKey), RockID, Rock and GPM copied onto every list row (portfolio and rock filter without joins in Cowork), Score, High, NeedsAction, SlipWeeks, InWindow, Overdue, DecisionState, DueNextSteerco, Stale, the rock signals, and in RockSnapshots the GPM, Rock and UpdateDate (portfolio filter and G1 in the M3 look back), in EpicSnapshots the PlannedDate (re baselines). Lookups `lkp_LeadStatus` and `lkp_DecisionState` hold allowed values only.
* Dropped: a separate "On watch" flag column. Lead status (Delivered, On hold, On watch, or empty) is one dropdown.
* Consequences: zero extra typing for leads; one quarterly task for the workbook owner (flagged to `pm`).

## 0008 How the factory tests formulas it cannot run (14 Oct 2026)
* Context: the factory has no Excel. openpyxl writes formulas but cannot calculate them; LibreOffice 24.2 is installed but has no VSTACK, FILTER or LET.
* Options: trust the formulas; a Python mirror of every rule; LibreOffice recalculation; manual check in Excel.
* Decision: all four layers, each where it is cheap. `scripts/rock_model.py` mirrors every schema rule in Python and feeds tests, preview and email. A test recalculates the sample workbook headless in LibreOffice and compares every rock tab formula result (status, flags, signals) with the mirror; only the consolidation cells are out of its reach. The spike (PLAN T05) and the deploy checklist cover the consolidation in Excel for the web.
* Consequences: drift between the Excel formula and the Python rule is caught by the LibreOffice comparison; consolidation correctness depends on one manual check per release.

## 0007 History: snapshot Office Script on a Monday schedule (14 Oct 2026, user decision)
* Superseded in part by 0010 and 0014 (2.0.0): EpicSnapshots is MilestoneSnapshots, positions columns are PositionsBudgeted and PositionsActual.
* Context: PRD section History. Formulas recalculate, so past states are not frozen.
* Decision: `scripts/office/snapshot.ts` reads the Rocks and Epics spills and appends one row per active rock to `RockSnapshots` and one row per epic of an active rock to `EpicSnapshots` (real Excel Tables). Idempotent per day (SnapshotID = date|key). Run by a Power Automate recurrence every Monday 06:00; fallback a "Save snapshot" button the GPM presses before steerco. SharePoint version history stays on as backstop.
* Consequences: one off setup by the director (about 15 minutes, documented in DEPLOY); the flow runs under one person's account (flagged to `pm`). The script also unprotects and reprotects the history sheets.

## 0006 Six month window, x of y counts and the data signal (14 Oct 2026)
* Superseded by 0011 (MC quarters and outlook) and 0014 (positions from teams).
* Context: PRD asks for slip counts, positions x of y, update age and a data based signal next to the lead's call.
* Decision: the window is the current calendar quarter plus the next (WindowStart to WindowEnd, named formulas), stable within a quarter. y = committed epics with a planned or forecast date in the window; x = those Slipped. Data signal: Off track when a Slipped epic planned this quarter is forecast after quarter end; At risk when any committed epic in the window slipped or a High risk lacks key action or owner; else On track. CheckCall = data signal worse than the lead's State. All calculated on the rock tab so the lead sees them while updating.
* Consequences: the watermelon guard is in the data from M1; showing it in the portal and email is M2 work, with no schema change.

## 0005 Epic status: one hand set column, everything else derived (14 Oct 2026)
* Amended by 0011: Delivered follows from the Actual date; Lead status holds On hold and On watch only.
* Context: PRD epic status table; as much as possible derived.
* Decision: the lead sets Lead status only (Delivered, On hold, On watch, or empty). Status is calculated, first match wins: Delivered, On hold, Not committed (commitment not Committed or empty), Slipped (forecast later than planned), On watch, On plan. An empty forecast means "on the planned date". "Releases this period" uses the forecast date of Delivered epics as ship date.
* Consequences: Slipped cannot be hidden behind On watch. No delivered date field; leads set Forecast date to the ship date when marking Delivered (on the About sheet).

## 0004 Rock tab layout: fixed blocks with fixed capacity, protected (14 Oct 2026)
* Context: one tab per rock (user decision) and consolidation by 3D reference (0002) need every rock tab to have the same cell layout forever.
* Options: Excel Tables per block (auto expand collides with the next block, table names get renamed on duplicate); free ranges (rows get inserted and break alignment); fixed blocks on a protected sheet.
* Decision: fixed blocks in a fixed order (Update, Signals, Epics 15 rows, Risks 10, Call outs 8, Decisions 25, Profile), sheet protection without password, only entry cells unlocked, no row insert or delete. Keys are slot based (R03-E04); a slot is one epic for life. Every rock tab also has a hidden row 2 that lays out the rock's single values as one row for consolidation.
* Consequences: departs from "each sheet is one Excel Table" for rock tabs (user decision wins). Capacity is a limit: more rows need a schema change and migration. Decisions accumulate; at 25 per rock an archive is needed around the M3 milestone (TECH_DEBT). Tab names of rocks are free; formulas never refer to them.

## 0003 Consolidated sheets are spill ranges, not Excel Tables (14 Oct 2026)
* Context: design rule "each sheet is one Excel Table", but a dynamic array cannot spill inside a Table.
* Decision: Rocks, Epics, Risks, CallOuts and Decisions are protected read only sheets: static header in row 1, one formula in A2 that spills all rows. Lookup and history sheets stay Excel Tables (`tbl_<sheet>`). PORTAL_BUILD tells Cowork to read these five sheets as tables with the header in row 1.
* Consequences: if the spike shows Cowork reads spill ranges badly, plan B is a "publish" step in the same Office Script that copies the five spills into real Tables on a schedule (adds latency, keeps zero manual steps). If Excel rejects the formula itself, plan C in 0002 applies. Go or no go: Thu 15 Oct 12:00, from the user's spike check (PLAN T05).

## 0002 T02: consolidation across rock tabs (14 Oct 2026)
* Context: one tab per rock is a user decision. Portal, email and history need all rocks together, meeting the 7 conditions in PRD "Upkeep requirement".
* Options considered:
  1. Identical Excel Tables per rock tab plus `VSTACK(tbl_R01_Epics, tbl_R02_Epics, ...)`. Fails condition 5: every new rock means editing five formulas by hand.
  2. Power Query appending all tables by name. Refresh is manual in Excel for the web (fails condition 4), refresh conflicts with co-authoring (condition 6), and the generator cannot author queries.
  3. Office Script that copies rock tabs into consolidated Tables, on a schedule. Data is stale between runs, and the portal itself then depends on Power Automate being allowed.
  4. Copilot Cowork reads every rock tab itself. Depends on the generated portal discovering new tabs; not reliable or testable.
  5. Fixed layout rock tabs between two bookend sheets plus one 3D `VSTACK` + `FILTER` formula per consolidated sheet (`VSTACK(RockTemplate:RocksEnd!A25:P39)`).
* Decision: option 5. New rock = duplicate RockTemplate (the copy lands inside the bookends), rename, fill the profile. Rows without a key (blank, half filled without a title, inactive rock) are filtered out at the source.
* How it meets the 7 conditions: (1) the lead types only on the rock tab; (2) one screen top to bottom, values stay in place; (3) nothing is copied or retyped, consolidation is a formula; (4) formulas recalculate live, zero steps; (5) duplicate, rename, fill nine profile cells, no formula or portal change; (6) co-authoring merges per cell and leads work on different tabs, nothing locks the file (no Power Query, no macros); (7) blank keys are filtered out, every calculated column tolerates empty cells.
* Consequences: needs Excel 365 dynamic arrays (Excel for the web and current desktop). openpyxl cannot mark a formula as a dynamic array, so the generator patches the cell metadata in the xlsx; fallback is a one off `setup.ts` Office Script that writes the five formulas at deploy. Both proven or rejected by the spike (PLAN T05). A tab moved outside the bookends silently drops out; the About sheet shows the count of rocks found.
* Plan C, if Excel for the web rejects the 3D reference inside VSTACK (go or no go Thu 15 Oct 12:00): `scripts/office/consolidate.ts` walks every sheet between RockTemplate and RocksEnd by position, reads the same fixed blocks and the row 2 strip (calculated cells on the rock tab still work, they need no 3D reference), applies the same key filter and rewrites five real Excel Tables `tbl_Rocks`, `tbl_Epics`, `tbl_Risks`, `tbl_CallOuts`, `tbl_Decisions` with the same columns. It runs from a Power Automate recurrence every 30 minutes on working days 07:00 to 20:00, again before every snapshot, and behind a "Refresh portal data" button. Condition 4 holds (no one copies anything; the flow does). Condition 5 holds (the script finds new tabs by position, no list to maintain, no portal change). Cost: the portal can be up to 30 minutes behind, and consolidation then depends on Power Automate. If the tenant also blocks Power Automate, plan C2: a tab list `lkp_RockTabs` (the owner adds one row per new rock, still inside 10 minutes) and one `REDUCE(…,LAMBDA(a,s,VSTACK(a,INDIRECT("'"&s&"'!range"))))` formula per sheet; live, no 3D reference. The spike file tests the 3D formula and the C2 formula side by side so one user check settles both.

## 0001 Excel workbook as backend, Copilot Cowork portal as frontend
* Context: product team apps must be cheap to run and easy for non developers to own.
* Decision: one shared workbook is the source of truth; the factory builds and tests the workbook; the product owner builds the portal
  in Copilot Cowork from the deployed workbook and the portal pack.
* Consequences: the workbook schema is the contract and is tested on every change.
