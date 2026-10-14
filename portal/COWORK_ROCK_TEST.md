# Copilot Cowork brief: one rock page (test)

Paste everything below the line into Copilot Cowork, with the Rock Tracker workbook attached or
linked from SharePoint. It builds one page for one rock, so you can test the look, the reading
order and whether Cowork reads the workbook correctly before the full portal is built. This
version follows workbook schema 2.1.0 and change request 1: Milestones (not Epics), MC quarters,
an outlook of two quarters, teams, light and dark mode, and one tab per section.

**Before you start:** upload `workbook.xlsx` to SharePoint and open it once in Excel for the web,
so it calculates and saves its values. The generated file has no stored results, so if Cowork
reads it unopened, the calculated cells (Status, Score, MC quarter, Visible, signals) come back
empty.

Default test rock: the tab **`R01 Checkout Speed`** in the sample workbook. To test another rock,
replace that tab name everywhere below (for example `R03 Same Day Fulfilment`, which shows the
"check the call" warning).

---

## Your task

Build a single, read only web page that briefs a steering committee on **one strategic initiative
(a "rock")**. Read the data from the attached Excel workbook, from the sheet named
**`R01 Checkout Speed`**. Do not invent, round or reword data: show values exactly as they are in
the workbook. If a value is empty, show a quiet dash and never an error.

Words matter: always say **Milestone** (never Epic) and **Completed** (never Delivered).

The page has a masthead and **six tabs, one per section**, in the order the steerco runs. Each tab
title is a question:

1. What does steerco need to hear?
2. Where does the rock stand?
3. What ships in the next two quarters?
3.1 Which choices are open?
4. What could stop us?
5. What did steerco decide?

Show tab 1 first. Only one tab is visible at a time; the active tab has a crimson underline.

## Where the data is (sheet `R01 Checkout Speed`)

Labels are in column B, values in column C, for the single value sections.

**Section 1, Update and steerco message (rows 6 to 17, column C):**
| Row | Field | Note |
| :--- | :--- | :--- |
| 6 | Update date | |
| 7 | State | On track, At risk or Off track |
| 8 | Main message | |
| 9, 10, 11 | Attention point 1, 2, 3 | one line each, may be empty |
| 12 | Open decision requests | calculated count, can be more than 5 |
| 13 to 17 | Decision requested 1 to 5 | calculated, empty when there is none |

**Section 2, Signals (rows 20 to 33, column C, calculated by the workbook, use as is):**
20 Days since update, 21 Data signal, 22 Check the call (Yes or No), 23 Outlook (the two MC
quarters, for example `MC26Q3 and MC26Q4`), 24 Committed milestones in the outlook, 25 of which
Slipped, 26 of which On plan, On watch or Completed, 27 of which Completed, 28 Committed
milestones overdue, 29 Open High risks, 30 High risks without key action or owner, 31 Positions
budgeted, 32 Positions actual, 33 Fill % (a fraction, show as a percentage; empty means no
budget).

**Section 7, Rock profile (rows 106 to 114, column C):**
| Row | Field |
| :--- | :--- |
| 106 | Rock ID |
| 107 | Rock name |
| 108 | Value chain |
| 109 | Initiative lead |
| 110 | GPM |
| 111 | Active (Yes or No) |
| 112 | Purpose |
| 113 | Goals |
| 114 | What it delivers |

**Tables.** Each table has its column headers in the row named below and data from the next row
down. A row counts only when its **Key** (column A) is not empty. Ignore all other rows.

| Table | Header row | Data rows | Columns |
| :--- | :--- | :--- | :--- |
| Milestones | 36 | 37 to 51 | A Key, B Milestone, C Owner, D Commitment, E Start date, F Planned date, G Forecast date, H Actual date, I Lead status, J Comment, K Key result link, L ADO id, M ADO link, N Description, O Detail 1, P Detail 2, Q Detail 3, R Status, S Slip (weeks), T Timeline date, U MC quarter, V In outlook, W Visible, X Overdue |
| Risks | 54 | 55 to 64 | A Key, B Risk, C Likelihood, D Impact, E Key action, F Action owner, G Status (empty means Open), H Score, I High, J Needs action |
| Call outs | 67 | 68 to 75 | A Key, B Call out, C Date, D Status (empty means Open) |
| Decisions | 78 | 79 to 103 | A Key, B Decision requested, C Steerco, D Decide by, E Choice point, F Options, G Outcome, H Follow up owner, I Follow up (empty means Open), J State (Requested or Decided), K Request no, L Due at next steerco, M Open follow up |
| Teams (section 8) | 117 | 118 to 122 | A Key, B Team, C Team lead, D Budgeted, E Actual, F Fill % |

