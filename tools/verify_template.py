#!/usr/bin/env python3
"""Tool 1 — verify repository pages follow the shared page template.

Errors (fail the run):
  * missing or empty ``## Sources`` section
  * a ``page-type: case-study`` page missing a core section (Context/What happened/Takeaways)
  * broken relative link (target not on disk)
  * link into the tooling layer (research/, research-toolkit/, .claude/, tools/, CLAUDE.md)
  * absolute filesystem path, or a relative link escaping the repository root

Warnings (informational unless ``--strict``):
  * spine order off (H1 -> callout -> lead -> body H2s -> Sources -> Read more)
  * missing the ``> **In one sentence:**`` callout
  * a ``page-type`` marker that is not the last line of the page
  * a case-study page with an unrecognised subtype (not failure/success/demo)
  * a Sources/Read more line with no markdown link in it

Run from anywhere:  python tools/verify_template.py [--root PATH] ...
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repositorykit import pages as P  # noqa: E402

ERROR = "error"
WARNING = "warning"

# Core H2 sections every ``case-study`` page must carry, regardless of subtype (case-insensitive,
# exact text). ``Sources`` is required on every page already, so it is checked separately. Each
# subtype (failure/success/demo) adds its own *optional* sections — those are documented in the
# template, not enforced here, so a case study stays flexible.
CASE_STUDY_CORE = ("Agent Goal", "Context", "What happened", "Takeaways")

# Known case-study subtypes (the part after ``case-study:``). A bare ``case-study`` is allowed;
# an unrecognised subtype is flagged so typos don't slip through.
CASE_STUDY_TYPES = {"failure", "success", "demo"}


@dataclass
class Finding:
    path: str
    line: int
    level: str
    code: str
    message: str


# --------------------------------------------------------------------------- #
# Section helpers
# --------------------------------------------------------------------------- #
def _section_body(page: P.ParsedPage, title: str) -> list[str] | None:
    """Lines under the ``## {title}`` heading up to the next heading, or None."""
    start = None
    for idx, line in enumerate(page.lines):
        if line.strip().lower() == f"## {title}".lower():
            start = idx
            break
    if start is None:
        return None
    body: list[str] = []
    for line in page.lines[start + 1 :]:
        stripped = line.lstrip()
        if stripped.startswith("# ") or stripped.startswith("## "):
            break
        body.append(line)
    return body


def _is_meaningful(line: str) -> bool:
    s = line.strip()
    return bool(s) and not s.startswith("<!--")


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #
def _check_sources(page: P.ParsedPage) -> list[Finding]:
    body = _section_body(page, "Sources")
    if body is None:
        return [Finding(page.rel, -1, ERROR, "missing-sources",
                        "no `## Sources` section")]
    if not any(_is_meaningful(l) for l in body):
        line = next((h.line for h in page.headings
                     if h.level == 2 and h.text.lower() == "sources"), -1)
        return [Finding(page.rel, line, ERROR, "empty-sources",
                        "`## Sources` section is empty")]
    return []


def _check_links(page: P.ParsedPage) -> list[Finding]:
    findings: list[Finding] = []
    for link in page.links:
        url = link.url.strip()
        if not url or url.startswith(("http://", "https://", "mailto:", "#")):
            continue  # external / pure anchor — not disk-checked
        target = url.split("#", 1)[0]
        if not target:
            continue
        if target.startswith("/"):
            findings.append(Finding(page.rel, link.line, ERROR, "absolute-link",
                                    f"absolute path link `{url}`"))
            continue
        resolved = (page.path.parent / target).resolve()
        try:
            rel = resolved.relative_to(page.root)
        except ValueError:
            findings.append(Finding(page.rel, link.line, ERROR, "escapes-root",
                                    f"link escapes the repository root `{url}`"))
            continue
        parts = rel.parts
        if (parts and parts[0] in P.LAYER_EXCLUDE_DIRS) or rel.name in P.LAYER_EXCLUDE_FILES:
            findings.append(Finding(page.rel, link.line, ERROR, "links-tooling",
                                    f"repository page links into the tooling layer `{url}`"))
            continue
        if not resolved.exists():
            findings.append(Finding(page.rel, link.line, ERROR, "broken-link",
                                    f"relative link target missing `{url}`"))
    return findings


