# Repository tools

Two small Python CLIs that keep the repository self-consistent. They ship beside the
repository but are authoring scaffolding — they read the Markdown pages, they do not
change them (except the one generated page Tool 2 owns).

| Tool | What it does |
| --- | --- |
| [`verify_template.py`](verify_template.py) | Checks every repository page follows the shared structure in [`templates/page-template.md`](../templates/page-template.md): a non-empty `## Sources` section, links that stay inside the repository and resolve, and the expected spine order. Pages marked `<!-- page-type: case-study:<type> -->` (failure/success/demo) additionally must carry the core sections from [`templates/case-study-template.md`](../templates/case-study-template.md). |
| [`collect_links.py`](collect_links.py) | Harvests every external source across all pages, dedupes by URL, and writes a grouped source-list page ([`docs/link-collection.md`](../docs/link-collection.md)) showing each source's publisher and where it is used. |

## Setup

Python 3.10+.

```bash
cd tools
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt        # runtime: markdown-it-py
pip install -r requirements-dev.txt    # also pytest, to run the tests
```

Run the tools from anywhere; they default `--root` to the repo root.

## Tool 1 — verify the template

```bash
python verify_template.py            # human-readable report, exits non-zero on errors
python verify_template.py --strict   # warnings also fail (use in CI)
python verify_template.py --json     # machine-readable findings
python verify_template.py --exclude "docs/draft-*.md"   # skip extra pages (repeatable)
```

**Errors** (fail the run): missing/empty `## Sources`; a `page-type: case-study` page
missing a core section (`Context`, `What happened`, `Takeaways`); a relative link whose
target is missing; a repository page linking into the tooling layer (`research/`,
`research-toolkit/`, `.claude/`, `tools/`, `CLAUDE.md`); an absolute path or a link escaping
the repository root.

**Warnings** (informational unless `--strict`): spine order off; missing the
`> **In one sentence:**` callout; a `page-type` marker that is not the last line; a
case-study page with an unrecognised subtype (not `failure`/`success`/`demo`); a
Sources/Read-more line with no link.

**Page types** — every page ends with a `<!-- page-type: ... -->` marker. `standard` (or no
marker) gets the spine checks; `case-study:<type>` (failure/success/demo) also gets the core
sections above. Each type adds its own optional sections (documented in the template, not
enforced), so the one shape flexes across all three.

**Excluded by default** — pages that legitimately do not follow the spine:
`README.md`, `CONTRIBUTING.md`, `templates/*.md`, and any page carrying the
generated banner (Tool 2's output). Add more with `--exclude`.

## Tool 2 — collect the links

```bash
python collect_links.py                       # (re)write docs/link-collection.md
python collect_links.py --output PATH         # write elsewhere
python collect_links.py --check               # CI: exit non-zero if the file is stale
```

The output page carries a `do not edit by hand` banner — regenerate it whenever a
source changes; never hand-edit it. External sources are grouped by domain;
internal cross-references are ignored (this is a sources list, not a link index).

## CI

```bash
python tools/verify_template.py --strict
python tools/collect_links.py --check
```

## Tests

```bash
source .venv/bin/activate
python -m pytest -q
```
