from pathlib import Path

import verify_template as V
from repositorykit import pages as P

GOOD_PAGE = """# Sample Page — tagline

> **In one sentence:** A well-formed page that follows the template spine.

Lead paragraph explaining what this page is and who it is for.

---

## Body Section

Some prose with a [valid relative link](other.md).

---

## Sources

- **[Some Standard](https://example.org/spec)** (Example Org) — backs the claim above.

## Read more

- **External:** **[More](https://example.org/more)** (Example Org) — further reading.
"""


def _repository(tmp_path: Path) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "other.md").write_text("# Other\n\n## Sources\n- x\n", encoding="utf-8")
    return tmp_path


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / "docs" / name
    path.write_text(text, encoding="utf-8")
    return path


def codes(findings, level=None):
    return {f.code for f in findings if level is None or f.level == level}


def test_good_page_is_clean(tmp_path):
    root = _repository(tmp_path)
    page = _write(tmp_path, "good.md", GOOD_PAGE)
    findings = V.verify_page(page, root)
    assert [f for f in findings if f.level == V.ERROR] == []


def test_missing_sources_is_error(tmp_path):
    root = _repository(tmp_path)
    page = _write(tmp_path, "nosrc.md", "# Page\n\nBody only, no sources.\n")
    assert "missing-sources" in codes(V.verify_page(page, root), V.ERROR)


def test_empty_sources_is_error(tmp_path):
    root = _repository(tmp_path)
    page = _write(tmp_path, "empty.md", "# Page\n\n## Sources\n\n<!-- nothing -->\n")
    assert "empty-sources" in codes(V.verify_page(page, root), V.ERROR)


def test_broken_relative_link_is_error(tmp_path):
    root = _repository(tmp_path)
    text = "# Page\n\n[dead](does-not-exist.md)\n\n## Sources\n- **[s](http://x.io)** (X) — y.\n"
    page = _write(tmp_path, "broken.md", text)
    assert "broken-link" in codes(V.verify_page(page, root), V.ERROR)


def test_link_into_tooling_layer_is_error(tmp_path):
    root = _repository(tmp_path)
    (tmp_path / "research").mkdir()
    (tmp_path / "research" / "note.md").write_text("x", encoding="utf-8")
    text = "# Page\n\n[oops](../research/note.md)\n\n## Sources\n- **[s](http://x.io)** (X) — y.\n"
    page = _write(tmp_path, "tooling.md", text)
    assert "links-tooling" in codes(V.verify_page(page, root), V.ERROR)


def test_absolute_link_is_error(tmp_path):
    root = _repository(tmp_path)
    text = "# Page\n\n[abs](/etc/passwd)\n\n## Sources\n- **[s](http://x.io)** (X) — y.\n"
    page = _write(tmp_path, "abs.md", text)
    assert "absolute-link" in codes(V.verify_page(page, root), V.ERROR)


def test_escapes_root_is_error(tmp_path):
    root = _repository(tmp_path)
    text = "# Page\n\n[up](../../outside.md)\n\n## Sources\n- **[s](http://x.io)** (X) — y.\n"
    page = _write(tmp_path, "escape.md", text)
    assert "escapes-root" in codes(V.verify_page(page, root), V.ERROR)


def test_missing_callout_is_warning_only(tmp_path):
    root = _repository(tmp_path)
    text = "# Page\n\nLead.\n\n## Body\n\nx\n\n## Sources\n- **[s](http://x.io)** (X) — y.\n"
    findings = V.verify_page(_write(tmp_path, "nocallout.md", text), root)
    assert "missing-callout" in codes(findings, V.WARNING)
    assert [f for f in findings if f.level == V.ERROR] == []


def test_excluded_page_is_skipped(tmp_path):
    root = _repository(tmp_path)
    # A page with no Sources would normally error, but exclusion skips all checks.
    page = _write(tmp_path, "skip.md", "# Off template\n\nno sources here\n")
    assert V.verify_page(page, root, excludes=["docs/skip.md"]) == []


def test_generated_banner_page_is_skipped(tmp_path):
    root = _repository(tmp_path)
    banner = f"<!-- {P.GENERATED_BANNER} -->\n# Gen\n\nno sources\n"
    page = _write(tmp_path, "link-collection.md", banner)
    assert V.verify_page(page, root) == []


