"""Layer 1: the schema is valid and internally consistent."""
import re

from conftest import split_ref

TYPES = {"string", "number", "integer", "date", "boolean"}
KINDS = {"consolidated", "history", "lookup"}


def test_sheet_names_unique(schema):
    names = [s["name"] for s in schema["sheets"]]
    assert len(names) == len(set(names))


def test_columns_well_formed(schema):
    for sheet in schema["sheets"]:
        names = [c["name"] for c in sheet["columns"]]
        assert len(names) == len(set(names)), f"duplicate column in {sheet['name']}"
        assert sheet["primary_key"] in names, f"{sheet['name']} primary key missing"
        for col in sheet["columns"]:
            assert col["type"] in TYPES, f"{sheet['name']}.{col['name']} bad type"


def test_every_sheet_has_owner_and_purpose(schema):
    for sheet in schema["sheets"]:
        assert sheet.get("owner"), f"{sheet['name']} has no owner"
        assert sheet.get("purpose"), f"{sheet['name']} has no purpose"


def test_references_and_lookups_resolve(sheets):
    for sheet in sheets.values():
        for col in sheet["columns"]:
            for key in ("references", "lookup"):
                if key in col:
                    target, target_col = split_ref(col[key])
                    assert target in sheets, f"{sheet['name']}.{col['name']} points to missing {target}"
                    names = [c["name"] for c in sheets[target]["columns"]]
                    assert target_col in names, f"{col[key]} does not exist"


def test_every_sheet_has_a_known_kind(schema):
    for sheet in schema["sheets"]:
        assert sheet.get("kind") in KINDS, f"{sheet['name']} kind {sheet.get('kind')}"


def test_rock_tab_fields_and_blocks_do_not_overlap(schema):
    rt = schema["rock_tab"]
    used = {}
    for sec in rt["sections"]:
        rows = [sec["header_row"]]
        if sec["kind"] == "fields":
            rows += [f["row"] for f in sec["fields"]]
        else:
            rows += [sec["column_header_row"]] + list(range(sec["first_row"], sec["first_row"] + sec["capacity"]))
        for r in rows:
            assert r not in used, f"row {r} used by section {sec['id']} and {used[r]}"
            assert r > rt["strip_row"], f"row {r} collides with the strip"
            used[r] = sec["id"]


def test_blocks_match_consolidated_sheets(schema, sheets):
    blocks = [s["block"] for s in schema["rock_tab"]["sections"] if s["kind"] == "block"]
    from_blocks = [n for n, s in sheets.items() if s["kind"] == "consolidated" and s.get("source") == "block"]
    assert sorted(blocks) == sorted(from_blocks)
    for name in blocks:
        typed = [i for i, c in enumerate(sheets[name]["columns"]) if not c.get("formula")]
        assert typed == list(range(typed[0], typed[-1] + 1)), f"{name} typed columns must be contiguous"
        assert typed[0] == 1, f"{name}: column 1 is the key, column 2 the title"
        assert sheets[name]["columns"][0].get("formula"), f"{name} key must be calculated"


def test_strip_columns_map_to_fields(schema, sheets):
    fields = {f["name"]: f for s in schema["rock_tab"]["sections"] if s["kind"] == "fields" for f in s["fields"]}
    for col in sheets["Rocks"]["columns"]:
        if col.get("excel"):
            continue
        assert col.get("from") in fields, f"Rocks.{col['name']} has no from field"
    assert "{FROM}" in sheets["Rocks"]["strip_default_excel"]


def test_placeholders_resolve(schema):
    from build_workbook import Resolver
    R = Resolver(schema)
    sheets = {s["name"]: s for s in schema["sheets"]}
    formulas = [f["excel"] for s in schema["rock_tab"]["sections"] for f in s.get("fields", []) if f.get("excel")]
    formulas += [f["highlight_when"] for s in schema["rock_tab"]["sections"] for f in s.get("fields", []) if f.get("highlight_when")]
    formulas.append(schema["rock_tab"]["title_formula"])
    for name, sheet in sheets.items():
        for c in sheet["columns"]:
            if c.get("excel"):
                block = name if sheet.get("source") == "block" else None
                formulas.append((c["excel"], block))
    for item in formulas:
        f, block = item if isinstance(item, tuple) else (item, None)
        if block is None and "[" in f:
            continue  # strip formulas of Rocks use {} only
        out = R.resolve(f, block=block, row=25, slot=1)
        assert not re.search(r"[{}\[\]]", out), f"unresolved placeholder in {f}"


def test_params_and_lists_are_defined_names_in_formulas(schema):
    names = {p["name"] for p in schema["params"]}
    assert {"HighRiskMin", "StaleDays", "MCQuarterStart", "MCQuarterEnd", "OutlookEnd", "CurrentMCQuarter", "NextMCQuarter", "NextSteerco"} <= names
    for s in schema["rock_tab"]["sections"]:
        for f in s.get("fields", []):
            for m in re.findall(r"lst_lkp_\w+", f.get("excel", "")):
                sheet, col = re.match(r"lst_(lkp_\w+?)_(\w+)$", m).groups()
                assert col in {c["name"] for c in next(x for x in schema["sheets"] if x["name"] == sheet)["columns"]}
