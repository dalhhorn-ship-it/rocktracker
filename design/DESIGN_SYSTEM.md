# Dashboard Design System — "Editorial Portfolio" style

Captured from the **Finance, Procurement, Margin & Forecasting Hub** (Eneco · Group Product Management · Product 2), the "Where do we stand?" tab. Use this as the reference for every new portfolio or OKR dashboard so they look and read the same.

> **Notes on where the values come from:** colours were sampled directly from a screenshot of the dashboard, so the hex values are close but may be off by a shade. Typefaces were **inferred** by eye: the sans looks like a neo-grotesk (Inter-like) and the narrative serif looks like a text serif (Source Serif-like). Before calling the system final, swap in the real font names and hex values from the source CSS.

---

## 1. Design principles

1. **Editorial, not "BI tool".** The page reads like a short briefing: headline, then lede, then a one-sentence summary, then evidence. Numbers sit inside sentences before they appear as tiles.
2. **Question-led navigation.** Each tab is a question a stakeholder asks ("Where do we stand?", "What ships next?"), not a data category.
3. **Quiet canvas, one loud colour.** The page is white with ink-black text and hairline borders. **Crimson** is the only emphasis colour. It marks key figures, the lede and the active state.
4. **One highlight per row.** In a KPI row, at most one tile gets a tinted "spotlight" background, used for the metric that matters most right now (here: *In flight*).
5. **Answer first, detail after.** Each section runs from summary sentence to insight cards to KPI tiles to charts to the full list.
6. **Every number has context.** Each KPI carries a sub-line that explains it ("28 active · 1 in review", "created → delivered").

---

## 2. Design tokens

### 2.1 Colour: core

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#0F1116` | Headlines, titles, KPI numbers, active tab |
| `--ink-2` | `#1E2025` | Body / narrative text |
| `--ink-3` | `#3D3F43` | Card body text |
| `--slate` | `#5B6067` | Inactive tab labels, neutral bars ("Backlog") |
| `--muted` | `#686D73` | KPI sub-lines, secondary metadata |
| `--subtle` | `#72777D` | Eyebrows, uppercase labels, "AS OF" / "BOARD" labels |
| `--rule-strong` | `#45474B` | 1px rule under header and under tab bar |
| `--rule` | `#E6E7E9` | Card borders |
| `--rule-soft` | `#EAEAEA` | Divider under chart-card titles |
| `--grid` | `#F3F3F4` | Chart gridlines |
| `--bg` | `#FFFFFF` | Page and card background |

### 2.2 Colour: accent and status

| Token | Hex | Use |
|---|---|---|
| `--accent` (crimson) | `#B22D5B` | Lede text, highlighted figures in narrative, active-tab underline, "In Progress" bar |
| `--accent-tint` | `#F6E8EE` | Hover / selected backgrounds (sparingly); Major slip extension on roadmap bars |
| `--amber-tint` | `#F5E3D1` | Minor slip extension on roadmap bars |
| `--plan-bar` | `#D5D7DA` | Grey plan bar (start to planned) on roadmap bars |
| `--brand-red` | `#D4494C` | Logo mark only (plus one category colour) |
| `--spot-bg` | `#DDEFDF` | Spotlight KPI tile background (positive / "live" state) |
| `--spot-ink` | `#1F3C23` | Number on spotlight tile |
| `--spot-label` | `#486B4F` | Label + sub-line on spotlight tile |

### 2.3 Colour: categorical chart palette (use in this order)

| # | Token | Hex | Example in source |
|---|---|---|---|
| 0 | `--cat-other` | `#8B8F96` | "Other …" / unclassified (always grey, always largest-first) |
| 1 | `--cat-1` crimson | `#B22D5B` | Reporting & BI |
| 2 | `--cat-2` amber | `#CC7C2E` | P&L / Margin / Darwin |
| 3 | `--cat-3` rust | `#A85923` | Procurement & AP |
| 4 | `--cat-4` red | `#D4494C` | Master Data & Migration |
| 5 | `--cat-5` blue | `#2D679C` | — |
| 6 | `--cat-6` green | `#438852` | — |
| 7 | `--cat-7` purple | `#743EE4` | — |
| 8 | `--cat-8` wine | `#AE2A3F` | — |

