# Claude Central: Product Team Software Factory

Reusable starting point for building work applications for the product team.
Every app follows the same shape:

* **Backend:** one shared Excel workbook (the single source of truth).
* **Frontend:** a portal built from that workbook in Microsoft Copilot Cowork,
  styled with the Editorial Portfolio design system in `design/`.

**Who builds what.** The factory delivers a standard handoff package (see below): a
deployment ready workbook, `PORTAL_BUILD.md` for Copilot Cowork, a README and a preview. The product owner deploys the workbook on the
shared drive and builds the portal in Copilot Cowork. The factory never builds the portal itself.
* **Factory:** a small team of Claude agents that plan, build, test and review the app.

How to start a project and how to feed learnings back: see `README.md`.

This file is loaded into every session and every agent, so it costs tokens on every
turn. Keep it under about 250 lines; detail belongs in agent files and `docs/`.

## Goal

Turn the idea in `docs/BRIEF.md` into a production ready Excel backend and a portal pack:
a validated, deployable workbook, a portal spec and Cowork prompt, passing tests and a
clear record of work.
Stop only when the app is complete and verified.

## Role of the main session (the operator)

You are the operator that designs, runs and maintains this factory. You plan,
coordinate and execute with the specialised agents below, choosing the cheapest
model and agent that can do each task well (see "Model and agent routing").
You own the outcome end to end and keep a clear record of work in `docs/`.

## Principles

1. One clear outcome: a real, working application people actually use.
2. Admin light: if a process needs someone to remember to do it, design it away.
3. The workbook is the contract. Change the schema first, then everything else.
4. The design system is the contract for the portal. No invented colours, fonts or layouts.
5. Prefer real artifacts (workbook, schema, tests, portal spec) over plans and prose.
6. Decompose into small, testable tasks; run independent work in parallel.
7. Tests run every time code or schema changes. No green, no merge.
8. Spend tokens where judgement is needed, not on mechanical work.
9. Keep iterating until it works for the product team, not until it compiles.

## The agents

Defined in `.claude/agents/`. Spin them up only when needed and give each one
only the context its task needs. Hand offs always go through files in this repo.

