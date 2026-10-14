# Brainstorm: Rock Tracker (strategic initiative cockpit)

Owner: `brainstorm`. Status: draft, awaiting user answers. Comes before `docs/PRD.md`.

## Purpose

Today each rock (strategic initiative) is reported through hand-built steerco decks, ad hoc status mails and one-off answers to executive questions. Product managers rebuild the same facts in several formats; executives see slightly different versions of state, dates and commitments; the product director has to chase people to know where bottlenecks are.

A single workbook that every view and every email is generated from would make three things better: the director sees risk and slippage without asking, executives see one consistent story (committed vs choice point vs not committed), and PMs update one place once a week instead of answering in many formats.

If we do nothing: deck preparation keeps eating PM time before each steerco, state drifts between decks, and decisions (choice points) are surfaced late because nobody sees them across all rocks at once.

## Objective

**Recommended:** Leadership can see, at any moment and without asking anyone, where every rock stands, what is committed in the next six months and which risks and choices need them, from data PMs keep current in 15 minutes a week.

Alternatives considered:
1. "Steerco runs from the cockpit, not from decks." Sharp and testable, but narrows the value to meetings and ignores the director's continuous view.
2. "PMs report once and every executive question is answered from that." Strong on the PM pain, weak on what leadership actually gets.

The recommended framing keeps both sides (consumer clarity and producer effort) and makes the upkeep budget part of the objective, so the PRD cannot trade it away.

## Goals

| # | Goal | How we know (workbook computable where possible) | Time frame |
| :--- | :--- | :--- | :--- |
| G1 | Data is fresh | At least 90% of active rocks have a check-in dated in the last 7 days | Every week from week 4 after go-live |
| G2 | Steerco decks retired | Number of rock steercos run from the portal vs from a deck (director logs it); target 100% portal | By the second steerco cycle after go-live |
| G3 | Upkeep within budget | Median self-reported minutes per PM per week at or below 15 (one question in the check-in row) | Measured weeks 2 to 6 |
| G4 | Every risk to delivery has an owner and action | 100% of milestones with forecast later than plan, and of high risks, have an open action with owner and due date | Within 6 weeks of go-live |
| G5 | Email update on demand | Director produces a sendable update for one or all rocks in under 5 minutes | From go-live |

## Users and moments

* **Product director** (weekly, Monday or before 1:1s): opens the overview, scans rocks that turned amber or red, slipping milestones and stale check-ins; next step is a conversation with the PM or an escalation.
* **Executives / steerco** (monthly or per steerco): open the overview and one rock page during the meeting; look at roadmap commitment state, top risks, choice points awaiting decision; next step is a decision recorded against the choice point.
* **Product managers / initiative leads** (weekly, the person who keeps data current): add one check-in row per rock (status, one-line headline, attention point), adjust forecast dates on milestones that moved, touch risks only when they change. Next step: done, no deck to make.
* **Director or PMO** (on request): generates the email update from the latest check-ins and pastes it into Outlook.
* **Workbook owner** (quarterly): adds or closes rocks, updates purpose, goals and value chain, maintains lookups.

## Options compared

| Option | Shape | Effort | Upkeep per PM per week | Value |
| :--- | :--- | :--- | :--- | :--- |
| A. Smallest possible | One `Rocks` table (one row per rock: purpose, lead, status, headline, positions filled / planned, next milestone, top risk as text). Portal: overview and one rock page. | Low | 5 min | Consistent state in one place, but no real roadmap, no risk matrix, no history; email update is thin. |
| B. Cockpit core (recommended) | Tables: `Rocks` (slow-changing profile plus resourcing counts), `Milestones` (release, planned date, forecast date, commitment: Committed / Choice point / Not committed), `Risks` (likelihood x impact, owner), `Actions` (linked to risk or milestone), `CheckIns` (one row per rock per week: status, headline, attention point, minutes spent). Status partly computed (forecast vs plan slip). Email text built from latest check-in plus slipping milestones and top risks. Tabs as questions: "Where do the rocks stand?", "What ships in the next six months?", "What could stop us?", "What do we need to decide?", plus a rock detail page. | Medium | 10 to 15 min | Covers every brief requirement, gives trend and freshness, makes choice points visible. |
| C. Full portfolio system | B plus `Roles` (each position, filled or open, person), `Dependencies` between rocks, decision log, budget, snapshot history per field. | High | 20 to 30 min | Richer, but breaks the 15 minute budget and drifts toward a PPM tool in Excel. |
| D. Change a habit, do not build | One standard one-page steerco template (Word or PowerPoint) with fixed sections, filled monthly by each PM. | Very low | 15 to 30 min per cycle | Fixes format sprawl only; no overview, no on-demand view, still a static deck. |
| E. Feed from existing tool | If releases already live in Jira / Azure DevOps / a roadmap tool, the workbook holds only rock profile, risks and check-ins, and milestones are pasted or linked. | Medium | Lowest if export is automated | Avoids double entry but depends on access and export discipline the factory cannot verify. |

