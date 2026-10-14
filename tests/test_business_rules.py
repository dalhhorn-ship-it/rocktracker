"""Layer 3: business rules ("Computed rules" in docs/ARCHITECTURE.md) against the Python mirror
scripts/rock_model.py. All fixtures are built here, with today frozen, so the tests do not
depend on sample data."""
import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import rock_model as rm  # noqa: E402

TODAY = dt.date(2026, 10, 14)  # Q4 2026: quarter 2026-10-01..2026-12-31, window to 2027-03-31
STEERCOS = ["2026-09-01", "2026-10-28", "2026-12-02"]


def rock(**kw):
    base = dict(RockID="R01", RockName="Checkout", ValueChain="Buy", Lead="Alex Example",
                GPM="Sam Example", Active="Yes", Purpose="p", UpdateDate="2026-10-10",
                State="On track", MainMessage="m", PositionsPlanned=4, PositionsFilled=3)
    base.update(kw)
    return base


def model(*rocks, today=TODAY, steercos=STEERCOS):
    return rm.build_model(list(rocks), today, steercos)


def epic(**kw):
    base = dict(Title="E", Commitment="Committed", PlannedDate="2026-11-30")
    base.update(kw)
    return base


def epic_of(**kw):
    """Compute one epic through a rock and return its consolidated row."""
    return model(rock(Epics=[epic(**kw)]))["Epics"][0]


def strip_of(**kw):
    return model(rock(**kw))["Rocks"][0]


# ------------------------------------------------------------------ params
def test_params_quarter_and_window():
    p = rm.params(TODAY, STEERCOS)
    assert p["QuarterStart"] == dt.date(2026, 10, 1)
    assert p["QuarterEnd"] == dt.date(2026, 12, 31)
    assert p["WindowEnd"] == dt.date(2027, 3, 31)
    assert p["NextSteerco"] == dt.date(2026, 10, 28)


def test_next_steerco_today_counts_and_none_when_absent():
    assert rm.params(dt.date(2026, 10, 28), STEERCOS)["NextSteerco"] == dt.date(2026, 10, 28)
    assert rm.params(dt.date(2027, 1, 1), STEERCOS)["NextSteerco"] is None


@pytest.mark.parametrize("today,qs,we", [
    (dt.date(2026, 1, 1), dt.date(2026, 1, 1), dt.date(2026, 6, 30)),
    (dt.date(2026, 3, 31), dt.date(2026, 1, 1), dt.date(2026, 6, 30)),
    (dt.date(2026, 4, 1), dt.date(2026, 4, 1), dt.date(2026, 9, 30)),
    (dt.date(2026, 12, 31), dt.date(2026, 10, 1), dt.date(2027, 3, 31)),
])
def test_window_on_quarter_boundaries(today, qs, we):
    p = rm.params(today)
    assert p["WindowStart"] == qs and p["WindowEnd"] == we


# ------------------------------------------------------------------ epic status
def test_status_committed_on_plan_default():
    assert epic_of()["Status"] == "On plan"


def test_status_empty_forecast_is_on_plan():
    assert epic_of(ForecastDate=None)["Status"] == "On plan"


def test_status_forecast_equal_or_earlier_is_on_plan():
    assert epic_of(ForecastDate="2026-11-30")["Status"] == "On plan"
    assert epic_of(ForecastDate="2026-11-01")["Status"] == "On plan"


def test_status_slipped_and_slip_weeks():
    e = epic_of(ForecastDate="2026-12-14")
    assert e["Status"] == "Slipped"
    assert e["SlipWeeks"] == 2.0


def test_slip_weeks_one_decimal_and_blank_when_not_slipped():
    assert epic_of(ForecastDate="2026-12-03")["SlipWeeks"] == 0.4
    assert epic_of()["SlipWeeks"] == ""


def test_status_empty_planned_never_slips():
    assert epic_of(PlannedDate=None, ForecastDate="2026-12-14")["Status"] == "On plan"


def test_status_on_watch_when_on_plan():
    assert epic_of(LeadStatus="On watch")["Status"] == "On watch"


def test_slipped_beats_on_watch():
    assert epic_of(LeadStatus="On watch", ForecastDate="2026-12-14")["Status"] == "Slipped"


def test_delivered_beats_slipped():
    assert epic_of(LeadStatus="Delivered", ForecastDate="2026-12-14")["Status"] == "Delivered"


def test_on_hold_beats_slipped_and_not_committed():
    assert epic_of(LeadStatus="On hold", ForecastDate="2026-12-14")["Status"] == "On hold"
    assert epic_of(LeadStatus="On hold", Commitment="Choice point")["Status"] == "On hold"


