# Copilot Cowork brief: one rock page (test)

Paste everything below the line into Copilot Cowork, with the Rock Tracker workbook attached or
linked from SharePoint. It builds one page for one rock, so you can test the look, the reading
order and whether Cowork reads the workbook correctly before the full portal is built.

**Before you start:** upload `workbook.xlsx` to SharePoint and open it once in Excel for the web,
so it calculates and saves its values. The generated file has no stored results, so if Cowork
reads it unopened, the calculated cells (Status, Score, signals) come back empty.

Default test rock: the tab **`R01 Checkout Speed`** in the sample workbook. To test another rock,
replace that tab name everywhere below (for example `R03 Same Day Fulfilment`, which shows the
"check the call" warning).

---

## Your task

Build a single, read only web page that briefs a steering committee on **one strategic initiative
(a "rock")**. Read the data from the attached Excel workbook, from the sheet named
**`R01 Checkout Speed`**. Do not invent, round or reword data: show values exactly as they are in
the workbook. If a value is empty, show a quiet dash and never an error.

The page reads like a short editorial briefing, top to bottom, in the order the steerco runs:

1. What does steerco need to hear?
2. Where does the rock stand?
3. What ships in the next six months? (with 3.1 Which choices are open?)
4. What could stop us?
5. What did steerco decide?

## Where the data is (sheet `R01 Checkout Speed`)

Labels are in column B, values in column C, for the single value sections.

**Rock profile (rows 94 to 102, value in column C)**
| Row | Field |
| :--- | :--- |
| 94 | Rock ID |
| 95 | Rock name |
| 96 | Value chain |
| 97 | Initiative lead |
| 98 | GPM |
| 99 | Active (Yes or No) |
| 100 | Purpose |
| 101 | Goals |
| 102 | What it delivers |

**Update (rows 6 to 10, column C):** 6 Update date, 7 State (On track, At risk or Off track),
8 Main message, 9 Positions planned, 10 Positions filled.

**Signals (rows 13 to 21, column C, calculated by the workbook, use as is):**
13 Days since update, 14 Data signal, 15 Check the call (Yes or No), 16 Committed epics in the six
month window, 17 of which Slipped, 18 of which On plan, On watch or Delivered, 19 of which
Delivered, 20 Open High risks, 21 High risks without key action or owner.

**Tables.** Each table has its header in the row named below and data from the next row down.
A row counts only when its **Key** (column A) is not empty. Ignore all other rows.

| Table | Header row | Data rows | Columns |
| :--- | :--- | :--- | :--- |
| Epics | 24 | 25 to 39 | A Key, B Epic, C ADO id, D Commitment, E Planned date, F Forecast date (empty means same as planned), G Lead status, H Comment, I Key result link, J Status, K Slip (weeks), L In six month window, M Forecast overdue |
| Risks | 42 | 43 to 52 | A Key, B Risk, C Likelihood, D Impact, E Key action, F Action owner, G Status (empty means Open), H Top risk, I Score, J High, K Needs action |
| Call outs | 55 | 56 to 63 | A Key, B Call out, C Date, D Status (empty means Open) |
| Decisions | 66 | 67 to 91 | A Key, B Decision requested, C Steerco, D Decide by, E Choice point, F Options, G Outcome, H Follow up owner, I Follow up (empty means Open), J State (Requested or Decided), K Due at next steerco, L Open follow up |

Use the workbook's own calculated columns (Status, Score, High, Needs action, State, Due at next
steerco, Open follow up). Do not recalculate them.

## Page layout

Follow the "Editorial Portfolio" design system (attach `DESIGN_SYSTEM.md` from the handoff
package if you can). The essentials are below.

**Masthead.** Eyebrow in small uppercase grey: `ROCK TRACKER · {Value chain} · {GPM}`. Title:
`{Rock ID} · {Rock name}`. On the right, two meta pairs: `AS OF` with the Update date, and
`LEAD` with the initiative lead. Under the title, one quiet line with Purpose, then Goals and What
it delivers as two short lines in grey.

**Section pattern.** Each of the five sections starts with a small uppercase grey eyebrow
(`SECTION 01 · STEERCO`), a headline that is a short sentence ending in a full stop, and a crimson
serif lede of one or two lines. Then the evidence. Sections are separated by generous white space
and a 1px hairline, not by boxes.

### Section 01 · What does steerco need to hear?
* Headline: the lead's **Main message**, as written.
* Lede: `State: {State}. Updated {Days since update} days ago.` If Days since update is more than
  14, add `Update is stale.` in crimson.
* If **Check the call** is Yes, show one crimson line under the lede:
  `The data says {Data signal}, the lead says {State}. Check the call.`
* Three cards side by side, each with a serif heading phrased as a question:
  1. **What could hurt us?** Risks where Top risk is Yes and Status is not Closed: risk title,
     then `Likelihood x Impact`, then the key action and owner.
  2. **What should you know?** Call outs where Status is not Closed, newest date first: date in
     bold, then the text.
  3. **What do we need from you?** Decisions where State is Requested: decision text, decide by
     date in bold, and `Choice point` as a small label when Choice point is Yes. Put the ones with
     Due at next steerco = Yes first, marked `Today`.

### Section 02 · Where does the rock stand?
Six KPI tiles in one row. Each has an uppercase grey label, a large number or word, and a grey
sub line. Exactly **one** tile is the spotlight (pale green background `#DDEFDF`): the State tile
when State is On track; otherwise the tile that explains the problem (Slipped epics when it is
above 0, else High risks without action).

