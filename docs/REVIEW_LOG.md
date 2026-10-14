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
