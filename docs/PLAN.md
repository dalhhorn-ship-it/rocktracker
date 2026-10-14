# Plan

Owners: `pm` (what and priority), `architect` (acceptance criteria).
Agent column: who should do the task, per the routing table in CLAUDE.md.
Statuses: `todo`, `doing`, `review`, `done`, `blocked`.

Source of truth for scope: `docs/PRD.md` (approved 14 Oct 2026). Design: `schema/workbook.schema.json`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` 0002 to 0009.

**Order (user, 14 Oct 2026): the Excel workbook first.** M1 runs in two phases. Phase 1a builds, tests and reviews the workbook so it can be deployed and loaded by leads. Phase 1b adds the portal spec, preview and the full handoff package. Both phases are still M1 and target Fri 16 Oct 2026.

## Milestones

| Milestone | Outcome | Factory done by | Exit check |
| :--- | :--- | :--- | :--- |
| M1a Workbook | Deployable workbook: rock tabs, consolidation, history tables, snapshot script, About and update guide | Thu 15 Oct 2026 (end of day) | Tests green, workbook review approved, spike confirmed in Excel for the web, workbook package built |
| M1b Portal pack | Portal spec and preview for tabs 1, 2, 3, 3.1, 4, 5; full handoff package | Fri 16 Oct 2026 | Tests green, reviewer approved, `dist/` built, steerco of week of 19 Oct held from the portal (S0) |
| M2 Email and trust | Portfolio email, check the call flag and freshness shown, live migration | Fri 30 Oct 2026 | Email reference rendering matches the six section structure; G5 under 5 minutes |
| M3 Look back | Quarter look back from snapshots, decision archive, cockpit health | Fri 11 Dec 2026 | Quarter view works on sample history; `/retro` done |

## M1a: Workbook first

Task graph (arrows are dependencies; same group runs in parallel):

```
T02, T03 (done by architect, in review)
   └─▶ group C (parallel): T05 spike · T06 sample data · T10 snapshot script
          T05, T06 ─▶ T07 generator ─▶ T11 About and guide ─┐
          T06 ─▶ T08 rule mirror and tests ─┐               │
                       T07, T08 ─▶ T09 LibreOffice recalc ──┤
                                         T10 ──────────────┴─▶ T12 workbook review ─▶ T13 workbook package
