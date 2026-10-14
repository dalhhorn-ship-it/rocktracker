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


def test_coverage_of_cases():
    epics = [e for r in S["rocks"] for e in r["Epics"] if e]
    assert {e["Commitment"] for e in epics} == {"Committed", "Choice point", "Not committed"}
    assert {e["LeadStatus"] for e in epics} >= {"Delivered", "On hold", "On watch"}
    risks = [k for r in S["rocks"] for k in r["Risks"] if k.get("Likelihood") and k.get("Impact")]
    assert {k["Likelihood"] for k in risks} == {"Low", "Medium", "High"}
    assert {k["Impact"] for k in risks} == {"Low", "Medium", "High"}
    decisions = [d for r in S["rocks"] for d in r["Decisions"]]
    assert any(d["ChoicePoint"] == "Yes" for d in decisions)
    assert any(d["Outcome"] and d["FollowUp"] != "Closed" for d in decisions)
    assert len({r[1] for r in S["snapshots"]["RockSnapshots"]}) == 3