def test_delivered_beats_not_committed():
    assert epic_of(LeadStatus="Delivered", Commitment="Choice point")["Status"] == "Delivered"


@pytest.mark.parametrize("commitment", ["Choice point", "Not committed", ""])
def test_not_committed_including_empty_commitment(commitment):
    e = epic_of(Commitment=commitment, ForecastDate="2026-12-14")
    assert e["Status"] == "Not committed"
    assert e["SlipWeeks"] == ""


def test_on_watch_flag_ignored_when_not_committed():
    assert epic_of(Commitment="Choice point", LeadStatus="On watch")["Status"] == "Not committed"


# ------------------------------------------------------------------ in window / overdue
@pytest.mark.parametrize("planned,forecast,expected", [
    ("2026-10-01", None, "Yes"),    # window start
    ("2026-09-30", None, "No"),     # day before
    ("2027-03-31", None, "Yes"),    # window end
    ("2027-04-01", None, "No"),     # day after
    ("2026-09-30", "2026-10-01", "Yes"),   # forecast inside saves it
    ("2027-03-31", "2027-04-01", "Yes"),   # planned inside
    (None, None, "No"),
    (None, "2026-11-01", "Yes"),
])
def test_in_window_edges(planned, forecast, expected):
    assert epic_of(PlannedDate=planned, ForecastDate=forecast)["InWindow"] == expected


def test_overdue_uses_forecast_else_planned():
    assert epic_of(PlannedDate="2026-10-13")["Overdue"] == "Yes"
    assert epic_of(PlannedDate="2026-10-13", ForecastDate="2026-10-20")["Overdue"] == "No"
    assert epic_of(PlannedDate="2026-11-30", ForecastDate="2026-10-01")["Overdue"] == "Yes"


def test_overdue_today_is_not_overdue():
    assert epic_of(PlannedDate="2026-10-14")["Overdue"] == "No"


def test_overdue_excludes_delivered_on_hold_not_committed_and_no_dates():
    assert epic_of(PlannedDate="2026-10-01", LeadStatus="Delivered")["Overdue"] == "No"
    assert epic_of(PlannedDate="2026-10-01", LeadStatus="On hold")["Overdue"] == "No"
    assert epic_of(PlannedDate="2026-10-01", Commitment="Not committed")["Overdue"] == "No"
    assert epic_of(PlannedDate=None)["Overdue"] == "No"


# ------------------------------------------------------------------ risks
@pytest.mark.parametrize("lk,im,score,high", [
    ("Low", "Low", 1, "No"), ("Medium", "Medium", 4, "No"), ("High", "Low", 3, "No"),
    ("Medium", "High", 6, "Yes"), ("High", "Medium", 6, "Yes"), ("High", "High", 9, "Yes"),
])
def test_risk_score_and_high(lk, im, score, high):
    r = model(rock(Risks=[dict(Title="x", Likelihood=lk, Impact=im)]))["Risks"][0]
    assert (r["Score"], r["High"]) == (score, high)


def test_risk_without_impact_has_no_score_and_is_not_high():
    r = model(rock(Risks=[dict(Title="x", Likelihood="High")]))["Risks"][0]
    assert r["Score"] == "" and r["High"] == "No" and r["NeedsAction"] == "No"


def test_needs_action_when_high_without_action_or_owner():
    base = dict(Title="x", Likelihood="High", Impact="High")
    rows = model(rock(Risks=[
        base,
        dict(base, KeyAction="a"),
        dict(base, ActionOwner="o"),
        dict(base, KeyAction="a", ActionOwner="o"),
    ]))["Risks"]
    assert [r["NeedsAction"] for r in rows] == ["Yes", "Yes", "Yes", "No"]


def test_closed_high_risk_needs_no_action_and_is_not_open():
    risks = [dict(Title="x", Likelihood="High", Impact="High", RiskStatus="Closed")]
    m = model(rock(Risks=risks))
    assert m["Risks"][0]["NeedsAction"] == "No"
    assert m["Rocks"][0]["OpenHighRisks"] == 0 and m["Rocks"][0]["HighRisksNoAction"] == 0


def test_empty_risk_status_counts_as_open():
    risks = [dict(Title="x", Likelihood="High", Impact="High", KeyAction="a", ActionOwner="o")]
    s = model(rock(Risks=risks))["Rocks"][0]
    assert s["OpenHighRisks"] == 1 and s["HighRisksNoAction"] == 0