def _check_spine(page: P.ParsedPage) -> list[Finding]:
    findings: list[Finding] = []
    h = page.headings

    if not h or h[0].level != 1:
        findings.append(Finding(page.rel, h[0].line if h else 1, WARNING,
                                "spine-h1", "page should open with a single H1"))

    if not any(l.lstrip().startswith("> **In one sentence:**") for l in page.lines):
        findings.append(Finding(page.rel, 1, WARNING, "missing-callout",
                                "no `> **In one sentence:**` callout (minimal variant?)"))

    h2 = [x for x in h if x.level == 2]
    titles = [x.text.lower() for x in h2]
    if "sources" in titles:
        si = titles.index("sources")
        trailing = {"sources", "read more"}
        for later in titles[si + 1 :]:
            if later not in trailing:
                line = next(x.line for x in h2 if x.text.lower() == "sources")
                findings.append(Finding(page.rel, line, WARNING, "sources-not-last",
                                        "`## Sources` should come after the body sections"))
                break
        if "read more" in titles and titles.index("read more") < si:
            findings.append(Finding(page.rel, h2[titles.index("read more")].line,
                                    WARNING, "readmore-order",
                                    "`## Read more` should come after `## Sources`"))
    return findings


def _check_source_lines(page: P.ParsedPage) -> list[Finding]:
    findings: list[Finding] = []
    for title in ("Sources", "Read more"):
        body = _section_body(page, title)
        if not body:
            continue
        # body lines have no absolute line numbers; report against the heading.
        line = next((x.line for x in page.headings
                     if x.level == 2 and x.text.lower() == title.lower()), -1)
        for raw in body:
            s = raw.strip()
            if s.startswith(("-", "*")) and "](" not in s:
                findings.append(Finding(page.rel, line, WARNING, "source-line-format",
                                        f"`## {title}` item has no markdown link: {s[:60]}"))
    return findings


def _check_case_study(page: P.ParsedPage) -> list[Finding]:
    """A ``case-study`` page must carry the core sections; the subtype, if any, must be known.

    Subtype-specific sections (e.g. ``Failure mode`` for a failure) are optional, so the same
    template flexes across the failure/success/demo types.
    """
    base, _, subtype = P.page_type(page).partition(":")
    if base != "case-study":
        return []
    findings: list[Finding] = []
    if subtype and subtype not in CASE_STUDY_TYPES:
        known = ", ".join(sorted(CASE_STUDY_TYPES))
        findings.append(Finding(page.rel, -1, WARNING, "case-study-unknown-type",
                                f"unknown case-study subtype `{subtype}` (known: {known})"))
    have = {x.text.lower() for x in page.headings if x.level == 2}
    for title in CASE_STUDY_CORE:
        if title.lower() not in have:
            findings.append(Finding(page.rel, -1, ERROR, "case-study-missing-section",
                                    f"case-study page missing required `## {title}` section"))
    return findings


def _check_marker(page: P.ParsedPage) -> list[Finding]:
    """The ``page-type`` marker, if present, should be the page's last meaningful line."""
    marker_lines = [i for i, l in enumerate(page.lines) if P.PAGE_TYPE_RE.search(l)]
    if not marker_lines:
        return []
    last_nonblank = max((i for i, l in enumerate(page.lines) if l.strip()), default=-1)
    if marker_lines[-1] != last_nonblank:
        return [Finding(page.rel, marker_lines[-1] + 1, WARNING, "marker-not-at-end",
                        "`page-type` marker should be the last line of the page")]
    return []


def _base_type(page: P.ParsedPage) -> str:
    """Page-type base name (the part before any ``:subtype``)."""
    return P.page_type(page).partition(":")[0]


def _resolved_internal_targets(page: P.ParsedPage) -> set[Path]:
    """Resolved on-disk targets of this page's relative (non-external) links."""
    out: set[Path] = set()
    for link in page.links:
        url = link.url.strip()
        if not url or url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = url.split("#", 1)[0]
        if not target or target.startswith("/"):
            continue
        out.add((page.path.parent / target).resolve())
    return out


def _check_page_type(page: P.ParsedPage) -> list[Finding]:
    """An unrecognised page-type base (typo in the marker) is a warning."""
    base = _base_type(page)
    if base not in P.KNOWN_PAGE_TYPES:
        known = ", ".join(sorted(P.KNOWN_PAGE_TYPES))
        return [Finding(page.rel, -1, WARNING, "unknown-page-type",
                        f"unknown page-type `{base}` (known: {known})")]
    return []


