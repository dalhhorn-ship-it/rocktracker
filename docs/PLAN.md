# Plan

Owners: `pm` (what and priority), `architect` (acceptance criteria).
Agent column: who should do the task, per the routing table in CLAUDE.md.
Statuses: `todo`, `doing`, `review`, `done`, `blocked`.

Source of truth for scope: `docs/PRD.md`. Milestone 1 has a hard date: the factory hands over on Fri 16 Oct 2026 so the steerco in the week of 19 Oct runs from the portal. Anything not needed for that steerco waits for M2 or M3.

## Milestones

| Milestone | Outcome | Factory done by | Exit check |
| :--- | :--- | :--- | :--- |
| M1 Steerco slice | Deployable workbook, portal pack for tabs 1 to 5, handoff package | Fri 16 Oct 2026 | Tests green, reviewer approved, `dist/` built, steerco held from the portal (S0) |
| M2 Email and trust | Portfolio email update, watermelon flag, freshness and minutes visible, live migration | Fri 30 Oct 2026 | Email reference rendering matches the six section structure; G5 under 5 minutes |
| M3 Look back | Tab 6 quarter look back, choice point outcomes, cockpit health (G1 to G4) | Fri 11 Dec 2026 | Quarter view works on sample history; `/retro` done |

## Milestone 1: Steerco slice

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T01 | PRD and first plan | pm | BRIEF, BRAINSTORM | `docs/PRD.md`, `docs/PLAN.md` | | A | Tabs, decisions, upkeep budget, milestones and risks written; operator accepts | review |
| T02 | Decide upkeep shape: one tab per rock vs one sheet per table | architect | PRD section "Upkeep requirement for the architect" | Entry in `docs/DECISIONS.md` | T01 | B | Decision meets all 7 upkeep requirements, explains the trade off, states how a new rock is added and how consolidation works with zero copy steps | todo |
| T03 | Workbook model and schema for M1 | architect | PRD (vocabulary, facts table, definitions), T02 | `schema/workbook.schema.json`, `docs/ARCHITECTURE.md` (data model, sheets) | T02 | B | Every fact in the PRD facts table has a column, owner and dropdown where fixed; derived epic status, slip counts, positions x of y and update age defined as formulas; every field the M2 email needs is present; About sheet carries the definitions; `test_schema.py` passes | todo |
| T04 | Portal spec for tabs 1 to 5 | architect | PRD tabs section, `design/DESIGN_SYSTEM.md`, T03 | `portal/portal.spec.json`, `docs/ARCHITECTURE.md` (portal views) | T03 | C | Each tab is a PRD question mapped to its decision; answer first anatomy; 6 KPI tiles with exactly one spotlight; sub lines and "need a look" cues on exceptions; timeline and 3 by 3 matrix with simple fallbacks; ends with "The full list" | todo |
| T05 | Synthetic sample data | developer | T03 | `data/sample.json` | T03 | C | 2 GPM portfolios, 5 rocks, 3 to 5 epics each covering all six statuses and three commitment levels, risks in every matrix row, call outs, at least 3 updates per rock; no real names or data | todo |
| T06 | Build workbook from schema, including lead entry layout and update guide | developer | T03, T02 decision | `scripts/build_workbook.py`, `data/workbook.xlsx` | T03, T05 | D | Workbook builds with and without `--deploy`; dropdowns from lookups; lead can update one rock in one place as decided in T02; values carry forward; blank rows safe; `./scripts/test.sh` green | todo |
| T07 | Business rule tests | developer | PRD definitions, T03 | `tests/test_business_rules.py` | T03 | D | Tests cover: Slipped when committed and forecast later than planned; Not committed when commitment is not Committed; High risk band; epics slipped x of y; update age; blank and half filled rows do not error | todo |
| T08 | Preview render for tabs 1 to 5 | developer | T04, T06 | `portal/preview.html` | T04, T06 | E | `python3 scripts/render_preview.py` renders all five tabs from sample data; `tests/test_portal.py` green; design checklist items pass | todo |
| T09 | Review M1 build | reviewer | T02 to T08 | `docs/REVIEW_LOG.md` entry | T06, T07, T08 | F | Verdict per task: spec, schema contract, tests run by reviewer, admin load against the 7 upkeep requirements, each view tied to a PRD decision, design checklist | todo |
| T10 | Handoff package and deploy guide | scout | T09 approved | `dist/<title>/`, `docs/DEPLOY.md` | T09 | G | `python3 scripts/build_handoff.py` green; DEPLOY states SharePoint steps, first load guide (30 to 45 min per rock, outside budget), load deadline Mon 19 Oct noon | todo |
| T11 | Deploy, load rocks, build portal in Cowork | product owner (user) | `dist/` package | Live workbook on SharePoint, portal in Cowork | T10 | H | Leads have loaded every active rock; portal shows tabs 1 to 5 on live data before steerco | todo |
| T12 | M1 milestone review and reprioritise | reviewer (opus), then pm | Whole repo, steerco feedback | `docs/REVIEW_LOG.md`, updated `docs/PLAN.md` | T11 | I | Findings logged; PM reprioritises M2 from findings and steerco feedback | todo |