# --------------------------------------------------------------------------- #
# Case study pages
# --------------------------------------------------------------------------- #
GOOD_CASE_STUDY = """# Runaway Agent — burned the budget

> **In one sentence:** No spend cap let an agent loop until the bill ballooned.

Lead describing the system and the agent's job.

---

## Agent Goal

The operator deployed an agent to do a job, optimising for an outcome.

## Context

What the agent did and at what scale.

## What happened

The incident in order.

## Failure mode

Missing spend limit — an infrastructure gap, not model quality.

## Mitigation

Add a hard per-run budget cap.

## Takeaways

- Cap spend per run.

## Sources

- **[Some Report](https://example.org/r)** (Example Org) — backs the incident.

<!-- page-type: case-study:failure -->
"""

# A success-type case study: core sections only, no failure-specific sections.
GOOD_SUCCESS = """# Shipped Agent — held the line under load

> **In one sentence:** Hard limits and tracing carried the deployment.

Lead describing the system.

---

## Agent Goal

The operator deployed an agent to do a job, optimising for an outcome.

## Context

What the agent did and at what scale.

## What happened

It ran for months without incident.

## What worked

Per-run budget caps and full request tracing.

## Takeaways

- Cap spend per run.

## Sources

- **[Some Report](https://example.org/r)** (Example Org) — backs the claim.

<!-- page-type: case-study:success -->
"""


def test_good_case_study_is_clean(tmp_path):
    root = _repository(tmp_path)
    page = _write(tmp_path, "case.md", GOOD_CASE_STUDY)
    findings = V.verify_page(page, root)
    assert [f for f in findings if f.level == V.ERROR] == []


def test_success_type_with_core_only_is_clean(tmp_path):
    # No "Failure mode"/"Mitigation" — those are optional, type-specific.
    root = _repository(tmp_path)
    page = _write(tmp_path, "success.md", GOOD_SUCCESS)
    findings = V.verify_page(page, root)
    assert [f for f in findings if f.level == V.ERROR] == []


def test_missing_core_section_is_error(tmp_path):
    root = _repository(tmp_path)
    text = GOOD_CASE_STUDY.replace("## Context\n\nWhat the agent did and at what scale.\n\n", "")
    page = _write(tmp_path, "case2.md", text)
    findings = V.verify_page(page, root)
    assert "case-study-missing-section" in codes(findings, V.ERROR)


def test_optional_type_section_not_required(tmp_path):
    # Dropping the failure-only "Mitigation" section must NOT error.
    root = _repository(tmp_path)
    text = GOOD_CASE_STUDY.replace("## Mitigation\n\nAdd a hard per-run budget cap.\n\n", "")
    page = _write(tmp_path, "case3.md", text)
    assert "case-study-missing-section" not in codes(V.verify_page(page, root), V.ERROR)


def test_unknown_subtype_is_warning(tmp_path):
    root = _repository(tmp_path)
    text = GOOD_CASE_STUDY.replace("case-study:failure", "case-study:bogus")
    page = _write(tmp_path, "case4.md", text)
    findings = V.verify_page(page, root)
    assert "case-study-unknown-type" in codes(findings, V.WARNING)


def test_standard_page_skips_case_study_checks(tmp_path):
    root = _repository(tmp_path)
    # GOOD_PAGE has no incident sections but is not a case-study page -> no section errors.
    page = _write(tmp_path, "std.md", GOOD_PAGE)
    assert "case-study-missing-section" not in codes(V.verify_page(page, root))


def test_marker_not_at_end_is_warning(tmp_path):
    root = _repository(tmp_path)
    text = GOOD_CASE_STUDY.replace(
        "<!-- page-type: case-study:failure -->\n",
        "<!-- page-type: case-study:failure -->\n\nTrailing text after the marker.\n",
    )
    page = _write(tmp_path, "case5.md", text)
    findings = V.verify_page(page, root)
    assert "marker-not-at-end" in codes(findings, V.WARNING)


def test_page_type_defaults_to_standard(tmp_path):
    root = _repository(tmp_path)
    page = P.parse(_write(tmp_path, "notype.md", GOOD_PAGE), root)
    assert P.page_type(page) == "standard"
