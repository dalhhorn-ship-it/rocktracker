# Build the Product portfolio hub portal in Microsoft Copilot Cowork

Workbook version 0.1.0 · package built 14 Oct 2026

**How to use this file:** in Copilot Cowork, attach this file and `preview.html`, link the
deployed workbook `Product portfolio hub.xlsx` (the shared drive (SharePoint, Teams or OneDrive)), and ask: *Build the portal described in PORTAL_BUILD.md.*

## 1. Instructions for Copilot Cowork

* Build a read only portal on top of the linked Excel workbook. The workbook is the single
  source of truth: read from its named tables, never copy data into the portal.
* Build exactly the pages in section 4, in that order, with the given labels and text.
* Compute every number, list and chart from the definitions given. Never type a number in.
* Follow the look and feel in section 5 and match `preview.html` as closely as you can.
* Words in [square brackets] are replaced by the value of the KPI tile with that label.
* If something cannot be built as described, do not improvise: list what and why at the end.

## 2. Data source

Workbook: `Product portfolio hub.xlsx` at the shared drive (SharePoint, Teams or OneDrive). Each sheet holds one Excel table named `tbl_<sheet>`.
Ignore the About sheet.

### Table `tbl_lkp_Status` (sheet lkp_Status)

Allowed status values. Key: `Value`.

| Column | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| Value | string | yes |  |
| Meaning | string | yes |  |

### Table `tbl_Goals` (sheet Goals)

Strategic goals the team commits to. Key: `ID`.

| Column | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| ID | string | yes |  |
| Title | string | yes |  |
| Owner | string | yes |  |

### Table `tbl_Initiatives` (sheet Initiatives)

Work that delivers a goal. Key: `ID`.

| Column | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| ID | string | yes |  |
| GoalID | string | yes | links to `Goals.ID` |
| Title | string | yes |  |
| Owner | string | yes |  |
| Status | string | yes | one of the values in `lkp_Status.Value` |
| TargetDate | date | no |  |

## 3. Status colours

Every status always uses the same colour on every page (dots, bars, legends).

| Status value | Stage | Colour |
| :--- | :--- | :--- |
| Not started | Backlog | `#5B6067` |
| On track | In progress | `#B22D5B` |
| At risk | Review | `#CC7C2E` |
| Done | Done | `#438852` |

## 4. Pages

Top bar on every page (masthead):
* Small uppercase breadcrumb: Org · Group Product Management · Product team
* Title: Product portfolio hub
* Right side: AS OF with the date the data was last refreshed, and BOARD: Product leadership
* Below it, a tab bar with one tab per page, labels in uppercase.

### Page 1: Where do we stand?

* Eyebrow: Section 01 · Portfolio
* Headline: Where delivery stands.
* Lede: Every initiative the product team has committed to, and how it is tracking against its goal.
* Narrative sentence: The portfolio holds [Live portfolio] initiatives across [Goals] goals and [Owners] owners, with [In flight] in flight right now. [Delivered] have been delivered. (KPI values in crimson, semibold)

**Insight cards** (3 across, heading in serif):

* **Are we on track?** [In flight] in flight, [Delivered] delivered. [At risk] at risk and need a look.
* **What needs a look?** up to 3 rows from `tbl_Initiatives` where Status is At risk, earliest `TargetDate` first, shown as `Title — TargetDate`. If none: "Nothing is at risk."
* **What lands next?** up to 3 rows from `tbl_Initiatives` where Status is On track or At risk, earliest `TargetDate` first, shown as `Title — TargetDate`. If none: "Nothing scheduled."

**KPI tiles** (6 across: label, big number, sub line):

| Label | Number | Sub line | Highlight |
| :--- | :--- | :--- | :--- |
| Live portfolio | number of rows in table `tbl_Initiatives` where Status is Not started or On track or At risk | initiatives not yet done |  |
| In flight | number of rows in table `tbl_Initiatives` where Status is On track or At risk | [At risk] at risk | spotlight (green tile) |
| At risk | number of rows in table `tbl_Initiatives` where Status is At risk | need a look this week |  |
| Delivered | number of rows in table `tbl_Initiatives` where Status is Done | all time |  |
| Goals | number of rows in table `tbl_Goals` | strategic goals |  |
| Owners | number of different `Owner` values in `tbl_Initiatives` | people leading work |  |

