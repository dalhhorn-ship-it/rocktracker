"""T10: snapshot Office Script and its Python mirror."""
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot  # noqa: E402

SCHEMA = json.loads((ROOT / "schema" / "workbook.schema.json").read_text())
TS = (ROOT / "scripts" / "office" / "snapshot.ts").read_text()
SHEETS = {s["name"]: [c["name"] for c in s["columns"]] for s in SCHEMA["sheets"]}


def const_strings(name):
    m = re.search(r"const %s = \[(.*?)\];" % name, TS, re.S)
    assert m, name
    return re.findall(r'"([^"]+)"', m.group(1))


def const_value(name):
    m = re.search(r'const %s = "([^"]+)";' % name, TS)
    assert m, name
    return m.group(1)


def test_sheet_and_table_names_exist_in_schema():
    for c in ("ROCKS_SHEET", "MILESTONES_SHEET", "ROCK_SNAP_SHEET", "MILESTONE_SNAP_SHEET"):
        assert const_value(c) in SHEETS, c
    assert const_value("ROCK_SNAP_TABLE") == "tbl_" + const_value("ROCK_SNAP_SHEET")
    assert const_value("MILESTONE_SNAP_TABLE") == "tbl_" + const_value("MILESTONE_SNAP_SHEET")


def test_columns_exist_in_schema():
    rocks, milestones = SHEETS["Rocks"], SHEETS["Milestones"]
    rs, es = SHEETS["RockSnapshots"], SHEETS["MilestoneSnapshots"]
    rock_copy = const_strings("ROCK_COPY_COLUMNS")
    milestone_copy = const_strings("MILESTONE_COPY_COLUMNS")
    src = const_value("ROCK_NAME_SOURCE")
    assert const_value("ACTIVE_COLUMN") in rocks and src in rocks
    for c in rock_copy:
        assert c in rs
        assert (src if c == "Rock" else c) in rocks
    for c in milestone_copy:
        assert c in es and c in milestones
    assert const_value("ID_COLUMN") in rs and const_value("DATE_COLUMN") in es


def test_script_column_order_matches_snapshot_tables():
    """Rows are written positionally, so the order must equal the table columns."""
    assert ["SnapshotID", "SnapshotDate"] + const_strings("ROCK_COPY_COLUMNS") == SHEETS["RockSnapshots"]
    assert ["SnapshotID", "SnapshotDate"] + const_strings("MILESTONE_COPY_COLUMNS") == SHEETS["MilestoneSnapshots"]
    assert snapshot.ROCK_COPY == const_strings("ROCK_COPY_COLUMNS")
    assert snapshot.MILESTONE_COPY == const_strings("MILESTONE_COPY_COLUMNS")


def test_script_unprotects_and_reprotects():
    assert "unprotect(" in TS and ".protect(" in TS and "finally" in TS


@pytest.mark.skipif(not shutil.which("tsc"), reason="tsc not installed")
def test_typescript_compiles():
    r = subprocess.run(["tsc", "-p", str(ROOT / "scripts" / "office" / "tsconfig.json")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


ROCKS = [
    {"RockID": "R01", "RockName": "Alpha", "GPM": "G1", "Active": "Yes", "State": "On track",
     "UpdateDate": 46300, "MainMessage": "ok", "MilestonesCommitted": 2, "MilestonesSlipped": 0,
     "MilestonesCompleted": 1, "PositionsBudgeted": 3, "PositionsActual": 2, "OpenHighRisks": 0},
    {"RockID": "R02", "RockName": "Beta", "GPM": "G1", "Active": "No", "State": "Done"},
    {"RockID": "", "Active": ""},
]
MILESTONES = [
    {"MilestoneKey": "R01-M01", "RockID": "R01", "Title": "A", "Status": "On plan"},
    {"MilestoneKey": "R01-M02", "RockID": "R01", "Title": "B", "Status": "Completed"},
    {"MilestoneKey": "R02-M01", "RockID": "R02", "Title": "C", "Status": "On plan"},
    {"MilestoneKey": "", "RockID": ""},
]
DAY = date(2026, 10, 19)


def test_mirror_keeps_only_active_rocks_and_their_milestones():
    r, e = snapshot.snapshot_rows(ROCKS, MILESTONES, DAY)
    assert [x["SnapshotID"] for x in r] == ["2026-10-19|R01"]
    assert [x["SnapshotID"] for x in e] == ["2026-10-19|R01-M01", "2026-10-19|R01-M02"]
    assert r[0]["Rock"] == "Alpha"
    assert list(r[0]) == SHEETS["RockSnapshots"]
    assert list(e[0]) == SHEETS["MilestoneSnapshots"]


def test_mirror_is_idempotent():
    r1, e1 = snapshot.snapshot_rows(ROCKS, MILESTONES, DAY)
    r2, e2 = snapshot.snapshot_rows(ROCKS, MILESTONES, DAY,
                                    [x["SnapshotID"] for x in r1], [x["SnapshotID"] for x in e1])
    assert r2 == [] and e2 == []
    # a later week adds rows again
    r3, _ = snapshot.snapshot_rows(ROCKS, MILESTONES, date(2026, 10, 26), [x["SnapshotID"] for x in r1])
    assert len(r3) == 1


def test_snapshot_ids_unique_within_run():
    r, e = snapshot.snapshot_rows(ROCKS + ROCKS, MILESTONES + MILESTONES, DAY)
    assert len(r) == 1 and len(e) == 2