Use the workbook's own calculated columns (Status, Slip, Timeline date, MC quarter, In outlook,
Visible, Overdue, Score, High, Needs action, State, Request no, Due at next steerco, Open follow
up, Fill %). Do not recalculate them. In particular, **use the Visible flag (column W) to decide
which milestones to show; never work out visibility from the dates yourself.**

**MC quarters** are the company quarters. The MC year starts in April. MC26Q3 is October to
December 2026, MC26Q4 is January to March 2027, MC27Q1 is April to June 2027. The workbook
already gives each milestone its MC quarter in column U; show it as is.

## Page layout

Follow the "Editorial Portfolio" design system (attach `DESIGN_SYSTEM.md` from the handoff
package if you can). The essentials are below.

**Masthead.** Eyebrow in small uppercase grey: `ROCK TRACKER · {Value chain} · {GPM}`. Title:
`{Rock ID} · {Rock name}`. On the right, meta pairs: `AS OF` with the Update date, `LEAD` with the
initiative lead, and a theme switch written as text, `LIGHT` and `DARK` (not an icon). The active
choice is in ink, the other in grey. Default follows the system setting; the choice is remembered
for the session. Under the title, one quiet line with Purpose, then Goals and What it delivers as
two short lines in grey.

**Tab pattern.** Each tab starts with a small uppercase grey eyebrow (`SECTION 01 · STEERCO`), a
headline that is a short sentence ending in a full stop, and a crimson serif lede of one or two
lines. Then the evidence. Blocks are separated by generous white space and a 1px hairline.

### Tab 1 · What does steerco need to hear?
* Headline: the lead's **Main message** (C8), as written.
* Lede: `State: {State}. Updated {Days since update} days ago.` If Days since update is more than
  14, add `Update is stale.` in crimson.
* If **Check the call** is Yes, show one crimson line under the lede:
  `The data says {Data signal}, the lead says {State}. Check the call.`
* Two cards side by side, each with a serif heading phrased as a question:
  1. **What do we need from you?** The requested decisions from C13 to C17, in order, skipping
     empty ones (up to 5). For each, look up the decision row in the Decisions table by exact
     match of the text in column B, and add the decide by date in bold and a small `Choice point`
     label when Choice point is Yes. Mark rows with Due at next steerco = Yes as `Next steerco`
     and put them first within their order. If Open decision requests (C12) is more than 5, add a
     grey line `{C12} requests are open, showing the first 5. All are in the workbook.`
  2. **What should you know?** The attention points from C9 to C11, skipping empty ones (up to
     3), one line each. Under them, a small grey list `Coming up` of Call outs where Status is
     not Closed, newest date first: date in bold, then the text.

### Tab 2 · Where does the rock stand?
Six KPI tiles in one row. Each has an uppercase grey label, a large number or word, and a grey
sub line. Exactly **one** tile is the spotlight (green tint background): the State tile when
State is On track; otherwise the tile that explains the problem (Slipped milestones when above 0,
else Overdue milestones when above 0, else High risks without action).

| Tile | Big value | Sub line |
| :--- | :--- | :--- |
| State | State | `Data says {Data signal}` |
| Roadmap | `{Slipped} of {Committed}` | `committed milestones slipped, {Outlook}, {Overdue} overdue` |
| On plan | `{On plan, On watch or Completed} of {Committed}` | `{Completed} completed` |
| Risks | Open High risks | `{High risks without key action or owner} without an action` |
| Resourcing | `{Positions actual} of {Positions budgeted}` | `positions filled, {Fill %}` |
| Freshness | Days since update | `days since the last update` |

State words always use the same colours: On track green, At risk amber, Off track crimson (see
Look and feel for light and dark values).

**Teams, inside this tab.** Under the tiles, a quiet table headed `Teams` with the rows of the
Teams table: Team, Team lead, Budgeted, Actual, Fill %. Add a total line with Positions budgeted,
Positions actual and Fill %. If there are no teams, show `No teams recorded yet.` in grey.

### Tab 3 · What ships in the next two quarters?
* A filter above the chart, **MC quarter**, with the choices `All`, and the two quarters of the
  Outlook cell (C23, for example MC26Q3 and MC26Q4). Default `All`. It filters the chart and the
  list below by the MC quarter in column U. Milestones without an MC quarter (no date yet) show
  only under `All`, in the `Not dated yet` list.
* Show only milestones whose **Visible** (column W) is Yes. Completed milestones in the past are
  already hidden by the workbook (Visible is No); do not bring them back.
* A horizontal timeline from the first day of the first outlook quarter to the last day of the
  second, with quarter and month labels along the top (each quarter labelled with its MC name)
  and a thin vertical line for today.
* One row per visible milestone, labelled with the milestone title and its MC quarter in grey.
  The ADO id (column L) sits next to it in grey; when the ADO link (column M) is filled it is a
  link that opens in a new tab.
