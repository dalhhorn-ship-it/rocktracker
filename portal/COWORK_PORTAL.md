# Copilot Cowork brief: Rock Tracker portal

Paste everything below the line into Copilot Cowork, with the Rock Tracker workbook linked from
SharePoint. It builds the full steerco portal for all rocks, with a rock and portfolio filter.
This version follows workbook schema 2.4.0, change requests 1 to 3 (milestones, MC quarters, teams,
4 quarter horizon, roadmap bars) and change request 4 (audience selection, filterable decision log).
Cowork first asks you which rocks to include, so you can build a portal for a specific audience.

**Before you start:** open the workbook once in Excel for the web, so it calculates and saves its
values. A freshly generated file has no stored results, and Cowork would find the calculated
columns empty.

**If the six summary sheets show errors** (Rocks, Milestones, Risks, CallOuts, Decisions, Teams),
the Excel check T05 has failed. Use `portal/COWORK_ROCK_TEST.md` for one rock until that is fixed.

---

## Your task

Build a read only web portal that briefs a steering committee on the company's strategic
initiatives, called **rocks**. Read all data from the linked Excel workbook. Do not invent, round
or reword data: show values exactly as they are in the workbook. If a value is empty, show a quiet
dash, never an error.

Words matter: always say **Milestone** (never Epic) and **Completed** (never Delivered).

The portal has a masthead, a filter bar and **six tabs** in the order the steerco runs. Each tab
title is a question:

1. What does steerco need to hear?
2. Where do we stand?
3. What are we delivering?
3.1 Which choices are open?
4. What could stop us?
5. What did steerco decide?

Show tab 1 first. Only one tab is visible at a time; the active tab has a crimson underline.

## Step 0: ask who this portal is for (before building anything)

Before you build, read the Rocks sheet and ask me two questions. Wait for my answers.

1. **Which rocks should this portal include?** Show me the active rocks (Active = Yes) as a numbered
   list, one line each: `{RockID} · {RockName} · GPM {GPM} · {ValueChain} · {State}`. Under the list,
   show the closed rocks (Active = No) separately as `Closed: {RockID} · {RockName}`. I can answer
   with:
   * `All`;
   * RockIDs, for example `R01, R03`;
   * one or more GPM names (all their active rocks);
   * one or more value chains (all active rocks in it).

   Repeat the resulting selection back to me as a list of RockIDs and names, and ask me to confirm.
2. **Who is the audience?** A short name for the masthead, for example `Executive steerco` or
   `B2C portfolio review`. When I give none, use `Steerco`.

Then build the portal **for the selected rocks only**:
* **Every number, list, chart, filter option and decision** uses only rows whose RockID is in the
  selection. This includes the decision log, the major risks and every total. Data of rocks outside
  the selection must not appear anywhere on the page, not even in counts.
* **Closed rocks:** their decisions appear in the decision log only when I named them explicitly
  (by RockID), or when I answered All.
* **Masthead:** the eyebrow becomes `ROCK TRACKER · {AUDIENCE}`. A grey meta line under the title
  reads `{n} rocks: {RockID list}`.
* **Footer:** `Built for {audience}. Shows {n} of {m} active rocks.`

To change the selection later, I rebuild the portal from this brief.

## Where the data is

Read only these six sheets. Each has its column names in row 1 and one record per row from row 2.
Find columns **by their header name**, never by position. A row counts only when its key column
(the first column) is not empty; ignore all other rows.