def _check_overview(page: P.ParsedPage, root: Path, excludes=()) -> list[Finding]:
    """An ``overview`` hub must map its directory: link every sibling deep-dive.

    A sibling ``*.md`` the hub does not link to is an **orphan** (error) — that is how the
    chapter stays wired as it grows. A hub that links to no deep-dive in its own directory at
    all gets a warning (a fresh pillar with the hub written before its spokes).
    """
    if _base_type(page) != "overview":
        return []
    here = page.path.parent.resolve()
    siblings = {
        p.resolve()
        for p in page.path.parent.glob("*.md")
        if p.resolve() != page.path.resolve()
        and not P.is_template_excluded(p, root, excludes)
    }
    in_dir_linked = {t for t in _resolved_internal_targets(page) if t.parent == here}

    findings: list[Finding] = []
    for orphan in sorted(siblings - in_dir_linked):
        findings.append(Finding(page.rel, -1, ERROR, "orphan-page",
                                f"deep-dive `{P.relpath(orphan, root)}` is not linked from this "
                                f"overview (orphan)"))
    if not in_dir_linked:
        findings.append(Finding(page.rel, -1, WARNING, "overview-no-map",
                                "overview links to no deep-dive in its own directory"))
    return findings


def _check_breadcrumb(page: P.ParsedPage) -> list[Finding]:
    """A deep-dive (a ``standard`` page in a dir whose README is an ``overview``) should link
    up to that README — the breadcrumb. Missing it is a warning, not an error.
    """
    if page.path.name == "README.md" or _base_type(page) != "standard":
        return []
    readme = page.path.parent / "README.md"
    if not readme.is_file():
        return []
    if _base_type(P.parse(readme, page.root)) != "overview":
        return []
    if readme.resolve() in _resolved_internal_targets(page):
        return []
    return [Finding(page.rel, -1, WARNING, "missing-breadcrumb",
                    "deep-dive should breadcrumb up to its pillar overview (link to README.md)")]


def _is_table_separator(line: str) -> bool:
    s = line.strip()
    return "|" in s and "-" in s and set(s) <= set("|:- ")


def _check_checklist(page: P.ParsedPage) -> list[Finding]:
    """A ``checklist`` page should carry ``- [ ]`` checkbox lines — that is the point of it."""
    if _base_type(page) != "checklist":
        return []
    if not any(re.match(r"\s*[-*]\s+\[[ xX]\]", l) for l in page.lines):
        return [Finding(page.rel, -1, WARNING, "checklist-no-boxes",
                        "checklist page has no `- [ ]` checkbox lines")]
    return []


def _check_risk_register(page: P.ParsedPage) -> list[Finding]:
    """A ``risk-register`` page should carry a table — the scored-risk artifact."""
    if _base_type(page) != "risk-register":
        return []
    if not any(_is_table_separator(l) for l in page.lines):
        return [Finding(page.rel, -1, WARNING, "risk-register-no-table",
                        "risk-register page has no table")]
    return []


def verify_page(path: Path, root: Path, excludes=()) -> list[Finding]:
    if P.is_template_excluded(path, root, excludes):
        return []
    page = P.parse(path, root)
    return [
        *_check_sources(page),
        *_check_case_study(page),
        *_check_links(page),
        *_check_spine(page),
        *_check_marker(page),
        *_check_source_lines(page),
        *_check_page_type(page),
        *_check_overview(page, root, excludes),
        *_check_breadcrumb(page),
        *_check_checklist(page),
        *_check_risk_register(page),
    ]


def verify_all(root: Path, excludes=()) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    pages = P.discover_pages(root)
    for path in pages:
        findings.extend(verify_page(path, root, excludes))
    return findings, len(pages)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify repository pages against the page template.")
    parser.add_argument("--root", default=str(P.default_repository_root()),
                        help="repository root (default: repo root)")
    parser.add_argument("--exclude", action="append", default=[],
                        metavar="GLOB", help="extra page to skip (repeatable)")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    findings, n_pages = verify_all(root, args.exclude)

    errors = [f for f in findings if f.level == ERROR]
    warnings = [f for f in findings if f.level == WARNING]
    failed = bool(errors) or (args.strict and bool(warnings))

    if args.json:
        print(json.dumps({
            "pages": n_pages,
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [asdict(f) for f in findings],
        }, indent=2))
        return 1 if failed else 0

    by_path: dict[str, list[Finding]] = {}
    for f in findings:
        by_path.setdefault(f.path, []).append(f)
    for path in sorted(by_path):
        print(f"\n{path}")
        for f in sorted(by_path[path], key=lambda x: (x.level, x.line)):
            loc = f"L{f.line}" if f.line > 0 else "-"
            print(f"  {f.level:7} {loc:>5}  {f.code}: {f.message}")

    print(f"\n{n_pages} pages, {len(errors)} errors, {len(warnings)} warnings")
    if args.strict and warnings:
        print("(--strict: warnings count as failures)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