**Lifecycle / stage colours (fixed meaning, reuse everywhere):**

| Stage | Hex |
|---|---|
| Backlog | `#5B6067` (slate) |
| In Progress | `#B22D5B` (crimson) |
| Review | `#CC7C2E` (amber) |
| Done / Delivered | `#438852` (green), recommended for consistency with the spotlight tile |

### 2.4 Typography

| Role | Family | Size | Weight | Case / tracking | Colour |
|---|---|---|---|---|---|
| Header eyebrow | Sans | 10px | 500 | UPPERCASE, `letter-spacing: .12em` | `--subtle` |
| Dashboard title | Sans | 16px | 600 | Sentence | `--ink` |
| Meta label ("AS OF") | Sans | 9px | 500 | UPPERCASE, `.12em` | `--subtle` |
| Meta value | Sans | 11–12px | 600 | — | `--ink` |
| Tab label | Sans | 11px | 500 | UPPERCASE, `.06em` | `--slate` → `--ink` active |
| Section eyebrow ("SECTION 01 · PORTFOLIO") | Sans | 10px | 500 | UPPERCASE, `.14em` | `--subtle` |
| H1 section headline | Sans | 30–32px | 600 | Sentence, ends with a full stop, `letter-spacing: -.01em` | `--ink` |
| Lede | Serif | 13–14px | 400 | Sentence, max 2 lines | `--accent` |
| Narrative summary | Serif | 13px | 400 (figures 600) | — | `--ink-2`, figures `--accent` |
| Insight card heading | Serif | 15px | 600 | Question form | `--ink` |
| Card body | Sans | 11–12px | 400 (dates 600) | — | `--ink-3` |
| KPI label | Sans | 9–10px | 500 | UPPERCASE, `.12em` | `--subtle` |
| KPI number | Sans | 34–38px | 600 | `font-variant-numeric: tabular-nums`, `letter-spacing: -.02em` | `--ink` |
| KPI sub-line | Sans | 9–10px | 400 | — | `--muted` |
| Chart eyebrow | Sans | 9–10px | 500 | UPPERCASE, `.14em` | `--subtle` |
| Chart title | Sans | 15px | 500 | Sentence | `--ink` |
| Axis / legend | Sans | 10px | 400–500 | — | `--ink-3` |

Suggested stacks:
```css
--font-sans:  "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
--font-serif: "Source Serif 4", "Source Serif Pro", Georgia, serif;
```

### 2.5 Spacing, radius and elevation

- **Base unit:** 4px. Common steps are 8 / 12 / 16 / 20 / 24 / 32 / 48.
- **Content width:** max ~1180px, centred. Page side padding is 24px.
- **Grid gutter:** 16px between cards.
- **Card padding:** 16px (KPI tiles), 20px (insight and chart cards).
- **Radius:** 8px on all cards and tiles, 3px on bar ends.
- **Elevation:** none. Use a 1px `--rule` border only, with no shadows.
- **Vertical rhythm:** 8px eyebrow to H1, 12px H1 to lede, 32px lede to narrative, 24px narrative to cards, 16px between card rows.

### 2.6 Dark mode

Dark mode is a second value set for the same token names (`design/tokens.css`), under `:root[data-theme="dark"]` and under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }`. Rules:

- Same names, same hues, same fonts, radius and spacing. No shadows, no gradients. `--brand-red` is unchanged.
- Crimson stays the only emphasis colour. It is lightened (`#E06A93`) so it reads on dark; nothing else becomes an accent.
- `--card` is a new token (light `#FFFFFF`, dark `#1A1C21`). Cards and KPI tiles use `--card`; the page uses `--bg`.
- Default follows the system setting. The masthead meta holds a theme switch written as text (LIGHT and DARK, not an icon) that sets `data-theme` on the root element and is remembered for the session.
- Body text, labels and the accent reach a contrast of 4.5:1 or more against both `--bg` and `--card` in both modes. `tests/test_portal.py::test_dark_mode_tokens` enforces this and that every light token has a dark value. To reach 4.5:1 in light mode, `--subtle` moved from `#8C9097` to `#72777D`.