| Sheet | Key | Columns used |
| :--- | :--- | :--- |
| Rocks | RockID | RockID, RockName, ValueChain, Lead, GPM, Active, Purpose, Goals, Delivers, UpdateDate, State, MainMessage, Attention1, Attention2, Attention3, UpdateAgeDays, Stale, MilestonesCommitted, MilestonesSlipped, MilestonesOnPlan, MilestonesCompleted, MilestonesOverdue, OpenHighRisks, HighRisksNoAction, PositionsBudgeted, PositionsActual, FillPct, DataSignal, CheckCall, CurrentMCQuarter, NextMCQuarter, ThirdMCQuarter, FourthMCQuarter |
| Milestones | MilestoneKey | MilestoneKey, Title, Owner, Commitment, StartDate, PlannedDate, ForecastDate, ActualDate, LeadStatus, Comment, KRLink, ADOId, ADOLink, Description, Detail1, Detail2, Detail3, ProgressShown, Status, SlipWeeks, SlipSeverity, TimelineDate, MCQuarter, QuarterAhead, Visible, Overdue, RockID, Rock, GPM |
| Risks | RiskKey | RiskKey, Title, Likelihood, Impact, KeyAction, ActionOwner, RiskStatus, Score, High, NeedsAction, RockID, Rock, GPM |
| CallOuts | CallOutKey | CallOutKey, Text, Date, CallOutStatus, RockID, Rock, GPM |
| Decisions | DecisionKey | DecisionKey, Decision, SteercoDate, DecideBy, ChoicePoint, Options, Outcome, Owner, FollowUp, DecisionState, RequestNo, DueNextSteerco, OpenFollowUp, RockID, Rock, GPM |
| Teams | TeamKey | TeamKey, TeamName, TeamLead, Budgeted, Actual, FillPct, RockID, Rock, GPM |

Rules:
* **Active rocks only.** Show a rock only when Rocks.Active is Yes. Milestones, risks, call outs and
  teams belong to a rock through RockID; drop rows whose rock is not active. Decisions are the one
  exception: the decision log on tab 5 keeps decisions of closed rocks.
* **Use the workbook's calculated columns as they are.** Do not work these out yourself:
  * ProgressShown, Status, SlipWeeks, SlipSeverity, TimelineDate, MCQuarter, QuarterAhead, Visible
    and Overdue.
  * Score, High and NeedsAction.
  * DecisionState, RequestNo, DueNextSteerco and OpenFollowUp.
  * FillPct, and every count and signal on Rocks.
* **Show a milestone only when Visible is Yes.** Never work out visibility from dates.
* **Percentages.** FillPct is a fraction, so show it as a whole percentage (0.83 shows as 83%).
  ProgressShown is already a whole number from 0 to 100.
* **Dates** show as `11 Dec 26`.
* **MC quarters** are the company quarters. The MC year starts in April:
  * MC26Q3 is October to December 2026.
  * MC26Q4 is January to March 2027.
  * MC27Q1 is April to June 2027.
  * MC27Q2 is July to September 2027.

  The workbook already labels everything. CurrentMCQuarter, NextMCQuarter, ThirdMCQuarter and
  FourthMCQuarter on Rocks name the four quarters of the horizon; take them from any active rock,
  since they are the same on every row.

## Masthead and filter bar

**Masthead.**
* **Left:** a small grey uppercase eyebrow `ROCK TRACKER · STEERCO`, with the title
  `Strategic rocks` under it.
* **Top right:** three meta pairs, label over value.
  * `UPDATED`: the most recent UpdateDate among the rocks in view.
  * `NEXT STEERCO`: the earliest SteercoDate of a decision with DueNextSteerco = Yes; a dash when
    there is none.
  * A theme switch written as text, `LIGHT` and `DARK`, not an icon. The active choice is in ink
    and the other in grey. The default follows the system setting, and the choice is remembered
    for the session.

**Filter bar** under the tab bar, on every tab:
* `PORTFOLIO`: All, or one GPM.
* `ROCK`: All, or one rock (`R01 · Checkout Speed`). The rock list follows the portfolio choice.

Both filters apply to every tab. When one rock is chosen, show its profile under the filter bar in
three quiet lines:
* Purpose.
* Goals and What it delivers, in grey.
* `Lead {Lead} · {ValueChain} · updated {UpdateDate}`.

## Tab pattern

Each tab starts with:
1. A small uppercase grey eyebrow, for example `SECTION 01 · STEERCO`.
2. A headline: a short sentence that ends in a full stop and states the answer with real numbers.
3. A crimson serif lede of one or two lines.

The evidence follows. Blocks are separated by generous white space and a 1px hairline.

## Tab 1 · What does steerco need to hear?

**Headline and lede.**
* Headline: `{n} decisions are needed today.`, where n is the number of decisions with
  DueNextSteerco = Yes in view. When n is 0, use `No decisions are due at the next steerco.`
* Lede: `{a} of {b} rocks are At risk or Off track.`