def test_low_risk_does_not_need_action():
    r = model(rock(Risks=[dict(Title="x", Likelihood="Low", Impact="Low")]))["Risks"][0]
    assert r["NeedsAction"] == "No"


# ------------------------------------------------------------------ strip counts
def test_epics_counts_x_of_y_and_delivered_never_lowers_ratio():
    epics = [
        epic(Title="a"),                                   # on plan
        epic(Title="b", LeadStatus="On watch"),            # on watch
        epic(Title="c", ForecastDate="2026-12-20"),        # slipped
        epic(Title="d", LeadStatus="Delivered"),           # delivered
        epic(Title="e", Commitment="Choice point"),        # not counted
        epic(Title="f", LeadStatus="On hold"),             # committed? hold is status, not counted as OnPlan
        epic(Title="g", PlannedDate="2028-01-01"),         # outside window
    ]
    s = strip_of(Epics=epics)
    assert s["EpicsCommitted"] == 5     # a b c d f
    assert s["EpicsSlipped"] == 1
    assert s["EpicsOnPlan"] == 3        # a b d
    assert s["EpicsDelivered"] == 1


def test_epics_on_plan_counts_delivered_so_ratio_is_stable():
    e = [epic(Title="a"), epic(Title="b")]
    before = strip_of(Epics=e)
    e[1]["LeadStatus"] = "Delivered"
    after = strip_of(Epics=e)
    assert (before["EpicsOnPlan"], before["EpicsCommitted"]) == (2, 2)
    assert (after["EpicsOnPlan"], after["EpicsCommitted"]) == (2, 2)


def test_empty_rock_has_real_zero_counts():
    s = strip_of()
    for c in ("EpicsCommitted", "EpicsSlipped", "EpicsOnPlan", "EpicsDelivered",
              "OpenHighRisks", "HighRisksNoAction"):
        assert s[c] == 0


def test_positions_are_typed_and_zero_survives():
    s = strip_of(PositionsPlanned=0, PositionsFilled=0)
    assert s["PositionsPlanned"] == 0 and s["PositionsFilled"] == 0
    s = strip_of(PositionsPlanned=None)
    assert s["PositionsPlanned"] == ""


# ------------------------------------------------------------------ update age, stale
def test_update_age_and_stale_edges():
    assert strip_of(UpdateDate="2026-10-14")["UpdateAgeDays"] == 0
    s = strip_of(UpdateDate="2026-09-30")  # exactly 14 days
    assert s["UpdateAgeDays"] == 14 and s["Stale"] == "No"
    s = strip_of(UpdateDate="2026-09-29")  # 15 days
    assert s["UpdateAgeDays"] == 15 and s["Stale"] == "Yes"


def test_empty_update_date_is_stale_with_empty_age():
    s = strip_of(UpdateDate=None)
    assert s["UpdateAgeDays"] == "" and s["Stale"] == "Yes"


# ------------------------------------------------------------------ data signal, check the call
def test_signal_on_track_for_empty_rock():
    s = strip_of()
    assert s["DataSignal"] == "On track" and s["CheckCall"] == "No"


def test_signal_at_risk_when_slipped_epic_still_inside_quarter():
    s = strip_of(Epics=[epic(PlannedDate="2026-11-30", ForecastDate="2026-12-31")])
    assert s["DataSignal"] == "At risk"


def test_signal_off_track_when_forecast_after_quarter_end():
    s = strip_of(Epics=[epic(PlannedDate="2026-11-30", ForecastDate="2027-01-01")])
    assert s["DataSignal"] == "Off track"


def test_signal_off_track_needs_planned_in_current_quarter():
    s = strip_of(Epics=[epic(PlannedDate="2027-01-15", ForecastDate="2027-03-01")])
    assert s["DataSignal"] == "At risk"  # slipped, in window, but planned next quarter


def test_signal_off_track_quarter_edges():
    on_edge = strip_of(Epics=[epic(PlannedDate="2026-12-31", ForecastDate="2027-01-01")])
    assert on_edge["DataSignal"] == "Off track"
    start = strip_of(Epics=[epic(PlannedDate="2026-10-01", ForecastDate="2027-01-01")])
    assert start["DataSignal"] == "Off track"
    prev = strip_of(Epics=[epic(PlannedDate="2026-09-30", ForecastDate="2027-01-01")])
    assert prev["DataSignal"] == "At risk"  # planned before the quarter, in window via forecast


def test_signal_at_risk_from_high_risk_without_action():
    s = strip_of(Risks=[dict(Title="x", Likelihood="High", Impact="High")])
    assert s["DataSignal"] == "At risk"
    s = strip_of(Risks=[dict(Title="x", Likelihood="High", Impact="High",
                             KeyAction="a", ActionOwner="o")])
    assert s["DataSignal"] == "On track"


