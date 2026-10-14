"""Build the Excel backend from schema/workbook.schema.json (nothing about layout lives here).

  python3 scripts/build_workbook.py                 sample workbook (data/workbook.xlsx), for tests and preview
  python3 scripts/build_workbook.py --deploy        deployment workbook (dist/...), lookups seeded, no rock tabs
  python3 scripts/build_workbook.py --deploy --from live.xlsx
                                                    migration: new structure, rows copied from a downloaded
                                                    live copy (every rock tab's typed cells, lookups, history)

Sheet order: About, RockTemplate, rock tabs, RocksEnd, then the sheets in schema order (Rocks,
Milestones, Risks, CallOuts, Decisions, Teams, RockSnapshots, MilestoneSnapshots, lookups).
Rock tabs follow `rock_tab` in the schema, the six consolidated sheets hold one dynamic array
formula each (DECISIONS 0002, 0003), history and lookup sheets are Excel Tables `tbl_<sheet>`.
Params are defined names. `--from` a schema 1.0.0 file applies the schema `migration` (DECISIONS 0010 to 0017).
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parent.parent
MAX_ROWS = 2000  # date formats and validation range on consolidated, history and lookup sheets
LOOKUP_ROWS = 200  # last row of a lookup list (defined names lst_*); NextSteerco uses the same bound
INK, SUBTLE, RULE, ACCENT_TINT = "0F1116", "8C9097", "E6E7E9", "F6E8EE"  # design/tokens.css
CALC_GREY, SLATE = "EAEAEA", "5B6067"  # --rule-soft, --slate
DATE_FORMAT = "d mmm yyyy"

# Layout of the formula that fills a consolidated sheet (plan A, 3D VSTACK). One place only:
# a change of formula path (plan B or C) edits `consolidation_formula` and `consolidation_names`.
CONSOLIDATION_NAMES = "dkf"  # LET variable names used by the schema formulas


def load_schema():
    return json.loads((ROOT / "schema" / "workbook.schema.json").read_text())


def coerce(value, col_type):
    if col_type == "date" and isinstance(value, str) and value:
        return dt.date.fromisoformat(value)
    return value


def number_format(c):
    """Excel number format of a field or column: the schema `number_format`, else the date format."""
    if c.get("number_format"):
        return c["number_format"]
    return DATE_FORMAT if c["type"] == "date" else None


def list_name(ref):
    sheet, column = ref.split(".", 1)
    return f"lst_{sheet}_{column}"


def col_letter(sheet, name):
    return get_column_letter([c["name"] for c in sheet["columns"]].index(name) + 1)


# ---------------------------------------------------------------------------
# Formula placeholders of the schema (rock_tab.formula_syntax)
# ---------------------------------------------------------------------------
class Resolver:
    """Turns schema formulas into cell formulas: {Field}, {Block.Column}, {slot}, [Column]."""

    def __init__(self, schema):
        rt = schema["rock_tab"]
        self.sheets = {s["name"]: s for s in schema["sheets"]}
        self.fields, self.blocks = {}, {}
        for sec in rt["sections"]:
            if sec["kind"] == "fields":
                for f in sec["fields"]:
                    self.fields[f["name"]] = f"${rt['value_column']}${f['row']}"
            else:
                self.blocks[sec["block"]] = sec

    def block_range(self, block, column):
        sec = self.blocks[block]
        letter = col_letter(self.sheets[block], column)
        return f"${letter}${sec['first_row']}:${letter}${sec['first_row'] + sec['capacity'] - 1}"

    def resolve(self, formula, block=None, row=None, slot=None):
        def curly(m):
            a, b = m.group(1), m.group(2)
            if a == "slot":
                return str(slot)
            if b:
                return self.block_range(a, b)
            return self.fields[a]

        def square(m):
            return f"{col_letter(self.sheets[block], m.group(1))}{row}"

        out = re.sub(r"\{(\w+)(?:\.(\w+))?\}", curly, formula)
        out = re.sub(r"\[(\w+)\]", square, out)
        return spill_refs(out)


def spill_refs(formula):
    """Sheet!$A$2# (as typed in Excel) to the file format _xlfn.ANCHORARRAY(Sheet!$A$2)."""
    return re.sub(r"((?:'[^']+'|[A-Za-z_][\w.]*)!\$?[A-Z]+\$?\d+)#", r"_xlfn.ANCHORARRAY(\1)", formula)


