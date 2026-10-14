# Product Requirements: Rock Tracker (strategic initiative cockpit)

Owner: `pm`. Status: v1, 14 Oct 2026. Builds on `docs/BRAINSTORM.md`, option B "cockpit core" as adjusted by the user answers of 14 Oct 2026. The "how" (sheets, keys, formulas, portal layout) belongs to the `architect`.

## Problem

Each rock (strategic initiative) is reported today through hand built steerco decks, ad hoc status mails and one off answers to executive questions. Product managers rebuild the same facts in several formats, executives see slightly different versions of state, dates and commitments, and the product director has to chase people to find bottlenecks. Choice points surface late because nobody sees them across all rocks at once.

**Objective.** Leadership can see, at any moment and without asking anyone, where every rock stands, what is committed in the next six months and which risks and choices need them, from data initiative leads keep current in 15 minutes a week or less.

**Deadline.** The next steerco (week of 19 Oct 2026) runs from the portal, not from a deck. The director has committed to enforce this. Milestone 1 exists only to make that steerco work.

## Users and jobs

| User | Moment | Job to be done | Upkeep role |
| :--- | :--- | :--- | :--- |
| Product director | Weekly (Monday or before 1:1s), and in every steerco | Spot rocks turning At risk or Off track, slipping epics, stale updates; prepare the steerco; build and keep the portal in Copilot Cowork | Reader, portal owner, workbook owner |
| Executives / steerco | Each steerco, occasionally between | See roadmap commitments, top risks and choice points; take decisions; never be confused about state | Reader only, zero upkeep |
| Initiative lead (PM, 1 or at most 2 rocks) | Every one or two weeks | Record the rock's state, one line summary, epic forecast changes, risks and call outs that changed. Nothing else, no deck | Main data entry |
| GPM (portfolio of 1 to 5 rocks) | Every one or two weeks, and on request | Check the leads' updates, add portfolio level decisions needed and events, send the portfolio email update | Light review, email sender |
| Workbook owner (director or PMO) | Quarterly | Add or close rocks, maintain lookups (people, value chains) | Structural upkeep |

## Vocabulary and definitions

These go verbatim on the About sheet and in the portal, so nobody has to guess.

**Rock state** (set by the lead at each update; one of three):

| State | Meaning | Exit rule |
| :--- | :--- | :--- |
| On track | All committed epics are forecast on or before their planned date and no High risk is without an action | Moves to At risk as soon as one of those stops being true |
| At risk | At least one committed epic is slipping or a High risk is open, and the lead believes it is recoverable this quarter | Back to On track when forecasts are back on plan; to Off track when not recoverable without a steerco decision |
| Off track | Commitments for this quarter will be missed without a steerco decision (scope, date or people) | Leaves only after steerco has decided and the plan is re baselined |

**Epic status** (the six statuses of the email example). Requirement: as much as possible is derived, not typed.

| Status | Rule | Set by |
| :--- | :--- | :--- |
| Delivered | Shipped | Lead (by hand) |
| On hold | Paused by decision | Lead (by hand) |
| Not committed | Commitment level is Choice point or Not committed, and not Delivered | Derived |
| Slipped | Committed, and forecast date later than planned date | Derived |
| On watch | Committed, forecast still on plan, but the lead flags a concern | Lead (one flag) |
| On plan | Committed, forecast on or before planned date, no flag | Derived (default) |

**Planned date** is the date steerco committed to. It changes only when steerco re baselines. **Forecast date** is the lead's current best estimate and is the date leads update.

**Roadmap commitment level** (set by hand from the steerco outcome, no rule computes it):

* **Committed:** steerco has agreed to deliver this epic by its planned date.
* **Choice point:** a decision (scope, date, funding or people) is needed before it can be committed. Carries a decide by date.
* **Not committed:** a known future need on the horizon, with no promise of date or scope.