def test_signal_ignores_delivered_slip_and_uncommitted():
    e = [epic(LeadStatus="Delivered", ForecastDate="2027-06-01"),
         epic(Commitment="Choice point", ForecastDate="2027-06-01")]
    assert strip_of(Epics=e)["DataSignal"] == "On track"


@pytest.mark.parametrize("state,expected", [
    ("On track", "Yes"), ("At risk", "Yes"), ("Off track", "No"),
])
def test_check_call_when_signal_off_track(state, expected):
    s = strip_of(State=state, Epics=[epic(PlannedDate="2026-11-30", ForecastDate="2027-02-01")])
    assert s["DataSignal"] == "Off track" and s["CheckCall"] == expected


def test_check_call_data_better_than_state_is_no():
    assert strip_of(State="Off track")["CheckCall"] == "No"


def test_check_call_empty_without_state():
    assert strip_of(State=None)["CheckCall"] == ""


# ------------------------------------------------------------------ decisions
def decisions(*ds, **rockkw):
    return model(rock(Decisions=list(ds), **rockkw))["Decisions"]


def test_decision_state_requested_until_outcome():
    a, b = decisions(dict(Decision="d1"), dict(Decision="d2", Outcome="Go"))
    assert (a["DecisionState"], b["DecisionState"]) == ("Requested", "Decided")


def test_due_next_steerco_by_steerco_date_or_decide_by():
    rows = decisions(
        dict(Decision="a", SteercoDate="2026-10-28"),                        # raised for next
        dict(Decision="b", SteercoDate="2026-12-02", DecideBy="2026-10-28"),  # due by next
        dict(Decision="c", SteercoDate="2026-12-02", DecideBy="2026-10-27"),  # earlier than next
        dict(Decision="d", SteercoDate="2026-12-02", DecideBy="2026-10-29"),  # after next
        dict(Decision="e", SteercoDate="2026-12-02"),                        # later steerco
        dict(Decision="f", SteercoDate="2026-10-28", Outcome="Go"),          # decided
    )
    assert [r["DueNextSteerco"] for r in rows] == ["Yes", "Yes", "Yes", "No", "No", "No"]


def test_due_next_steerco_no_future_steerco():
    rows = rm.build_model([rock(Decisions=[dict(Decision="a", SteercoDate="2026-10-28",
                                                 DecideBy="2026-01-01")])],
                          TODAY, steercos=["2026-01-01"])["Decisions"]
    assert rows[0]["DueNextSteerco"] == "No"


def test_due_next_steerco_empty_dates_not_due():
    assert decisions(dict(Decision="a"))[0]["DueNextSteerco"] == "No"


def test_open_follow_up_rules():
    rows = decisions(
        dict(Decision="a"),                                                # requested
        dict(Decision="b", Outcome="Go"),                                  # empty follow up
        dict(Decision="c", Outcome="Go", FollowUp="Open"),
        dict(Decision="d", Outcome="Go", FollowUp="Closed"),
    )
    assert [r["OpenFollowUp"] for r in rows] == ["No", "Yes", "Yes", "No"]


def test_requested_decision_with_closed_follow_up_is_not_open_follow_up():
    assert decisions(dict(Decision="a", FollowUp="Closed"))[0]["OpenFollowUp"] == "No"


# ------------------------------------------------------------------ consolidation filter
def test_keys_use_slot_numbers_including_gaps():
    m = model(rock(Epics=[epic(Title="a"), {}, epic(Title="c")]))
    assert [e["EpicKey"] for e in m["Epics"]] == ["R01-E01", "R01-E03"]


def test_row_without_title_is_dropped_everywhere():
    m = model(rock(
        Epics=[epic(Title="")], Risks=[dict(Likelihood="High", Impact="High")],
        CallOuts=[dict(Date="2026-11-01")], Decisions=[dict(Outcome="Go")]))
    assert m["Epics"] == [] and m["Risks"] == [] and m["CallOuts"] == [] and m["Decisions"] == []


def test_inactive_rock_keeps_decisions_only():
    m = model(rock(
        Active="No", Epics=[epic()], Risks=[dict(Title="r", Likelihood="High", Impact="High")],
        CallOuts=[dict(Text="c")], Decisions=[dict(Decision="d", Outcome="Go")]))
    assert m["Epics"] == [] and m["Risks"] == [] and m["CallOuts"] == []
    assert [d["DecisionKey"] for d in m["Decisions"]] == ["R01-D01"]
    assert m["Decisions"][0]["Rock"] == "Checkout"


