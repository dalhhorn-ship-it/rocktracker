"""Layer 1: the schema is valid and internally consistent."""
from conftest import split_ref

TYPES = {"string", "number", "integer", "date", "boolean"}


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