| Token | Light | Dark | Ratio light on `--bg` | Ratio dark on `--bg` | Ratio dark on `--card` |
|---|---|---|---|---|---|
| `--bg` | `#FFFFFF` | `#121317` | | | |
| `--card` | `#FFFFFF` | `#1A1C21` | | | |
| `--ink` | `#0F1116` | `#F2F2F3` | 18.88 | 16.59 | 15.24 |
| `--ink-2` | `#1E2025` | `#E1E2E4` | 16.30 | 14.32 | 13.15 |
| `--ink-3` | `#3D3F43` | `#C4C6CA` | 10.55 | 10.85 | 9.97 |
| `--slate` | `#5B6067` | `#A3A7AD` | 6.34 | 7.68 | 7.05 |
| `--muted` | `#686D73` | `#9A9EA5` | 5.22 | 6.90 | 6.34 |
| `--subtle` | `#72777D` | `#868B92` | 4.52 | 5.41 | 4.97 |
| `--accent` | `#B22D5B` | `#E06A93` | 6.14 | 5.88 | 5.40 |
| `--accent-tint` | `#F6E8EE` | `#3A1E29` | | | |
| `--amber-tint` | `#F5E3D1` | `#3A2A1B` | | | |
| `--plan-bar` | `#D5D7DA` | `#3A3D43` | | | |
| `--rule-strong` | `#45474B` | `#5A5D63` | | | |
| `--rule` | `#E6E7E9` | `#2C2E33` | | | |
| `--rule-soft` | `#EAEAEA` | `#26282C` | | | |
| `--grid` | `#F3F3F4` | `#202226` | | | |
| `--spot-bg` | `#DDEFDF` | `#1E3323` | | | |
| `--spot-ink` | `#1F3C23` | `#CFEBD4` | 10.11 on spot-bg | 10.62 on spot-bg | |
| `--spot-label` | `#486B4F` | `#8DBB96` | 5.01 on spot-bg | 6.23 on spot-bg | |
| `--stage-backlog` | `#5B6067` | `#8C9097` | | | |
| `--stage-progress` | `#B22D5B` | `#E06A93` | | | |
| `--stage-review` | `#CC7C2E` | `#E0A15F` | | | |
| `--stage-done` | `#438852` | `#6DB97E` | | | |
| `--cat-other` | `#8B8F96` | `#8C9097` | | | |
| `--cat-1` | `#B22D5B` | `#E06A93` | | | |
| `--cat-2` | `#CC7C2E` | `#E0A15F` | | | |
| `--cat-3` | `#A85923` | `#D08A55` | | | |
| `--cat-4` | `#D4494C` | `#E8787A` | | | |
| `--cat-5` | `#2D679C` | `#6FA3D6` | | | |
| `--cat-6` | `#438852` | `#6DB97E` | | | |
| `--cat-7` | `#743EE4` | `#A585F0` | | | |
| `--cat-8` | `#AE2A3F` | `#D9677A` | | | |

Stage, status and chart colours are fills and marks, not text. They keep at least 3:1 against the surface in dark mode (lowest: `--stage-progress` 5.4 and `--stage-done` 7.2 on `--card`, `--stage-backlog` 5.3). In light mode amber (3.24) and grey (3.2) stay above 3:1 and `--stage-done` is 4.3. Always put the status word next to the colour; colour is never the only signal.

**Milestone status and rock state colours.** Milestone statuses reuse the stage colours; Slipped and Off track are the strongest marks. Same meaning in both modes.

| Item | Token (stage) | Light | Dark | Mark |
|---|---|---|---|---|
| Milestone Completed | `--stage-done` (Done) | `#438852` | `#6DB97E` | solid |
| Milestone On plan | `--stage-backlog` (slate) | `#5B6067` | `#8C9097` | solid |
| Milestone On watch | `--stage-review` (amber) | `#CC7C2E` | `#E0A15F` | solid |
| Milestone Slipped | `--stage-progress` / `--accent` (crimson) | `#B22D5B` | `#E06A93` | solid, label in crimson |
| Milestone On hold | `--cat-other` (grey) | `#8B8F96` | `#8C9097` | solid |
| Milestone Not committed | `--cat-other` (grey) | `#8B8F96` | `#8C9097` | outline only, no fill |
| Rock On track | `--stage-done` (green) | `#438852` | `#6DB97E` | solid |
| Rock At risk | `--stage-review` (amber) | `#CC7C2E` | `#E0A15F` | solid |
| Rock Off track | `--accent` (crimson) | `#B22D5B` | `#E06A93` | solid, bold label |