**One block per rock** in view. Order the blocks Off track first, then At risk, then On track,
using the lead's State; keep RockID order within each group. Each block holds:
* **Rock line:** the rock name in bold, then a state chip with the State word in its colour.
* **Warnings.** If CheckCall is Yes, add one crimson line:
  `The data says {DataSignal}, the lead says {State}. Check the call.` If Stale is Yes, add a
  crimson `Update is stale` label.
* **The main message**, as written, in serif.
* **Two columns side by side:**
  * **What do we need from you?** Decisions of this rock with DecisionState = Requested and
    RequestNo from 1 to 5, in RequestNo order. Each shows the decision text, the DecideBy date in
    bold, a small `Choice point` label when ChoicePoint is Yes, and a small `Next steerco` label
    when DueNextSteerco is Yes. Do not reorder. If the rock has more than 5 requested decisions,
    add a grey line: `{count} requests are open, showing the first 5.`
  * **What should you know?** Attention1 to Attention3, skipping empty ones, one line each. Under
    them, a small grey `Coming up` list of call outs that are not Closed (empty status means
    open), newest date first, each with its date in bold and then the text.

**Major risks**, at the bottom of the tab, under a hairline. A list headed `Major risks` with every
risk in view where High = Yes and RiskStatus is not Closed, highest Score first. Each risk shows:
* the rock name in grey;
* the risk title;
* `{Likelihood} x {Impact}`;
* the key action and owner.

A risk with NeedsAction = Yes gets a small crimson label, `Needs an action`. When there are no major
risks, show `No major risks open.` in grey.

## Tab 2 · Where do we stand?

The tab runs, top to bottom: header, **roadmap**, **key metrics**, **teams**.

**Headline and lede.**
* Headline: `{x} of {y} committed milestones have slipped.`, using the sums of
  MilestonesSlipped and MilestonesCommitted over the rocks in view.
* Lede: `Outlook {CurrentMCQuarter} and {NextMCQuarter}. {o} overdue.`, where o is the sum of
  MilestonesOverdue.

### Roadmap: milestones in time

A card titled `Milestones in time`, with the grey note `grey is plan, the shaded extension is
slip, the marker is the adjusted date` next to the title.

**Horizon selector** at the top right of the card, as four text choices: `1Q`, `2Q`, `3Q` and
`4Q`. The default is `2Q`, and the active choice is in ink with a crimson underline. Choosing N
shows milestones with QuarterAhead from 1 to N. Milestones with no date (empty QuarterAhead, empty
TimelineDate) are listed under the chart as `Not dated yet` whatever the horizon.

**Time axis.**
* The axis runs from the earliest StartDate among the shown milestones (or the first day of the
  current MC quarter, whichever is earlier) to the last day of the Nth MC quarter.
* Month labels along the top in grey (`Jan 27`), every month or every other month so they never
  crowd.
* A thin crimson vertical line for today.
* Above the months, the MC quarter names (`MC26Q3`, `MC26Q4` and so on) over their months, with a
  faint vertical hairline at each quarter boundary.

**Rows.** One row per shown milestone, grouped by rock. When All rocks are shown, start each group
with a small grey uppercase rock name; within a rock, sort by TimelineDate. Each row has two parts:
* **Left label column** (about 30% of the width):
  * the milestone Title in bold ink, clickable;
  * under it, one grey line: `{ADOId} · {KRLink} · {Owner} · {Commitment}`, skipping empty parts.
    When ADOLink is filled, the ADO id is a link that opens in a new tab.
* **The bar,** drawn on the time axis:
  * **Plan:** a thin grey bar (6px high, rounded ends) from StartDate to PlannedDate. If StartDate
    is empty, there is no grey bar, only the marker.
  * **Slip:** when Status is Slipped, a shaded extension of the same height from PlannedDate to
    ForecastDate. Use the crimson tint when SlipSeverity is Major and the amber tint when it is
    Minor.
  * **Marker:** a short vertical tick (3px wide, a little taller than the bar) at the adjusted
    date, which is TimelineDate. It is coloured by Status: Completed green, On plan slate, On watch
    amber, On hold grey and Not committed grey. Slipped is crimson for Major and amber for Minor.
    When the forecast is earlier than planned, the grey bar still ends at PlannedDate and the
    marker sits on the bar at the forecast.
  * **Label** to the right of the marker, in ink 3: the date, plus a word when it applies:
    * `11 Dec 26 · slipped` when Slipped;
    * `30 Sep 26 · completed` when Completed;
    * `· overdue` in crimson when Overdue is Yes;
    * `· on watch` when On watch.
  * **Not committed and Choice point:** the grey bar is dashed, the marker is grey, and the line
    under the title says `Not committed` or `Choice point`.

