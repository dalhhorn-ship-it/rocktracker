#!/usr/bin/env python3
"""Python mirror of the Rock Tracker calculated columns (schema 2.2.0 `excel` plus `rule`).

Input: rock tabs, one dict per rock (see `normalize_rock`). Output: the six consolidated
sheets (Rocks, Milestones, Risks, CallOuts, Decisions, Teams) as lists of dicts in schema
column order, with the consolidation filter applied. Used by the tests, the LibreOffice
recalc check and the preview, so the preview never reads formula cells.

Rock dict shape (all keys optional, missing means empty):
  profile/update fields by name: RockID, RockName, ValueChain, Lead, GPM, Active, Purpose,
    Goals, Delivers, UpdateDate, State, MainMessage, Attention1, Attention2, Attention3
  block rows: "Milestones", "Risks", "CallOuts", "Decisions", "Teams": lists of dicts keyed
    by the typed column names, one item per slot in order. {} or None is an empty slot.
Dates may be date, datetime or YYYY-MM-DD text.

Blank safety follows the workbook: calculated cells are "" when the row has no key.
List blocks are consolidated with the zero to blank wrap, so a numeric 0 is "" on the
consolidated sheet, except the schema `keep_zero_columns` (Teams Budgeted, Actual, FillPct;
DECISIONS 0018), where a real 0 stays 0 and an empty typed count arrives as 0 through VSTACK.
The Rocks strip keeps real zeros.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "workbook.schema.json"

HIGH_RISK_MIN = 6
STALE_DAYS = 14
LEVEL_SCORE = {"Low": 1, "Medium": 2, "High": 3}
STATE_ORDER = ["On track", "At risk", "Off track"]

BLOCKS = ("Milestones", "Risks", "CallOuts", "Decisions", "Teams")
PROFILE_FIELDS = ["RockID", "RockName", "ValueChain", "Lead", "GPM", "Active", "Purpose",
                  "Goals", "Delivers"]
UPDATE_FIELDS = ["UpdateDate", "State", "MainMessage", "Attention1", "Attention2", "Attention3"]
DATE_COLUMNS = {"UpdateDate", "StartDate", "PlannedDate", "ForecastDate", "ActualDate", "Date",
                "SteercoDate", "DecideBy"}
MILESTONE_INPUTS = ("Title", "Owner", "Commitment", "StartDate", "PlannedDate", "ForecastDate",
                    "ActualDate", "LeadStatus", "Comment", "KRLink", "ADOId", "ADOLink",
                    "Description", "Detail1", "Detail2", "Detail3", "Progress")


# ---------------------------------------------------------------- helpers
def to_date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.date.fromisoformat(str(v)[:10])


def n(d):
    """Excel N() of a date: 0 when empty, else a comparable number."""
    return 0 if d is None or d == "" else d.toordinal()


def num(v):
    """Excel N() of a number cell: 0 when empty or text."""
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def edate(d: dt.date, months: int) -> dt.date:
    m = d.month - 1 + months
    y, m = d.year + m // 12, m % 12 + 1
    return dt.date(y, m, min(d.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28,
                                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]))


def excel_round1(x):
    """Excel ROUND(x, 1): half away from zero."""
    sign = -1 if x < 0 else 1
    return sign * int(abs(x) * 10 + 0.5 + 1e-9) / 10


def mc_quarter(d):
    """MC quarter label: shift back 3 months, then MC, 2 digit year, Q, quarter."""
    if d is None or d == "":
        return ""
    s = edate(d, -3)
    return f"MC{s.year % 100:02d}Q{(s.month + 2) // 3}"


def params(today: dt.date, steercos=()):
    qs = dt.date(today.year, (today.month - 1) // 3 * 3 + 1, 1)
    dates = sorted(d for d in (to_date(s) for s in steercos) if d)
    nxt = next((d for d in dates if d >= today), None)
    return {
        "MCQuarterStart": qs,
        "MCQuarterEnd": edate(qs, 3) - dt.timedelta(days=1),
        "OutlookEnd": edate(qs, 6) - dt.timedelta(days=1),
        "CurrentMCQuarter": mc_quarter(qs),
        "NextMCQuarter": mc_quarter(edate(qs, 3)),
        "NextSteerco": nxt,  # None means 0 in Excel
        "HighRiskMin": HIGH_RISK_MIN,
        "StaleDays": STALE_DAYS,
    }


def normalize_rock(rock: dict) -> dict:
    out = {}
    for f in PROFILE_FIELDS + UPDATE_FIELDS:
        v = rock.get(f)
        out[f] = to_date(v) if f == "UpdateDate" else ("" if v is None else v)
    for b in BLOCKS:
        src = rock.get(b)
        rows = []
        for r in src or []:
            r = dict(r or {})
            for c in list(r):
                if c in DATE_COLUMNS:
                    r[c] = to_date(r[c])
                elif r[c] is None:
                    r[c] = ""
            rows.append(r)
        out[b] = rows
    return out


# ---------------------------------------------------------------- row rules
def _keyed(rock, text, active_needed=True):
    return text != "" and rock["RockID"] != "" and (not active_needed or rock["Active"] == "Yes")


def milestone_status(m):
    lead, commit = m.get("LeadStatus", ""), m.get("Commitment", "")
    planned, forecast = m.get("PlannedDate"), m.get("ForecastDate")
    if lead == "Completed":
        return "Completed"
    if lead == "On hold":
        return "On hold"
    if commit != "Committed":
        return "Not committed"
    if n(planned) > 0 and n(forecast) > n(planned):
        return "Slipped"
    if lead == "On watch":
        return "On watch"
    return "On plan"


def milestone_row(m, rock, slot, p, today):
    key = f"{rock['RockID']}-M{slot:02d}" if _keyed(rock, m.get("Title", "")) else ""
    row = {"MilestoneKey": key}
    for c in MILESTONE_INPUTS:
        row[c] = m.get(c, None if c in DATE_COLUMNS else "")
    calc = ("Status", "ProgressShown", "SlipWeeks", "TimelineDate", "MCQuarter", "InOutlook", "Visible", "Overdue",
            "RockID", "Rock", "GPM")
    if key == "":
        row.update({c: "" for c in calc})
        return row
    status = milestone_status(m)
    pl, fc, ac = m.get("PlannedDate"), m.get("ForecastDate"), m.get("ActualDate")
    row["Status"] = status
    prog = m.get("Progress", "")
    row["ProgressShown"] = 100 if status == "Completed" else ("" if prog in ("", None) else prog)
    row["SlipWeeks"] = excel_round1((n(fc) - n(pl)) / 7) if status == "Slipped" else ""
    tl = ac if n(ac) > 0 else fc if n(fc) > 0 else pl if n(pl) > 0 else ""
    row["TimelineDate"] = tl
    row["MCQuarter"] = mc_quarter(tl) if n(tl) > 0 else ""
    lo, hi = n(p["MCQuarterStart"]), n(p["OutlookEnd"])
    in_out = (lo <= n(pl) <= hi) or (lo <= n(tl) <= hi)
    row["InOutlook"] = "Yes" if in_out else "No"
    if status == "Completed":
        ref = n(ac) if n(ac) > 0 else n(pl)
        row["Visible"] = "No" if ref < n(today) else row["InOutlook"]
    else:
        shown = in_out or n(tl) == 0 or n(tl) < n(today)
        row["Visible"] = "Yes" if shown else "No"
    row["Overdue"] = ("Yes" if (m.get("Commitment") == "Committed"
                                and status not in ("Completed", "On hold")
                                and 0 < n(tl) < n(today)) else "No")
    row.update(RockID=rock["RockID"], Rock=rock["RockName"], GPM=rock["GPM"])
    return row


def risk_row(r, rock, slot, p):
    key = f"{rock['RockID']}-R{slot:02d}" if _keyed(rock, r.get("Title", "")) else ""
    row = {"RiskKey": key}
    for c in ("Title", "Likelihood", "Impact", "KeyAction", "ActionOwner", "RiskStatus"):
        row[c] = r.get(c, "")
    if key == "":
        row.update(Score="", High="", NeedsAction="", RockID="", Rock="", GPM="")
        return row
    lk, im = row["Likelihood"], row["Impact"]
    score = LEVEL_SCORE[lk] * LEVEL_SCORE[im] if lk != "" and im != "" else ""
    row["Score"] = score
    high = num(score) >= p["HighRiskMin"]
    row["High"] = "Yes" if high else "No"
    needs = (high and row["RiskStatus"] != "Closed"
             and (row["KeyAction"] == "" or row["ActionOwner"] == ""))
    row["NeedsAction"] = "Yes" if needs else "No"
    row.update(RockID=rock["RockID"], Rock=rock["RockName"], GPM=rock["GPM"])
    return row


def callout_row(c, rock, slot):
    key = f"{rock['RockID']}-C{slot:02d}" if _keyed(rock, c.get("Text", "")) else ""
    row = {"CallOutKey": key, "Text": c.get("Text", ""), "Date": c.get("Date"),
           "CallOutStatus": c.get("CallOutStatus", "")}
    on = key != ""
    row.update(RockID=rock["RockID"] if on else "", Rock=rock["RockName"] if on else "",
               GPM=rock["GPM"] if on else "")
    return row


def decision_row(d, rock, slot, p):
    # Kept after the rock closes: no Active condition.
    key = f"{rock['RockID']}-D{slot:02d}" if _keyed(rock, d.get("Decision", ""), False) else ""
    row = {"DecisionKey": key}
    for c in ("Decision", "SteercoDate", "DecideBy", "ChoicePoint", "Options", "Outcome",
              "Owner", "FollowUp"):
        row[c] = d.get(c, None if c in DATE_COLUMNS else "")
    if key == "":
        row.update(DecisionState="", RequestNo="", DueNextSteerco="", OpenFollowUp="",
                   RockID="", Rock="", GPM="")
        return row
    state = "Requested" if row["Outcome"] == "" else "Decided"
    nxt = n(p["NextSteerco"])
    due = (state == "Requested" and nxt > 0
           and (n(row["SteercoDate"]) == nxt
                or (n(row["DecideBy"]) > 0 and n(row["DecideBy"]) <= nxt)))
    row["DecisionState"] = state
    row["RequestNo"] = ""  # filled in by the rock, which knows the other rows
    row["DueNextSteerco"] = "Yes" if due else "No"
    row["OpenFollowUp"] = "Yes" if state == "Decided" and row["FollowUp"] != "Closed" else "No"
    row.update(RockID=rock["RockID"], Rock=rock["RockName"], GPM=rock["GPM"])
    return row


def number_request_nos(decisions):
    """RequestNo: position of a Requested row among the rock's Requested rows, by slot."""
    k = 0
    for d in decisions:
        if d["DecisionState"] == "Requested":
            k += 1
            d["RequestNo"] = k
    return decisions