def file_formula(formula, names=()):
    return to_file_formula(formula, names)


def consolidation_formula(schema, sheet, resolver):
    """The formula in A2 of a consolidated sheet (plan A). The only place that knows the path."""
    cf = schema["rock_tab"]["consolidation_formula"]
    cols = len(sheet["columns"])
    last = get_column_letter(cols)
    if sheet["source"] == "strip":
        rng, pattern = f"$A${schema['rock_tab']['strip_row']}:${last}${schema['rock_tab']['strip_row']}", cf["rocks"]
    else:
        sec = resolver.blocks[sheet["name"]]
        rng = f"$A${sec['first_row']}:${last}${sec['first_row'] + sec['capacity'] - 1}"
        pattern = cf["lists"]
    return pattern.replace("{span}", cf["span"]).replace("{range}", rng)


def dynamic_cells(schema):
    """(sheet, cell) pairs to mark as dynamic arrays after saving."""
    anchor = schema["rock_tab"]["consolidation_formula"]["anchor"]
    return [(s["name"], anchor) for s in schema["sheets"] if s["kind"] == "consolidated"]


# ---------------------------------------------------------------------------
# Reading a live copy (migration)
# ---------------------------------------------------------------------------
def read_existing(path):
    """Rows per sheet from an existing workbook, as dicts keyed by header (lookups and history)."""
    wb = load_workbook(path, data_only=False)
    out = {}
    for ws in wb.worksheets:
        values = list(ws.iter_rows(values_only=True))
        if not values:
            continue
        headers = list(values[0])
        out[ws.title] = [dict(zip(headers, r)) for r in values[1:] if any(v is not None for v in r)]
    return out


def read_rock_tabs(path, schema):
    """Typed cells of every rock tab between the template and the end sheet, by the schema layout."""
    rt = schema["rock_tab"]
    sheets = {s["name"]: s for s in schema["sheets"]}
    wb = load_workbook(path, data_only=False)
    names = wb.sheetnames
    if rt["template_sheet"] not in names or rt["end_sheet"] not in names:
        return []
    first, last = names.index(rt["template_sheet"]), names.index(rt["end_sheet"])
    rocks = []
    for name in names[first + 1:last]:
        ws = wb[name]
        rock = {"RockTab": name}
        for sec in rt["sections"]:
            if sec["kind"] == "fields":
                for f in sec["fields"]:
                    v = ws[f"{rt['value_column']}{f['row']}"].value
                    if not f.get("formula") and v is not None:
                        rock[f["name"]] = v
            else:
                cols = sheets[sec["block"]]["columns"]
                rows = []
                for r in range(sec["first_row"], sec["first_row"] + sec["capacity"]):
                    row = {}
                    for i, c in enumerate(cols, start=1):
                        v = ws.cell(row=r, column=i).value
                        if not c.get("formula") and v is not None:
                            row[c["name"]] = v
                    rows.append(row)
                while rows and not rows[-1]:
                    rows.pop()
                rock[sec["block"]] = rows
        rocks.append(rock)
    return rocks


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------
def solid(color):
    return PatternFill("solid", start_color=color, end_color=color)


def pink():
    return solid(ACCENT_TINT)


