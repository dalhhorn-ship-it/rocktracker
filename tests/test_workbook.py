"""Layer 2: the sample workbook matches the schema.

Rock tabs hold the typed cells; the five consolidated sheets hold one formula each. Nothing
outside Excel calculates those formulas, so data level checks run on the rows the Python mirror
derives from the rock tabs of the workbook (see the `rows` fixture in conftest.py)."""
import datetime as dt

from conftest import split_ref

CHECKS = {
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "date": lambda v: isinstance(v, (dt.date, dt.datetime)),
    "boolean": lambda v: isinstance(v, bool),
}
# The sample's deliberately half filled rock (data/sample.json _note): required typed cells may be empty here.
HALF_FILLED = "R04"


def kind(schema, k):
    return [s for s in schema["sheets"] if s["kind"] == k]


def rock_tab_names(workbook, schema):
    rt = schema["rock_tab"]
    names = workbook.sheetnames
    return names[names.index(rt["template_sheet"]) + 1:names.index(rt["end_sheet"])]


def test_sheets_exist_in_order(workbook, schema):
    rt = schema["rock_tab"]
    missing = [s["name"] for s in schema["sheets"] if s["name"] not in workbook.sheetnames]
    assert not missing, f"missing sheets: {missing}"
    names = workbook.sheetnames
    assert names[0] == rt["template_sheet"]
    assert rock_tab_names(workbook, schema), "the sample needs rock tabs between the bookends"
    after = names[names.index(rt["end_sheet"]) + 1:]
    assert after == [s["name"] for s in schema["sheets"]], f"sheet order after {rt['end_sheet']}: {after}"


def test_headers_match(workbook, schema):
    for sheet in schema["sheets"]:
        header = [c.value for c in workbook[sheet["name"]][1]]
        expected = [c["name"] for c in sheet["columns"]]
        assert header == expected, f"{sheet['name']} headers {header} != {expected}"


def test_rock_tab_block_headers_match(workbook, schema):
    sheets = {s["name"]: s for s in schema["sheets"]}
    for tab in [schema["rock_tab"]["template_sheet"]] + rock_tab_names(workbook, schema):
        ws = workbook[tab]
        for sec in schema["rock_tab"]["sections"]:
            if sec["kind"] != "block":
                continue
            header = [c.value for c in ws[sec["column_header_row"]]][:len(sheets[sec["block"]]["columns"])]
            assert header == [c.get("label") or c["name"] for c in sheets[sec["block"]]["columns"]], (tab, sec["block"])


def test_tables_only_on_history_and_lookup(workbook, schema):
    for sheet in schema["sheets"]:
        tables = workbook[sheet["name"]].tables
        if sheet["kind"] == "consolidated":
            assert not tables, f"{sheet['name']} must not be a Table (a dynamic array cannot spill in one)"
        else:
            assert f"tbl_{sheet['name']}" in tables, f"{sheet['name']} has no Excel Table"


def test_nothing_outside_tables_on_table_sheets(workbook, schema):
    for sheet in kind(schema, "history") + kind(schema, "lookup"):
        ws = workbook[sheet["name"]]
        ref = ws.tables[f"tbl_{sheet['name']}"].ref
        last_row = int("".join(ch for ch in ref.split(":")[1] if ch.isdigit()))
        for row in ws.iter_rows(min_row=last_row + 1, values_only=True):
            assert not any(v is not None for v in row), f"{sheet['name']} has data outside {ref}"


def test_required_and_types(rows, schema):
    errors = []
    for sheet in schema["sheets"]:
        for i, row in enumerate(rows[sheet["name"]], start=2):
            for col in sheet["columns"]:
                value = row.get(col["name"])
                if value in (None, ""):
                    if col.get("required") and (sheet["kind"] != "consolidated" or col.get("formula")):
                        errors.append(f"{sheet['name']}!row {i} {col['name']} is empty")
                    elif col.get("required") and row.get("RockID") != HALF_FILLED:
                        errors.append(f"{sheet['name']}!row {i} {col['name']} is empty outside the half filled rock")
                elif not CHECKS[col["type"]](value):
                    errors.append(f"{sheet['name']}!row {i} {col['name']}={value!r} not {col['type']}")
    assert not errors, "\n".join(errors)


def test_primary_keys_unique(rows, schema):
    for sheet in schema["sheets"]:
        keys = [r[sheet["primary_key"]] for r in rows[sheet["name"]]]
        dupes = {k for k in keys if keys.count(k) > 1}
        assert not dupes, f"{sheet['name']} duplicate keys {dupes}"


def test_references_and_lookups_valid(rows, schema):
    errors = []
    for sheet in schema["sheets"]:
        for col in sheet["columns"]:
            ref = col.get("references") or col.get("lookup")
            if not ref:
                continue
            target, target_col = split_ref(ref)
            allowed = {r[target_col] for r in rows[target]}
            if col.get("validation") == "warning":
                continue  # a dropdown with a warning: unlisted values are allowed on purpose
            for i, row in enumerate(rows[sheet["name"]], start=2):
                value = row.get(col["name"])
                if value not in (None, "") and value not in allowed:
                    errors.append(f"{sheet['name']}!row {i} {col['name']}={value!r} not in {ref}")
    assert not errors, "\n".join(errors)


def test_every_rock_in_the_sample_is_on_a_tab(workbook, schema, rows):
    import json
    from conftest import ROOT
    sample = json.loads((ROOT / "data" / "sample.json").read_text())["rocks"]
    assert rock_tab_names(workbook, schema) == [r["RockTab"] for r in sample]
    assert [r["RockID"] for r in rows["Rocks"]] == [r["RockID"] for r in sample]


def test_snapshot_history_rows_in_workbook(rows, schema):
    assert rows["RockSnapshots"] and rows["EpicSnapshots"]
