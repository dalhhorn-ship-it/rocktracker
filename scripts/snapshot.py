"""Python mirror of scripts/office/snapshot.ts (DECISIONS 0007).

Pure functions on lists of dicts so the snapshot rules are testable without Excel.
Keep the two in step: tests/test_snapshot.py checks the column lists of the script
against the schema and this mirror against the same rules.
"""
from __future__ import annotations

from datetime import date

ROCK_COPY = ["RockID", "Rock", "GPM", "UpdateDate", "State", "MainMessage",
             "MilestonesCommitted", "MilestonesSlipped", "MilestonesCompleted",
             "PositionsBudgeted", "PositionsActual", "OpenHighRisks"]
ROCK_NAME_SOURCE = "RockName"   # Rocks column that feeds snapshot column Rock
MILESTONE_COPY = ["MilestoneKey", "RockID", "Title", "Commitment", "PlannedDate", "ForecastDate",
                  "ActualDate", "MCQuarter", "Status"]


def snapshot_rows(rocks: list[dict], milestones: list[dict], today: date,
                  existing_rock_ids=(), existing_milestone_ids=()):
    """Return (new RockSnapshots rows, new MilestoneSnapshots rows) as dicts.

    Active rocks only (Active == "Yes"); milestones only of active rocks; rows with an
    empty key are spill blanks and are skipped; SnapshotIDs already present are skipped.
    """
    day = today.isoformat()
    seen_r, seen_e = set(existing_rock_ids), set(existing_milestone_ids)
    active = set()
    rock_out, milestone_out = [], []
    for r in rocks:
        rid = str(r.get("RockID") or "")
        if not rid or r.get("Active") != "Yes":
            continue
        active.add(rid)
        sid = f"{day}|{rid}"
        if sid in seen_r:
            continue
        seen_r.add(sid)
        row = {"SnapshotID": sid, "SnapshotDate": day}
        for c in ROCK_COPY:
            row[c] = r.get(ROCK_NAME_SOURCE if c == "Rock" else c, "")
        rock_out.append(row)
    for e in milestones:
        key = str(e.get("MilestoneKey") or "")
        if not key or str(e.get("RockID") or "") not in active:
            continue
        sid = f"{day}|{key}"
        if sid in seen_e:
            continue
        seen_e.add(sid)
        row = {"SnapshotID": sid, "SnapshotDate": day}
        for c in MILESTONE_COPY:
            row[c] = e.get(c, "")
        milestone_out.append(row)
    return rock_out, milestone_out
