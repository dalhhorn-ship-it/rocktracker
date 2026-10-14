"""Build the standard handoff package from the schema and portal spec.

  python3 scripts/build_handoff.py                      run tests, then build the package
  python3 scripts/build_handoff.py --from live.xlsx     same, migrating a downloaded live workbook
  python3 scripts/build_handoff.py --skip-tests --out DIR

Package (folder next to the deployment workbook, plus a zip of it):
  <title>.xlsx        the workbook to upload to the shared drive
  README.md           for the person deploying: what is in the package and what to do
  PORTAL_BUILD.md     for Microsoft Copilot Cowork: everything needed to build the portal
  preview.html        reference render of the portal on sample data
  DESIGN_SYSTEM.md    full design system reference
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_workbook  # noqa: E402

STAGE_NAMES = {"backlog": "Backlog", "progress": "In progress", "review": "Review", "done": "Done"}


def tokens(css):
    return dict(re.findall(r"--([\w-]+):\s*([^;]+);", css))


def run_tests():
    result = subprocess.run([str(ROOT / "scripts" / "test.sh")], capture_output=True, text=True)
    lines = [l for l in result.stdout.splitlines() if " passed" in l or " failed" in l or " error" in l]
    summary = lines[-1].strip() if lines else "no summary"
    if result.returncode != 0:
        print(result.stdout[-3000:])
        sys.exit(f"tests failed, no package built: {summary}")
    return summary


def where_text(where):
    if not where:
        return ""
    parts = [f"{col} is {' or '.join(values)}" for col, values in where.items()]
    return " where " + " and ".join(parts)


def kpi_text(k):
    if k["agg"] == "count":
        what = f"number of rows in table `tbl_{k['table']}`"
    elif k["agg"] == "distinct":
        what = f"number of different `{k['column']}` values in `tbl_{k['table']}`"
    elif k["agg"] == "sum":
        what = f"sum of `{k['column']}` in `tbl_{k['table']}`"
    else:
        what = f"average of `{k['column']}` in `tbl_{k['table']}`, one decimal"
    return what + where_text(k.get("where"))


def placeholders(text, labels):
    return re.sub(r"\{(\w+)\}", lambda m: f"[{labels[m.group(1)]}]", text)


def column_rule(c):
    if c.get("lookup"):
        return f"one of the values in `{c['lookup']}`"
    if c.get("references"):
        return f"links to `{c['references']}`"
    if c.get("formula"):
        return "calculated in the workbook, read only"
    return ""


def portal_build_md(schema, spec, tok, file_name, location):
    labels = {k["id"]: k["label"] for t in spec["tabs"] for k in t.get("kpis", [])}
    m = spec["masthead"]
    out = [
        f"# Build the {schema['title']} portal in Microsoft Copilot Cowork",
        "",
        f"Workbook version {schema['version']} · package built {dt.date.today():%d %b %Y}",
        "",
        "**How to use this file:** in Copilot Cowork, attach this file and `preview.html`, link the",
        f"deployed workbook `{file_name}` ({location}), and ask: *Build the portal described in PORTAL_BUILD.md.*",
        "",
        "## 1. Instructions for Copilot Cowork",
        "",
        "* Build a read only portal on top of the linked Excel workbook. The workbook is the single",
        "  source of truth: read from its named tables, never copy data into the portal.",
        "* Build exactly the pages in section 4, in that order, with the given labels and text.",
        "* Compute every number, list and chart from the definitions given. Never type a number in.",
        "* Follow the look and feel in section 5 and match `preview.html` as closely as you can.",
        "* Words in [square brackets] are replaced by the value of the KPI tile with that label.",
        "* If something cannot be built as described, do not improvise: list what and why at the end.",
        "",
        "## 2. Data source",
        "",
        f"Workbook: `{file_name}` at {location}. Each sheet holds one Excel table named `tbl_<sheet>`.",
        "Ignore the About sheet.",
        "",
    ]
    for s in schema["sheets"]:
        out += [f"### Table `tbl_{s['name']}` (sheet {s['name']})", "", f"{s.get('purpose', '')}. Key: `{s['primary_key']}`.", "",
                "| Column | Type | Required | Rule |", "| :--- | :--- | :--- | :--- |"]
        out += [f"| {c['name']} | {c['type']} | {'yes' if c.get('required') else 'no'} | {column_rule(c)} |" for c in s["columns"]]
        out.append("")

    out += ["## 3. Status colours", "",
            "Every status always uses the same colour on every page (dots, bars, legends).", "",
            "| Status value | Stage | Colour |", "| :--- | :--- | :--- |"]
    for status, stage in spec["stage_map"].items():
        out.append(f"| {status} | {STAGE_NAMES[stage]} | `{tok['stage-' + stage]}` |")
    out += ["", "## 4. Pages", "",
            "Top bar on every page (masthead):",
            f"* Small uppercase breadcrumb: {' · '.join(m['breadcrumb'])}",
            f"* Title: {m['title']}",
            f"* Right side: AS OF with the date the data was last refreshed, and BOARD: {m['board']}",
            "* Below it, a tab bar with one tab per page, labels in uppercase.", ""]

    for i, tab in enumerate(spec["tabs"], start=1):
        out += [f"### Page {i}: {tab['question']}", "",
                f"* Eyebrow: {tab['eyebrow']}", f"* Headline: {tab['headline']}", f"* Lede: {tab['lede']}"]
        if tab.get("narrative"):
            out.append(f"* Narrative sentence: {placeholders(tab['narrative'], labels)} (KPI values in crimson, semibold)")
        out.append("")
        if tab.get("insights"):
            out += ["**Insight cards** (3 across, heading in serif):", ""]
            for ins in tab["insights"]:
                if "list" in ins:
                    lst = ins["list"]
                    order = f", earliest `{lst['date']}` first, shown as `{lst['item']} — {lst['date']}`" if lst.get("date") else ""
                    body = (f"up to {lst.get('limit', 3)} rows from `tbl_{lst['table']}`{where_text(lst.get('where'))}{order}. "
                            f"If none: \"{ins.get('empty', '')}\"")
                else:
                    body = placeholders(ins["text"], labels)
                out.append(f"* **{ins['question']}** {body}")
            out.append("")
        if tab.get("kpis"):
            out += ["**KPI tiles** (6 across: label, big number, sub line):", "",
                    "| Label | Number | Sub line | Highlight |", "| :--- | :--- | :--- | :--- |"]
            for k in tab["kpis"]:
                out.append(f"| {k['label']} | {kpi_text(k)} | {placeholders(k['sub'], labels)} | {'spotlight (green tile)' if k.get('spotlight') else ''} |")
            out.append("")
        if tab.get("charts"):
            out += ["**Charts** (2 across):", ""]
            for ch in tab["charts"]:
                colour = "status colours from section 3, in lifecycle order" if ch["color"] == "stage" else "categorical palette in order, largest first, Other in grey"
                kind = "horizontal bar chart" if ch["type"] == "bar" else "donut chart, legend on the right, no labels on slices"
                out.append(f"* {ch['eyebrow'].upper()} · **{ch['title']}**: {kind}; count of rows in `tbl_{ch['table']}` per `{ch['group_by']}`; colours: {colour}.")
            out.append("")
        if tab.get("table"):
            t = tab["table"]
            out += [f"**Table** of all rows in `tbl_{t['table']}` with columns {', '.join(t['columns'])}. "
                    f"Filterable and sortable. Show `{t.get('status_column', '')}` as a coloured dot plus text. Dates as 16 Oct 2026.", ""]

    out += ["## 5. Look and feel", "",
            "Editorial, not a BI tool: the page reads like a short briefing. Full reference in `DESIGN_SYSTEM.md`.", "",
            "* White page, near black text, 1px light grey borders, 8px rounded corners, no shadows or gradients.",
            f"* Crimson `{tok['accent']}` is the only emphasis colour: the lede, key figures, the active tab underline.",
            f"* One spotlight KPI tile per row: background `{tok['spot-bg']}`, number `{tok['spot-ink']}`.",
            "* Headline in a sans serif, large and bold, ending in a full stop. Lede, narrative and card headings in a serif.",
            "* Small uppercase labels with wide letter spacing for eyebrows, tabs and KPI labels.",
            "* Big KPI numbers with tabular figures. Dates as 16 Oct 2026.",
            f"* Fonts: {tok['font-sans']} for text, {tok['font-serif']} for serif text.",
            f"* Categorical colours in order: {', '.join(tok[f'cat-{i}'] for i in range(1, 9))}; Other is {tok['cat-other']}.",
            "",
            "Colour tokens:", "", "```css", (ROOT / "design" / "tokens.css").read_text().split("}")[0] + "}", "```", "",
            "## 6. Acceptance checklist", "",
            "* [ ] Every page in section 4 exists, in order, with the given labels",
            "* [ ] Masthead shows breadcrumb, title, an AS OF date and the board",
            "* [ ] Every KPI, list and chart is computed from the workbook tables, nothing typed in",
            "* [ ] Each section has eyebrow, headline, crimson lede and narrative sentence",
            "* [ ] At most one spotlight tile per row; every tile has a sub line",
            "* [ ] Status colours match section 3 on every page",
            "* [ ] Hairline borders, 8px radius, no shadows; looks like `preview.html`",
            "* [ ] Adding a row in the workbook shows up in the portal after refresh",
            "",
            "## 7. Could not build",
            "",
            "Copilot Cowork: list here anything you could not build as described, and why.",
            ""]
    return "\n".join(out)


def readme_md(schema, spec, file_name, location, test_summary):
    return "\n".join([
        f"# {schema['title']}: deployment package",
        "",
        f"Version {schema['version']} · built {dt.date.today():%d %b %Y} · tests: {test_summary}",
        "",
        "This package holds everything needed to put the workbook live and build its portal.",
        "",
        "## What is in it",
        "",
        "| File | What it is | Who uses it |",
        "| :--- | :--- | :--- |",
        f"| `{file_name}` | The workbook (backend). Lookups filled in, no sample data. | Upload to the shared drive |",
        "| `PORTAL_BUILD.md` | Complete build instructions for the portal | Give to Copilot Cowork |",
        "| `preview.html` | What the portal should look like, on sample data | Open in a browser; give to Copilot Cowork |",
        "| `DESIGN_SYSTEM.md` | Full design system reference | Copilot Cowork, and you when checking |",
        "",
        "## Steps",
        "",
        "### 1. Put the workbook live",
        f"1. Upload `{file_name}` to {location}. Keep the file name as it is.",
        "2. Give edit rights only to the people who maintain the data; everyone else read only.",
        "3. Check version history is on (it is by default on SharePoint and OneDrive).",
        "4. Open the About sheet: it lists every sheet, its owner and the editing rules.",
        "5. Enter or paste the first real data. Use the dropdowns; pink cells are required and still empty.",
        "",
        "### 2. Build the portal in Copilot Cowork",
        "1. Open Copilot Cowork.",
        "2. Attach `PORTAL_BUILD.md` and `preview.html`, and link the live workbook (not a local copy).",
        "3. Ask: *Build the portal described in PORTAL_BUILD.md.*",
        "4. Check the result against `preview.html` and the checklist in section 6 of `PORTAL_BUILD.md`.",
        "5. If Cowork lists anything under \"Could not build\", note it for the next `/retro`.",
        "",
        "### 3. Keep it running",
        "* Edit data in the workbook only; the portal follows after refresh.",
        "* Never rename, reorder or delete sheets or columns: the portal depends on them.",
        "* Need a new column, sheet or page? Ask for it in the factory repository. You will get a new",
        "  package with a migrated copy of your live workbook, so no data is lost.",
        "",
        "## Contents at a glance",
        "",
        "| Sheet | Purpose | Owner |",
        "| :--- | :--- | :--- |",
        *[f"| {s['name']} | {s.get('purpose', '')} | {s.get('owner', '')} |" for s in schema["sheets"]],
        "",
        "| Portal page | Question it answers |",
        "| :--- | :--- |",
        *[f"| {i} | {t['question']} |" for i, t in enumerate(spec["tabs"], start=1)],
        "",
    ])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="source", help="downloaded live workbook to migrate")
    ap.add_argument("--out", help="package folder (default: folder of deploy_file in the schema)")
    ap.add_argument("--skip-tests", action="store_true")
    args = ap.parse_args(argv)

    schema = build_workbook.load_schema()
    spec = json.loads((ROOT / "portal" / "portal.spec.json").read_text())
    tok = tokens((ROOT / spec["tokens"]).read_text())
    deploy = ROOT / schema["deploy_file"]
    pkg = Path(args.out) if args.out else deploy.parent
    file_name = deploy.name
    location = schema.get("deploy_location") or "the shared drive (SharePoint, Teams or OneDrive)"
    test_summary = "not run" if args.skip_tests else run_tests()

    if pkg.exists():
        shutil.rmtree(pkg)
    pkg.mkdir(parents=True)
    wb_args = ["--deploy", "--out", str(pkg / file_name)] + (["--from", args.source] if args.source else [])
    build_workbook.main(wb_args)
    (pkg / "PORTAL_BUILD.md").write_text(portal_build_md(schema, spec, tok, file_name, location))
    (pkg / "README.md").write_text(readme_md(schema, spec, file_name, location, test_summary))
    shutil.copyfile(ROOT / spec["design_system"], pkg / "DESIGN_SYSTEM.md")
    preview = ROOT / "portal" / "preview.html"
    if preview.exists():
        shutil.copyfile(preview, pkg / "preview.html")
    zip_path = shutil.make_archive(str(pkg), "zip", pkg.parent, pkg.name)
    print(f"package: {pkg}\nzip: {zip_path}")


if __name__ == "__main__":
    sys.exit(main())
