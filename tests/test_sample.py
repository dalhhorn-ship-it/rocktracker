"""Shape and coverage of data/sample.json (the synthetic rock portfolio)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "data" / "sample.json").read_text())
SCHEMA = json.loads((ROOT / "schema" / "workbook.schema.json").read_text())
CAP = {s["block"]: s["capacity"] for s in SCHEMA["rock_tab"]["sections"] if s["kind"] == "block"}
INPUT = {sh["name"]: {c["name"] for c in sh["columns"] if not c.get("formula")} for sh in SCHEMA["sheets"]}


def test_block_rows_use_input_columns_and_fit_capacity():
    for r in S["rocks"]:
        for block, cap in CAP.items():
            assert len(r[block]) <= cap, (r["RockID"], block)
            for row in r[block]:
                assert set(row) <= INPUT[block], (r["RockID"], block, set(row) - INPUT[block])


def test_profile_fields_and_unique_ids():
    ids = [r["RockID"] for r in S["rocks"]]
    assert len(ids) == len(set(ids)) == 5
    assert len({r["GPM"] for r in S["rocks"]}) == 2
    assert [r["Active"] for r in S["rocks"]].count("No") == 1


def test_lookup_values_are_known():
    people = {p[0] for p in S["lookups"]["lkp_People"]}
    chains = {c[0] for c in S["lookups"]["lkp_ValueChains"]}
    for r in S["rocks"]:
        assert {r["Lead"], r["GPM"]} <= people and r["ValueChain"] in chains


def _ms():
    return [(r, m) for r in S["rocks"] for m in r["Milestones"] if m]


def _find(title):
    return next(m for _, m in _ms() if m["Title"] == title)


def test_no_retired_fields_or_statuses():
    text = json.dumps(S["rocks"]) + json.dumps(S["snapshots"])
    for word in ("TopRisk", "PositionsPlanned", "PositionsFilled", "Delivered", "Epics"):
        assert word not in text, word


def test_attention_lines_and_teams():
    counts = {r["RockID"]: sum(bool(r["Attention%d" % i]) for i in (1, 2, 3)) for r in S["rocks"]}
    active = [r for r in S["rocks"] if r["Active"] == "Yes"]
    assert sum(1 for r in active if counts[r["RockID"]] == 0) == 1
    assert all(0 <= counts[r["RockID"]] <= 3 for r in S["rocks"])
    for r in S["rocks"]:
        assert 1 <= len(r["Teams"]) <= 5, r["RockID"]
    teams = [t for r in S["rocks"] for t in r["Teams"]]
    assert any(t["Budgeted"] == 0 for t in teams)
    assert any(t["Budgeted"] and t["Actual"] > t["Budgeted"] for t in teams)


def test_milestone_details_and_ado_link():
    ms = _ms()
    full = [m for r, m in ms if r["RockID"] in ("R01", "R02", "R03")]
    for m in full:
        assert m["Owner"] and m["StartDate"] or m["Commitment"] != "Committed" or m["Title"] == "Points ledger", m["Title"]
        assert m["Description"] and m["Detail1"], m["Title"]
    links = [m["ADOLink"] for _, m in ms if m.get("ADOLink")]
    assert links and all(link.startswith("https://") for link in links)
    assert any(not m.get("ADOLink") for _, m in ms)


def test_milestone_cases():
    t = S["today"]
    ms = [m for _, m in _ms()]
    assert {m["LeadStatus"] for m in ms} == {None, "Completed", "On hold", "On watch"}
    assert {m["Commitment"] for m in ms} == {"Committed", "Choice point", "Not committed"}
    # Completed, actual before today
    assert any(m["LeadStatus"] == "Completed" and m["ActualDate"] and m["ActualDate"] < t for m in ms)
    # Completed, no actual date, planned before today (About warning)
    assert any(m["LeadStatus"] == "Completed" and not m["ActualDate"] and m["PlannedDate"] < t for m in ms)
    # Completed, actual today
    assert any(m["LeadStatus"] == "Completed" and m["ActualDate"] == t for m in ms)
    # overdue committed, undelivered, date in MC26Q2 (Jul to Sep 2026)
    assert any(m["Commitment"] == "Committed" and not m["LeadStatus"] and m["PlannedDate"] and "2026-07-01" <= (m["ForecastDate"] or m["PlannedDate"]) < "2026-10-01" for m in ms)
    # beyond MC26Q4 (after 2027-03-31), and MC27Q1
    assert any(m["PlannedDate"] and m["PlannedDate"] > "2027-03-31" for m in ms)
    # no dates at all
    assert any(not (m["PlannedDate"] or m["ForecastDate"] or m["ActualDate"]) for m in ms)
    # off track: planned MC26Q3, forecast MC26Q4
    assert any(m["Commitment"] == "Committed" and m["PlannedDate"] and "2026-10-01" <= m["PlannedDate"] <= "2026-12-31" and m["ForecastDate"] and m["ForecastDate"] > "2026-12-31" and not m["LeadStatus"] for m in ms)
    # slipped: forecast later than planned, and planned in each of three quarters
    assert any(m["ForecastDate"] and m["PlannedDate"] and m["ForecastDate"] > m["PlannedDate"] for m in ms)
    planned = [m["PlannedDate"] for m in ms if m["PlannedDate"]]
    assert any("2026-10-01" <= p <= "2026-12-31" for p in planned)
    assert any("2027-01-01" <= p <= "2027-03-31" for p in planned)
    assert any("2027-04-01" <= p <= "2027-06-30" for p in planned)
    # Completed with lead status and On hold also carry a forecast or comment (Completed beats On hold is a mirror test)
    assert not any(m["LeadStatus"] == "Delivered" for m in ms)


def test_decision_cases():
    r1 = next(r for r in S["rocks"] if r["RockID"] == "R01")
    open_req = [d for d in r1["Decisions"] if d["Decision"] and not d["Outcome"]]
    assert len(open_req) == 6
    assert any(d["ChoicePoint"] == "Yes" and not d["Outcome"] for d in r1["Decisions"])
    # a decided row sits between two requests
    idx = [i for i, d in enumerate(r1["Decisions"]) if d["Outcome"]]
    assert any(0 < i < len(r1["Decisions"]) - 1 and not r1["Decisions"][i - 1]["Outcome"] and not r1["Decisions"][i + 1]["Outcome"] for i in idx)
    all_d = [d for r in S["rocks"] for d in r["Decisions"]]
    assert any(d["Outcome"] and d["FollowUp"] == "Open" for d in all_d)
    assert any(d["Outcome"] and d["FollowUp"] == "Closed" for d in all_d)
    steercos = {"2026-10-21"} | {row[0] for row in S["lookups"]["lkp_Steercos"]}
    assert {d["SteercoDate"] for d in all_d if d["SteercoDate"]} <= steercos
    inactive = next(r for r in S["rocks"] if r["Active"] == "No")
    assert inactive["Decisions"] and inactive["Teams"]


def test_risk_cases():
    risks = [k for r in S["rocks"] for k in r["Risks"] if k.get("Likelihood") and k.get("Impact")]
    assert {k["Likelihood"] for k in risks} == {"Low", "Medium", "High"}
    assert {k["Impact"] for k in risks} == {"Low", "Medium", "High"}
    # a High risk without a key action (R02)
    assert any(k["Likelihood"] == "High" and k["Impact"] == "High" and not k["KeyAction"] for k in risks)


def test_snapshots_use_new_columns():
    snaps = S["snapshots"]
    assert set(snaps) == {"RockSnapshots", "MilestoneSnapshots"}
    cols = {sh["name"]: [c["name"] for c in sh["columns"]] for sh in SCHEMA["sheets"]}
    for name, rows in snaps.items():
        assert rows and all(len(row) == len(cols[name]) for row in rows), name
    assert len({r[1] for r in snaps["RockSnapshots"]}) == 3
    assert len({r[1] for r in snaps["MilestoneSnapshots"]}) == 3
    assert all("-M" in r[2] and "-E" not in r[2] for r in snaps["MilestoneSnapshots"])
    assert {r[10] for r in snaps["MilestoneSnapshots"]} >= {"Completed", "Slipped", "On hold", "On plan", "Not committed"}


def test_progress_cases():
    ms = [m for _, m in _ms()]
    vals = [m.get("Progress") for m in ms]
    assert any(v is None for v in vals) and any(v for v in vals)
    assert all(v is None or (isinstance(v, int) and 0 <= v <= 100) for v in vals)
    # a Completed milestone with a typed value below 100 proves the override
    assert any(m["LeadStatus"] == "Completed" and m.get("Progress") is not None and m["Progress"] < 100 for m in ms)
    assert any(m.get("Progress") == 0 for m in ms)


def test_every_milestone_has_an_owner_from_the_people_lookup():
    people = {p[0] for p in S["lookups"]["lkp_People"]}
    ms = [m for _, m in _ms()]
    assert all(m["Owner"] in people for m in ms)
    assert len({m["Owner"] for m in ms}) >= 4


def test_sample_steercos_hold_the_next_steerco():
    assert "2026-10-21" in {row[0] for row in S["lookups"]["lkp_Steercos"]}


def test_sample_covers_every_quarter_ahead_and_slip_severity():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import datetime as dt
    import rock_model as rm
    today = dt.date.fromisoformat(S["today"])
    mdl = rm.build_model([rm.normalize_rock(r) for r in S["rocks"]], today, [x[0] for x in S["lookups"]["lkp_Steercos"]] if S["lookups"].get("lkp_Steercos") else ())
    rows = mdl["Milestones"]
    assert {m["QuarterAhead"] for m in rows if m["MilestoneKey"]} >= {1, 2, 3, 4, ""}
    assert {m["MCQuarter"] for m in rows} >= {"MC26Q3", "MC26Q4", "MC27Q1", "MC27Q2"}
    assert any(m["MCQuarter"] > "MC27Q2" for m in rows)
    assert {m["SlipSeverity"] for m in rows} >= {"Major", "Minor", ""}