Wine on `--bg`: 6.56 light, 5.46 dark, so Off track text is also readable.

---

## 3. Page anatomy (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ [logo]  EYEBROW · ORG · TEAM                      AS OF      BOARD   │
│         Dashboard title                          13 Oct 2026  Name   │
├──────────────────────────────────────────────────────────────────────┤  ← 1px --rule-strong
│ WHERE DO WE STAND?  WHAT MATTERS MOST?  WHAT'S BEING BUILT?  …       │  ← tab bar
│ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ (2px crimson underline on active)                 │
├──────────────────────────────────────────────────────────────────────┤  ← 1px --rule-strong
│ SECTION 01 · PORTFOLIO                                               │
│ Where delivery stands.                                  (H1)         │
│ Crimson serif lede, one or two lines.                                │
│                                                                      │
│ Serif narrative sentence with crimson key figures …                  │
│                                                                      │
│ ┌ Insight card ┐ ┌ Insight card ┐ ┌ Insight card ┐   ← 3 columns     │
│ ┌KPI┐┌SPOT┐┌KPI┐┌KPI┐┌KPI┐┌KPI┐                      ← 6 columns     │
│ ┌ Chart card (bar) ──────┐ ┌ Chart card (donut) ────┐ ← 2 columns     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Components

### 4.1 Masthead
- Left side: the **logo mark** (cluster of three `--brand-red` dots, ~20px), then a stacked eyebrow (org breadcrumb with `·` separators) over the title.
- Right side: one or more **meta pairs** (label over value, right-aligned), e.g. *As of* and *Board*. Always show the data-as-of date.
- Bottom: a 1px `--rule-strong` rule across the content width.

### 4.2 Tab bar
- Labels are UPPERCASE questions ending in "?", with the exception of one "The full list" catch-all tab at the end.
- Space tabs 28–32px apart.
- Active tab: `--ink` text with a 2px `--accent` underline that sits on the bottom rule.
- Inactive tabs use `--slate`. On hover, switch to `--ink`. Don't use pills or backgrounds.

**Standard tab set for portfolio dashboards:**
1. Where do we stand? (portfolio overview)
2. What matters most? (priorities)
3. What's being built? (in-flight work)
4. When does it land? (timeline / roadmap)
5. Who's building it? (owners / teams)
6. Are we responsive? (cycle time, SLA, intake)
7. The full list (filterable table)

### 4.3 Section intro
- **Eyebrow:** `SECTION 0N · TOPIC`
- **H1:** a short declarative statement ending in a full stop ("Where delivery stands.")
- **Lede:** one crimson serif sentence that frames the scope, max ~560px wide.

### 4.4 Narrative summary sentence
One paragraph (max ~2 lines) that states the headline numbers in plain language. Wrap each key figure in `<em class="fig">` (crimson, semibold, not italic).

> The portfolio holds **116 live features** across 10 owners, with **29 in flight** right now. Over the last 12 months the team delivered **64**, about **5.3 a month**, at a typical **81-day** cycle. Most active area: **Reporting & BI**.

### 4.5 Insight cards (3-up)
- **Heading:** a question in serif ("Are we on track?", "What ships next?", "What shipped recently?").
- **Body:** 1–3 short lines or a list of up to 3 items as `Item name — **date**`.
- Use crimson for the lead figure in a status sentence ("**29 in flight**, 64 delivered. 2 are past target and need a look.").
- Always end with an action cue when something is off ("…need a look").

### 4.6 KPI tiles (6-up)
- Each tile has three lines: **LABEL**, **Number**, sub-line.
- Keep units short and attached: `81 d`, `5.3`, plus the unit in the sub-line ("features / month").
- The sub-line gives a breakdown or the definition: `212 total · 96 archived`, `created → delivered`.
- **Spotlight variant:** `--spot-bg` background with no border, and the number and labels in the spot inks. Use one per row at most.
- Standard portfolio set: Live portfolio · In flight (spotlight) · Delivered · 12 mo · Throughput · Avg cycle time · Owners.