def team_row(t, rock, slot):
    key = f"{rock['RockID']}-T{slot:02d}" if _keyed(rock, t.get("TeamName", "")) else ""
    row = {"TeamKey": key, "TeamName": t.get("TeamName", ""), "TeamLead": t.get("TeamLead", ""),
           "Budgeted": t.get("Budgeted", ""), "Actual": t.get("Actual", "")}
    if key == "":
        row.update(FillPct="", RockID="", Rock="", GPM="")
        return row
    row["FillPct"] = num(row["Actual"]) / row["Budgeted"] if num(row["Budgeted"]) > 0 else ""
    row.update(RockID=rock["RockID"], Rock=rock["RockName"], GPM=rock["GPM"])
    return row


def rock_fields(rock, milestones, risks, teams, decisions, p, today):
    """The calculated fields of the rock tab (sections 1 request lines and 2 Signals)."""
    ud = rock["UpdateDate"]
    age = (today - ud).days if ud else ""
    mk = [m for m in milestones if m["MilestoneKey"]]
    committed = [m for m in mk if m["Commitment"] == "Committed" and m["InOutlook"] == "Yes"]
    slipped = [m for m in mk if m["Status"] == "Slipped" and m["InOutlook"] == "Yes"]
    onplan = [m for m in committed if m["Status"] in ("On plan", "On watch", "Completed")]
    completed = [m for m in committed if m["Status"] == "Completed"]
    overdue = [m for m in mk if m["Overdue"] == "Yes"]
    rk = [r for r in risks if r["RiskKey"]]
    open_high = [r for r in rk if r["High"] == "Yes" and r["RiskStatus"] != "Closed"]
    no_action = [r for r in rk if r["NeedsAction"] == "Yes"]
    tk = [t for t in teams if t["TeamKey"]]
    budgeted = sum(num(t["Budgeted"]) for t in tk)
    actual = sum(num(t["Actual"]) for t in tk)
    signal = ""
    if rock["RockID"] != "":
        off = any(m["Status"] == "Slipped"
                  and n(p["MCQuarterStart"]) <= n(m["PlannedDate"]) <= n(p["MCQuarterEnd"])
                  and n(m["ForecastDate"]) > n(p["MCQuarterEnd"]) for m in mk)
        signal = ("Off track" if off else
                  "At risk" if len(slipped) + len(overdue) + len(no_action) > 0 else "On track")
    state = rock["State"]
    check = ""
    if state != "" and signal != "":
        check = "Yes" if STATE_ORDER.index(signal) > STATE_ORDER.index(state) else "No"
    requests = {d["RequestNo"]: d["Decision"] for d in decisions
                if d["DecisionState"] == "Requested"}
    f = {
        "OpenRequests": sum(1 for d in decisions if d["DecisionState"] == "Requested"),
    }
    for i in range(1, 6):
        f[f"Request{i}"] = requests.get(i, "")
    f.update(
        UpdateAgeDays=age, DataSignal=signal, CheckCall=check,
        OutlookQuarters=f"{p['CurrentMCQuarter']} and {p['NextMCQuarter']}",
        MilestonesCommitted=len(committed), MilestonesSlipped=len(slipped),
        MilestonesOnPlan=len(onplan), MilestonesCompleted=len(completed),
        MilestonesOverdue=len(overdue), OpenHighRisks=len(open_high),
        HighRisksNoAction=len(no_action), PositionsBudgeted=budgeted, PositionsActual=actual,
        FillPct=actual / budgeted if budgeted > 0 else "",
    )
    return f


