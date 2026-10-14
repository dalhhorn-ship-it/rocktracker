"""Layer 6: the handoff package is complete and PORTAL_BUILD.md covers the whole spec."""
import json
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
import build_handoff  # noqa: E402

FILES = ["README.md", "PORTAL_BUILD.md", "DESIGN_SYSTEM.md"]


@pytest.fixture(scope="module")
def package(tmp_path_factory, schema):
    out = tmp_path_factory.mktemp("handoff") / "pkg"
    build_handoff.main(["--skip-tests", "--out", str(out)])
    return out


@pytest.fixture(scope="module")
def build_md(package):
    return (package / "PORTAL_BUILD.md").read_text()


def test_package_files(package, schema):
    names = {p.name for p in package.iterdir()}
    assert set(FILES) | {schema["deploy_file"].rsplit("/", 1)[-1]} <= names
    assert package.with_suffix(".zip").exists()


def test_build_file_covers_data_model(build_md, schema):
    for s in schema["sheets"]:
        assert f"tbl_{s['name']}" in build_md
        for c in s["columns"]:
            assert f"| {c['name']} |" in build_md, f"{s['name']}.{c['name']} missing"


def test_build_file_covers_portal_spec(build_md):
    spec = json.loads((ROOT / "portal" / "portal.spec.json").read_text())
    for status in spec["stage_map"]:
        assert f"| {status} |" in build_md
    for tab in spec["tabs"]:
        for text in [tab["question"], tab["headline"], tab["lede"]]:
            assert text in build_md
        for k in tab.get("kpis", []):
            assert f"| {k['label']} |" in build_md
        for ins in tab.get("insights", []):
            assert ins["question"] in build_md
        for ch in tab.get("charts", []):
            assert ch["title"] in build_md


def test_no_unresolved_placeholders(package):
    for name in ["README.md", "PORTAL_BUILD.md"]:
        text = (package / name).read_text()
        assert not build_handoff.re.search(r"\{\w+\}", text), f"placeholder left in {name}"
