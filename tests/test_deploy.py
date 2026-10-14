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


# ---------------------------------------------------------------------------
# Migration from schema 1.0.0 (schema `migration`)
# ---------------------------------------------------------------------------
import datetime as dt  # noqa: E402
import json  # noqa: E402

V1 = json.loads((ROOT / build_workbook.V1_SCHEMA).read_text())
D = dt.date


def day(v):
    return v.date() if isinstance(v, dt.datetime) else v


@pytest.fixture(scope="module")
def v1_file(tmp_path_factory):
    """A small workbook in the v1 layout, built by the same generator from the v1 schema."""
    rock = {
        "RockTab": "R01 Checkout", "RockID": "R01", "RockName": "Checkout", "ValueChain": "Sell", "Lead": "Mia Sandbox",
        "GPM": "Noor Testwell", "Active": "Yes", "Purpose": "Faster checkout", "Goals": "Goal text", "Delivers": "Delivers text",
        "UpdateDate": D(2026, 10, 1), "State": "At risk", "MainMessage": "On track mostly",
        "PositionsPlanned": 6, "PositionsFilled": 4,
        "Epics": [
            {"Title": "Done thing", "ADOId": "1001", "Commitment": "Committed", "PlannedDate": D(2026, 9, 1),
             "ForecastDate": D(2026, 9, 5), "LeadStatus": "Delivered", "Comment": "Shipped", "KRLink": "KR1"},
            {},
            {"Title": "Late thing", "ADOId": "1002", "Commitment": "Committed", "PlannedDate": D(2026, 11, 1),
             "ForecastDate": D(2026, 12, 15), "LeadStatus": "On watch", "Comment": "Slipping"},
        ],
        "Risks": [
            {"Title": "Risk A", "Likelihood": "High", "Impact": "High", "KeyAction": "Act", "ActionOwner": "Mia Sandbox", "RiskStatus": "Open", "TopRisk": "Yes"},
            {"Title": "Risk B", "Likelihood": "Low", "Impact": "Low", "RiskStatus": "Open", "TopRisk": "No"},
            {"Title": "Risk C", "Likelihood": "Medium", "Impact": "High", "RiskStatus": "Closed", "TopRisk": "Yes"},
            {"Title": "Risk D", "Likelihood": "Medium", "Impact": "Medium", "RiskStatus": "Open", "TopRisk": "Yes"},
            {"Title": "Risk E", "Likelihood": "Medium", "Impact": "Medium", "RiskStatus": "Open", "TopRisk": "Yes"},
            {"Title": "Risk F", "Likelihood": "Medium", "Impact": "Medium", "RiskStatus": "Open", "TopRisk": "Yes"},
        ],
        "CallOuts": [{"Text": "Call out", "Date": D(2026, 10, 2), "CallOutStatus": "Open"}],
        "Decisions": [{"Decision": "Pick vendor", "SteercoDate": D(2026, 10, 16), "DecideBy": D(2026, 10, 14), "ChoicePoint": "No",
                       "Options": "A or B", "Outcome": "", "Owner": "Mia Sandbox", "FollowUp": "Send note"}],
    }
    rows = {s["name"]: [list(r) for r in s.get("seed", [])] for s in V1["sheets"] if s["kind"] != "consolidated"}
    rows["lkp_People"] = [["Mia Sandbox", "Product"], ["Noor Testwell", "Product"]]
    rows["RockSnapshots"] = [{
        "SnapshotID": "2026-09-28-R01", "SnapshotDate": D(2026, 9, 28), "RockID": "R01", "Rock": "Checkout", "GPM": "Noor Testwell",
        "UpdateDate": D(2026, 9, 25), "State": "On track", "MainMessage": "Fine", "EpicsCommitted": 2, "EpicsSlipped": 0,
        "EpicsDelivered": 1, "PositionsPlanned": 6, "PositionsFilled": 3, "OpenHighRisks": 1}]
    rows["EpicSnapshots"] = [{
        "SnapshotID": "2026-09-28-R01-E03", "SnapshotDate": D(2026, 9, 28), "EpicKey": "R01-E03", "RockID": "R01",
        "Title": "Late thing", "Commitment": "Committed", "PlannedDate": D(2026, 11, 1), "ForecastDate": D(2026, 11, 1), "Status": "On plan"}]
    wb = build_workbook.build(V1, {"rocks": [rock], "rows": rows}, deploy=False)
    path = tmp_path_factory.mktemp("v1") / "v1.xlsx"
    wb.save(path)
    return path, rock