def rock_strip(rock, fields, p):
    """Rocks row from the rock tab fields; None when the tab has no RockID."""
    if rock["RockID"] == "":
        return None

    def blank(v):  # strip returns "" for blanks, keeps real zeros
        return "" if v in ("", None) else v

    ud = rock["UpdateDate"]
    row = {c: blank(rock[c]) for c in PROFILE_FIELDS + UPDATE_FIELDS}
    row["Stale"] = "Yes" if (ud is None or num(fields["UpdateAgeDays"]) > p["StaleDays"]) else "No"
    for c in ("UpdateAgeDays", "MilestonesCommitted", "MilestonesSlipped", "MilestonesOnPlan",
              "MilestonesCompleted", "MilestonesOverdue", "OpenHighRisks", "HighRisksNoAction",
              "PositionsBudgeted", "PositionsActual", "FillPct", "DataSignal", "CheckCall"):
        row[c] = fields[c]
    row.update(CurrentMCQuarter=p["CurrentMCQuarter"], NextMCQuarter=p["NextMCQuarter"])
    return row


# ---------------------------------------------------------------- consolidation
def compute_rock(raw, p, today):
    """Everything one rock tab computes: block rows, tab fields and the strip."""
    rock = normalize_rock(raw)
    ms = [milestone_row(m, rock, i, p, today) for i, m in enumerate(rock["Milestones"], 1)]
    rs = [risk_row(r, rock, i, p) for i, r in enumerate(rock["Risks"], 1)]
    cs = [callout_row(c, rock, i) for i, c in enumerate(rock["CallOuts"], 1)]
    ds = number_request_nos([decision_row(d, rock, i, p)
                             for i, d in enumerate(rock["Decisions"], 1)])
    ts = [team_row(t, rock, i) for i, t in enumerate(rock["Teams"], 1)]
    fields = rock_fields(rock, ms, rs, ts, ds, p, today)
    return {"rock": rock, "fields": fields, "strip": rock_strip(rock, fields, p),
            "Milestones": ms, "Risks": rs, "CallOuts": cs, "Decisions": ds, "Teams": ts}