### 4.7 Chart cards (2-up)
- Header is an eyebrow (e.g. `LIFECYCLE`, `MIX`), then a sans title ("Portfolio by stage"), then a 1px `--rule-soft` divider.
- **Horizontal bar:** category labels on the left (right-aligned, 10px, 500 weight), bars ~18px tall with 3px radius, faint vertical gridlines in `--grid`, no axis line. Colour bars by stage colour, not by rank.
- **Donut:** thick ring (inner radius ~55%), segments start at 12 o'clock and run clockwise, sorted largest first, with "Other" always grey. The legend sits on the right with 8px square swatches and 10px labels. Put no labels on the slices.
- Don't add 3D, drop shadows or gradients. Show values in a tooltip or table, not on the chart.

### 4.8 Full list (table)
Use the same tokens: 11px sans body, UPPERCASE 9–10px header in `--subtle`, 1px `--rule` row separators, no zebra stripes. Show status with a small stage-coloured dot plus text.

---

## 5. Copy and voice rules

- Write headings as questions and headlines as statements.
- Use sentence case everywhere except eyebrows, tab labels and KPI labels, which are UPPERCASE.
- Separate breadcrumbs and sub-line facts with ` · ` and use an em dash ` — ` before dates.
- Write dates as `16 Oct 2026` (day, short month, year).
- Round averages to one decimal place, and always state the time window ("12 mo", "last 12 months").
- Call out exceptions explicitly and kindly ("2 are past target and need a look").

---

## 6. Do / Don't

| Do | Don't |
|---|---|
| Use crimson only for the few things that matter | Colour every number or every chart differently |
| Put the "as of" date in the masthead | Leave the data freshness ambiguous |
| Lead with a sentence, then show tiles | Open with a wall of charts |
| Use hairline borders and white space | Use shadows, gradients or filled headers |
| Keep stage colours identical across all tabs | Re-map colours per chart |
| Use one spotlight tile per row | Highlight several KPIs at once |

---

## 7. Starter CSS

```css
:root{
  /* core */
  --ink:#0F1116; --ink-2:#1E2025; --ink-3:#3D3F43;
  --slate:#5B6067; --muted:#686D73; --subtle:#72777D;
  --rule-strong:#45474B; --rule:#E6E7E9; --rule-soft:#EAEAEA; --grid:#F3F3F4;
  --bg:#FFFFFF;
  /* accent & status */
  --accent:#B22D5B; --accent-tint:#F6E8EE; --amber-tint:#F5E3D1; --plan-bar:#D5D7DA; --brand-red:#D4494C;
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
body{margin:0;background:var(--bg);color:var(--ink-2);font:400 12px/1.5 var(--font-sans);}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px;}

.eyebrow{font:500 10px/1 var(--font-sans);letter-spacing:.14em;text-transform:uppercase;color:var(--subtle);}

/* masthead */
.mast{display:flex;justify-content:space-between;align-items:center;padding:20px 0 16px;border-bottom:1px solid var(--rule-strong);}
.mast h1{font:600 16px/1.2 var(--font-sans);color:var(--ink);margin:4px 0 0;}
.meta{text-align:right;margin-left:32px;}
.meta b{display:block;font:600 11px/1.4 var(--font-sans);color:var(--ink);margin-top:4px;}

/* tabs */
.tabs{display:flex;gap:30px;border-bottom:1px solid var(--rule-strong);}
.tab{font:500 11px/1 var(--font-sans);letter-spacing:.06em;text-transform:uppercase;color:var(--slate);
     padding:14px 4px 12px;border-bottom:2px solid transparent;margin-bottom:-1px;cursor:pointer;}
.tab:hover{color:var(--ink);}
.tab.active{color:var(--ink);border-bottom-color:var(--accent);}

/* section intro */
.h1{font:600 31px/1.15 var(--font-sans);letter-spacing:-.01em;color:var(--ink);margin:8px 0 12px;}
.lede{font:400 13.5px/1.6 var(--font-serif);color:var(--accent);max-width:560px;}
.narrative{font:400 13px/1.6 var(--font-serif);color:var(--ink-2);margin:32px 0 24px;}
.fig{font-style:normal;font-weight:600;color:var(--accent);}

/* cards */
.grid{display:grid;gap:var(--gap);margin-bottom:var(--gap);}
.g3{grid-template-columns:repeat(3,1fr);} .g6{grid-template-columns:repeat(6,1fr);} .g2{grid-template-columns:repeat(2,1fr);}
.card{background:var(--bg);border:1px solid var(--rule);border-radius:var(--radius);padding:20px;}
.card h3{font:600 15px/1.3 var(--font-serif);color:var(--ink);margin:0 0 12px;}
.card p,.card li{font-size:11.5px;color:var(--ink-3);}

/* KPI */
.kpi{padding:16px;}
.kpi .num{font:600 36px/1.1 var(--font-sans);letter-spacing:-.02em;font-variant-numeric:tabular-nums;color:var(--ink);margin:12px 0 10px;}
.kpi .sub{font-size:9.5px;color:var(--muted);}
.kpi.spot{background:var(--spot-bg);border-color:transparent;}
.kpi.spot .eyebrow,.kpi.spot .sub{color:var(--spot-label);}
.kpi.spot .num{color:var(--spot-ink);}

/* chart card */
.chart h4{font:500 15px/1.3 var(--font-sans);color:var(--ink);margin:6px 0 12px;padding-bottom:12px;border-bottom:1px solid var(--rule-soft);}
.bar{height:18px;border-radius:3px;}
.legend i{display:inline-block;width:8px;height:8px;margin-right:6px;}
```