**Risk rating** on a 3 by 3 grid (likelihood Low, Medium, High by impact Low, Medium, High). A risk is **High** when it is very likely to impact the timeline. Assumption: High = likelihood High and impact Medium or High, or likelihood Medium and impact High (score 6 or 9 on a 1 to 3 by 1 to 3 scale). To be confirmed (Q1).

## Decisions this tool supports

| # | Decision | Who | When | Where in the tool |
| :--- | :--- | :--- | :--- | :--- |
| D1 | What must steerco hear and decide today? | Steerco | Each steerco | Tab 1 |
| D2 | Which rocks need attention: roadmap, risk or resourcing? | Director, steerco | Weekly, each steerco | Tab 2 |
| D3 | Do we confirm, change or re baseline the six month commitments? | Steerco | Each steerco | Tab 3 |
| D4 | Which choice points do we close, and which way? | Steerco | Each steerco | Tab 3.1 |
| D5 | Which risks need help, an owner or an escalation? | Director, steerco | Each steerco | Tab 4 |
| D6 | What did we decide before, and did it happen? | Director, steerco | Each steerco, quarter end | Tab 5 |
| D7 | What do I tell my stakeholders this week? | GPM, director | Every one or two weeks | Email update |

## Portal tabs (the steerco reading order, set by the user)

The portal reads in the order steerco runs. Each tab follows `design/DESIGN_SYSTEM.md` (headline, lede, narrative, insight cards, KPI tiles with one spotlight, charts, full list). Every tab can be filtered to one rock or one GPM portfolio, so there is no separate rock page. The architect finalises tiles in `portal/portal.spec.json`.

**Tab 1. "What does steerco need to hear?"** (M1). Supports D1. Everything here is written by the initiative lead on the rock tab.
* Per rock: main message (one or two lines), top risks, call outs, and steerco decisions requested with a decide by date.
* Spotlight: decisions requested for this steerco.

**Tab 2. "Where do the rocks stand?"** (M1). Supports D2. Overall state per rock across three lenses.
* Per rock: state (On track, At risk, Off track), roadmap (committed epics slipped x of y), risks (open high risks), resourcing (positions filled x of y).
* Spotlight: rocks At risk or Off track.

**Tab 3. "What ships in the next six months?"** (M1). Supports D3.
* Six month timeline per rock showing Committed, Choice point and Not committed, with planned vs forecast.
* Spotlight: committed epics on plan (x of y).
* **3.1 "Which choices are open?"** Choice points only: what the choice is, options, decide by date, rock. Spotlight: choice points due by the next steerco.

**Tab 4. "What could stop us?"** (M1). Supports D5.
* 3 by 3 risk matrix with counts per cell, then the risk list with key action and owner.
* Spotlight: high risks without a key action.

**Tab 5. "What did steerco decide?"** (M1). Supports D6. Decision log from previous steercos.
* Each decision: steerco date, rock, decision, outcome, owner, follow up status.
* Spotlight: decisions with an open follow up.
* The log is the same table as the decisions requested on tab 1: the lead raises the request, and after steerco the outcome is filled in on the same row. Nothing is typed twice.

## Only essential information

Every field must feed one of the five tabs or the email. If no tab or email section reads it, it is not in the workbook. Fields dropped for this reason: a separate key results table (the key result link is a short text on the epic, for example "60% of KR 1.1"), minutes spent per update, an attention point separate from the main message, links from risks to epics, risk due dates, and per field change history. A separate call out type for events is dropped too: call outs are free text, and decisions have their own table.

## Email update (M2, required structure)

Generated from the same data for one GPM portfolio (or one rock, or all rocks). It must reproduce the user's example, in this order:

1. **Header:** week of, rocks in the portfolio, prepared by (name, role).
2. **Portfolio table:** rock, state, epics slipped (x of y), positions filled (x of y), one line summary.
3. **Key call outs:** decisions needed with a date, overdue forecasts, upcoming events.
4. **Development update:** count of epics per status (Delivered, On plan, On watch, Slipped, On hold, Not committed), releases this period, average slip in weeks.
5. **Key risks and issues:** short bullets from the top risks.
6. **Per rock section:** state, resourcing, headline, then the epic table (epic, ADO id, planned date, forecast date, status, comment, contribution to key results such as "60% of KR 1.1").

