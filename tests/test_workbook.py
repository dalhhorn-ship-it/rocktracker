"""Layer 2: the workbook matches the schema."""
import datetime as dt

from conftest import split_ref

CHECKS = {
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "date": lambda v: isinstance(v, (dt.date, dt.datetime)),
    "boolean": lambda v: isinstance(v, bool),
}


def test_sheets_exist(workbook, schema):
    missing = [s["name"] for s in schema["sheets"] if s["name"] not in workbook.sheetnames]
    assert not missing, f"missing sheets: {missing}"


def test_headers_match(workbook, schema):
    for sheet in schema["sheets"]:
        header = [c.value for c in workbook[sheet["name"]][1]]
        expected = [c["name"] for c in sheet["columns"]]
        assert header == expected, f"{sheet['name']} headers {header} != {expected}"


def test_data_is_in_a_table(workbook, schema):
    for sheet in schema["sheets"]:
        assert workbook[sheet["name"]].tables, f"{sheet['name']} has no Excel Table"


def test_required_and_types(rows, schema):
    errors = []
    for sheet in schema["sheets"]:
        for i, row in enumerate(rows[sheet["name"]], start=2):
            for col in sheet["columns"]:
                value = row.get(col["name"])
                if value in (None, ""):
                    if col.get("required") and not col.get("formula"):
                        errors.append(f"{sheet['name']}!row {i} {col['name']} is empty")
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
            for i, row in enumerate(rows[sheet["name"]], start=2):
                value = row.get(col["name"])
                if value not in (None, "") and value not in allowed:
                    errors.append(f"{sheet['name']}!row {i} {col['name']}={value!r} not in {ref}")
    assert not errors, "\n".join(errors)