**Charts** (2 across):

* LIFECYCLE · **Initiatives by status**: horizontal bar chart; count of rows in `tbl_Initiatives` per `Status`; colours: status colours from section 3, in lifecycle order.
* MIX · **Initiatives by owner**: donut chart, legend on the right, no labels on slices; count of rows in `tbl_Initiatives` per `Owner`; colours: categorical palette in order, largest first, Other in grey.

### Page 2: The full list

* Eyebrow: Section 02 · Full list
* Headline: Every initiative in one place.
* Lede: Filter and sort the whole portfolio. This is the same data as the workbook.

**Table** of all rows in `tbl_Initiatives` with columns ID, Title, Owner, Status, TargetDate. Filterable and sortable. Show `Status` as a coloured dot plus text. Dates as 16 Oct 2026.

## 5. Look and feel

Editorial, not a BI tool: the page reads like a short briefing. Full reference in `DESIGN_SYSTEM.md`.

* White page, near black text, 1px light grey borders, 8px rounded corners, no shadows or gradients.
* Crimson `#B22D5B` is the only emphasis colour: the lede, key figures, the active tab underline.
* One spotlight KPI tile per row: background `#DDEFDF`, number `#1F3C23`.
* Headline in a sans serif, large and bold, ending in a full stop. Lede, narrative and card headings in a serif.
* Small uppercase labels with wide letter spacing for eyebrows, tabs and KPI labels.
* Big KPI numbers with tabular figures. Dates as 16 Oct 2026.
* Fonts: "Inter","Segoe UI",system-ui,sans-serif for text, "Source Serif 4","Source Serif Pro",Georgia,serif for serif text.
* Categorical colours in order: #B22D5B, #CC7C2E, #A85923, #D4494C, #2D679C, #438852, #743EE4, #AE2A3F; Other is #8B8F96.

Colour tokens:

```css
/* Editorial Portfolio design tokens and starter CSS. Source of truth: design/DESIGN_SYSTEM.md */
:root{
  /* core */
  --ink:#0F1116; --ink-2:#1E2025; --ink-3:#3D3F43;
  --slate:#5B6067; --muted:#686D73; --subtle:#8C9097;
  --rule-strong:#45474B; --rule:#E6E7E9; --rule-soft:#EAEAEA; --grid:#F3F3F4;
  --bg:#FFFFFF;
  /* accent & status */
  --accent:#B22D5B; --accent-tint:#F6E8EE; --brand-red:#D4494C;
  --spot-bg:#DDEFDF; --spot-ink:#1F3C23; --spot-label:#486B4F;
  /* categorical */
  --cat-other:#8B8F96; --cat-1:#B22D5B; --cat-2:#CC7C2E; --cat-3:#A85923;
  --cat-4:#D4494C; --cat-5:#2D679C; --cat-6:#438852; --cat-7:#743EE4; --cat-8:#AE2A3F;
  /* stages */
  --stage-backlog:#5B6067; --stage-progress:#B22D5B; --stage-review:#CC7C2E; --stage-done:#438852;
  /* type */
  --font-sans:"Inter","Segoe UI",system-ui,sans-serif;
  --font-serif:"Source Serif 4","Source Serif Pro",Georgia,serif;
  /* shape */
  --radius:8px; --gap:16px; --maxw:1180px;
}
```

## 6. Acceptance checklist

* [ ] Every page in section 4 exists, in order, with the given labels
* [ ] Masthead shows breadcrumb, title, an AS OF date and the board
* [ ] Every KPI, list and chart is computed from the workbook tables, nothing typed in
* [ ] Each section has eyebrow, headline, crimson lede and narrative sentence
* [ ] At most one spotlight tile per row; every tile has a sub line
* [ ] Status colours match section 3 on every page
* [ ] Hairline borders, 8px radius, no shadows; looks like `preview.html`
* [ ] Adding a row in the workbook shows up in the portal after refresh

## 7. Could not build

Copilot Cowork: list here anything you could not build as described, and why.