Requirements: no value is typed for the email that is not already in the workbook; the sender only picks the portfolio and the date; a sendable text is ready in under 5 minutes (G5). The mechanism (Cowork prompt, workbook generated text, or both) is the architect's call. The factory must ship a reference rendering on sample data that tests can check section by section.

Assumed derivations, to be confirmed by the architect: "this period" is the 14 days ending on the update date; "releases this period" is epics marked Delivered in that window; "average slip" is the mean of forecast minus planned, in weeks, over slipped committed epics; "epics slipped x of y" counts committed epics in the six month window.

## What the workbook must hold (what, not how)

| Fact | Owner | Changes | Why it exists |
| :--- | :--- | :--- | :--- |
| Rock profile: name, purpose, goals, what it delivers, value chain, initiative lead, GPM, active flag | Workbook owner, lead may edit | Quarterly | Name, lead and GPM: rock and portfolio filter on every tab, email header. Purpose, goals, what it delivers and value chain: rock header on tab 1 and the per rock section of the email (from the brief) |
| Positions planned and filled (counts only) | Lead | When it changes | Tab 2, email |
| Epics: title, ADO id, commitment, planned date, forecast date, status (hand set values only), comment, key result link as short text | Lead | Forecast and comment when they move | Tabs 2 and 3, email |
| Risks: title, likelihood, impact, key action, action owner, open or closed, top risk flag | Lead | Only when they change | Tabs 1 and 4, email |
| Call outs: text, date, open or closed | Lead | When raised or closed | Tab 1, email |
| Decisions: steerco date, decision requested, decide by, choice point flag, options (choice points only), outcome, owner, follow up status | Lead raises, lead records the outcome after steerco | When raised and after each steerco | Tabs 1, 3.1 and 5, email |
| Update: date, state, main message (one or two lines) | Lead | Every one or two weeks, overwritten in place on the rock tab; history comes from the snapshot log | Tabs 1 and 2, history, G1 |
| Lookups: people (name, role), value chains, states, statuses, commitment levels | Workbook owner | Rarely | Dropdowns everywhere |

One key action per risk is enough; no separate actions log in M1 or M2. Names are kept to people in their work role; no HR detail, no reasons for vacancies.

## Upkeep requirement: one tab per rock (decided by the user)

Each rock has its own Excel tab that holds all of its key information: profile, state and main message, resourcing, epics, risks with key actions, call outs and decisions. This is a user decision, not open for the architect. The architect designs how the portal, the email and history consolidate across the rock tabs, and records that design in `docs/DECISIONS.md`. The design must meet all of these:

1. A lead does the whole regular update for one rock on that rock's tab, without touching any other tab.
2. The regular update takes 7 minutes or less per rock, so a lead with two rocks stays within 15 minutes.
3. No fact is typed twice. Unchanged values carry over without retyping (for example, the new update row starts from the previous state and summary, or only changed fields are entered).
4. Consolidation across rocks for the portal, the email and history needs zero manual copy steps by anyone.
5. Adding or closing a rock takes the workbook owner 10 minutes or less and needs no change to the portal in Cowork.
6. Two leads updating different rocks at the same time on SharePoint do not overwrite each other.
7. A blank or half filled row never breaks the portal or the email.

## History (decided by the user: automatic snapshot log)