Rows are separated by hairlines, and each row is about 56px high. Clicking a title, bar or marker
opens the **milestone pop up** (see below).

### Key metrics

Six KPI tiles in one row, under the roadmap. Each tile has an uppercase grey label, a large number
or word, and a grey sub line. Sums run over the rocks in view.

| Tile | Big value | Sub line |
| :--- | :--- | :--- |
| Rocks needing attention | count of rocks with State At risk or Off track, `of {rocks}` | `{c} where the data disagrees` (count of CheckCall Yes) |
| Roadmap | `{sum MilestonesSlipped} of {sum MilestonesCommitted}` | `committed slipped, {sum MilestonesOverdue} overdue` |
| On plan | `{sum MilestonesOnPlan} of {sum MilestonesCommitted}` | `{sum MilestonesCompleted} completed` |
| Risks | sum of OpenHighRisks | `{sum HighRisksNoAction} without an action` |
| Resourcing | `{sum PositionsActual} of {sum PositionsBudgeted}` | `positions filled, {percent}` (sum actual over sum budgeted) |
| Freshness | count of rocks with Stale Yes | `rocks not updated in time` |

**Exactly one tile is the spotlight** (green tint background):
* the Rocks needing attention tile when its count is above 0;
* otherwise the Roadmap tile when slipped is above 0;
* otherwise the Resourcing tile.

When one rock is chosen, the first tile shows that rock's State word in its colour, with the sub
line `Data says {DataSignal}`.

### Teams

A quiet table headed `Teams`, from the Teams sheet: Rock (only when All rocks are shown), Team, Team
lead, Budgeted, Actual and Fill %. Show Fill % as a whole percentage, plus a thin bar in the
spotlight green. A team whose Actual is above its Budgeted gets a grey `over budget` label. End the
table with a total line: the summed Budgeted, the summed Actual and the overall percentage. When
there are no teams, show `No teams recorded yet.` in grey.

## Tab 3 · What are we delivering?

The full list of deliveries.

**Headline and lede.**
* Headline: `{n} milestones in the next {N} quarters.`
* Lede: `{completed} completed, {slipped} slipped, {notcommitted} not yet committed.`

**Filters.** The same horizon selector (`1Q` to `4Q`, default `2Q`), shared with tab 2, so a choice
on one tab carries over to the other. Next to it, an **MC quarter** chip row: `All` and the
quarter names inside the horizon. Overdue milestones from an earlier quarter, and milestones not
dated yet, show only under `All`.

**The list.** One card per milestone (Visible = Yes, inside the horizon), grouped by rock and
sorted by TimelineDate. Each card holds:
* **Title line:** the title in bold, the Status word in its colour, the MC quarter in grey, and an
  `Overdue` label in crimson when it applies.
* **Description,** in serif, as written.
* **Detail bullets:** Detail1 to Detail3 as up to three bullets, skipping empty ones.
* **Facts row** in grey: Owner, Commitment, Start, Planned, Forecast, Actual (only when
  Completed), Slip in weeks (only when Slipped), and Key result link.
* **Progress bar** from ProgressShown, with the percentage beside it (see the milestone pop up).
* **Links:** the ADO id, as a link that opens in a new tab when ADOLink is filled. The comment
  shows in grey italics when present.

Clicking a card opens the same pop up.

## Milestone pop up

A modal on the card colour, with a close control. It also closes on the Escape key and on a click
outside. It shows:
* **Title and status:** the title, then the Status word in its colour and the MC quarter.
* **Owner.**
* **Description.**
* **Dates:** Start, Planned, Forecast, and Actual when it is filled.
* **The three detail bullets,** skipping empty ones.
* **Progress bar:** read ProgressShown, never the typed Progress, so a Completed milestone shows
  100%.
  * Draw a 6px bar with rounded ends. The track uses the rule colour and the fill uses the status
    colour.
  * Show the percentage beside it, for example `60%`.
  * When ProgressShown is empty, show a dash and no bar.