@pytest.fixture(scope="module")
def migrated_v1(v1_file, schema, tmp_path_factory):
    path, rock = v1_file
    out = tmp_path_factory.mktemp("v1out") / "migrated.xlsx"
    build_workbook.main(["--deploy", "--from", str(path), "--out", str(out)])
    return out, build_workbook.read_rock_tabs(out, schema)[0], rock


def test_v1_file_is_detected_and_current_file_is_not(v1_file, schema):
    assert build_workbook.is_v1(v1_file[0], schema)
    assert not build_workbook.is_v1(ROOT / schema["workbook"], schema)


def test_v1_migration_rock_fields_and_blocks_keep_every_value(migrated_v1):
    _, new, old = migrated_v1
    for k, v in old.items():
        if k in ("Epics", "Risks", "CallOuts", "Decisions", "PositionsPlanned", "PositionsFilled"):
            continue
        assert day(new[k]) == v, k
    for name in ("CallOuts", "Decisions"):
        got = [{k: day(v) for k, v in r.items()} for r in new[name]]
        assert got == [{k: v for k, v in r.items() if v != ""} for r in old[name]]
    for got, was in zip(new["Risks"], old["Risks"]):
        assert {k: v for k, v in got.items()} == {k: v for k, v in was.items() if k != "TopRisk"}


def test_v1_migration_epics_become_milestones_in_the_same_slot(migrated_v1):
    _, new, old = migrated_v1
    ms = new["Milestones"]
    assert len(ms) == 3 and ms[1] == {}
    done = {k: day(v) for k, v in ms[0].items()}
    assert done["LeadStatus"] == "Completed" and done["ActualDate"] == D(2026, 9, 5)
    for k, v in old["Epics"][0].items():
        if k != "LeadStatus":
            assert done[k] == v, k
    late = {k: day(v) for k, v in ms[2].items()}
    assert late == old["Epics"][2] and "ActualDate" not in late


def test_v1_migration_top_risks_become_three_attention_lines(migrated_v1):
    _, new, _ = migrated_v1
    assert [new.get(f"Attention{i}") for i in (1, 2, 3)] == ["Risk A", "Risk D", "Risk E"]  # open top risks, slot order, max 3


def test_v1_migration_positions_become_team_slot_one(migrated_v1):
    _, new, _ = migrated_v1
    assert new["Teams"] == [{"TeamName": "Team (migrated)", "Budgeted": 6, "Actual": 4}]


def test_v1_migration_history_lookups_and_names(migrated_v1):
    out, _, _ = migrated_v1
    wb = load_workbook(out)

    def table(name):
        vals = list(wb[name].iter_rows(values_only=True))
        return [dict(zip(vals[0], r)) for r in vals[1:] if any(v is not None for v in r)]

    assert "Epics" not in wb.sheetnames and "EpicSnapshots" not in wb.sheetnames
    snap = table("RockSnapshots")[0]
    assert (snap["MilestonesCommitted"], snap["MilestonesSlipped"], snap["MilestonesCompleted"]) == (2, 0, 1)
    assert (snap["PositionsBudgeted"], snap["PositionsActual"]) == (6, 3)
    m = table("MilestoneSnapshots")[0]
    assert m["MilestoneKey"] == "R01-M03" and m["SnapshotID"] == "2026-09-28-R01-M03"
    assert m["ActualDate"] is None and m["MCQuarter"] == "MC26Q3"  # forecast 1 Nov 2026 is MC26Q3
    assert [r["Name"] for r in table("lkp_People")] == ["Mia Sandbox", "Noor Testwell"]
    status = [r["Value"] for r in table("lkp_LeadStatus")]
    assert "Completed" in status and "Delivered" not in status
    assert "lkp_MilestoneStatus" in wb.sheetnames


def test_mc_quarter_labels():
    q = build_workbook.mc_quarter
    assert q(D(2026, 10, 1)) == "MC26Q3" and q(D(2026, 12, 31)) == "MC26Q3"
    assert q(D(2027, 1, 1)) == "MC26Q4" and q(D(2026, 4, 1)) == "MC26Q1" and q(D(2026, 3, 31)) == "MC25Q4"