## Challenges and risks

| Challenge | Seriousness | What would settle it |
| :--- | :--- | :--- |
| Executives still ask for slides, so the deck never dies and the workbook becomes extra work. This is the assumption that kills the idea. | High | Director commits to running the next two steercos from the portal; ask one exec sponsor up front. |
| Upkeep breaks 15 minutes when a PM leads several rocks or risk lists grow long. | High | Count rocks per PM; cap risks shown per rock (top 5); make check-in a single row; prefill unchanged values. |
| "Watermelon" status: green on the surface, red inside. Self-reported RAG is political. | High | Compute at least part of status from data (forecast later than plan, open high risks, positions unfilled) and show the PM's call next to the computed one. |
| Double entry with an existing delivery tool (Jira, ADO, roadmap) for releases and dates. | Medium to high | Ask which tool holds releases today; if one exists, consider option E for milestones. |
| Unclear semantics of Committed vs Choice point vs Not committed, so execs are still confused. | Medium | Agree three one-line definitions with the director before the PRD; put them on the About sheet and portal. |
| Sensitive content (risks naming people, open positions, strategic choices) in a workbook every editor can read. | Medium | Confirm audience and location permissions; keep names to role level where possible; no HR detail. |
| Excel and Cowork fit: volume is tiny (tens of rocks, hundreds of rows), but co-authoring conflicts and Cowork's ability to render a roadmap timeline and 5x5 risk matrix are unverified. | Medium | Use structured tables only, one row per update (append, not overwrite); spike the roadmap and matrix in the preview early. |
| Email update format unknown; generating good prose from cells can read robotic. | Low to medium | Get one real past update email as the template; build text from fixed sentences plus the PM's headline. |
| Freshness decays after the launch weeks. | Medium | Show "last check-in" age per rock prominently; stale rocks appear on the director's first tab. |

## Assumptions to validate

1. Steerco members will use a portal (or its printout) instead of a deck.
2. Between 5 and 15 active rocks, each with one lead PM, and few PMs lead more than two.
3. A weekly check-in is the right cadence; steerco is monthly or less.
4. Releases are not already maintained in a tool that could feed the workbook.
5. A simple 1 to 5 likelihood x impact scale is acceptable to leadership.
6. History of status (trend) matters, so append-only check-ins are worth it over overwrite.
7. The audience of the workbook is trusted to see all rocks, risks and resourcing gaps.

## Questions for the user

Ranked by impact on the design.

1. Will the director and steerco commit to running reviews from the portal instead of decks? Who is the executive sponsor?
2. How many rocks are tracked, and how many PMs / initiative leads? How many rocks does the busiest PM lead?
3. Update cadence: weekly check-in by PMs, and how often is steerco (monthly, quarterly)?
4. Where do releases and dates live today (Jira, Azure DevOps, a roadmap tool, nowhere)? Should milestones be entered by hand or pasted from an export?
5. Email update format: who receives it, per rock or all rocks, how long, and can you share one past example to use as the template?
6. Risk scoring scale: 3x3 or 5x5 likelihood x impact, and what score counts as "high" for escalation?
7. Definitions: what exactly makes a release Committed, a Choice point, or Not committed, and who decides a choice point?
8. Workbook location ({LOCATION}): which SharePoint site or OneDrive folder, and who can read and edit it?
9. Portal owner ({OWNER}): who builds and maintains the portal in Copilot Cowork?
10. Other constraints ({CONSTRAINTS}): sensitivity labels, naming rules, language, branding, data that must not be included?
11. Deadline ({DATE}): when is the first steerco or review that should run on this?
12. Is status trend (history) needed, or is the latest state enough?
13. Resourcing: are counts (x of y positions filled) enough, or do you need named roles?