THIN = Side(style="thin", color=RULE)
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def value_validation(c, first_cell="A1"):
    """DataValidation for an entry cell or column, or None. `first_cell` is the top left cell of the
    range it will be added to (custom formulas are relative to it)."""
    ref = c.get("lookup")
    if ref:
        dv = DataValidation(type="list", formula1=list_name(ref), allow_blank=True)
        dv.error, dv.errorTitle = f"Pick a value from the list ({ref})", "Not in the list"
        if c.get("validation") == "warning":
            dv.errorStyle = "warning"
            dv.error = "This date is not in lkp_Steercos yet. Keep it, or ask the workbook owner to add the steerco date."
            dv.errorTitle = "Not a listed steerco date"
    elif c["type"] == "date":
        dv = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True)
        dv.error, dv.errorTitle = "Enter a date, for example 16 Oct 2026", "Not a date"
    elif c.get("format") == "url":
        dv = DataValidation(type="custom", formula1=f'OR({first_cell}="",LEFT({first_cell},8)="https://")', allow_blank=True)
        dv.error, dv.errorTitle = "Enter a link that starts with https://", "Not a secure link"
    elif c["type"] == "integer":
        dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
        dv.error, dv.errorTitle = "Enter a whole number, 0 or more", "Not a number"
    else:
        return None
    dv.showErrorMessage = True
    return dv


