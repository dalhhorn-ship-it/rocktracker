import json
from pathlib import Path

import pytest
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "workbook.schema.json"


@pytest.fixture(scope="session")
def schema():
    return json.loads(SCHEMA_PATH.read_text())


@pytest.fixture(scope="session")
def sheets(schema):
    return {s["name"]: s for s in schema["sheets"]}


@pytest.fixture(scope="session")
def workbook(schema):
    path = ROOT / schema["workbook"]
    if not path.exists():
        pytest.skip(f"{schema['workbook']} not found; run scripts/build_workbook.py")
    return load_workbook(path, data_only=True)


@pytest.fixture(scope="session")
def rows(workbook, schema):
    """Sheet name to list of row dicts keyed by header."""
    out = {}
    for sheet in schema["sheets"]:
        if sheet["name"] not in workbook.sheetnames:
            continue
        values = list(workbook[sheet["name"]].iter_rows(values_only=True))
        headers = list(values[0]) if values else []
        out[sheet["name"]] = [
            dict(zip(headers, r)) for r in values[1:] if any(v is not None for v in r)
        ]
    return out


def split_ref(ref):
    sheet, column = ref.split(".", 1)
    return sheet, column