### Minimal markup skeleton

```html
<header class="wrap mast">
  <div style="display:flex;gap:16px;align-items:center">
    <svg width="20" height="20" aria-hidden="true"><circle cx="5" cy="5" r="3" fill="#D4494C"/><circle cx="13" cy="9" r="2.5" fill="#D4494C"/><circle cx="8" cy="15" r="2.5" fill="#D4494C"/></svg>
    <div><div class="eyebrow">Eneco · Group Product Management · Product 2</div><h1>Dashboard title</h1></div>
  </div>
  <div style="display:flex"><div class="meta eyebrow">As of<b>13 Oct 2026</b></div><div class="meta eyebrow">Board<b>Board name</b></div></div>
</header>
<nav class="wrap tabs"><span class="tab active">Where do we stand?</span><span class="tab">What matters most?</span>…</nav>
<main class="wrap">
  <div class="eyebrow" style="margin-top:24px">Section 01 · Portfolio</div>
  <h2 class="h1">Where delivery stands.</h2>
  <p class="lede">Scope sentence …</p>
  <p class="narrative">The portfolio holds <em class="fig">116 live features</em> …</p>
  <section class="grid g3"><div class="card"><h3>Are we on track?</h3><p>…</p></div>…</section>
  <section class="grid g6"><div class="card kpi"><div class="eyebrow">Live portfolio</div><div class="num">116</div><div class="sub">212 total · 96 archived</div></div>
    <div class="card kpi spot">…</div>…</section>
  <section class="grid g2"><div class="card chart"><div class="eyebrow">Lifecycle</div><h4>Portfolio by stage</h4>…</div>…</section>
</main>
```

---

## 8. Checklist for a new dashboard

- [ ] Masthead shows the org breadcrumb, the title, an **As of** date and the board/owner
- [ ] Tabs are phrased as questions, with "The full list" last
- [ ] Each section has an eyebrow, an H1 ending in a full stop, a crimson lede and a narrative sentence
- [ ] Key figures in the narrative are crimson and semibold
- [ ] There are 3 insight cards with question headings
- [ ] There are 6 KPI tiles, each with a sub-line, and at most one spotlight tile
- [ ] Charts use the stage colours and the categorical order above, with "Other" in grey
- [ ] Borders are 1px hairlines with an 8px radius, and there are no shadows
- [ ] Numbers use tabular figures, dates use the `16 Oct 2026` format, and time windows are stated