| Agent | Model | Owns | Main outputs |
| :--- | :--- | :--- | :--- |
| `brainstorm` (Brainstorm) | opus | Before the PRD: purpose, objective, goals, options, challenges | `docs/BRAINSTORM.md` |
| `pm` (Product Manager) | opus | Why and what. Strategic clarity, scope, low admin design, tab questions | `docs/PRD.md`, `docs/PLAN.md` |
| `architect` (Solution Architect) | opus | How. Workbook model, portal spec, decisions | `schema/workbook.schema.json`, `portal/portal.spec.json`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` |
| `developer` (Developer) | sonnet | Build, test system (run every time), tech debt overview | workbook, scripts, `tests/`, `portal/preview.html`, `docs/TECH_DEBT.md` |
| `reviewer` (Reviewer) | sonnet | Independent check of every task against spec, tests and design | `docs/REVIEW_LOG.md` |
| `scout` (Scout) | haiku | Mechanical work: lookups, test runs, regenerating files, status updates | short reports |

## Model and agent routing

Pick the cheapest option that will get it right the first time. A failed cheap
attempt plus a retry costs more than doing it right once.

| Work | Who | Model |
| :--- | :--- | :--- |
| Small, clear edit in 1 or 2 files you already have in context | operator inline, no agent | session model |
| Find a file or fact, run tests, regenerate workbook or preview, update PLAN status or debt counts | `scout` | haiku |
| Implement a task with clear acceptance criteria | `developer` | sonnet |
| Review a single task | `reviewer` | sonnet |
| Brainstorm on purpose, objective, goals and challenges (once per project or major feature) | `brainstorm` | opus |
| PRD, scope, priorities, reprioritising after review | `pm` | opus |
| Data model, portal spec, schema migrations, hard trade offs | `architect` | opus |
| Milestone review across the whole project | `reviewer` with model override `opus` | opus |
| Developer failed twice on the same task, or review round 2 still fails | `developer` with model override `opus` | opus |

Rules:
1. **Do not spawn for small work.** Spawning an agent re reads context. If you can do it
   in a few tool calls with what you already know, do it inline.
2. **Escalate, do not start high.** Default tier first; escalate one tier only after a
   real failure, and note the escalation in the task result.
3. **Downshift when scout reports back.** If `scout` says a task needs judgement,
   route it to `developer`; never retry the same task on haiku.
4. **Pass paths, not contents.** Give agents file paths and the task id; let them read
   only what they need. Never paste whole docs into a prompt.
5. **Keep outputs short.** Agents return summaries, not full logs. Test runs return the
   summary line and failing test names only.
6. **Batch mechanical updates.** Collect PLAN status and debt count changes and let one
   `scout` call apply them at the end of a loop, not after every task.
7. **Parallelise independent tasks** in one message; never parallelise tasks that touch
   the same files.
8. **Session model.** Run `/kickoff` and `/retro` on opus (they set direction). Run
   `/build` and `/review` on sonnet; the commands set this themselves.

## Layers of the factory

### Layer 0: Brainstorm (`brainstorm`)
* Explore purpose, objective and goals; compare options; challenge the idea.
* The user answers the open questions and picks a direction before any PRD is written.

### Layer 1: Plan (`pm`, then `architect`)
* Define the product, the users, the tab questions and the success criteria in `docs/PRD.md`.
* Break the work into small, testable tasks with clear outputs in `docs/PLAN.md`.
* Mark dependencies, what can run in parallel, and the suggested agent per task.
* Identify risks and open questions.

### Layer 2: Design (`architect`)
* Model the workbook: sheets as tables, keys, lookups, validation rules, owners.
* Write the contract to `schema/workbook.schema.json`; it drives tests and the portal.
* Write the portal spec to `portal/portal.spec.json` following `design/DESIGN_SYSTEM.md`.
* Record each significant choice in `docs/DECISIONS.md`.

### Layer 3: Execution (`developer`, `scout`)
For each task:
1. Read the task spec, inputs and success criteria.
2. Produce the output (schema, sample data, portal spec, scripts, tests). The workbook is
   always generated by `scripts/build_workbook.py` from the schema, never edited by hand.
3. Run `./scripts/test.sh`; for portal work also `python3 scripts/render_preview.py`.
4. Update `docs/TECH_DEBT.md` with anything deferred or fragile.
5. Return the result, the evidence (test summary) and the next steps.

### Layer 4: Artifacts
Every task returns concrete artifacts: files, commands run with their output,
test results, and a short summary of what was built and what is next.

### Layer 5: Verification and review loop (`reviewer`)
See "Review loop" below. Only mark a task complete when it actually works.

### Layer 6: Feedback
If something fails:
* Read the error, logs and context.
* Write a focused fix for the real issue, not the symptom.
* Retry up to 3 times (escalating model per the routing rules), then escalate to the user with options.
* Add the lesson to "Lessons learned" below so it does not repeat.

### Layer 7: Completion
Before finishing, all of these must hold:
* All core features work and are tested.
* No critical errors or security issues (no secrets in the repo, no personal data in sample workbooks).
* `/handoff` done: the handoff package is built in `dist/` and `docs/DEPLOY.md` is filled in.
* The design system checklist passes on the portal.
* `docs/` is up to date.
* A final summary of what was built, what works and what is left.
* `/retro` has been run so the template learns from this project.

## Execution loop

```
1. Read docs/PLAN.md and pick the next ready tasks.
2. Route each task to the cheapest capable agent; run independent tasks in parallel.
3. Developer runs ./scripts/test.sh after every change.
4. Reviewer checks the output (review loop).
5. Fix any issues and retry, escalating the model only after a real failure.
6. Merge completed work, update PLAN.md status (batched, via scout).
7. Continue until the application is fully working.
```

## Review loop

Every task passes through this loop before it is marked done:

```
developer builds + tests  →  reviewer reviews  →  verdict
     ^                                                 |
     |___________ CHANGES (max 3 rounds) _____________|
                                                       |
                         APPROVED → merge, update PLAN.md
                         BLOCKED  → escalate to pm / user