* **ADO link:** when ADOLink is filled, a link `Open {ADOId} in ADO` that opens in a new tab.

## Tab 3.1 · Which choices are open?

Decisions where ChoicePoint is Yes and DecisionState is Requested. Each is a card that shows:
* the rock name in grey;
* the decision text;
* the Options text, broken onto separate lines at `A:`, `B:` and `C:`;
* the DecideBy date in bold;
* a `Next steerco` label when DueNextSteerco is Yes.

When there are none, show `No open choice points.` in grey.

## Tab 4 · What could stop us?

**The grid.** A 3 by 3 grid with Likelihood on the vertical axis (High at the top) and Impact on the
horizontal axis (Low to High). Each cell shows how many risks are not Closed (an empty status counts
as open), with the risk titles in small text; prefix each title with its RockID when All rocks are
shown. Cells with Score 6 or 9 have the accent tint background, and all others use the card colour.
Risks without both a likelihood and an impact are left out of the grid and listed under it as
`Not yet rated`.

**The list.** Below the grid, the full risk list: Rock, Risk, Likelihood, Impact, Score, Key action,
Owner and Status. Rows with NeedsAction = Yes get a crimson `Needs an action` label, and closed risks
stay in the list with the word Closed.

## Tab 5 · What did steerco decide?

The decision log: every decision of the selected rocks, both Requested and Decided, in one
filterable table. It also includes the decisions of selected closed rocks.

**Headline and lede.**
* Headline: `{d} decisions taken, {r} still requested.`
* Lede: `{f} follow ups are still open.`, where f is the count of OpenFollowUp = Yes.

**Four small KPI tiles** in one row (this tab uses 4, not 6). The spotlight is Open follow ups when
it is above 0; otherwise it is Due at next steerco.

| Tile | Big value | Sub line |
| :--- | :--- | :--- |
| Requested | count of DecisionState Requested | `{n} choice points` |
| Due at next steerco | count of DueNextSteerco Yes | `next steerco {date}` |
| Decided | count of DecisionState Decided | `across {k} steercos` (distinct SteercoDate) |
| Open follow ups | count of OpenFollowUp Yes | `decided, follow up not closed` |

**Filter row** above the table. Each filter is a set of text chips or a dropdown; the default is
`All`, and filters combine. Each choice shows its count, for example `Requested (8)`. A `Clear
filters` link resets them all. The filters are:
* `STATE`: All, Requested, Decided.
* `FOLLOW UP`: All, Open, Closed. It applies to decided rows only; an empty FollowUp counts as Open.
* `OWNER`: All, then every distinct person in alphabetical order. A decided row matches its Owner
  (the follow up owner). A requested row has no owner yet, so it matches the Lead of its rock (look
  it up on Rocks by RockID).
* `ROCK`: All, then the selected rocks. This follows the global ROCK filter when that is set.
* `STEERCO`: All, then every distinct SteercoDate, newest first.
* `TYPE`: All, Choice points only.

**The table.** Newest SteercoDate first; within a date, Requested rows before Decided rows, then by
DecisionKey. Columns:
* Steerco (date);
* Rock;
* Decision, with a small `Choice point` label when ChoicePoint is Yes;
* Decide by;
* State, as a word: Requested in ink, Decided in the muted grey;
* Outcome;
* Owner: the Owner for decided rows; for requested rows, `raised by {Lead}` in grey;
* Follow up: `Open` in crimson when OpenFollowUp is Yes, `Closed` in grey, and a dash for requested
  rows.

Requested rows with DueNextSteerco = Yes get a small crimson `Next steerco` label. Clicking a row
opens a pop up with all of its fields, including the Options of a choice point broken onto lines at
`A:`, `B:` and `C:`. A line under the table reads `{shown} of {total} decisions shown`. When the
filters leave nothing, show `No decisions match these filters.` in grey.

## Look and feel

* **Two colour sets** share the same token names. Light is the default when the system is light and
  dark when it is dark; the LIGHT and DARK switch overrides both.
* **Style:** no shadows and no gradients, 8px corners, 1px hairline borders.
* **Crimson is the only emphasis colour.** Use it for the lede, key figures, today's line and
  warnings, never decoratively.

