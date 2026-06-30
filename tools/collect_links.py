#!/usr/bin/env python3
"""Tool 2 — harvest every external source from the repository into one grouped page.

Scans all repository pages, dedupes by URL, records every page+section a source is used
in, and writes a generated source-list page: external sources grouped by
registrable domain (anthropic.com, owasp.org, ...) as tables of
Title / Publisher / Used on. Internal cross-references are ignored — this is a
sources list, not a link index.

Default output: docs/link-collection.md (carries a do-not-edit banner so the
verifier skips it).

Run:  python tools/collect_links.py [--root PATH] [--output PATH] [--check]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repositorykit import pages as P  # noqa: E402

DEFAULT_OUTPUT = "docs/link-collection.md"
BANNER = f"<!-- {P.GENERATED_BANNER} — do not edit by hand. Run the tool to regenerate. -->"

# Publisher sits in `](URL)** (Publisher) — ...` in the source-line format.
_PUBLISHER_RE = re.compile(r"\)\*\*\s*\(([^)]+)\)")


@dataclass
class Usage:
    page: str  # path relative to repository root
    section: str


@dataclass
class Entry:
    url: str
    title: str = ""
    publisher: str = ""
    usages: list[Usage] = field(default_factory=list)


def _slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s)


def _registrable_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def _is_external(url: str) -> bool:
    return url.startswith(("http://", "https://"))


def collect(root: Path | str, output: Path | str) -> dict[str, Entry]:
    """Map url -> Entry for every external source link across repository pages."""
    root = Path(root).resolve()
    output = Path(output).resolve()
    entries: dict[str, Entry] = {}

    for path in P.discover_pages(root):
        if path.resolve() == output:
            continue  # never harvest the generated page itself
        page = P.parse(path, root)
        for link in page.links:
            url = link.url.strip()
            if not _is_external(url):
                continue
            entry = entries.get(url)
            if entry is None:
                entry = entries[url] = Entry(url=url)
            if not entry.title and link.text:
                entry.title = link.text
            if not entry.publisher:
                raw = page.lines[link.line - 1] if 0 < link.line <= len(page.lines) else ""
                m = _PUBLISHER_RE.search(raw)
                if m:
                    entry.publisher = m.group(1).strip()
            usage = Usage(page.rel, link.section)
            if usage not in entry.usages:
                entry.usages.append(usage)
    return entries


def _used_on(entry: Entry, output: Path, root: Path) -> str:
    out_dir = output.parent
    cells = []
    for u in sorted(entry.usages, key=lambda x: (x.page, x.section)):
        target = os.path.relpath(root / u.page, out_dir)
        anchor = f"#{_slug(u.section)}" if u.section else ""
        label = f"{u.page}" + (f" § {u.section}" if u.section else "")
        cells.append(f"[{label}]({target}{anchor})")
    return "<br>".join(cells)


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def render(entries: dict[str, Entry], output: Path | str, root: Path | str) -> str:
    output = Path(output).resolve()
    root = Path(root).resolve()

    lines: list[str] = [
        BANNER,
        "",
        "# Source list",
        "",
        "Every external source used across the repository, deduped by URL and grouped by "
        "domain for quick lookup. Generated from the pages — do not edit by hand.",
        "",
    ]

    if not entries:
        lines += ["_No sources found._", ""]
        return "\n".join(lines).rstrip() + "\n"

    by_domain: dict[str, list[Entry]] = {}
    for url, entry in entries.items():
        by_domain.setdefault(_registrable_domain(url), []).append(entry)
    for domain in sorted(by_domain):
        lines += [f"## {domain}", "", "| Title | Publisher | Used on |", "| --- | --- | --- |"]
        for entry in sorted(by_domain[domain], key=lambda e: (e.title.lower(), e.url)):
            title = _md_escape(entry.title or entry.url)
            lines.append(
                f"| [{title}]({entry.url}) | {_md_escape(entry.publisher)} "
                f"| {_used_on(entry, output, root)} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect all repository links into one grouped page.")
    parser.add_argument("--root", default=str(P.default_repository_root()),
                        help="repository root (default: repo root)")
    parser.add_argument("--output", default=None,
                        help=f"output page (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if the file would change (CI drift check)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    output = Path(args.output).resolve() if args.output else (root / DEFAULT_OUTPUT)

    entries = collect(root, output)
    content = render(entries, output, root)

    if args.check:
        current = output.read_text(encoding="utf-8") if output.exists() else None
        if current == content:
            print(f"up to date: {P.relpath(output, root) if output.exists() else output}")
            return 0
        print(f"DRIFT: {output} is out of date — run collect_links.py to regenerate")
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"wrote {output} — {len(entries)} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
