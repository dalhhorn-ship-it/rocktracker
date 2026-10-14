"""Layer 4: the portal spec follows design/DESIGN_SYSTEM.md and matches the workbook."""
import json
import re
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
import portal_metrics as pm  # noqa: E402

STAGES = {"backlog", "progress", "review", "done"}


@pytest.fixture(scope="session")
def spec():
    return json.loads((ROOT / "portal" / "portal.spec.json").read_text())


@pytest.fixture(scope="session")
def content_tabs(spec):
    return [t for t in spec["tabs"] if t["question"] != "The full list"]


def columns(sheets, table):
    assert table in sheets, f"portal uses unknown table {table}"
    return {c["name"] for c in sheets[table]["columns"]}


def test_design_system_present(spec):
    assert (ROOT / spec["design_system"]).exists()
    tokens = (ROOT / spec["tokens"]).read_text()
    for token in ("--ink", "--accent", "--spot-bg", "--stage-done", "--cat-other"):
        assert token + ":" in tokens


def _css_block(css, start):
    i = css.index(start)
    j = css.index("{", i)
    depth, k = 0, j
    while True:
        depth += css[k] == "{"
        depth -= css[k] == "}"
        if depth == 0:
            return css[j + 1:k]
        k += 1


def _vars(block):
    return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", block))


def _lum(hex_):
    ch = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _contrast(a, b):
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_dark_mode_tokens():
    css = (ROOT / "design" / "tokens.css").read_text()
    light = _vars(_block_root(css))
    dark = _vars(_css_block(css, ':root[data-theme="dark"]'))
    auto = _vars(_css_block(css, ":root:not([data-theme=\"light\"])"))
    assert "--card" in light and "--card" in dark
    missing = set(light) - set(dark) - {"--brand-red"}
    assert not missing, f"no dark value for {sorted(missing)}"
    assert dark == auto, "prefers-color-scheme block must match the data-theme dark block"
    for mode, tokens in (("light", light), ("dark", dark)):
        for fg in ("--ink", "--ink-2", "--ink-3", "--muted", "--subtle", "--accent"):
            for bg in ("--bg", "--card"):
                ratio = _contrast(tokens[fg], tokens[bg])
                assert ratio >= 4.5, f"{mode} {fg} on {bg} is {ratio:.2f}"


def _block_root(css):
    return _css_block(css, ":root{")


def test_tabs_are_questions_with_full_list_last(spec, content_tabs):
    assert spec["tabs"][-1]["question"] == "The full list"
    assert len(content_tabs) == len(spec["tabs"]) - 1
    for tab in content_tabs:
        assert tab["question"].endswith("?"), tab["question"]


def test_section_intros(spec):
    for i, tab in enumerate(spec["tabs"], start=1):
        assert re.fullmatch(rf"Section {i:02d} · .+", tab["eyebrow"]), tab["eyebrow"]
        assert tab["headline"].endswith("."), tab["headline"]
        assert tab["lede"] and len(tab["lede"]) <= 160, "lede is one or two lines"


def test_overview_tab_anatomy(content_tabs):
    first = content_tabs[0]
    assert first.get("narrative"), "overview needs a narrative sentence"
    assert len(first.get("insights", [])) == 3
    assert len(first.get("kpis", [])) == 6


def test_cards_rules(content_tabs):
    for tab in content_tabs:
        assert len(tab.get("insights", [])) <= 3
        assert len(tab.get("kpis", [])) <= 6
        assert sum(bool(k.get("spotlight")) for k in tab.get("kpis", [])) <= 1, "one spotlight per row"
        for ins in tab.get("insights", []):
            assert ins["question"].endswith("?")
        for kpi in tab.get("kpis", []):
            assert kpi.get("sub"), f"KPI {kpi['id']} needs a sub line"
        for chart in tab.get("charts", []):
            assert chart["type"] in {"bar", "donut"}
            assert chart["color"] in {"stage", "categorical"}


def test_kpi_ids_unique_and_placeholders_resolve(spec):
    ids = [k["id"] for t in spec["tabs"] for k in t.get("kpis", [])]
    assert len(ids) == len(set(ids))
    texts = [t.get("narrative", "") for t in spec["tabs"]]
    texts += [i.get("text", "") for t in spec["tabs"] for i in t.get("insights", [])]
    texts += [k["sub"] for t in spec["tabs"] for k in t.get("kpis", [])]
    for text in texts:
        for name in pm.PLACEHOLDER.findall(text):
            assert name in ids, f"unknown placeholder {{{name}}} in: {text}"


def test_references_exist_in_schema(spec, sheets):
    for tab in spec["tabs"]:
        for kpi in tab.get("kpis", []):
            cols = columns(sheets, kpi["table"])
            assert set(kpi.get("where", {})) <= cols
            if "column" in kpi:
                assert kpi["column"] in cols
        for ins in tab.get("insights", []):
            if "list" in ins:
                lst = ins["list"]
                assert {lst["item"], lst.get("date", lst["item"])} | set(lst.get("where", {})) <= columns(sheets, lst["table"])
        for chart in tab.get("charts", []):
            assert chart["group_by"] in columns(sheets, chart["table"])
        if "table" in tab:
            assert set(tab["table"]["columns"]) <= columns(sheets, tab["table"]["table"])


def test_stage_map_covers_every_status(spec, rows):
    assert set(spec["stage_map"].values()) <= STAGES
    statuses = {r["Value"] for r in rows.get("lkp_Status", [])}
    assert statuses <= set(spec["stage_map"]), f"no stage colour for {statuses - set(spec['stage_map'])}"


def test_filters_use_allowed_values(spec, sheets, rows):
    for tab in spec["tabs"]:
        filters = [k for k in tab.get("kpis", [])] + [i["list"] for i in tab.get("insights", []) if "list" in i]
        for f in filters:
            for col, values in f.get("where", {}).items():
                meta = next(c for c in sheets[f["table"]]["columns"] if c["name"] == col)
                if "lookup" in meta:
                    target, target_col = meta["lookup"].split(".")
                    allowed = {r[target_col] for r in rows[target]}
                    assert set(values) <= allowed, f"{values} not in {meta['lookup']}"


def test_kpis_compute_on_workbook(spec, rows):
    values = pm.all_kpis(spec, rows)
    assert all(isinstance(v, (int, float)) for v in values.values())