## Recommendation

Build **option B, cockpit core**, with option E held in reserve if releases already live in a delivery tool. It meets every requirement in the brief while staying inside the 15 minute budget, provided a PM leads no more than two or three rocks.

The PRD should focus on:
* The weekly PM check-in as the single upkeep moment: one row per rock, plus only the milestone dates and risks that changed. Design the 15 minute budget in, and measure it (G3).
* Clear commitment semantics on the six-month roadmap and a visible list of choice points awaiting decision.
* Status that is partly computed from data, to protect trust in the cockpit.
* Freshness made visible (last check-in age), so staleness is an attention point, not a hidden failure.
* An email update generated from the same data, matched to one real example.
* Deferring roles detail, dependencies, decision log and budget (option C) until after two steerco cycles prove adoption.

## User answers and chosen direction


Answers given on 14 Oct 2026.

1. **Adoption:** yes. Steerco updates will run off the portal, and the director will enforce this.
2. **Scale:** each initiative lead has one, at most two, rocks. A GPM owns a portfolio of 1 to 5 rocks.
3. **Cadence:** updates every one or two weeks. The check-in must not assume a strict weekly rhythm.
4. **Source of releases:** entered by hand. Expect 3 to 5 key items (epics) per rock per quarter. No integration (option E dropped).
5. **Email update:** example shared (weekly status update for a GPM portfolio of three rocks). Its structure is the template:
   * Header: week of, rocks in the portfolio, prepared by (name, role).
   * Portfolio table: rock, state (On track, At risk, Off track), epics slipped (x of y), positions filled (x of y), one line summary.
   * Key call outs: decisions needed with a date, overdue forecasts, upcoming events.
   * Development update: counts of epics by status (Delivered, On plan, On watch, Slipped, On hold, Not committed), releases this period, average slip in weeks.
   * Key risks and issues: short bullets, often linked to epics and key results.
   * Per rock section: state, resourcing, headline, then an epic table with planned date, forecast date, status and comment. Each epic carries an ADO id and its contribution to key results (for example "60% of KR 1.1").
6. **Risk scale:** 3x3. "High" means very likely to impact the timeline.
7. **Commitment states** (Committed, Choice point, Not committed) are set by hand from the steerco outcome. No rule to compute them.
8. **Location:** a SharePoint site shared across stakeholders.
9. **Portal owner:** the user (product director) builds and maintains the portal in Copilot Cowork.
10. **Deadline:** next steerco is next week (week of 19 Oct 2026). A usable first version must be ready before then.
11. **History:** yes, keep it light, but it must be possible to look back quarter by quarter.
12. **Staffing:** counts only (x of y positions filled).
13. **Upkeep shape:** ideally one rock is one Excel tab to upkeep.

### Chosen direction

Option B, "cockpit core", adjusted with the answers above:

* Vocabulary follows the email example: rocks have **epics** (the key deliverables, with ADO id and key result contribution), a **state** (On track, At risk, Off track) and an epic **status** (Delivered, On plan, On watch, Slipped, On hold, Not committed), plus the roadmap commitment level (Committed, Choice point, Not committed) set by hand.
* Key results per rock are in scope because the example links epics and risks to them.
* Decisions needed and call outs are first class, since they lead the email.
* The email update reproduces the example structure for a portfolio (one GPM, several rocks).
* Light history: a check-in snapshot per rock per update (state, counts, summary) is enough to look back quarter by quarter.
* **Open design tension for the architect:** the user prefers one tab per rock for upkeep, while the factory standard is one sheet per table so the portal and email can consolidate across rocks. The architect must resolve this and record the decision, with upkeep per PM as the deciding factor.
* Deadline is tight: plan a minimal first slice that can run next week's steerco, then iterate.
