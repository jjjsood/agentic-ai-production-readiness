"""Tests for the hub-and-spoke architecture checks: page-type taxonomy,
overview sub-topic map / orphan detection, deep-dive breadcrumbs, and the
checklist / risk-register structural checks.
"""

from pathlib import Path

import verify_template as V
from repositorykit import pages as P


def codes(findings, level=None):
    return {f.code for f in findings if level is None or f.level == level}


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
HUB = """# Pillar — tagline

> **In one sentence:** The hub for this pillar.

Lead introducing the pillar.

---

## Why this fails when it's missing

The failure story.

## Core concepts

The concepts.

## Sub-topics

| Sub-topic | What it covers | Status |
|-----------|----------------|--------|
| **[Deep dive](deep.md)** | covers the thing | building |

## Where this connects

- Nothing yet.

---

## Sources

- **[Std](https://example.org/s)** (Org) — backs the claim.

<!-- page-type: overview -->
"""

DEEP = """# Deep Dive — tagline

> **In one sentence:** A focused sub-topic.

> Part of **[Pillar overview](README.md)**

Lead.

---

## Body

Text.

## Sources

- **[Std](https://example.org/s)** (Org) — backs the claim.

<!-- page-type: standard -->
"""


def _pillar(tmp_path: Path, hub: str = HUB, deeps: dict | None = None) -> Path:
    d = tmp_path / "docs" / "pillar"
    d.mkdir(parents=True)
    (d / "README.md").write_text(hub, encoding="utf-8")
    for name, text in (deeps or {"deep": DEEP}).items():
        (d / f"{name}.md").write_text(text, encoding="utf-8")
    return tmp_path


# --------------------------------------------------------------------------- #
# Page-type taxonomy
# --------------------------------------------------------------------------- #
def test_unknown_page_type_is_warning(tmp_path):
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "x.md"
    p.write_text("# X\n\n## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: bogus -->\n",
                 encoding="utf-8")
    assert "unknown-page-type" in codes(V.verify_page(p, tmp_path), V.WARNING)


def test_overview_type_is_known(tmp_path):
    root = _pillar(tmp_path)
    findings = V.verify_page(tmp_path / "docs" / "pillar" / "README.md", root)
    assert "unknown-page-type" not in codes(findings)


# --------------------------------------------------------------------------- #
# Overview: sub-topic map + orphan detection
# --------------------------------------------------------------------------- #
def test_overview_links_deep_dive_is_clean(tmp_path):
    root = _pillar(tmp_path)  # HUB links deep.md, deep.md exists
    findings = V.verify_page(tmp_path / "docs" / "pillar" / "README.md", root)
    assert [f for f in findings if f.level == V.ERROR] == []


def test_orphan_deep_dive_is_error(tmp_path):
    # An extra sibling the hub does not link to is an orphan.
    root = _pillar(tmp_path, deeps={"deep": DEEP, "orphan": DEEP})
    findings = V.verify_page(tmp_path / "docs" / "pillar" / "README.md", root)
    assert "orphan-page" in codes(findings, V.ERROR)
    assert any("orphan.md" in f.message for f in findings if f.code == "orphan-page")


def test_overview_mapping_nowhere_is_warning(tmp_path):
    hub = HUB.replace("| **[Deep dive](deep.md)** | covers the thing | building |\n", "")
    d = tmp_path / "docs" / "pillar"
    d.mkdir(parents=True)
    (d / "README.md").write_text(hub, encoding="utf-8")  # no siblings at all
    findings = V.verify_page(d / "README.md", tmp_path)
    assert "overview-no-map" in codes(findings, V.WARNING)


# --------------------------------------------------------------------------- #
# Deep-dive breadcrumb
# --------------------------------------------------------------------------- #
def test_deep_dive_with_breadcrumb_is_clean(tmp_path):
    root = _pillar(tmp_path)
    findings = V.verify_page(tmp_path / "docs" / "pillar" / "deep.md", root)
    assert "missing-breadcrumb" not in codes(findings)


def test_deep_dive_without_breadcrumb_is_warning(tmp_path):
    no_crumb = DEEP.replace("> Part of **[Pillar overview](README.md)**\n\n", "")
    root = _pillar(tmp_path, deeps={"deep": no_crumb})
    findings = V.verify_page(tmp_path / "docs" / "pillar" / "deep.md", root)
    assert "missing-breadcrumb" in codes(findings, V.WARNING)


def test_standard_page_without_overview_dir_skips_breadcrumb(tmp_path):
    # A standard page in a dir with no overview README must NOT be asked for a breadcrumb.
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "lonely.md"
    p.write_text("# Lonely\n\n## Sources\n- **[s](https://e.org)** (O) — y.\n", encoding="utf-8")
    assert "missing-breadcrumb" not in codes(V.verify_page(p, tmp_path))


# --------------------------------------------------------------------------- #
# Checklist + risk-register structural checks
# --------------------------------------------------------------------------- #
def test_checklist_with_boxes_is_clean(tmp_path):
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "cl.md"
    p.write_text("# CL\n\n## Items\n\n- [ ] A checkable control.\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: checklist -->\n",
                 encoding="utf-8")
    assert "checklist-no-boxes" not in codes(V.verify_page(p, tmp_path))


def test_checklist_with_checkbox_table_is_clean(tmp_path):
    # A checklist expressed as a ☐ table (no `- [ ]` bullets) must also pass.
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "cl.md"
    p.write_text("# CL\n\n## Items\n\n"
                 "| Done | Control | Pass criterion / metric | Source |\n"
                 "|------|---------|-------------------------|--------|\n"
                 "| ☐ | Token ceiling | Cost cap configured; run aborts on breach | [s](https://e.org) |\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: checklist -->\n",
                 encoding="utf-8")
    assert "checklist-no-boxes" not in codes(V.verify_page(p, tmp_path))


def test_checklist_without_boxes_is_warning(tmp_path):
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "cl.md"
    p.write_text("# CL\n\n## Items\n\nJust prose, no boxes.\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: checklist -->\n",
                 encoding="utf-8")
    assert "checklist-no-boxes" in codes(V.verify_page(p, tmp_path), V.WARNING)


def test_checklist_plain_table_without_checkbox_is_warning(tmp_path):
    # A table with no ☐/[ ] cell is not a checklist — still warns.
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "cl.md"
    p.write_text("# CL\n\n## Items\n\n"
                 "| Control | Metric |\n| --- | --- |\n| Token ceiling | cap set |\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: checklist -->\n",
                 encoding="utf-8")
    assert "checklist-no-boxes" in codes(V.verify_page(p, tmp_path), V.WARNING)


def test_risk_register_with_table_is_clean(tmp_path):
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "rr.md"
    p.write_text("# RR\n\n## Risks\n\n| # | Risk | Score |\n| --- | --- | --- |\n| 1 | x | 9 |\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: risk-register -->\n",
                 encoding="utf-8")
    assert "risk-register-no-table" not in codes(V.verify_page(p, tmp_path))


def test_risk_register_without_table_is_warning(tmp_path):
    (tmp_path / "docs").mkdir()
    p = tmp_path / "docs" / "rr.md"
    p.write_text("# RR\n\n## Risks\n\nNo table here.\n\n"
                 "## Sources\n- **[s](https://e.org)** (O) — y.\n\n<!-- page-type: risk-register -->\n",
                 encoding="utf-8")
    assert "risk-register-no-table" in codes(V.verify_page(p, tmp_path), V.WARNING)