* Each milestone is a marker at its **Timeline date** (column T). If Status is Slipped, draw a
  thin line from the Planned date to the Forecast date. If Overdue (column X) is Yes, add a small
  crimson label `Overdue`.
* Commitment decides the style: **Committed** filled marker, **Choice point** hollow amber
  marker, **Not committed** hollow grey dashed marker. Milestones without any date sit in a short
  list under the chart titled `Not dated yet`.
* Status decides the colour of filled markers: Completed green, On plan slate, On watch amber,
  Slipped crimson, On hold grey (see Look and feel).
* **Every milestone is clickable** (marker, title and row in the full list). Clicking opens a pop
  up (modal) with a close control, closing also on the Escape key and a click outside. The pop up
  shows: Milestone title, Owner, Description, Start date, Planned date, Forecast date, Status
  (coloured word), MC quarter, and the three detail bullets (Detail 1, 2, 3, skipping empty
  ones). When the ADO link is filled, add a link `Open {ADO id} in ADO` that opens in a **new
  tab**; when it is empty, show the ADO id as plain grey text.
* Under the timeline, "The full list": a quiet table with Milestone, MC quarter, ADO id (a link
  that opens in a new tab when the ADO link exists), Commitment, Start, Planned, Forecast, Status
  (coloured word), Slip (weeks), Key result link and Comment.

### Tab 3.1 · Which choices are open?
Decisions where Choice point is Yes and State is Requested, each as a card: the decision, the
Options text broken onto separate lines at "A:", "B:", "C:", and the decide by date. If there are
none, show `No open choice points.` in grey.

### Tab 4 · What could stop us?
* A 3 by 3 grid: Likelihood on the vertical axis (High at the top), Impact on the horizontal axis
  (Low to High). Each cell shows the number of risks that are not Closed (empty status counts as
  open), and the risk titles in small text. Cells with Score 6 or 9 have the accent tint
  background; all others use the card colour with a hairline border.
* Below it, the full risk list: Risk, Likelihood, Impact, Score, Key action, Owner, Status. Rows
  where Needs action is Yes get a small crimson label `Needs an action`. Closed risks stay in the
  list with the word Closed.

### Tab 5 · What did steerco decide?
The decision log: every decision with State Decided, newest Steerco date first. Columns: Steerco,
Decision, Outcome, Follow up owner, Follow up. Rows where Open follow up is Yes show `Open` in
crimson. If there are none yet, show `No decisions recorded yet.` in grey.

## Look and feel
* Two colour sets with the same token names. Light is the default when the system is light, dark
  when the system is dark; the LIGHT and DARK switch overrides it. No shadows, no gradients,
  8px corners, 1px hairline borders.
* **Crimson is the only emphasis colour.** Use it for the lede, key figures and warnings, nothing
  decorative.

| Token | Use | Light | Dark |
| :--- | :--- | :--- | :--- |
| page background | page | `#FFFFFF` | `#121317` |
| card | cards, tiles, pop up | `#FFFFFF` | `#1A1C21` |
| ink | headlines, numbers | `#0F1116` | `#F2F2F3` |
| ink 2 | body text | `#1E2025` | `#E1E2E4` |
| ink 3 | card body text | `#3D3F43` | `#C4C6CA` |
| slate | inactive tabs, On plan | `#5B6067` | `#A3A7AD` |
| muted | sub lines, metadata | `#686D73` | `#9A9EA5` |
| subtle | eyebrows, uppercase labels | `#72777D` | `#868B92` |
| accent (crimson) | lede, warnings, active tab | `#B22D5B` | `#E06A93` |
| accent tint | selected cells, risk grid | `#F6E8EE` | `#3A1E29` |
| rule strong | line under header and tab bar | `#45474B` | `#5A5D63` |
| rule | borders | `#E6E7E9` | `#2C2E33` |
| spotlight background | spotlight tile | `#DDEFDF` | `#1E3323` |
| spotlight number | number on spotlight | `#1F3C23` | `#CFEBD4` |
| spotlight label | label and sub line on spotlight | `#486B4F` | `#8DBB96` |

* **Rock state colours:** On track green (`#438852` light, `#6DB97E` dark), At risk amber
  (`#CC7C2E` light, `#E0A15F` dark), Off track crimson (`#B22D5B` light, `#E06A93` dark).
* **Milestone status colours:** Completed green (`#438852` / `#6DB97E`), On plan slate (`#5B6067`
  / `#A3A7AD`), On watch amber (`#CC7C2E` / `#E0A15F`), Slipped crimson (`#B22D5B` / `#E06A93`),
  On hold grey (`#8B8F96` / `#8C9097`), Not committed hollow grey.
* Fonts: a clean sans serif (Inter or Segoe UI) for labels, numbers and tables; a text serif
  (Source Serif or Georgia) for ledes, narrative and card headings.