def _keep_zero():
    return {s["name"]: set(s.get("keep_zero_columns", [])) for s in load_schema()["sheets"]}


def zero_wrap(row, keep=()):
    """List block consolidation wraps a numeric 0 to blank, except the keep_zero_columns.
    An empty typed count in a keep column arrives as 0 through VSTACK."""
    out = {}
    for k, v in row.items():
        if k in keep:
            out[k] = 0 if v == "" and k in TYPED_COUNTS else v
        else:
            out[k] = "" if isinstance(v, (int, float)) and not isinstance(v, bool) and v == 0 else v
    return out


TYPED_COUNTS = {"Budgeted", "Actual"}  # typed (not formula) keep zero columns: empty cell is 0


KEY = {"Milestones": "MilestoneKey", "Risks": "RiskKey", "CallOuts": "CallOutKey",
       "Decisions": "DecisionKey", "Teams": "TeamKey"}


def build_model(rocks, today: dt.date, steercos=(), schema=None):
    """Return {"Rocks", "Milestones", "Risks", "CallOuts", "Decisions", "Teams"} (lists of
    dicts) for the given rock tabs (in tab order) and frozen today."""
    p = params(today, steercos)
    out = {"Rocks": [], **{b: [] for b in BLOCKS}}
    keep = _keep_zero()
    for raw in rocks:
        c = compute_rock(raw, p, today)
        if c["strip"] is not None:
            out["Rocks"].append(c["strip"])
        for b in BLOCKS:  # consolidation filter: key must be non empty text
            out[b] += [zero_wrap(r, keep.get(b, ())) for r in c[b] if r[KEY[b]]]
    if schema is not None:
        out = order_columns(out, schema)
    return out


