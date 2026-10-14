# Review Log

Owner: `reviewer`. Newest entries at the bottom.

## 2026-10-14 Kickoff (T02, T03, T01 and plan T05 to T20) Design and plan review
Verdict: CHANGES
Round: 1
Scope: PRD (binding), schema/workbook.schema.json, docs/ARCHITECTURE.md, docs/DECISIONS.md 0002 to 0009, docs/PLAN.md. No code reviewed (none exists). Known and accepted: template tests fail until T07 and T15; Excel web spill behaviour unverified until T05.
Findings:
* [high] The fallback for a failed spike does not cover the real risk. Excel may reject a 3D reference (RockTemplate:RocksEnd!range) inside VSTACK, not only the dynamic array metadata. PLAN T05 fallback (`setup.ts` writing the same five formulas) and DECISIONS 0003 plan B (publish step) both still assume the 3D formula evaluates. Name a plan C that does not rely on a 3D reference and still meets conditions 4 and 5 (for example a scheduled Office Script that rebuilds the five consolidated tables from all rock tabs, or a tab list driven formula), and set the go/no go time. Files: docs/PLAN.md T05, docs/DECISIONS.md 0002/0003.
* [high] Tab 5 spotlight "decisions with an open follow up" has no precomputed flag and Decisions.FollowUp has no "empty = Open" rule (Risks and CallOuts do). ARCHITECTURE promises Cowork needs no logic for spotlights. Add a calculated column (for example OpenFollowUp: Decided and FollowUp not Closed) and say what empty means. File: schema/workbook.schema.json Decisions.
* [medium] Decisions.SteercoDate is required with a dropdown from lkp_Steercos, which the workbook owner fills. A lead raising a decision for a steerco not yet listed is blocked and must go to another tab (breaks condition 1). NextSteerco returns 0 once the listed dates pass, so the tab 1 and 3.1 spotlights go silently to zero. Make the validation a warning, not a stop, and add an About check "next steerco date missing" (T11 criteria). Files: schema/workbook.schema.json (Decisions, About), docs/PLAN.md T11.
* [medium] The formula `EpicsOnPlan` uses an array constant `{"On plan","On watch"}`, which collides with the `{Field}` placeholder syntax; T07 requires "no `{` left", so the generator or test will either fail or mangle it. Rewrite as two COUNTIFS added together, or define an escape. File: schema/workbook.schema.json rock_tab Signals EpicsOnPlan.
* [medium] Fields with no named reader. Purpose is required (pink) but no tab or email section reads Purpose, Goals, Delivers or ValueChain (tabs filter by rock and GPM only). The PRD lists them, so keep them, but name the reader (for example the per rock email section and a tab 2 insight card) in ARCHITECTURE "How the portal consumes", or make Purpose optional so it does not add pink cells and upkeep. Files: docs/ARCHITECTURE.md, schema/workbook.schema.json Rocks/section 7.
* [medium] docs/TECH_DEBT.md is empty although the design already defers things. Record: 25 decision slots with no archive until M3 (0004), button for Save snapshot is a manual one off in Excel (not generatable), flow runs under the director's account (0007), 3D formula unverified, capacity limits, protection is not security. File: docs/TECH_DEBT.md.
* [low] PLAN T14 omits the design anatomy (3 insight cards, charts, full list per tab) that tests/test_portal.py enforces. Add to acceptance. File: docs/PLAN.md T14.
* [low] PLAN timing: T07 to T13 must finish between the user's spike confirmation (Thu 12:00) and end of Thu. Let T06, T08, T10 and a Plan A T07 start now; treat the spike as a gate only for the final T07 formula path. File: docs/PLAN.md T05/T07.
Checks:
* Spec: the 7 upkeep conditions are each mapped in DECISIONS 0002 and the schema supports them (one tab per rock, fixed layout, bookends, slot keys, key filtering, N() wrapped blanks). Tabs 1, 2, 3, 3.1, 4, 5 are all readable from the five consolidated sheets; each tab tied to D1 to D6; history has the PRD fields for both snapshot tables; workbook first ordering is in PLAN. Email (M2) fields all present, no schema change expected.
* Admin load: typed fields all appear in the PRD list except lkp_Steercos (justified in 0009, quarterly 2 minutes, see finding 3). No other extra typed fields. 7 minute lead update is realistic for a rock that mostly carries over (about 5 to 8 cells touched plus rows that moved); it is not proven. T12 should count cells touched in a walked update and a retro measures G3.
* Clarity: every planned view supports a named PRD decision. Weakness: "Tab 3 spotlight committed epics on plan x of y" excludes Delivered epics from x but includes them in y, so delivering epics lowers the ratio. Define x as On plan, On watch or Delivered, or label it.
* Plan quality: dependencies are correct; acceptance criteria are testable and specific. T08 should also depend on T07 only if it reads a workbook; as written it does not, which is fine.
* Safety: no secrets, no real data; sample names to be synthetic (T06 states it). Prose has no dash punctuation.
Evidence: read the five documents in full; grep for dash punctuation (none); docs/TECH_DEBT.md checked (empty). Tests not run (no code to test; known failing template tests).