```

The reviewer checks, in order: spec, schema contract, tests (runs them itself),
admin load, clarity (each view supports a PRD decision), design system checklist,
safety, and tech debt. Details in `.claude/agents/reviewer.md`.

At the end of each milestone, run `/review` for a full pass across the whole project
and let the `pm` reprioritise `docs/PLAN.md` from the findings.

## Standard handoff package

Every project hands over the same package, generated by `scripts/build_handoff.py` from the
schema and portal spec, so it can never drift from what was built and tested:

| File | For | Content |
| :--- | :--- | :--- |
| `<title>.xlsx` | shared drive | the workbook: tables, dropdowns, About sheet, lookups seeded |
| `README.md` | the product owner | what is in the package, deploy steps, portal steps, rules |
| `PORTAL_BUILD.md` | Copilot Cowork | instructions, data model, status colours, every page, look and feel, checklist |
| `preview.html` | both | reference render on sample data |
| `DESIGN_SYSTEM.md` | both | full design system reference |

Improve the generator, never the output. `tests/test_handoff.py` checks the package covers
every table, column, status, page, KPI and chart.

## Design system

`design/DESIGN_SYSTEM.md` (Editorial Portfolio) is the reference for every portal and
dashboard. `design/tokens.css` holds the tokens and starter CSS. In short:
editorial not BI tool, tabs are questions, answer first (headline, lede, narrative,
3 insight cards, 6 KPI tiles, charts, full list), quiet canvas with crimson as the
only emphasis, one spotlight KPI per row, fixed stage colours everywhere.
`tests/test_portal.py` enforces the structural rules; the reviewer checks the rest.

## Commands

* `/kickoff`: start a new project from `docs/BRIEF.md` (brainstorm, plan, design, first tasks).
* `/brainstorm`: run only the brainstorm, for example for a major new feature.
* `/build`: run the execution loop on the next ready tasks.
* `/review`: run the review loop on recent work or the whole project.
* `/handoff`: build the standard handoff package, fill in `docs/DEPLOY.md`.
* `/retro`: capture learnings and propose improvements to this template.
* `./scripts/test.sh`: run the full test system (schema, workbook, rules, portal).
* `python3 scripts/build_workbook.py`: build the sample workbook (`--deploy` for the deployment
  workbook, `--deploy --from <live.xlsx>` to migrate a live copy and keep its data).
* `python3 scripts/render_preview.py`: render `portal/preview.html` from spec and workbook.
* `python3 scripts/build_handoff.py`: run tests and build the handoff package (`--from <live.xlsx>` to migrate).

## Repository map

```
CLAUDE.md                    this file: how the factory works
README.md                    how to start a project, how to improve the template
TEMPLATE_LEARNINGS.md        learnings fed back from projects (template level)
.claude/agents/              brainstorm, pm, architect, developer, reviewer, scout
.claude/commands/            kickoff, brainstorm, build, review, handoff, retro
design/                      design system and tokens
docs/                        BRIEF, BRAINSTORM, PRD, PLAN, ARCHITECTURE, DECISIONS, TECH_DEBT, REVIEW_LOG, DEPLOY
schema/workbook.schema.json  the workbook contract
portal/portal.spec.json      the portal contract
portal/preview.html          reference render (generated)
data/                        sample workbook and sample.json (synthetic data only)
dist/<title>/                the handoff package (generated), plus a zip of it
scripts/                     test runner, workbook generator, metrics, preview renderer
tests/                       the test system
```

## Lessons learned

Project level lessons. One line each, newest first: `date: lesson (where it bit us)`.
`/retro` decides which of these should move into the template itself.

* 2026-10-14: rock state and milestone status colours must follow the user's existing reports, not our own palette (the first brief used colours the user did not recognise).
* 2026-10-14: LibreOffice cannot evaluate VSTACK, FILTER or CHOOSECOLS, so the consolidated sheets are only proven in Excel; ship the one rock fallback brief and list the Excel check (T05, TD14, TD29) early.
* 2026-10-14: parallel developers editing `docs/TECH_DEBT.md` and `docs/PLAN.md` caused merge noise and a duplicate id (TD31); batch debt and plan changes through the operator.
* 2026-10-14: user feedback after seeing a real artifact changed the model twice (change requests 1 and 2), so ship a testable sample workbook and preview early and keep the schema, sample and rule mirror cheap to change together.
