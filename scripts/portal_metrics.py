"""Compute portal KPIs, lists and chart series from workbook rows and portal/portal.spec.json.

Shared by the tests and the preview renderer so both use the same definitions.
"""
import datetime as dt
import re
from collections import Counter

PLACEHOLDER = re.compile(r"\{(\w+)\}")


def filter_rows(rows, where=None):
    where = where or {}
    return [r for r in rows if all(r.get(col) in allowed for col, allowed in where.items())]


def kpi_value(kpi, data):
    picked = filter_rows(data[kpi["table"]], kpi.get("where"))
    agg = kpi["agg"]
    if agg == "count":
        return len(picked)
    values = [r[kpi["column"]] for r in picked if r.get(kpi["column"]) not in (None, "")]
    if agg == "distinct":
        return len(set(values))
    if agg == "sum":
        return sum(values)
    if agg == "avg":
        return round(sum(values) / len(values), 1) if values else 0
    raise ValueError(f"unknown agg {agg}")


def all_kpis(spec, data):
    return {k["id"]: kpi_value(k, data) for tab in spec["tabs"] for k in tab.get("kpis", [])}


def fill(template, values, wrap=str):
    """Replace {kpi_id} placeholders. Unknown ids raise KeyError."""
    return PLACEHOLDER.sub(lambda m: wrap(values[m.group(1)]), template)


def list_items(spec_list, data):
    picked = filter_rows(data[spec_list["table"]], spec_list.get("where"))
    date_col = spec_list.get("date")
    if date_col:
        picked.sort(key=lambda r: r.get(date_col) or dt.date.max)
    return [(r[spec_list["item"]], r.get(date_col) if date_col else None) for r in picked[: spec_list.get("limit", 3)]]


def series(chart, data):
    counts = Counter(r.get(chart["group_by"]) or "Other" for r in data[chart["table"]])
    return sorted(counts.items(), key=lambda kv: (kv[0] == "Other", -kv[1]))


def fmt_date(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return f"{value.day} {value:%b %Y}"
    return "" if value is None else str(value)