## 2026-10-14 Kickoff re-check (round 1 fixes, commit 8fdf9af)
Verdict: APPROVED
Round: 2
Findings:
* [ok] 1 Plan C and C2 with go or no go Thu 15 Oct 12:00: DECISIONS 0002/0003, PLAN T05, ARCHITECTURE. Plan C needs no 3D reference and keeps conditions 4 and 5; spike tests both formulas.
* [ok] 2 OpenFollowUp column and "empty = Open" for FollowUp: schema Decisions, ARCHITECTURE rules, T08 edge case.
* [ok] 3 SteercoDate validation is a warning; About check "next steerco date missing" in schema about.checks and T11.
* [ok] 4 EpicsOnPlan rewritten as three COUNTIFS (no array constant). Also fixes the on plan x of y ratio (Delivered now counted in x).
* [ok] 5 read_by on ValueChain, Purpose, Goals, Delivers (tab 1 rock header, email per rock section); PRD field table clarified.
* [ok] 6 TECH_DEBT TD01 to TD08 recorded, counts match (8: 1 high, 4 medium, 3 low).
* [ok] 7 T14 carries the test_portal anatomy.
* [ok] 8 T05/T06/T07 (plan A)/T08/T10 start now; spike gates only the final formula path.
* [ok] Notes: choice point mismatch checks both ways, duplicate Rock ID pink highlight, on plan ratio all done.
Notes (not blocking):
* The PRD was edited by the architect (field table "why it exists" cell only). Content is a clarification, not a scope change, but the pm should acknowledge it since the PRD is user approved.
* The choice point check counts only epics and decisions of active rocks and compares by RockID, not by epic, so one open decision covers several choice point epics on a rock. Acceptable for a warning check.
Evidence: git diff HEAD~1 over schema, DECISIONS, ARCHITECTURE, PLAN, TECH_DEBT, PRD read in full. No code exists; tests not run.

## 2026-10-14 T12 Workbook review (T05 to T11)
Verdict: APPROVED
Round: 1
Findings:
* [ok] Spec: T05 spike file and CHECK.md in dist/spike, T06 sample (5 rocks, R05 inactive, R04 half filled), T07 generator reads the schema only, T08 rule mirror with business rule tests, T09 LibreOffice recalc, T10 snapshot script with mirror and tsc check, T11 About sheet with guide, add and close rock, definitions and checks. Each has its tests green.
* [ok] Contract: schema last changed in 8fdf9af together with DECISIONS 0002 to 0009. No schema change since. Rebuilding data/workbook.xlsx from the generator gives the same sheets (binary differs only by file metadata; restored the committed copy).
* [ok] Seven upkeep conditions on data/workbook.xlsx: (1) all update cells are on the rock tab; (2) see walk below; (3) values stay in place, keys, RockID, Rock, GPM and dates are calculated, 0 unlocked formula cells on rock tabs; (4) five consolidated sheets are spill formulas over RockTemplate:RocksEnd, no copy step; (5) add rock is Duplicate, rename, fill section 7 (About steps, no portal change); (6) one tab per rock, so co-authors on different tabs do not collide; (7) half filled R04 and the template tab produce no errors (ISTEXT key filter, tests green).
* [ok] Essential fields: every typed field maps to PRD "What the workbook must hold"; the additions (lkp_Steercos, calculated keys and copies) are justified in DECISIONS 0009 and cost the leads no typing.
* [ok] Safety: synthetic names, no emails or secrets in sample.json or the workbook; sheet protection has no password by design (TD06); formulas are non destructive, no macros.
* [ok] Debt: TD list complete for what can be foreseen. Header counts match the table (17 open: 1 high, 6 medium, 10 low; 2 resolved). TD01, TD10, TD14, TD18 cover everything that needs Excel for the web.
Lead update walk (R01 Checkout Speed, typical week): Update date 1, State 1 (only if changed), Main message 1, positions 0 to 2, two epics that moved (forecast plus comment) 4, one Lead status 1, one risk changed 1 to 2, one new call out 2 (text, date) plus 1 to close one, one new decision request 3 to 5 (Decision, SteercoDate, DecideBy, optional ChoicePoint and Options). Total about 15 to 20 cells, about 25 s each including reading, which fits 7 minutes. Post steerco week adds Outcome, Owner, FollowUp per decision (3 cells each), about 30 cells, still plausible but the tightest case. The claim is credible, not measured; PRD G3 retro question is the real test.
Notes (not blocking):
* docs/DEPLOY.md sections jump from 4 to 6 (no section 5); renumber or fill when T13 writes the workbook part.
* The sample is dated October 2026 and rock tabs use TODAY(), so Stale and the data signal in the sample drift as the date moves; related to TD19, worth one line there.
* The Update date is typed each time; a note in the guide that Ctrl+; enters today would save a few seconds. No schema change.
* build_spike.py and dist/spike can be deleted after the user spike check (already in TD09).
Evidence: ./scripts/test.sh gave 163 passed, 3 failed; the 3 failures are tests/test_portal.py (test_references_exist_in_schema, test_filters_use_allowed_values, test_kpis_compute_on_workbook), the known T15 items (portal spec still references the old Initiatives table). Opened data/workbook.xlsx with openpyxl: sheet order, protection, unlocked cells, spill formulas, hidden strip row inspected; git status clean after the review.

