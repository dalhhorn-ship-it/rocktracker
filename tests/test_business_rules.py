"""Layer 3: business rules from docs/PRD.md. Add one test per rule."""
import pytest


def test_at_risk_initiatives_have_target_date(rows):
    # Example rule; replace with the rules in your PRD.
    if "Initiatives" not in rows:
        pytest.skip("no Initiatives sheet in this project")
    missing = [r["ID"] for r in rows["Initiatives"] if r["Status"] == "At risk" and not r["TargetDate"]]
    assert not missing, f"at risk initiatives without a target date: {missing}"