```

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T01 | PRD and first plan | pm | BRIEF, BRAINSTORM | `docs/PRD.md`, `docs/PLAN.md` | | A | PRD approved by the user | done |
| T02 | Consolidation across rock tabs | architect | PRD "Upkeep requirement" | `docs/DECISIONS.md` 0002 to 0004 | T01 | B | Options weighed; decision meets all 7 conditions; add and close a rock described; zero copy steps | review |
| T03 | Workbook model and schema | architect | PRD, T02 | `schema/workbook.schema.json`, `docs/ARCHITECTURE.md`, DECISIONS 0005 to 0009 | T02 | B | Every PRD fact has a field with owner and dropdown where fixed; computed rules defined as formula plus words; every email field present; extra fields have a written reason | review |
| T05 | Spike: 3D VSTACK consolidation in Excel for the web | developer, then user (5 min) | DECISIONS 0002, 0003; schema `rock_tab.consolidation_formula` | `scripts/build_workbook.py` helper that writes dynamic array formulas (`_xlfn` prefixes, `_xlpm` LET names, cell metadata), `dist/spike/consolidation_spike.xlsx`, note in TECH_DEBT | T03 | C | Spike file has RockTemplate, two rock tabs, RocksEnd and an Epics sheet with the schema formula in A2. Test asserts the anchor cell carries dynamic array metadata and the xlsx opens in openpyxl and LibreOffice without error. User uploads to SharePoint and confirms by Thu 15 Oct 12:00: opens without repair, Epics spills both rocks' rows, a duplicated RockTemplate shows up after a title is typed in it. If it fails: write `scripts/office/setup.ts` that sets the five formulas, and record the switch in DECISIONS | todo |
| T06 | Synthetic sample data | developer | Schema | `data/sample.json` (new shape: per rock profile, update, epics, risks, call outs, decisions; lookups; snapshot rows) | T03 | C | 2 GPMs, 5 rocks, one inactive and one half filled (no update date, an epic without dates, a risk without impact, a block row with data but no title). Epics cover all six statuses (incl. a Slipped one with On watch set, and an Off track case: planned this quarter, forecast next quarter) and all three commitments; risks in every likelihood row and every impact column, one High without action; call outs open and closed; decisions requested (due next steerco and later, one choice point) and decided (one follow up open); 3 weekly snapshots. Names synthetic only | todo |
| T07 | Generator: rock tabs, consolidation, lookups, history | developer | Schema `rock_tab`, `sheets`, `params`; T05 result | `scripts/build_workbook.py`, `data/workbook.xlsx`, adapted `tests/test_schema.py`, `tests/test_workbook.py`, `tests/test_deploy.py` | T05, T06 | D | Builds sample and `--deploy` from the schema only (no layout in code). Sheet order as in ARCHITECTURE. Rock tabs: fields and blocks at schema rows, placeholders resolved (test: no `{`, `[` left), hidden strip row 2, grey calculated cells, dropdowns and date validation on entry cells, pink required and orphan row highlight, protection with entry cells unlocked, Active defaults to Yes on RockTemplate. Five consolidated sheets: static header row equal to schema columns, A2 dynamic array formula, date formats, protected. Params as defined names. Lookups and history as `tbl_<sheet>` Tables; deploy has seed rows only and one RockTemplate, no rock tabs. Tests adapted per sheet kind (Tables only for lookup and history; dropdown checks on rock tab entry cells). `--deploy --from` round trip keeps every rock tab's entry values and history rows. `./scripts/test.sh` green | todo |
| T08 | Rule mirror and business rule tests | developer | Schema `rule` texts, T06 | `scripts/rock_model.py`, `tests/test_business_rules.py` | T06 | D | `rock_model.py` reads rock tabs (from sample.json or a workbook via the schema layout) and returns Rocks, Epics, Risks, CallOuts, Decisions rows with every calculated column, applying the consolidation filter. One test per rule in ARCHITECTURE "Computed rules" with edge cases: empty forecast, empty planned on committed, Slipped beats On watch, Delivered beats Slipped, empty commitment, risk without impact, closed High risk, inactive rock (no epics, decisions kept), row without title, no future steerco, window edges on quarter boundaries (tests freeze today) | todo |
| T09 | LibreOffice recalculation check | developer | T07, T08 | `tests/test_recalc.py` | T07, T08 | E | Converts the sample workbook headless with LibreOffice (skip with a clear message if `soffice` is missing), reads every rock tab calculated cell (signals, block columns, strip) and compares with `rock_model.py` for a fixed today; consolidation cells excluded (LibreOffice 24.2 lacks VSTACK). Runtime under 30 s | todo |
| T10 | Snapshot Office Script | developer | Schema history sheets, DECISIONS 0007 | `scripts/office/snapshot.ts`, `scripts/snapshot.py` (mirror), `tests/test_snapshot.py`, setup text for DEPLOY | T03 | C | Script reads the Rocks and Epics spills by header name, keeps Active Yes, appends to `tbl_RockSnapshots` and `tbl_EpicSnapshots`, skips SnapshotIDs already present, unprotects and reprotects. Compiles with `tsc --noEmit` against a minimal ExcelScript declaration file in the repo. Tests: every sheet, table and column name in the script exists in the schema; mirror run twice on sample gives the same rows (idempotent); inactive rocks excluded. Power Automate steps (Recurrence Monday 06:00, Run script) and button fallback written for DEPLOY | todo |
| T11 | About sheet and update guide | developer | Schema `about` | `scripts/build_workbook.py` (About), test in `tests/test_deploy.py` | T07 | E | About first: title, version, the 7 minute guide, add rock and close rock steps, rules, all definitions from schema `about.definitions`, sheet list with purpose and owner, "rock tabs found" (count of Rocks rows) and "duplicate rock IDs" checks, where the Save snapshot button goes. Test checks every definition term and guide line is on the sheet | todo |
| T12 | Workbook review | reviewer | T05 to T11 | `docs/REVIEW_LOG.md` | T09, T10, T11 | F | Reviewer runs tests itself; checks schema contract, the 7 upkeep conditions on the sample workbook (walk a lead update and an add rock), blank safety, no real data, TECH_DEBT updated. Verdict per task | todo |
| T13 | Workbook package for early load | scout | T12 approved | `dist/Rock Tracker/Rock Tracker.xlsx`, `docs/DEPLOY.md` workbook part | T12 | G | `python3 scripts/build_workbook.py --deploy` done; DEPLOY covers upload to SharePoint, permissions, lookups to fill first (people, value chains, steercos), adding each rock (10 min), first load guide (30 to 45 min per rock, outside the budget), load deadline Mon 19 Oct 12:00, snapshot flow setup | todo |

## M1b: Portal pack (after the workbook)

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T14 | Portal spec for the six views | architect | PRD tabs, DESIGN_SYSTEM, schema, ARCHITECTURE portal notes | `portal/portal.spec.json`, ARCHITECTURE portal section | T12 | H | Tabs in steerco order 1, 2, 3, 3.1, 4, 5 plus the full list, each a PRD question tied to D1 to D6; answer first anatomy; 6 KPI tiles with exactly one spotlight (the PRD spotlight); every KPI computable from the consolidated sheets with `where` on Active and flags; new element kinds (x of y ratio, six month timeline, 3 by 3 matrix, filter by rock or GPM) with simple fallbacks; `stage_map` covers epic statuses, rock states and decision states | todo |
| T15 | Metrics and preview for the new elements | developer | T14, T08 | `scripts/portal_metrics.py`, `scripts/render_preview.py`, `tests/test_portal.py`, `portal/preview.html` | T14, T08 | I | Preview renders all tabs from `rock_model.py` rows (not from formula cells); ratio KPIs, timeline grouped by month, 3 by 3 count grid; test_portal adapted to sheet kinds; design checklist passes | todo |
| T16 | Handoff generator for rock tabs and new elements | developer | T14, T10, T13 | `scripts/build_handoff.py`, `tests/test_handoff.py` | T14, T13 | I | PORTAL_BUILD reads the five consolidated sheets (header row 1, read only) and lookups, says to ignore rock tabs, RockTemplate, RocksEnd, About and snapshots; describes every new element; README covers add rock, close rock, snapshot flow; handoff test covers every consolidated column, status, page, KPI, chart | todo |
| T17 | Review portal pack | reviewer | T14 to T16 | `docs/REVIEW_LOG.md` | T15, T16 | J | Each view tied to a PRD decision; design checklist; tests run by reviewer | todo |
| T18 | Full handoff package and DEPLOY | scout | T17 approved | `dist/Rock Tracker/` and zip, `docs/DEPLOY.md` complete | T17 | K | `python3 scripts/build_handoff.py` green; DEPLOY adds the Cowork build steps | todo |
| T19 | Deploy, load rocks, build portal in Cowork | product owner (user) | `dist/` | Live workbook, portal | T13 (workbook), T18 (portal) | L | Every active rock loaded by Mon 19 Oct 12:00; portal shows the six views on live data before steerco Wed 21 Oct | todo |
| T20 | M1 milestone review and reprioritise | reviewer (opus), then pm | Whole repo, steerco feedback | `docs/REVIEW_LOG.md`, `docs/PLAN.md` | T19 | M | Findings logged; pm reprioritises M2 | todo |

## Milestone 2: Email and trust

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T21 | Email spec and mechanism | architect | PRD email section, ARCHITECTURE email notes | ARCHITECTURE email section, DECISIONS entry | T20 | N | Six sections in order; every value traced to a consolidated column; this period, releases and average slip confirmed; sender picks only portfolio and date; no schema change expected | todo |
| T22 | Check the call and freshness in the portal | architect | Rocks.CheckCall, Stale, UpdateAgeDays | Portal spec update | T20 | N | Flag on tab 1 and 2 insight cards and full list; stale rocks as an exception tile; no schema change | todo |
| T23 | Email reference renderer and tests | developer | T21 | Renderer, sample email, tests | T21 | O | Portfolio, single rock and all rocks from `rock_model.py`; tests per section and epic table column | todo |
| T24 | Build check the call and freshness | developer | T22 | Preview, tests | T22 | O | Business rule and portal tests cover it; tests green | todo |
| T25 | Email in the handoff | developer | T23 | `build_handoff.py`, `test_handoff.py` | T23 | P | PORTAL_BUILD tells Cowork how to produce the email with the exact structure | todo |
| T26 | Layout versioned migration | developer | DECISIONS 0004, ARCHITECTURE "Evolving" | `build_workbook.py --from` for rock tabs, `schema/history/` | T20 | N | Layout version cell on every rock tab; `--from` reads an older layout by its schema version and writes the current one; test migrates a v1.0.0 sample with no data loss | todo |
| T27 | Review M2, migrate live, rebuild handoff | reviewer, then scout | T23 to T26, live copy | `docs/REVIEW_LOG.md`, `dist/` | T24, T25, T26 | Q | Approved; G5 walk through under 5 minutes; all live data kept | todo |

## Milestone 3: Look back

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T30 | Look back, decision archive, cockpit health | architect | PRD M3, snapshots, DECISIONS 0004 | Schema, spec, decision entry | T27 | R | Quarter view from RockSnapshots and EpicSnapshots; archive for decided decisions before the 25 slot limit; G1 to G4 computable | todo |
| T31 | Build look back and health | developer | T30 | Generator, sample history over two quarters, preview, tests | T30 | S | Renders; health figures match hand counts; tests green | todo |
| T32 | Review M3 and handoff | reviewer, then scout | T31 | `docs/REVIEW_LOG.md`, `dist/` | T31 | T | Approved; package rebuilt with `--from` | todo |
| T33 | Retro | operator (opus) | Whole project | `TEMPLATE_LEARNINGS.md`, CLAUDE.md lessons | T32 | U | Learnings captured | todo |

## Admin load flagged to pm

* Workbook owner enters steerco dates in `lkp_Steercos` once a quarter (about 2 minutes).
* Director sets up the Power Automate snapshot flow once (about 15 minutes); it runs under the director's account.
* Capacity per rock (15 epics, 10 risks, 8 call outs, 25 decisions): leads reuse epic and call out slots only for closed items; decisions need the M3 archive.
* Portfolio level decisions and events from the GPM have no home of their own: assumed recorded on the most affected rock tab (open question).

## Change log

* 14 Oct 2026, architect: plan reworked to the approved PRD and the T02 decision (one tab per rock, 3D VSTACK consolidation, snapshot script). User asked for the workbook first: M1 split into M1a workbook and M1b portal pack, task ids renumbered (old T04 portal spec is now T14).
* 14 Oct 2026, pm: first plan from PRD v1.
