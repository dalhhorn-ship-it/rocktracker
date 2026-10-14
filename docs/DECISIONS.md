# Decision Log

Owner: `architect`. Newest first.

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
* Context: PRD section History. Formulas recalculate, so past states are not frozen.
* Decision: `scripts/office/snapshot.ts` reads the Rocks and Epics spills and appends one row per active rock to `RockSnapshots` and one row per epic of an active rock to `EpicSnapshots` (real Excel Tables). Idempotent per day (SnapshotID = date|key). Run by a Power Automate recurrence every Monday 06:00; fallback a "Save snapshot" button the GPM presses before steerco. SharePoint version history stays on as backstop.
* Consequences: one off setup by the director (about 15 minutes, documented in DEPLOY); the flow runs under one person's account (flagged to `pm`). The script also unprotects and reprotects the history sheets.

## 0006 Six month window, x of y counts and the data signal (14 Oct 2026)
* Context: PRD asks for slip counts, positions x of y, update age and a data based signal next to the lead's call.
* Decision: the window is the current calendar quarter plus the next (WindowStart to WindowEnd, named formulas), stable within a quarter. y = committed epics with a planned or forecast date in the window; x = those Slipped. Data signal: Off track when a Slipped epic planned this quarter is forecast after quarter end; At risk when any committed epic in the window slipped or a High risk lacks key action or owner; else On track. CheckCall = data signal worse than the lead's State. All calculated on the rock tab so the lead sees them while updating.
* Consequences: the watermelon guard is in the data from M1; showing it in the portal and email is M2 work, with no schema change.

## 0005 Epic status: one hand set column, everything else derived (14 Oct 2026)
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
* Consequences: if the spike shows Cowork reads spill ranges badly, plan B is a "publish" step in the same Office Script that copies the five spills into real Tables on a schedule (adds latency, keeps zero manual steps). Decided by Thu 15 Oct from the spike.

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

## 0001 Excel workbook as backend, Copilot Cowork portal as frontend
* Context: product team apps must be cheap to run and easy for non developers to own.
* Decision: one shared workbook is the source of truth; the factory builds and tests the workbook; the product owner builds the portal
  in Copilot Cowork from the deployed workbook and the portal pack.
* Consequences: the workbook schema is the contract and is tested on every change.