| Tile | Big value | Sub line |
| :--- | :--- | :--- |
| State | State | `Data says {Data signal}` |
| Roadmap | `{Slipped} of {Committed}` | `committed epics slipped, next six months` |
| On plan | `{On plan, On watch or Delivered} of {Committed}` | `{Delivered} delivered` |
| Risks | Open High risks | `{High risks without key action or owner} without an action` |
| Resourcing | `{Positions filled} of {Positions planned}` | `positions filled` |
| Freshness | Days since update | `days since the last update` |

State words always use the same colours: On track `#438852` green, At risk `#CC7C2E` amber,
Off track `#B22D5B` crimson.

### Section 03 · What ships in the next six months?
* A horizontal timeline from the first day of the current quarter to six months later, with a thin
  vertical line for today and month labels along the top.
* One row per epic (every epic with a Key), labelled with the epic title and its ADO id in grey.
* Each epic is a marker at its **Forecast date** (Planned date when the forecast is empty). If the
  forecast is later than planned, draw a thin line from the planned date to the forecast date.
* Commitment decides the style: **Committed** filled marker, **Choice point** hollow amber
  marker, **Not committed** hollow grey dashed marker. Epics without any date sit in a short list
  under the chart titled `Not dated yet`.
* Status decides the colour of filled markers: Delivered `#438852`, On plan `#5B6067`, On watch
  `#CC7C2E`, Slipped `#B22D5B`, On hold `#8B8F96`.
* Under the timeline, "The full list": a quiet table with Epic, ADO id, Commitment, Planned,
  Forecast, Status (coloured word), Slip (weeks), Key result link and Comment.

### Section 03.1 · Which choices are open?
Decisions where Choice point is Yes and State is Requested, each as a card: the decision, the
Options text broken onto separate lines at "A:", "B:", "C:", and the decide by date. If there are
none, show `No open choice points.` in grey.

### Section 04 · What could stop us?
* A 3 by 3 grid: Likelihood on the vertical axis (High at the top), Impact on the horizontal axis
  (Low to High). Each cell shows the number of risks that are not Closed, and the risk titles in
  small text. Cells with Score 6 or 9 have a pale crimson background `#F6E8EE`; all others are white
  with a hairline border.
* Below it, the full risk list: Risk, Likelihood, Impact, Score, Key action, Owner, Status. Rows
  where Needs action is Yes get a small crimson label `Needs an action`.

### Section 05 · What did steerco decide?
The decision log: every decision with State Decided, newest Steerco date first. Columns: Steerco,
Decision, Outcome, Follow up owner, Follow up. Rows where Open follow up is Yes show `Open` in
crimson. If there are none yet, show `No decisions recorded yet.` in grey.

## Look and feel
* White page, ink black text `#0F1116`, hairline borders `#E6E7E9`, no shadows, 8px corners.
* **Crimson `#B22D5B` is the only emphasis colour.** Use it for the lede, key figures and warnings,
  nothing decorative.
* Fonts: a clean sans serif (Inter or Segoe UI) for labels, numbers and tables; a text serif
  (Source Serif or Georgia) for ledes, narrative and card headings.
* Labels and eyebrows are small, uppercase and letter spaced, in grey `#8C9097`.
* Content width about 1180px, centred. On a narrow screen, cards and tiles stack.
* No charts other than the timeline and the risk grid. No icons, gradients or emoji.

## Check before you finish
1. Every number on the page comes from the workbook; nothing is estimated.
2. Exactly one spotlight tile.
3. Empty values show a dash, never `#N/A`, `#NAME?` or `0` where the cell is blank.
4. State colours match: On track green, At risk amber, Off track crimson.
5. Rows without a Key are ignored in every table.

---

## For you (not for Cowork): what R01 should show

Use this to check that Cowork read the workbook correctly.

* **Masthead:** R01 · Checkout Speed, value chain Checkout, GPM Priya Sampleton, lead Lena
  Testfield, as of 12 Oct 2026.
* **Section 01:** the headline starts "One page checkout is in test and on plan." State On track.
  There is no check the call warning. Top risk: "Peak season freeze blocks release", Medium x
  High. The open call out is "Vendor review call", 20 Oct. The decision requested is "Fund wallet
  support this half", decide by 21 Oct, marked Choice point and Today.
* **Section 02:**
  * State: On track, and it is the spotlight.
  * Roadmap: 0 of 3 slipped.
  * On plan: 3 of 3, with 1 delivered.
  * Risks: 1 open High risk, 0 without an action.
  * Resourcing: 5 of 6 positions filled.
  * Freshness: days since 12 Oct.
* **Section 03:**
  * One page checkout: On plan, 30 Nov.
  * Saved payment methods: On watch, 10 Dec. It is forecast before its 15 Dec plan, so there is no slip line.
  * Address form speed up: Delivered, 2 Oct.
  * Wallet support: a choice point with no dates, so it appears under "Not dated yet".
* **Section 03.1:** one card, Fund wallet support, with options A, B and C.
* **Section 04:**
  * 2 open risks:
    * Low x Low, score 1.
    * Medium x High, score 6, shaded.
  * The closed High x Medium risk is not counted in the grid but is listed as Closed.
* **Section 05:** "No decisions recorded yet."

If Cowork shows errors where the workbook calculates values (Status, Score, signals), open the
workbook in Excel for the web once so it recalculates and saves, then try again. The sample file
is generated without stored results.