* A History area holds one row per rock per snapshot (date, state, headline, epics slipped x of y, epics delivered, positions filled x of y, open high risks) and one row per epic per snapshot (forecast date, status, commitment).
* Snapshots are taken automatically by an Office Script run on a schedule by Power Automate, so nobody has to remember. Default schedule: every Monday morning, which covers both weekly and fortnightly update rhythms.
* Fallback if the tenant blocks Power Automate: the same script behind a "Save snapshot" button, pressed by the GPM before each steerco.
* SharePoint version history stays on as a free backstop. Planned (baseline) dates on epics show slip in the current data without history.
* Size stays small: about 400 rock rows and 2,000 epic rows a year at 15 rocks.
* M1 ships the History tables and the snapshot script so history accumulates from the first steerco; the look back tab comes in M3.

## Scope

### Milestone 1: Steerco slice (factory ready Fri 16 Oct 2026, steerco week of 19 Oct)
* Workbook with every fact listed above, dropdowns from lookups, About sheet with the definitions, a short "how to update in 7 minutes" guide, and synthetic sample data.
* One tab per rock, with consolidation for the portal built (see Upkeep requirement).
* History tables and the snapshot script with setup steps for Power Automate (see History).
* Derived epic status (Slipped, On plan, Not committed), slip counts, positions x of y, update age.
* Portal spec and preview for tabs 1 to 5 and 3.1, including the six month timeline, the 3 by 3 risk matrix and the decision log.
* Handoff package (`dist/`) and `docs/DEPLOY.md`, so the director can deploy on SharePoint on Friday, leads can load their rocks over Friday and Monday, and the director can build the portal in Cowork before the steerco.

### Milestone 2: Email and trust (target Fri 30 Oct 2026)
* Email update for a GPM portfolio, a single rock or all rocks, following the required structure, with a reference rendering and tests.
* Data based state signal next to the lead's call, and a "check the call" flag when the lead's state is greener than the data (watermelon guard).
* Freshness made visible (G1).
* Migration of the live workbook with `--from`, keeping all data entered since M1.

### Milestone 3: Look back (target before quarter end, Fri 11 Dec 2026)
* Quarter by quarter look back (trend on tabs 2 and 5) from the snapshot history.
* Cockpit health figures for G1 to G4 computed in the workbook.

### Out of scope (all milestones unless adoption after two steerco cycles proves the need)
* Integration with Azure DevOps or any other tool. ADO id is stored for traceability only.
* Named roles or people per position; dependencies between rocks; budget; per field change history; a separate actions log.
* Building the portal itself (the director builds it in Cowork from the handoff package).
* Slide or PDF export beyond printing the portal.

## Success criteria

All computable from the workbook unless marked.

| # | Criterion | Measure | Target and time |
| :--- | :--- | :--- | :--- |
| S0 | Steerco runs from the portal | Steerco of week of 19 Oct held from the portal without a deck (director confirms) | Week of 19 Oct 2026 |
| G1 | Data is fresh | Share of active rocks with an update dated in the last 14 days | 90% or more, every week from week 4 |
| G2 | Decks retired | Steercos run from the portal vs from a deck (director logs it) | 100% from the second steerco cycle |
| G3 | Upkeep within budget | Leads asked at the first two retros how long the update takes (no field in the workbook) | 15 or less, weeks 2 to 6 |
| G4 | Every delivery risk has an owner and action | Share of slipped committed epics and High risks that have an open key action with owner and due date | 100% within 6 weeks of go live |
| G5 | Email on demand | Time from opening the portal to a sendable portfolio email (GPM confirms) | Under 5 minutes from M2 |

## Upkeep budget

Steady state, per person per week. One off onboarding (first load of a rock, about 30 to 45 minutes per rock in the week of 16 Oct) is outside the budget and stated in `docs/DEPLOY.md`.

| Role | What they do | Minutes per week |
| :--- | :--- | :--- |
| Initiative lead, 1 rock | On the rock tab: state and main message, forecasts and comments that moved, risks and call outs that changed, decisions requested, outcomes and commitment levels after a steerco | 7 or less |
| Initiative lead, 2 rocks | Same, per rock | 15 or less |
| GPM, 1 to 5 rocks | Scan tabs 1 and 2 for the portfolio, send the email (from M2) | 15 or less |
| Product director | Weekly scan of tabs 1, 2 and 4, nudge stale rocks; portal changes only when the schema changes | 15 or less (portal build is one off) |
| Executives | Read only | 0 |
| Workbook owner | Add or close rocks and lookups at quarter start (about 30 minutes per quarter) | 3 or less averaged |

