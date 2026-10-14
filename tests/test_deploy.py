"""Layer 5: the deployment workbook is ready for the shared drive, and migration keeps data."""
import sys

import pytest
from openpyxl import load_workbook

from conftest import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
import build_workbook  # noqa: E402


@pytest.fixture(scope="module")
def deploy_path(tmp_path_factory):
    out = tmp_path_factory.mktemp("deploy") / "deploy.xlsx"
    build_workbook.main(["--deploy", "--out", str(out)])
    return out


@pytest.fixture(scope="module")
def deploy_wb(deploy_path):
    return load_workbook(deploy_path)


def validations(ws):
    return {str(r): dv for dv in ws.data_validations.dataValidation for r in dv.sqref.ranges}


def kinds(schema, *wanted):
    return [s for s in schema["sheets"] if s["kind"] in wanted]


def test_about_sheet_first(deploy_wb, schema):
    assert deploy_wb.sheetnames[0] == "About"
    listed = {deploy_wb["About"].cell(row=r, column=1).value for r in range(1, 60)}
    assert {s["name"] for s in schema["sheets"]} <= listed
    assert {schema["rock_tab"]["template_sheet"], schema["rock_tab"]["end_sheet"]} <= listed


def test_sheet_order_and_no_rock_tabs(deploy_wb, schema):
    rt = schema["rock_tab"]
    names = deploy_wb.sheetnames
    assert names[1:3] == [rt["template_sheet"], rt["end_sheet"]], "deploy ships the template and no rock tabs"
    assert names[3:] == [s["name"] for s in schema["sheets"]]


def test_table_sheets_are_tables_with_frozen_header(deploy_wb, schema):
    for s in kinds(schema, "history", "lookup"):
        ws = deploy_wb[s["name"]]
        assert f"tbl_{s['name']}" in ws.tables
        assert ws.freeze_panes == "A2"
    for s in kinds(schema, "consolidated"):
        ws = deploy_wb[s["name"]]
        assert not ws.tables and ws.freeze_panes == "A2" and ws.protection.sheet


def test_lookups_seeded_and_no_sample_rows(deploy_wb, schema):
    for s in kinds(schema, "history", "lookup"):
        data_rows = [r for r in deploy_wb[s["name"]].iter_rows(min_row=2, values_only=True) if any(r)]
        assert len(data_rows) == len(s.get("seed", [])), f"{s['name']} should ship with seed rows only"


def test_template_has_active_yes_and_empty_entries(deploy_wb, schema):
    ws = deploy_wb[schema["rock_tab"]["template_sheet"]]
    vcol = schema["rock_tab"]["value_column"]
    for sec in schema["rock_tab"]["sections"]:
        for f in sec.get("fields", []):
            if f.get("formula"):
                continue
            expected = f.get("template_value")
            assert ws[f"{vcol}{f['row']}"].value == expected, f["name"]


def test_dropdowns_on_lookup_columns_of_the_template(deploy_wb, schema):
    sheets = {s["name"]: s for s in schema["sheets"]}
    ws = deploy_wb[schema["rock_tab"]["template_sheet"]]
    dvs = validations(ws)
    for sec in schema["rock_tab"]["sections"]:
        if sec["kind"] == "fields":
            targets = [(f"{schema['rock_tab']['value_column']}{f['row']}", f) for f in sec["fields"] if not f.get("formula")]
        else:
            last = sec["first_row"] + sec["capacity"] - 1
            targets = []
            for i, c in enumerate(sheets[sec["block"]]["columns"], start=1):
                if not c.get("formula"):
                    letter = chr(ord("A") + i - 1)
                    targets.append((f"{letter}{sec['first_row']}:{letter}{last}", c))
        for rng, c in targets:
            if not c.get("lookup"):
                continue
            assert rng in dvs and dvs[rng].type == "list", f"{sec['id']} {c['name']} has no dropdown at {rng}"
            assert dvs[rng].formula1 == build_workbook.list_name(c["lookup"])
            assert build_workbook.list_name(c["lookup"]) in deploy_wb.defined_names
            if c.get("validation") == "warning":
                assert dvs[rng].errorStyle == "warning"
            else:
                assert dvs[rng].errorStyle in (None, "stop")


def test_params_are_defined_names(deploy_wb, schema):
    for p in schema["params"]:
        assert p["name"] in deploy_wb.defined_names


def test_lookup_sheet_date_validation(deploy_wb):
    dvs = validations(deploy_wb["lkp_Steercos"])
    assert any(dv.type == "date" for dv in dvs.values())


def test_migration_keeps_rock_tabs_lookups_and_history(tmp_path, workbook, schema):
    out = tmp_path / "migrated.xlsx"
    build_workbook.main(["--deploy", "--from", str(ROOT / schema["workbook"]), "--out", str(out)])
    migrated = load_workbook(out)
    rt = schema["rock_tab"]
    # every rock tab with its entry values
    before_tabs = build_workbook.read_rock_tabs(ROOT / schema["workbook"], schema)
    after_tabs = build_workbook.read_rock_tabs(out, schema)
    assert before_tabs and [t["RockTab"] for t in before_tabs] == [t["RockTab"] for t in after_tabs]
    assert before_tabs == after_tabs
    names = migrated.sheetnames
    assert names.index(rt["template_sheet"]) < names.index(before_tabs[0]["RockTab"]) < names.index(rt["end_sheet"])
    # lookup and history rows
    for s in kinds(schema, "history", "lookup"):
        before = sum(1 for r in workbook[s["name"]].iter_rows(min_row=2, values_only=True) if any(r))
        after = sum(1 for r in migrated[s["name"]].iter_rows(min_row=2, values_only=True) if any(r))
        assert before == after, f"{s['name']} lost rows in migration"