| Token | Use | Light | Dark |
| :--- | :--- | :--- | :--- |
| page | page background | `#FFFFFF` | `#121317` |
| card | cards, tiles, pop up | `#FFFFFF` | `#1A1C21` |
| ink | headlines, numbers | `#0F1116` | `#F2F2F3` |
| ink 2 | body text | `#1E2025` | `#E1E2E4` |
| ink 3 | card text, bar labels | `#3D3F43` | `#C4C6CA` |
| slate | inactive tabs | `#5B6067` | `#A3A7AD` |
| muted | sub lines, metadata | `#686D73` | `#9A9EA5` |
| subtle | eyebrows, uppercase labels | `#72777D` | `#868B92` |
| accent (crimson) | lede, warnings, active tab, today line | `#B22D5B` | `#E06A93` |
| accent tint | risk grid high cells, Major slip extension | `#F6E8EE` | `#3A1E29` |
| amber tint | Minor slip extension | `#F5E3D1` | `#3A2A1B` |
| plan bar | grey plan bar | `#D5D7DA` | `#3A3D43` |
| rule strong | line under header and tab bar | `#45474B` | `#5A5D63` |
| rule | borders, progress track | `#E6E7E9` | `#2C2E33` |
| spotlight background | spotlight tile, fill % bar | `#DDEFDF` | `#1E3323` |
| spotlight number | number on spotlight | `#1F3C23` | `#CFEBD4` |
| spotlight label | label on spotlight | `#486B4F` | `#8DBB96` |

* **Rock state colours:**

  | State | Light | Dark |
  | :--- | :--- | :--- |
  | On track (green) | `#438852` | `#6DB97E` |
  | At risk (amber) | `#CC7C2E` | `#E0A15F` |
  | Off track (crimson) | `#B22D5B` | `#E06A93` |

* **Milestone status colours:**

  | Status | Light | Dark |
  | :--- | :--- | :--- |
  | Completed (green) | `#438852` | `#6DB97E` |
  | On plan (slate) | `#5B6067` | `#8C9097` |
  | On watch (amber) | `#CC7C2E` | `#E0A15F` |
  | Slipped Major (crimson) | `#B22D5B` | `#E06A93` |
  | Slipped Minor (amber) | `#CC7C2E` | `#E0A15F` |
  | On hold (grey) | `#8B8F96` | `#8C9097` |
  | Not committed (grey, dashed plan bar) | `#8B8F96` | `#8C9097` |

* **Fonts:** a clean sans serif (Inter or Segoe UI) for labels, numbers, tables and bar labels; a
  text serif (Source Serif or Georgia) for ledes, main messages, descriptions and card headings.
* **Labels and eyebrows** are small, uppercase and letter spaced, in the subtle grey.
* **Layout:** content width about 1180px, centred. On a narrow screen, cards and tiles stack, and the
  roadmap scrolls sideways with the label column fixed.
* **Charts:** only the roadmap and the risk grid. No icons, gradients or emoji.
* **Contrast:** text and accent must stay readable in both modes, at 4.5 to 1 or more.

## Check before you finish

1. **Data:** every number on the page comes from the workbook; nothing is estimated.
2. **Words:** Milestone and Completed are used, and Epic and Delivered appear nowhere.
3. **Spotlight:** there is exactly one spotlight tile.
4. **Empty values:** they show a dash, never `#N/A`, `#NAME?`, or `0` where the cell is blank.
5. **Colours:** state and status colours match in both modes.
6. **Rows:** rows without a key and rocks with Active No are ignored, except in the decision log.
7. **Filters:**
   * The portfolio and rock filters change every tab.
   * The horizon selector (`1Q` to `4Q`) changes the roadmap and the full list.
   * Only milestones with Visible = Yes appear.
8. **Roadmap:** grey plan bars run from start to planned, slip extensions are crimson for Major and
   amber for Minor, and the marker sits at the adjusted date with its label.
9. **Pop up:** clicking a milestone opens it, the ADO link opens in a new tab, and the theme switch
   flips between light and dark.
10. **Masthead:** the update date shows top right.
11. **Audience:** you asked which rocks to include before building, and nothing from other rocks
    appears anywhere.
12. **Decision log:** the six filters on tab 5 work alone and combined, and each shows its counts.

