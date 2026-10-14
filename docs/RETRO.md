# Retro: Rock Tracker (kickoff stage)

Date: 14 Oct 2026. Run during kickoff, before any build work. Sources checked: Lessons learned in
`CLAUDE.md` (empty), `docs/REVIEW_LOG.md` (no entries yet), `docs/TECH_DEBT.md` (no entries yet),
`docs/DECISIONS.md` (architect still writing), the kickoff conversation and its agent runs.
With no build or review history yet, every learning below comes from the kickoff flow itself.

## Template learnings (proposed)

### L1. Add a user gate on the PRD before the architect starts
* **Evidence:** the architect was launched straight after the PM, as `/kickoff` step 4 says.
  The user then asked to review the PRD first and changed it twice (one tab per rock, history,
  steerco reading order, essential fields). The architect was stopped twice, wasting two runs.
* **Change:** in `/kickoff`, after the PM step, show the PRD summary (tabs, fields, upkeep
  budget, milestones, assumptions) and wait for the user's approval before running the architect.
  Record the approval at the bottom of `docs/BRAINSTORM.md`.
* **Files:** `.claude/commands/kickoff.md`.
* **Effect:** no architect run on a PRD the user has not accepted; fewer stopped agents.

### L2. Ask for an example of today's output in the brief
* **Evidence:** the user's existing weekly status email reshaped the whole vocabulary (epics,
  rock state, six epic statuses, key result contribution, call outs, decisions). It arrived
  only after the brainstorm, as an answer to question 5.
* **Change:** add a section "What it replaces (attach an example)" to the `docs/BRIEF.md`
  template, and make the brainstorm agent ask for it first if it is missing, before choosing
  options.
* **Files:** `docs/BRIEF.md` (template), `.claude/agents/brainstorm.md`.
* **Effect:** vocabulary and structure come from real artifacts from the start, not after a
  round of options.

### L3. Ask how the views will be read (meeting agenda or reading order)
* **Evidence:** the PM designed the portal tabs from scratch; the user replaced them with the
  steerco reading order (messages, state, roadmap, choice points, risks, decision log). A
  decision log the PM had put out of scope turned out to be core.
* **Change:** add to the brainstorm "Users and moments" step: "In which meeting or routine is
  this read, and in what order does that meeting run?" Add a rule to the PM: portal tabs follow
  that order when one exists.
* **Files:** `.claude/agents/brainstorm.md`, `.claude/agents/pm.md`, `docs/BRIEF.md` (template,
  one line under Users).
* **Effect:** first draft of the tabs matches how people actually use them.

### L4. Every field must name its reader
* **Evidence:** the first PRD listed fields no view read (minutes spent per update, a key
  results table, an attention point separate from the main message, risk due dates, call out
  types). The user had to push back with "only capture essential information".
* **Change:** PM admin light rule: "Every field names the tab, chart or output that reads it.
  No reader, no field." Reviewer admin load check verifies the field to reader mapping in the
  PRD and schema.
* **Files:** `.claude/agents/pm.md`, `.claude/agents/reviewer.md`, `.claude/agents/architect.md`
  (schema columns carry a `read_by` note).
* **Effect:** smaller workbooks, less upkeep, fewer user corrections.

### L5. Ask how people want to update, before fixing the sheet layout
* **Evidence:** the template's architect rule is "each sheet is one table". The user wants one
  tab per rock with everything about that rock on it. The conflict surfaced late and became an
  open design tension.
* **Change:** brainstorm asks: "Do updaters want one place per item (a tab per initiative,
  product or team) or shared lists?" Architect rule softened: "Each table is an Excel Table
  object. Default one table per sheet; an entity sheet holding several same shaped tables is
  allowed when the user asks for it, provided consolidation needs no manual copy."
* **Files:** `.claude/agents/brainstorm.md`, `.claude/agents/architect.md`.
* **Effect:** the layout question is settled in the brainstorm, not mid kickoff.
* **Note:** generator and test support for entity sheets is being built in this project. Promote
  that code in a later retro once it is built and reviewed; do not promote it now.

### L6. A default ladder for history
* **Evidence:** history ("look back quarter by quarter, keep it light") had no template answer,
  so it needed its own brainstorm round with the user.
* **Change:** add a "History" section to the `docs/ARCHITECTURE.md` template and to the architect
  agent with the default ladder: SharePoint version history (free backstop), baseline columns
  next to forecasts, automatic snapshot log by Office Script on a Power Automate schedule (button
  fallback). The brainstorm asks whether history is needed and how far back.
* **Files:** `docs/ARCHITECTURE.md` (template), `.claude/agents/architect.md`,
  `.claude/agents/brainstorm.md`.
* **Effect:** history is decided in one question instead of a separate round.
* **Confidence:** medium. Most trackers need it; the snapshot script itself is not built yet and
  is not promoted.

### L7. Plan the workbook first, the portal second
* **Evidence:** the first plan bundled workbook and portal into one milestone; the user asked to
  build the Excel first. This follows from principle 3 ("the workbook is the contract").
* **Change:** the `docs/PLAN.md` template and PM guidance split M1 into phase A (workbook,
  sample data, rules, tests, workbook review) and phase B (portal spec, preview, handoff).
* **Files:** `docs/PLAN.md` (template), `.claude/agents/pm.md`.
* **Effect:** a usable workbook earlier; portal work starts on a stable schema.

## Project only learnings (stay in this repo)

* One tab per rock, with consolidation for portal, email and history.
* Steerco reading order: messages and decisions requested, state, roadmap with choice points,
  risk matrix, decision log.
* Decisions requested and the decision log are one table.
* Email update follows the GPM weekly status example.
* 3x3 risk scale, High is 6 or 9; snapshots every Monday including epics.
* Deadline pressure: first steerco a week after kickoff.

## Status

Proposals awaiting the user's choice. No template change made yet.