def build_rock_tab(wb, name, schema, R, rock=None):
    """One rock tab. rock=None builds the empty template (Active = Yes)."""
    rt = schema["rock_tab"]
    sheets = R.sheets
    ws = wb.create_sheet(name)
    vcol, lcol = rt["value_column"], rt["label_column"]
    max_cols = max(len(sheets[b]["columns"]) for b in R.blocks)
    sections = rt["sections"]
    ws.sheet_view.showGridLines = False

    # title, strip, guide
    ws[f"{lcol}1"] = file_formula(R.resolve(rt["title_formula"]))
    ws[f"{lcol}1"].font = Font(bold=True, size=16, color=INK)
    rocks_sheet = sheets["Rocks"]
    for i, col in enumerate(rocks_sheet["columns"], start=1):
        if col.get("excel"):
            f = col["excel"]
        else:
            f = rocks_sheet["strip_default_excel"].replace("{FROM}", "{%s}" % col["from"])
        cell = ws.cell(row=rt["strip_row"], column=i, value=file_formula(R.resolve(f)))
        if number_format(col):
            cell.number_format = number_format(col)
    ws.row_dimensions[rt["strip_row"]].hidden = bool(rt.get("strip_hidden"))
    ws[rt["guide_cell"]] = rt["guide_text"]
    ws[rt["guide_cell"]].font = Font(italic=True, color=SLATE)

    unlocked = Protection(locked=False)
    cf_rules = []  # (range, formula)

    def style_calc(cell):
        cell.fill = solid(CALC_GREY)

    def style_entry(cell, col):
        cell.fill = PatternFill(fill_type=None)
        cell.border = BOX
        cell.protection = unlocked
        cell.alignment = Alignment(horizontal="left")
        if number_format(col):
            cell.number_format = number_format(col)

    def put(cell, col, value):
        if value not in (None, ""):
            cell.value = coerce(value, col["type"])

    for sec in sections:
        for cidx in range(1, max_cols + 1):
            ws.cell(row=sec["header_row"], column=cidx).fill = solid(INK)
        t = ws[f"{lcol}{sec['header_row']}"]
        t.value, t.font = sec["title"], Font(bold=True, color="FFFFFF")
        if sec["kind"] == "fields":
            for f in sec["fields"]:
                lab = ws[f"{lcol}{f['row']}"]
                lab.value = f["label"]
                cell = ws[f"{vcol}{f['row']}"]
                if f.get("formula"):
                    cell.value = file_formula(R.resolve(f["excel"]))
                    style_calc(cell)
                    cell.alignment = Alignment(horizontal="left")
                    if number_format(f):
                        cell.number_format = number_format(f)
                    continue
                style_entry(cell, f)
                value = rock.get(f["name"]) if rock is not None else f.get("template_value")
                put(cell, f, value)
                dv = value_validation(f, first_cell=cell.coordinate)
                if dv:
                    ws.add_data_validation(dv)
                    dv.add(cell.coordinate)
                if f.get("required"):
                    cf_rules.append((cell.coordinate, f'{cell.coordinate.replace(vcol, "$" + vcol)}=""'))
                if f.get("highlight_when"):
                    cf_rules.append((cell.coordinate, R.resolve(f["highlight_when"])))
        else:
            sheet = sheets[sec["block"]]
            cols = sheet["columns"]
            for i, c in enumerate(cols, start=1):
                h = ws.cell(row=sec["column_header_row"], column=i, value=c.get("label") or c["name"])
                h.font = Font(bold=True, color=SLATE)
                h.border = Border(bottom=Side(style="thin", color=INK))
                h.alignment = Alignment(wrap_text=True, vertical="bottom")
            last_row = sec["first_row"] + sec["capacity"] - 1
            slots = (rock or {}).get(sec["block"]) or []
            typed = [(i, c) for i, c in enumerate(cols, start=1) if not c.get("formula")]
            assert [i for i, _ in typed] == list(range(typed[0][0], typed[-1][0] + 1)), "typed columns must be contiguous"
            title_idx = typed[0][0]
            tl = get_column_letter(title_idx)
            for slot in range(1, sec["capacity"] + 1):
                r = sec["first_row"] + slot - 1
                data = slots[slot - 1] if slot <= len(slots) and slots[slot - 1] else {}
                for i, c in enumerate(cols, start=1):
                    cell = ws.cell(row=r, column=i)
                    if c.get("formula"):
                        cell.value = file_formula(R.resolve(c["excel"], block=sec["block"], row=r, slot=slot))
                        style_calc(cell)
                        if number_format(c):
                            cell.number_format = number_format(c)
                    else:
                        style_entry(cell, c)
                        put(cell, c, data.get(c["name"]))
            first = sec["first_row"]
            # validations: one per entry column
            for i, c in typed:
                dv = value_validation(c, first_cell=f"{get_column_letter(i)}{first}")
                if dv:
                    ws.add_data_validation(dv)
                    dv.add(f"{get_column_letter(i)}{first}:{get_column_letter(i)}{last_row}")
            # pink: required entry cell empty on a row that has a title, and conditional requirement
            for i, c in typed[1:]:
                letter = get_column_letter(i)
                rng = f"{letter}{first}:{letter}{last_row}"
                if c.get("required"):
                    cf_rules.append((rng, f'AND(${tl}{first}<>"",{letter}{first}="")'))
                elif c.get("required_when"):
                    m = re.fullmatch(r"(\w+) is (.+)", c["required_when"])
                    other = col_letter(sheet, m.group(1))
                    cf_rules.append((rng, f'AND(${tl}{first}<>"",${other}{first}="{m.group(2)}",{letter}{first}="")'))
            # pink row: data but no title (invisible to the portal)
            a, z = get_column_letter(typed[1][0]), get_column_letter(typed[-1][0])
            cf_rules.append((f"A{first}:{get_column_letter(len(cols))}{last_row}",
                             f'AND(${tl}{first}="",COUNTA(${a}{first}:${z}{first})>0)'))

    for rng, formula in cf_rules:
        ws.conditional_formatting.add(rng, FormulaRule(formula=[spill_refs(formula)], fill=pink()))

    # layout: A key, B labels and titles, C values, D onward block columns
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions[lcol].width = 46
    ws.column_dimensions[vcol].width = 24
    for i in range(4, max_cols + 1):
        ws.column_dimensions[get_column_letter(i)].width = 17
    ws.freeze_panes = "A4"
    ws.protection.sheet = True  # no password: a guard rail (rock_tab.protect); defaults forbid inserts and deletes
    return ws


def build_end_sheet(wb, rt):
    ws = wb.create_sheet(rt["end_sheet"])
    ws["A1"] = rt["end_sheet_note"]
    ws["A1"].font = Font(italic=True, color=SLATE)
    ws.protection.sheet = True
    return ws