* Labels and eyebrows are small, uppercase and letter spaced, in subtle grey.
* Content width about 1180px, centred. On a narrow screen, cards and tiles stack.
* No charts other than the timeline and the risk grid. No icons, gradients or emoji.
* Text and accent must stay readable in both modes (contrast of 4.5 to 1 or more).

## Check before you finish
1. Every number on the page comes from the workbook; nothing is estimated.
2. The words Milestone and Completed are used; Epic and Delivered appear nowhere.
3. Exactly one spotlight tile.
4. Empty values show a dash, never `#N/A`, `#NAME?` or `0` where the cell is blank.
5. State colours match: On track green, At risk amber, Off track crimson, in both modes.
6. Rows without a Key are ignored in every table.
7. Tab 3 shows only milestones with Visible = Yes, and the MC quarter filter works.
8. Clicking a milestone opens the pop up; the ADO link opens in a new tab; the switch flips
   between light and dark.

---

## For you (not for Cowork): what R01 should show

Use this to check that Cowork read the workbook correctly. Values come from
`scripts/rock_model.py` (it supports schema 2.1.0), run on `data/sample.json` with today
2026-10-14 and the sample steerco dates (21 Oct is the next steerco).

* **Masthead:** R01 · Checkout Speed, value chain Checkout, GPM Priya Sampleton, lead Lena
  Testfield, as of 12 Oct 2026. Theme switch LIGHT and DARK.
* **Tab 1:**
  * Headline starts "One page checkout is in test and on plan." State On track, updated 2 days
    ago, not stale. No check the call warning (data signal On track).
  * Open decision requests: 6, the tab shows 5 and a grey line says 6 are open, showing the
    first 5. The five, in order:
    1. Fund wallet support this half (decide by 21 Oct, Choice point, Next steerco).
    2. Extend the vendor sandbox contract (21 Oct, Next steerco).
    3. Approve extra test devices (18 Nov).
    4. Move the release window before the freeze (decide by 21 Oct, Next steerco).
    5. Add a fraud check on express pay (18 Nov).
    The sixth, Retire the old basket page (16 Dec), is not shown.
  * Attention points, 2 of 3: "Peak season freeze could block the release" and "Wallet funding
    decision needed before Q4". The third is empty and not shown.
  * Coming up: "Vendor review call", 20 Oct. The closed call out is not shown.
* **Tab 2:**
  * State: On track, and it is the spotlight. Data says On track.
  * Roadmap: 0 of 4 committed milestones slipped, MC26Q3 and MC26Q4, 0 overdue.
  * On plan: 4 of 4, 2 completed.
  * Risks: 1 open High risk, 0 without an action.
  * Resourcing: 5 of 6 positions filled, 83%.
  * Freshness: 2 days.
  * Teams: Checkout Web (Mia Sandbox) 3 of 3, 100%; Payments (Noor Testwell) 1 of 2, 50%;
    Checkout Design (Jonas Mockley) 1 of 1, 100%. Total 5 of 6, 83%.
* **Tab 3:** four milestones visible, one hidden.
  * One page checkout: MC26Q3, On plan, Committed, 30 Nov, ADO link present.
  * Saved payment methods: MC26Q3, On watch, forecast 10 Dec before its 15 Dec plan, so no slip
    line. No ADO link, so the ADO id is plain text.
  * Express pay button: MC26Q3, Completed today (14 Oct), still visible.
  * Wallet support: Choice point with no dates and no MC quarter, so it appears under "Not dated
    yet" and only when the filter is All.
  * Address form speed up: Completed on 2 Oct, in the past, so Visible is No and it is hidden.
  * With the filter on MC26Q3: the three dated milestones. With MC26Q4: none.
  * Pop up for One page checkout: owner Lena Testfield, description "Single page that replaces
    the five step checkout.", start 17 Aug 2026, planned 30 Nov 2026, forecast 30 Nov 2026,
    status On plan, bullets "Design signed off", "Build in test", "Release window to agree with
    ops", and an ADO link `https://ado.example.com/rocktracker/items/1101` opening in a new tab.
* **Tab 3.1:** one card, Fund wallet support this half, decide by 21 Oct, with options A, B and C.
* **Tab 4:**
  * 2 open risks: Low x Low, score 1 (Payment vendor delays sandbox); Medium x High, score 6,
    shaded (Peak season freeze blocks release).
  * The closed High x Medium risk (Legacy tax service times out) is not counted in the grid but is
    listed as Closed.
* **Tab 5:** one decided row: 16 Sep 2026, "Keep the checkout at three steps", outcome "Agreed,
  three steps", follow up owner Lena Testfield, follow up Closed (so no `Open` label).

If Cowork shows errors where the workbook calculates values (Status, Score, MC quarter, Visible,
signals), open the workbook in Excel for the web once so it recalculates and saves, then try
again. The sample file is generated without stored results.