The cap is 15 minutes per person per week. If a role reports being above budget for two consecutive weeks, the PM reprioritises the plan to remove fields or derive more, before adding anything new.

## Weekly and steerco rituals

* **Lead update** (every one or two weeks, any day before Monday): on the rock tab, state and main message, then only what moved.
* **Director scan** (Monday): tab 2 first, then exceptions on tabs 1 and 4. Output: nudges and 1:1 topics.
* **Steerco** (as scheduled): tabs in order 1, 2, 3 and 3.1, 4, 5. Within two working days after steerco, leads record decision outcomes and set commitment levels on their rock tab.
* **Email** (from M2, on request): GPM generates and sends the portfolio update.

## Risks and open questions

### Risks (carried from the brainstorm, plus the deadline)

| Risk | Seriousness | Mitigation |
| :--- | :--- | :--- |
| Deadline: four working days to build, deploy, load data and build the portal before steerco | High | M1 is the smallest slice that runs steerco; email, watermelon flag and history wait for M2 and M3; schema in M1 already holds every field the email needs so M2 adds no data entry |
| First data load slips because leads have not got the time before steerco | High | Short entry guide, synthetic sample as example, director asks leads to load by Mon 19 Oct noon; only active rocks needed |
| Upkeep breaks 15 minutes (long risk lists, many epics, two rocks) | High | Top 5 risks shown, 3 to 5 epics per quarter, values stay in place on the rock tab, only essential fields |
| Watermelon status: lead's call greener than the data | High | Derived epic status and slip counts shown next to the state in M1; explicit flag in M2 |
| Executives still ask for slides | Medium (director enforces) | Printable portal pages; G2 log |
| One tab per rock makes consolidation harder | Medium | User decision; architect designs consolidation against the upkeep requirements above |
| Dates drift from ADO because epics are entered by hand | Medium | Only 3 to 5 epics per rock; ADO id stored; planned date changes only at steerco |
| Commitment semantics misunderstood | Medium | Definitions on the About sheet and on tab 2 |
| Sensitive content on a SharePoint site shared across stakeholders (risks, vacancies, choices) | Medium | Counts only for staffing, people at role level, no HR detail; director confirms the audience (Q4) |
| Cowork cannot render the six month timeline or the 3 by 3 matrix well | Medium | Spec simple fallbacks (table grouped by month, 3 by 3 count table); preview them early |
| History of derived counts: formulas recalculate, so past slip counts are not frozen by themselves | Medium | Resolved by the automatic snapshot log (see History) |
| Email reads robotic | Low to medium | Fixed sentences around the lead's own summary and comments |
| Freshness decays after launch | Medium | Update age on tab 1, stale rocks as an exception tile |

### Open questions (none blocks M1; assumptions stated)

1. **High risk threshold.** Assumed: score 6 or 9 on the 3 by 3 grid. Confirm with the director.
2. **Number of rocks and GPMs.** Assumed up to 15 active rocks and up to 5 GPMs.
3. **Exact steerco date** in the week of 19 Oct. Assumed Wed 21 Oct; data load deadline Mon 19 Oct noon.
4. **Audience and permissions** on the SharePoint site: who may edit (leads, GPMs, owner) and who only reads.
5. **Email derivations:** "this period", "releases this period" and "average slip" as assumed above. Confirm against the example email.
6. **On watch:** is a lead flag acceptable, or should it be derived (for example, forecast within 2 weeks of planned)?
7. **Quarter definition** for history and the six month window: assumed calendar quarters.
8. **Prepared by** in the email: assumed the GPM of the portfolio.