## Milestone 2: Email and trust

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T20 | Email update spec and mechanism | architect | PRD email section, user's example structure | `docs/ARCHITECTURE.md` (email), `docs/DECISIONS.md` entry, spec additions | T12 | J | Six sections in the example order; every value traced to a workbook field or formula; derivations of "this period", releases and average slip confirmed; sender only picks portfolio and date | todo |
| T21 | Watermelon flag, freshness and minutes in schema | architect | PRD tab 1, G1, G3 | Schema and portal spec updates | T12 | J | Data based state signal defined; "check the call" flag when lead's state is greener; update age and minutes KPIs on tab 1 | todo |
| T22 | Email reference renderer and tests | developer | T20 | Email renderer script, sample email output, tests | T20 | K | Renders portfolio, single rock and all rocks from sample data; tests check each section and each epic table column; no value typed outside the workbook | todo |
| T23 | Build watermelon flag and freshness | developer | T21 | Workbook generator, preview, tests | T21 | K | Flag appears on tab 1 insight card and full list; business rule tests cover it; tests green | todo |
| T24 | Email build section in handoff | developer | T22 | `scripts/build_handoff.py`, `tests/test_handoff.py` | T22 | L | PORTAL_BUILD.md tells Cowork how to produce the email with the exact structure; handoff test covers it | todo |
| T25 | Review M2 | reviewer | T20 to T24 | `docs/REVIEW_LOG.md` | T23, T24 | M | Approved per task; G5 walk through under 5 minutes on sample data | todo |
| T26 | Migrate live workbook and rebuild handoff | scout | Live workbook copy from user | `dist/` with `--from` | T25 | N | All live data kept; tests green on migrated copy | todo |

## Milestone 3: Look back

| ID | Title | Agent | Inputs | Output | Depends on | Parallel group | Acceptance criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T30 | Quarter look back, choice point outcomes, cockpit health | architect | PRD tab 6, D7, G1 to G4 | Schema and portal spec updates, decision entry | T26 | O | Tab 6 answers "How did we move this quarter?" from update history; outcome fields add no more than 1 minute per steerco per lead; G1 to G4 computable | todo |
| T31 | Build tab 6 and health figures | developer | T30 | Generator, sample history over two quarters, preview, tests | T30 | P | Quarter by quarter view renders; health figures match hand counts on sample data; tests green | todo |
| T32 | Review M3 and handoff | reviewer, then scout | T31 | `docs/REVIEW_LOG.md`, `dist/` | T31 | Q | Approved; package rebuilt with `--from` | todo |
| T33 | Retro | operator (opus) | Whole project | `TEMPLATE_LEARNINGS.md`, CLAUDE.md lessons | T32 | R | Learnings captured; template proposals listed | todo |

## Change log

* 14 Oct 2026, pm: first plan from PRD v1. M1 cut to what the steerco of week of 19 Oct needs; email, watermelon flag and history moved to M2 and M3, but the M1 schema already holds every field they need so later milestones add no data entry for leads.
