from pathlib import Path

import collect_links as C

PAGE_A = """# Page A

> **In one sentence:** x

## Body

See **[Building agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — why.
Also a [local ref](b.md).

## Sources

- **[OWASP Top 10](https://genai.owasp.org/llm-top-10/)** (OWASP) — taxonomy.
"""

PAGE_B = """# Page B

## Sources

- **[Building agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — reused here too.
"""


def _repository(tmp_path: Path) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text(PAGE_A, encoding="utf-8")
    (tmp_path / "docs" / "b.md").write_text(PAGE_B, encoding="utf-8")
    return tmp_path


def test_dedupe_across_pages(tmp_path):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    entries = C.collect(root, out)
    url = "https://www.anthropic.com/research/building-effective-agents"
    assert url in entries
    pages = {u.page for u in entries[url].usages}
    assert pages == {"docs/a.md", "docs/b.md"}


def test_publisher_parsed(tmp_path):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    entries = C.collect(root, out)
    assert entries["https://genai.owasp.org/llm-top-10/"].publisher == "OWASP"


def test_internal_links_are_ignored(tmp_path):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    entries = C.collect(root, out)
    assert all(C._is_external(u) for u in entries)  # b.md relative link dropped
    assert "b.md" not in entries


def test_domain_grouping_in_render(tmp_path):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    content = C.render(C.collect(root, out), out, root)
    assert "## anthropic.com" in content
    assert "## genai.owasp.org" in content or "## owasp.org" in content
    assert C.BANNER in content
    assert "cross-reference" not in content.lower()


def test_check_detects_drift(tmp_path, capsys):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    # No file yet -> drift.
    assert C.main(["--root", str(root), "--check"]) == 1
    # Generate, then check -> clean.
    assert C.main(["--root", str(root)]) == 0
    assert C.main(["--root", str(root), "--check"]) == 0


def test_generated_page_not_self_harvested(tmp_path):
    root = _repository(tmp_path)
    out = root / "docs" / "link-collection.md"
    C.main(["--root", str(root)])
    # Re-collect: links inside the generated page must not appear as new entries
    # beyond what the source pages provide (idempotent regeneration).
    assert C.main(["--root", str(root), "--check"]) == 0