## 2026-10-14 T47 Review change request 1 workbook (T40 to T46)
Verdict: CHANGES
Round: 1
Findings:
* [ok] Spec, item 1 (Milestone): rename complete in data/workbook.xlsx (no Epic or Delivered in any cell), schema (only in `migration` and `schema/history/`), tests (only migration fixtures), the brief and the About sheet. Milestone fields all present: Title, Description, Detail1 to 3, Owner, Start, Planned, Forecast, Actual, Commitment, LeadStatus, Comment, KRLink, ADOId, ADOLink (custom validation requires https://).
* [ok] Item 2 (MC quarters): formula checked on the recalculated workbook: 2026-12-10 MC26Q3, 2027-01-14 MC26Q4, 2027-04-20 MC27Q1, 2026-09-18 MC26Q2; boundary cases (31 Mar, 1 Apr, 30 Sep, 1 Oct, 31 Dec, 1 Jan) are in tests/test_business_rules.py. Current and next quarter are MC26Q3 and MC26Q4 for 14 Oct 2026.
* [ok] Item 3 (outlook and visibility), LibreOffice recalc of the rock tabs: Completed with actual before today is hidden (R01-M03); Completed without actual and planned before today is hidden (R02-M05); Completed with actual today is shown (R01-M05); overdue committed MC26Q2 is shown and flagged (R03-M04); beyond the outlook is hidden (R03-M05, MC27Q1); undated is shown (R01-M04, R04-M01); About check "Completed milestones without an Actual date" is present (warning).
* [ok] Completed comes only from Lead status (R02-M05 has no actual and is still Completed); no Delivered left in schema, workbook, sample or brief.
* [ok] Item 4: section 1 has 3 attention lines (C9 to C11) and 5 request lines (C13 to C17, grey, locked) plus the open count (C12). R01 has 6 open requests: C12 = 6, 5 shown. About check "open requests beyond 5" present. Top risk flag is gone.
* [ok] Decision log walk (nothing typed twice): the lead types one row in section 6 (B text, C steerco, D decide by, E and F for a choice point); J State is Requested while Outcome is empty, K numbers it, C13 to C17 and tab 1 pick it up. After steerco the lead types Outcome, Follow up owner and Follow up on the same row: J becomes Decided, it leaves the request lines and shows on tab 5, M Open follow up stays Yes until Follow up is Closed. R01-D04 shows the Decided state in the sample.
* [ok] Item 5 (teams): Teams block rows 118 to 122, integer validation on Budgeted and Actual, FillPct calculated. Totals on the tab are sums over teams: R01 6 / 5 / 83%, R02 4 / 2 / 50%, R03 5 / 5 / 100%, R04 Budgeted 0 gives empty fill %, R05 inactive. Edge cases exist in the sample: R03-T01 over budget (3 of 2, 150%) and R04-T01 with Budgeted 0.
* [ok] Sections do not overlap: 1 rows 6 to 17, 2 rows 20 to 33, 3 header 36 and data 37 to 51, 4 header 54 and data 55 to 64, 5 header 67 and data 68 to 75, 6 header 78 and data 79 to 103, 7 rows 106 to 114, 8 header 117 and data 118 to 122; the sheet is protected, inputs unlocked, calculated cells locked.
* [ok] Tests: `./scripts/test.sh` 224 passed, 3 failed; the 3 are the known tests/test_portal.py items (T14). tests/test_recalc.py ran with LibreOffice (11 passed, none skipped).
* [ok] Debt: TD02 and TD03 updated to milestones and teams; TD29 records that LibreOffice cannot evaluate the consolidated sheets (the recalc check of those is the model plus formula text); TD30 resolved; no item on future actual dates. Header counts match the table (27 open: 1 high, 7 medium, 19 low; 4 resolved).
* [ok] Design tokens in the brief: all light and dark values match design/tokens.css, apart from the item below. No dashes as punctuation in the brief.
* [ok] Safety: synthetic names, no secrets, no macros.
* [ok] Brief addresses match the built R01 tab exactly: section 1 rows 6 to 17, signals 20 to 33, profile 106 to 114, Milestones header 36 and rows 37 to 51 (columns A to X as lettered, Y to AA are Rock ID, Rock and GPM copies), Risks 54/55 to 64, Call outs 67/68 to 75, Decisions 78/79 to 103 (A to M), Teams 117/118 to 122. Expected R01 values equal scripts/rock_model.py output and the LibreOffice recalc: signals 2, On track, No, MC26Q3 and MC26Q4, 4, 0, 4, 2, 0, 1, 0, 6, 5, 83%; the five requests in slot order; 4 visible milestones and 1 hidden; teams 3 of 3, 1 of 2, 1 of 1; risks and decision log as listed.
* [CHANGES, low] portal/COWORK_ROCK_TEST.md, Tab 1, card 1: "Mark rows with Due at next steerco = Yes as Next steerco and put them first within their order" contradicts the expected list in "For you" (D05 is Next steerco but is listed fourth, after D03 which is not). A literal Cowork build would show 1, 2, 4, 3, 5. Change: remove the reordering sentence (keep the label) or change the expected order.
* [CHANGES, low] portal/COWORK_ROCK_TEST.md, Look and feel: Milestone On plan dark is written `#A3A7AD`, but design/DESIGN_SYSTEM.md section on milestone colours (On plan, `--stage-backlog`) says dark `#8C9097`. Change the dark value to `#8C9097`.
Lead update walk (R01, typical week, cells touched): section 1: Update date 1, State 1 (only if changed), Main message 1, attention lines 2 changed = 5; section 3: 2 milestones moved (Forecast and Comment) 4, 1 completed (Lead status and Actual date) 2 = 6; section 4: 1 risk status 1; section 5: 1 call out (text and date) 2 plus 1 closed = 3; section 6: 1 new request (text, steerco, decide by) 3, or 5 for a choice point with options; after steerco 2 outcomes (Outcome, Owner, Follow up) 6; section 8: 1 team count 1. Total about 25 cells before steerco and about 31 in a steerco week, with 3 more only for a choice point. At 12 to 15 seconds a cell (type, tab, no hunting) that is 5 to 7 minutes, so the 7 minute budget holds but a steerco week is at the edge. The new work versus v1 is the 3 attention lines (replacing one flag) and Teams (replacing 2 position cells); the 7 new milestone columns (Owner, Start, Description, 3 details, ADO link) are first load only, outside the budget. Navigation is by scrolling 122 rows without frozen panes; acceptable.
Evidence: ./scripts/test.sh (224 passed, 3 known T14 failures); LibreOffice headless conversion of data/workbook.xlsx read cell by cell for all five rock tabs; rock_model.build_model on data/sample.json with today 2026-10-14; openpyxl check of validations, protection and named formulas; grep for Epic and Delivered across the repo and every workbook cell.
Notes (not blocking):
* Running rock_model on data/sample.json alone gives NextSteerco 18 Nov, because 21 Oct comes from the schema lookup seed and not from sample.json. The brief's values need the 21 Oct row (the built workbook has it). Add 21 Oct to sample.json lookups or say so in the brief.
* Brief Tab 3 filter: an overdue milestone from an earlier quarter (R03-M04, MC26Q2) is Visible Yes but matches neither chip; say it shows under All only, or in a quarter named Earlier.
* Brief Tab 1 hardcodes 14 days for stale; the workbook has the Stale flag (row 2 strip) and StaleDays. Optional: point to it.
* About update guide numbers its steps 1 to 6 then 8 (Teams); rename step 8 to 7 or label them by section.
* docs/PRD.md outside the Change request 1 section still says epic and Delivered (lines 28, 30, 42, 43, 46, 61, 116, 120, 144, 156 and more); docs/ARCHITECTURE.md line 54 says "27 delivered". Pm and architect to align.
* TD22 is partly stale: the brief now uses `#72777D` for subtle labels.
* Decided: workbook, schema, generator, sample and tests need no change; only the two brief edits above block approval. T13 can proceed once they are made.