---

## For you (not for Cowork): what the sample workbook should show

Values come from `scripts/rock_model.py` on `data/sample.json` with today 14 Oct 2026. They hold
for the sample `workbook.xlsx` once Excel has calculated it. With PORTFOLIO and ROCK on All:

* **Rocks:** four active rocks show, R01 to R04. R05 Legacy Returns is closed and appears only in
  the decision log.
* **Masthead:** UPDATED 13 Oct 26, NEXT STEERCO 21 Oct 26.
* **Tab 1:**
  * Headline: "4 decisions are needed today." Lede: "2 of 4 rocks are At risk or Off track."
  * Block order: R02 and R03 (At risk) first, then R01 and R04 (On track).
  * R03 shows "The data says Off track, the lead says At risk. Check the call." and `Update is
    stale`. R04 is also stale.
  * Major risks, highest score first:
    1. "Two engineering roles unfilled" (R02), High x High, score 9, with `Needs an action`.
    2. "Peak season freeze blocks release" (R01), Medium x High, score 6.
* **Tab 2:**
  * Headline: "2 of 10 committed milestones have slipped." Lede: "Outlook MC26Q3 and MC26Q4. 1
    overdue."
  * Roadmap at 1Q: 6 dated milestones; 2Q: 10; 3Q: 11; 4Q: 12. Plus 4 under "Not dated yet"
    whatever the horizon.
  * Slip extensions:
    * "Carrier integration" (R03): crimson (Major), from 10 Dec 26 to 14 Jan 27, so it moves from
      MC26Q3 into MC26Q4.
    * "Setup checklist" (R02): amber (Minor), from 20 Nov 26 to 4 Dec 26.
  * "Region one pilot" (R03) shows with `· overdue` in crimson. "Fourth region rollout" appears only
    at 4Q, and "Delivery analytics" (MC27Q3) never appears.
  * Key metrics, with Rocks needing attention as the spotlight:

    | Tile | Big value | Sub line |
    | :--- | :--- | :--- |
    | Rocks needing attention | 2 of 4 | 1 where the data disagrees |
    | Roadmap | 2 of 10 | 1 overdue |
    | On plan | 7 of 10 | 2 completed |
    | Risks | 2 | 1 without an action |
    | Resourcing | 13 of 15 | 87% |
    | Freshness | 2 | |

  * Teams: Carrier Integration (R03) has 3 actual against 2 budgeted, so it is `over budget`. Pilot
    squad (R04) has 0 budgeted and 1 actual, so its Fill % is a dash. Total 13 of 15, 87%.
* **Tab 3:** the same milestones as the roadmap. Each card has a description and bullets.
  "Express pay button" (R01) shows 100% although the lead typed 80, because it is Completed.
* **Tab 3.1:** one card, "Fund wallet support this half" (R01), decide by 21 Oct, Next steerco.
* **Step 0:** Cowork lists R01 to R04 as active and R05 Legacy Returns as closed, then asks which
  rocks to include and who the audience is. Answer `All` and `Steerco` for the values below.
  To see the selection at work, answer `R01, R03`: then only those two rocks appear anywhere, and
  tab 1 still says "4 decisions are needed today." (3 from R01, 1 from R03), but "1 of 2 rocks are At risk or Off track."
* **Tab 5:**
  * Tiles:

    | Tile | Big value | Sub line |
    | :--- | :--- | :--- |
    | Requested | 8 | 1 choice point |
    | Due at next steerco | 4 | next steerco 21 Oct 26 |
    | Decided | 4 | across 1 steerco |
    | Open follow ups | 1 | spotlight |

  * 12 rows in total. All four decided rows are from the 16 Sep 26 steerco, and one of them is
    R05's "Close the legacy returns rock".
  * "Pause in app tips until checklist ships" (R02) shows `Open`.
  * OWNER lists Ines Samplewood, Lena Testfield, Omar Fictiv and Tove Nomen. Lena Testfield
    matches 7 rows: R01's decided row plus its 6 requests, which she raised as lead.
  * STATE = Requested together with ROCK = R01 shows 6 rows.

For one rock, choose ROCK = R01 and compare with the R01 list in `portal/COWORK_ROCK_TEST.md`.
Note that its roadmap now sits on tab 2.