def tab_fields(rocks, today: dt.date, steercos=()):
    """Calculated rock tab fields (OpenRequests, Request1 to 5, Signals) per rock tab, in
    tab order, for the recalc check of the tab cells."""
    p = params(today, steercos)
    return [compute_rock(raw, p, today)["fields"] for raw in rocks]


def order_columns(model, schema):
    cols = {s["name"]: [c["name"] for c in s["columns"]] for s in schema["sheets"]}
    return {sheet: [{c: r.get(c, "") for c in cols[sheet]} for r in rows]
            for sheet, rows in model.items()}


# ---------------------------------------------------------------- loaders
def load_schema():
    return json.loads(SCHEMA_PATH.read_text())


def rocks_from_json(path):
    """Read rock dicts from a JSON file: a list, or {"rocks": [...]} / {"Rocks": [...]}."""
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict):
        data = data.get("rocks", data.get("Rocks"))
    return data


def rocks_from_workbook(path, schema=None):
    """Read the typed cells of every rock tab (between RockTemplate and RocksEnd) using the
    schema layout: fields by row in the value column, block columns by header label."""
    from openpyxl import load_workbook

    schema = schema or load_schema()
    rt = schema["rock_tab"]
    wb = load_workbook(path, data_only=True)
    names = wb.sheetnames
    first, last = names.index(rt["template_sheet"]), names.index(rt["end_sheet"])
    sheets = {s["name"]: s for s in schema["sheets"]}
    vcol = rt["value_column"]
    rocks = []
    for name in names[first + 1:last]:
        ws = wb[name]
        rock = {}
        for sec in rt["sections"]:
            if sec["kind"] == "fields":
                for f in sec["fields"]:
                    if not f.get("formula"):
                        rock[f["name"]] = ws[f"{vcol}{f['row']}"].value
            else:
                typed = [c for c in sheets[sec["block"]]["columns"] if not c.get("formula")]
                headers = {}
                for cell in ws[sec["column_header_row"]]:
                    if cell.value is not None:
                        headers[str(cell.value).strip()] = cell.column
                rows = []
                for r in range(sec["first_row"], sec["first_row"] + sec["capacity"]):
                    row = {}
                    for c in typed:
                        col = headers.get(c["label"]) or headers.get(c["name"])
                        row[c["name"]] = ws.cell(row=r, column=col).value if col else None
                    rows.append(row if any(v not in (None, "") for v in row.values()) else {})
                rock[sec["block"]] = rows
        rocks.append(rock)
    return rocks


if __name__ == "__main__":
    import sys

    src = sys.argv[1]
    rocks = rocks_from_workbook(src) if src.endswith(".xlsx") else rocks_from_json(src)
    model = build_model(rocks, dt.date.today(), schema=load_schema())
    print(json.dumps(model, default=str, indent=1))