def build_consolidated(wb, schema, sheet, R):
    ws = wb.create_sheet(sheet["name"])
    cols = sheet["columns"]
    header_font, header_fill = Font(bold=True, color="FFFFFF"), solid(INK)
    ws.append([c["name"] for c in cols])
    for i, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=i)
        cell.font, cell.fill = header_font, header_fill
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(40, len(c["name"]) + 6))
        if number_format(c):
            for r in range(2, sheet.get("max_rows", MAX_ROWS) + 1):
                ws.cell(row=r, column=i).number_format = number_format(c)
    anchor = schema["rock_tab"]["consolidation_formula"]["anchor"]
    set_dynamic_formula(ws, anchor, consolidation_formula(schema, sheet, R), CONSOLIDATION_NAMES)
    ws.freeze_panes = "A2"
    ws.protection.sheet = True
    return ws


def build_table_sheet(wb, schema, sheet, rows, deploy_kind):
    """History and lookup sheets: one Excel Table tbl_<sheet>."""
    ws = wb.create_sheet(sheet["name"])
    cols = sheet["columns"]
    header_font, header_fill = Font(bold=True, color="FFFFFF"), solid(INK)
    ws.append([c["name"] for c in cols])
    for row in rows:
        if isinstance(row, dict):
            row = [row.get(c["name"]) for c in cols]
        ws.append([coerce(v, c["type"]) for v, c in zip(row, cols)])
    last_row = max(ws.max_row, 2)
    last_col = get_column_letter(len(cols))
    table = Table(displayName=f"tbl_{sheet['name']}", ref=f"A1:{last_col}{last_row}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
    ws.add_table(table)
    ws.freeze_panes = "A2"
    max_rows = MAX_ROWS if sheet["kind"] == "history" else LOOKUP_ROWS
    pk = col_letter(sheet, sheet["primary_key"])
    for i, c in enumerate(cols, start=1):
        letter = get_column_letter(i)
        ws.column_dimensions[letter].width = max(12, min(40, len(c["name"]) + 6))
        cell = ws.cell(row=1, column=i)
        cell.font, cell.fill = header_font, header_fill
        cell.alignment = Alignment(vertical="center")
        if c["type"] == "date":
            for r in range(2, max_rows + 1):
                ws.cell(row=r, column=i).number_format = DATE_FORMAT
    if sheet["kind"] == "history":
        # Same options as scripts/office/snapshot.ts: protect() with allowAutoFilter and allowSort.
        ws.protection.sheet = True
        ws.protection.autoFilter = False
        ws.protection.sort = False
        return ws
    for i, c in enumerate(cols, start=1):
        letter = get_column_letter(i)
        rng = f"{letter}2:{letter}{max_rows}"
        if c["type"] == "date":
            dv = value_validation(c)
            ws.add_data_validation(dv)
            dv.add(rng)
        if c.get("required") and c["name"] != sheet["primary_key"]:
            ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND(${pk}2<>"",{letter}2="")'], fill=pink()))
    return ws


def check_formula(schema, excel):
    """An about.checks formula: <Sheet.Column> becomes INDEX(Sheet!$A$2#,,n), then file format."""
    sheets = {s["name"]: s for s in schema["sheets"]}
    anchor = schema["rock_tab"]["consolidation_formula"]["anchor"]
    anchor = "$" + re.sub(r"(\d+)", r"$\1", anchor)

    def ref(m):
        names = [c["name"] for c in sheets[m.group(1)]["columns"]]
        return f"INDEX({m.group(1)}!{anchor}#,,{names.index(m.group(2)) + 1})"

    return to_file_formula(spill_refs(re.sub(r"<(\w+)\.(\w+)>", ref, excel)))


def build_about(wb, schema):
    about = wb.create_sheet("About")
    header_font, header_fill = Font(bold=True, color="FFFFFF"), solid(INK)
    about["A1"] = schema.get("title", "Workbook")
    about["A1"].font = Font(bold=True, size=16, color=INK)
    about["A2"] = f"Version {schema.get('version', '0')} · built {dt.date.today():%d %b %Y}"
    about["A2"].font = Font(color=SUBTLE)
    about.append([])
    about.append(["Sheet", "Purpose", "Owner", "Rows"])
    for c in about[4]:
        c.font, c.fill = header_font, header_fill
    rt = schema["rock_tab"]
    about.append([rt["template_sheet"], "Copy this tab to add a rock (see Add a rock)", "workbook owner", ""])
    about.append([rt["end_sheet"], rt["end_sheet_note"], "no one", ""])
    for s in schema["sheets"]:
        pk = col_letter(s, s["primary_key"])
        about.append([s["name"], s.get("purpose", ""), s.get("owner", ""), f"=COUNTA('{s['name']}'!{pk}:{pk})-1"])
    spec = schema.get("about", {})
    widths = {"A": 34, "B": 60, "C": 28, "D": 40}
    wrap = Alignment(wrap_text=True, vertical="top")
    total = sum(widths.values())

    def section(title):
        about.append([])
        about.append([title])
        about.cell(row=about.max_row, column=1).font = Font(bold=True, size=13, color=INK)

    def header(*names):
        about.append(list(names))
        for c in about[about.max_row]:
            if c.value is not None:
                c.font, c.fill = header_font, header_fill

    def text_row(line):
        about.append([line])
        r = about.max_row
        about.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        about.cell(row=r, column=1).alignment = wrap
        about.row_dimensions[r].height = 15 * (len(line) // total + 1)

    def lines(title, items):
        section(title)
        for line in items:
            text_row(line)

    section("Checks")
    header("Check", "OK when", "Result")
    for chk in spec.get("checks", []):
        about.append([chk["label"], chk["ok_when"], check_formula(schema, chk["excel"])])
        r = about.max_row
        for col in (1, 2, 3):
            about.cell(row=r, column=col).alignment = wrap
        about.row_dimensions[r].height = 15 * (max(len(chk["label"]) // widths["A"], len(chk["ok_when"]) // widths["B"]) + 1)
    lines("Update guide", spec.get("update_guide", []))
    lines("Add a rock", spec.get("add_rock", []))
    lines("Close a rock", spec.get("close_rock", []))
    lines("Rules", spec.get("rules", []))
    section("Definitions")
    header("Term", "Meaning", "Group", "What ends it")
    for d in spec.get("definitions", []):
        about.append([d["term"], d["meaning"], d["group"], d.get("exit", "")])
        r = about.max_row
        for col in (1, 2, 3, 4):
            about.cell(row=r, column=col).alignment = wrap
        about.row_dimensions[r].height = 15 * (max(len(d["meaning"]) // widths["B"], len(d.get("exit", "")) // widths["D"]) + 1)
    for letter, w in widths.items():
        about.column_dimensions[letter].width = w
    return about


def add_names(wb, schema):
    """Params and lookup lists as defined names."""
    for p in schema["params"]:
        wb.defined_names[p["name"]] = DefinedName(p["name"], attr_text=file_formula(p["formula"]))
    sheets = {s["name"]: s for s in schema["sheets"]}
    refs = set()
    for s in schema["sheets"]:
        refs |= {c["lookup"] for c in s["columns"] if c.get("lookup")}
    for sec in schema["rock_tab"]["sections"]:
        for f in sec.get("fields", []):
            if f.get("lookup"):
                refs.add(f["lookup"])
    for ref in sorted(refs):
        sheet, column = ref.split(".", 1)
        if sheets[sheet]["kind"] != "lookup":
            continue
        letter = col_letter(sheets[sheet], column)
        name = list_name(ref)
        wb.defined_names[name] = DefinedName(name, attr_text=f"'{sheet}'!${letter}$2:${letter}${LOOKUP_ROWS}")


def build(schema, data, deploy):
    """data: {"rocks": [rock dicts with RockTab], "rows": {sheet name: rows for lookup and history sheets}}."""
    wb = Workbook()
    wb.remove(wb.active)
    R = Resolver(schema)
    rt = schema["rock_tab"]
    build_about(wb, schema)  # sample and deployment workbooks both start with About
    build_rock_tab(wb, rt["template_sheet"], schema, R)
    for rock in data.get("rocks", []):
        build_rock_tab(wb, rock["RockTab"], schema, R, rock)
    build_end_sheet(wb, rt)
    for sheet in schema["sheets"]:
        if sheet["kind"] == "consolidated":
            build_consolidated(wb, schema, sheet, R)
        else:
            build_table_sheet(wb, schema, sheet, data.get("rows", {}).get(sheet["name"], []), deploy)
    add_names(wb, schema)
    wb.calculation.fullCalcOnLoad = True  # no cached values: Excel calculates on open
    return wb


# ---------------------------------------------------------------------------
# Dynamic array helper (T05). Self contained: used by scripts/build_spike.py and,
# later, by the rock tab generator. openpyxl cannot mark a formula as a dynamic
# array, so we write it as an array formula and patch cell metadata in the xlsx.
# ---------------------------------------------------------------------------
XLFN_FUNCTIONS = {
    "LET": "_xlfn.LET", "VSTACK": "_xlfn.VSTACK", "HSTACK": "_xlfn.HSTACK",
    "CHOOSECOLS": "_xlfn.CHOOSECOLS", "TOCOL": "_xlfn.TOCOL", "REDUCE": "_xlfn.REDUCE",
    "LAMBDA": "_xlfn.LAMBDA", "SEQUENCE": "_xlfn.SEQUENCE", "FILTER": "_xlfn._xlws.FILTER",
    "SORT": "_xlfn._xlws.SORT", "MINIFS": "_xlfn.MINIFS", "UNIQUE": "_xlfn.UNIQUE", "XLOOKUP": "_xlfn.XLOOKUP",
}

_METADATA_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<metadata xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:xda="http://schemas.microsoft.com/office/spreadsheetml/2017/dynamicarray">'
    '<metadataTypes count="1"><metadataType name="XLDAPR" minSupportedVersion="120000" copy="1" '
    'pasteAll="1" pasteValues="1" merge="1" splitFirst="1" rowColShift="1" clearFormats="1" '
    'clearComments="1" assign="1" coerce="1" cellMeta="1"/></metadataTypes>'
    '<futureMetadata name="XLDAPR" count="1"><bk><extLst><ext uri="{bdbb8cdc-fa1e-496e-a857-3c3f30c029c3}">'
    '<xda:dynamicArrayProperties fDynamic="1" fCollapsed="0"/></ext></extLst></bk></futureMetadata>'
    '<cellMetadata count="1"><bk><rc t="1" v="0"/></bk></cellMetadata></metadata>'
)


def to_file_formula(formula, names=()):
    """Convert a formula as typed in Excel to the file format: _xlfn. prefixes on newer
    functions and _xlpm. on LET and LAMBDA variable names. String literals are untouched.
    `names` lists the LET and LAMBDA variable names used in the formula."""
    names = set(names)
    parts = re.split(r'("(?:[^"]|"")*")', formula)
    for i in range(0, len(parts), 2):  # even parts are outside string literals
        def sub(m):
            word, nxt = m.group(1), m.group(2)
            if nxt == "(" and word in XLFN_FUNCTIONS:
                return XLFN_FUNCTIONS[word] + nxt
            if nxt != "(" and word in names:
                return "_xlpm." + word + nxt
            return m.group(0)
        parts[i] = re.sub(r"(?<![\w.!:$'])([A-Za-z_][A-Za-z0-9_]*)(\(?)", sub, parts[i])
    return "".join(parts)


def set_dynamic_formula(ws, cell, formula, names=()):
    """Write a dynamic array formula (spills from `cell`). Call mark_dynamic_arrays on the
    saved file afterwards, passing the (sheet name, cell) pairs written here."""
    from openpyxl.worksheet.formula import ArrayFormula
    if not formula.startswith("="):
        formula = "=" + formula
    ws[cell] = ArrayFormula(cell, to_file_formula(formula, names))


def mark_dynamic_arrays(path, cells):
    """Patch a saved xlsx so the listed (sheet name, cell) pairs are dynamic arrays: adds
    cm="1" on the cell, xl/metadata.xml, its content type and workbook relationship."""
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
    wbxml = files["xl/workbook.xml"].decode()
    rels = files["xl/_rels/workbook.xml.rels"].decode()
    rid_target = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship\b[^>]*?\bId="([^"]+)"[^>]*?\bTarget="([^"]+)"', rels)}
    rid_target.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship\b[^>]*?\bTarget="([^"]+)"[^>]*?\bId="([^"]+)"', rels)})
    sheet_file = {}
    for m in re.finditer(r"<sheet\b[^>]*>", wbxml):
        tag = m.group(0)
        name = re.search(r'\bname="([^"]*)"', tag).group(1)
        rid = re.search(r'\br:id="([^"]*)"', tag).group(1)
        target = rid_target[rid].lstrip("/")
        sheet_file[name.replace("&amp;", "&")] = target if target.startswith("xl/") else "xl/" + target
    for sheet, cell in cells:
        fn = sheet_file[sheet]
        xml = files[fn].decode()
        new, n = re.subn(r'<c r="%s"(?![^>]*\bcm=)' % re.escape(cell), '<c r="%s" cm="1"' % cell, xml, count=1)
        if n != 1:
            raise ValueError(f"cell {sheet}!{cell} not found in {fn}")
        files[fn] = new.encode()
    files["xl/metadata.xml"] = _METADATA_XML.encode()
    ct = files["[Content_Types].xml"].decode()
    if "sheetMetadata" not in ct:
        ct = ct.replace("</Types>", '<Override PartName="/xl/metadata.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheetMetadata+xml"/></Types>')
    files["[Content_Types].xml"] = ct.encode()
    if "sheetMetadata" not in rels:
        rels = rels.replace("</Relationships>", '<Relationship Id="rIdMeta1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sheetMetadata" Target="metadata.xml"/></Relationships>')
    files["xl/_rels/workbook.xml.rels"] = rels.encode()
    tmp = Path(tempfile.mkdtemp()) / "patched.xlsx"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in files.items():
            z.writestr(n, b)
    shutil.move(str(tmp), path)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--deploy", action="store_true", help="build the deployment workbook")
    ap.add_argument("--from", dest="source", help="migrate rows from this existing workbook")
    ap.add_argument("--out", help="output path (default from schema)")
    args = ap.parse_args(argv)
    schema = load_schema()
    table_sheets = [s for s in schema["sheets"] if s["kind"] != "consolidated"]

    if args.source:
        existing = read_existing(args.source)
        rows, dropped = {}, []
        for s in table_sheets:
            old = existing.get(s["name"], [])
            names = {c["name"] for c in s["columns"]}
            dropped += [f"{s['name']}.{h}" for h in (old[0].keys() if old else []) if h not in names]
            rows[s["name"]] = old or [list(r) for r in s.get("seed", [])]
        data = {"rocks": read_rock_tabs(args.source, schema), "rows": rows}
        if dropped:
            print("WARNING: columns in the source that the schema no longer has (data not copied):")
            print("\n".join(f"  {d}" for d in dropped))
    elif args.deploy:
        data = {"rocks": [], "rows": {s["name"]: [list(r) for r in s.get("seed", [])] for s in table_sheets}}
    else:
        sample = json.loads((ROOT / "data" / "sample.json").read_text())
        rows = {}
        for s in table_sheets:
            if s["kind"] == "lookup":
                rows[s["name"]] = [list(r) for r in s.get("seed", [])] + sample["lookups"].get(s["name"], [])
            else:
                rows[s["name"]] = sample["snapshots"].get(s["name"], [])
        data = {"rocks": sample["rocks"], "rows": rows}

    out = Path(args.out) if args.out else ROOT / (schema["deploy_file"] if args.deploy else schema["workbook"])
    out.parent.mkdir(parents=True, exist_ok=True)
    build(schema, data, deploy=args.deploy).save(out)
    mark_dynamic_arrays(out, dynamic_cells(schema))
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


if __name__ == "__main__":
    sys.exit(main())