def test_empty_active_counts_as_inactive():
    assert model(rock(Active=None, Epics=[epic()]))["Epics"] == []


def test_rock_without_id_contributes_nothing():
    m = model(rock(RockID=None, Epics=[epic()], Decisions=[dict(Decision="d")]))
    assert all(v == [] for v in m.values())


def test_rock_template_style_empty_tab_contributes_nothing():
    assert all(v == [] for v in model({}).values())


def test_inactive_rock_stays_in_rocks_with_active_no():
    s = strip_of(Active="No", Epics=[epic(ForecastDate="2027-01-01")])
    assert s["Active"] == "No"
    assert s["EpicsCommitted"] == 0 and s["DataSignal"] == "On track"


def test_rows_copy_rock_profile_and_follow_tab_order():
    m = model(rock(Epics=[epic(Title="a")]),
              rock(RockID="R02", RockName="Search", GPM="Jo Example", Epics=[epic(Title="b")]))
    assert [(e["EpicKey"], e["Rock"], e["GPM"]) for e in m["Epics"]] == [
        ("R01-E01", "Checkout", "Sam Example"), ("R02-E01", "Search", "Jo Example")]
    assert [r["RockID"] for r in m["Rocks"]] == ["R01", "R02"]


def test_blank_cells_come_out_empty_not_none_in_text_columns():
    e = model(rock(Epics=[epic()]))["Epics"][0]
    assert e["Comment"] == "" and e["LeadStatus"] == ""


# ------------------------------------------------------------------ schema alignment
def test_model_columns_match_schema_order():
    schema = rm.load_schema()
    m = rm.build_model([rock(Epics=[epic()], Risks=[dict(Title="r")], CallOuts=[dict(Text="c")],
                             Decisions=[dict(Decision="d")])], TODAY, STEERCOS, schema=schema)
    for sheet, rows in m.items():
        cols = [c["name"] for c in next(s for s in schema["sheets"] if s["name"] == sheet)["columns"]]
        assert rows, sheet
        assert list(rows[0]) == cols


def test_every_formula_column_is_mirrored():
    """Every schema formula column on a consolidated sheet is produced by the model."""
    schema = rm.load_schema()
    m = rm.build_model([rock(Epics=[epic()], Risks=[dict(Title="r")], CallOuts=[dict(Text="c")],
                             Decisions=[dict(Decision="d")])], TODAY, STEERCOS)
    for s in schema["sheets"]:
        if s["kind"] != "consolidated":
            continue
        for c in s["columns"]:
            assert c["name"] in m[s["name"]][0], f"{s['name']}.{c['name']} not mirrored"


# ------------------------------------------------------------------ workbook loader
def test_loader_reads_rock_tab_by_schema_layout(tmp_path):
    from openpyxl import Workbook
    schema = rm.load_schema()
    rt = schema["rock_tab"]
    wb = Workbook()
    wb.active.title = rt["template_sheet"]
    ws = wb.create_sheet("R01 Checkout")
    wb.create_sheet(rt["end_sheet"])
    sheets = {s["name"]: s for s in schema["sheets"]}
    vals = {"RockID": "R01", "RockName": "Checkout", "Active": "Yes", "State": "At risk",
            "UpdateDate": dt.datetime(2026, 10, 10), "PositionsPlanned": 4, "PositionsFilled": 0}
    for sec in rt["sections"]:
        if sec["kind"] == "fields":
            for f in sec["fields"]:
                if f["name"] in vals:
                    ws[f"{rt['value_column']}{f['row']}"] = vals[f["name"]]
        else:
            typed = [c for c in sheets[sec["block"]]["columns"] if not c.get("formula")]
            for i, c in enumerate(typed, 2):
                ws.cell(row=sec["column_header_row"], column=i, value=c["label"])
            if sec["block"] == "Epics":
                for i, c in enumerate(typed, 2):
                    v = {"Title": "E1", "Commitment": "Committed",
                         "PlannedDate": dt.datetime(2026, 11, 30)}.get(c["name"])
                    ws.cell(row=sec["first_row"], column=i, value=v)
    path = tmp_path / "t.xlsx"
    wb.save(path)
    rocks = rm.rocks_from_workbook(path, schema)
    assert len(rocks) == 1 and len(rocks[0]["Epics"]) == 15
    m = rm.build_model(rocks, TODAY, STEERCOS)
    assert m["Epics"][0]["EpicKey"] == "R01-E01" and m["Epics"][0]["Status"] == "On plan"
    assert m["Rocks"][0]["PositionsFilled"] == 0
