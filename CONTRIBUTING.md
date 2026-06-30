# Contributing

This repository is a **living, growing artifact** — a curated knowledge and template
collection on production readiness for agentic AI. It is built page by page and is meant to
keep expanding: every contribution extends it, whether a new source, a sharpened checklist
line, a new incident pattern, or a whole new topic page.

## How the repository grows

The repository is organised **hub-and-spoke**, and it grows one page at a time. Each pillar is
a directory under [`docs/`](docs/) with an **overview hub** (`docs/<pillar>/README.md`) that maps
the pillar and points to **deep-dive** pages (spokes) in the same directory. You extend a pillar
by adding a spoke and registering it in its hub's sub-topic map — the verifier's orphan check
fails if a deep-dive is left unlinked, so the chapter stays wired as it expands. The cross-cutting
artifacts grow alongside the pillars: the per-pillar [checklists](checklists/) and
[risk registers](risk-register/), and the [case studies](docs/case-studies/).

Start every new page from the matching template in [`templates/`](templates/): the shared page
spine lives in [`templates/page-template.md`](templates/page-template.md), with dedicated
templates for [pillar overviews](templates/pillar-overview-template.md),
[checklists](templates/checklist-template.md), [risk registers](templates/risk-register-template.md),
and [case studies](templates/case-study-template.md). Then run the verifier (see **Tools** below)
before opening a pull request.

## Guiding principles

1. **Name your source.** Every claim with a number or "fact" needs a link. No source → no number.
2. **Prefer primary sources.** Anthropic Engineering, OWASP, NIST, FinOps Foundation, arXiv,
   official docs > vendor marketing blogs. Mark/use marketing sources sparingly.
3. **Order of magnitude, not false precision.** AI tooling changes fast. Mark numbers as
   ballpark figures, not constants.
4. **Practical & checkable.** Checklist items are verifiable, not vague.
5. **Terse.** Better one sharp sentence with a source than three without.
6. **Neutral.** No tool-recommendation spam. Tools are named as examples, not promoted.

## Adding a source

- Put it in the **`## Sources`** section of the page whose claim it backs (or **`## Read more`**
  for further reading that is not a backing source) — see
  [`templates/page-template.md`](templates/page-template.md). A non-empty `## Sources` section is
  required on every page; sources are authored on the page they support.
- Format: `**[Title](URL)** (Publisher) — one sentence on *why* it is relevant.`
- The generated [`docs/link-collection.md`](docs/link-collection.md) aggregates every source used
  across the repository, grouped by domain. It carries a *do not edit by hand* banner —
  regenerate it with Tool 2 (see below); never hand-edit it.
- Prefer primary sources; report or replace outdated/dead links.

## Changing a checklist or risk line

- Phrase checklist items so they are checkable, not vague. For risks, justify the L/I/score and
  link the relevant deep-dive.

## Page structure

- Every page ends with a `<!-- page-type: ... -->` marker — `standard`, `overview`, `checklist`,
  `risk-register`, or `case-study:<failure|success|demo>` — so the tools can tell page kinds apart.
- A deep-dive opens with a breadcrumb up to its hub and ends with `## Sources` (required) and an
  optional `## Read more`.

## Changing tools or templates

Changes to [`templates/`](templates/) and [`tools/`](tools/) are welcome when they add value —
a clearer page spine, a sharper check, a new page type. But the templates define the spine and
the tools enforce it, so a change there ripples across the content: **in the same pull request,
update every page the change governs** and re-run `verify_template.py --strict` clean so the
repository stays consistent. A change under [`tools/`](tools/) also has to keep the tests green
(`pytest -q`).

## Tools

Two small Python CLIs keep the growing repository self-consistent — see
[`tools/`](tools/) and [`tools/README.md`](tools/README.md). Python 3.10+:

```bash
cd tools
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt        # runtime
pip install -r requirements-dev.txt    # adds pytest, to run the tests
```

- **Tool 1 — [`verify_template.py`](tools/verify_template.py)** checks every page: a non-empty
  `## Sources`, relative links that resolve and stay inside the repository, the expected spine
  order, the core sections of case-study pages, the overview orphan check, and deep-dive
  breadcrumbs.

  ```bash
  python verify_template.py            # human-readable report; exits non-zero on errors
  python verify_template.py --strict   # warnings fail too (use as the ship gate / in CI)
  ```

- **Tool 2 — [`collect_links.py`](tools/collect_links.py)** harvests every external source across
  all pages, dedupes by URL, and regenerates [`docs/link-collection.md`](docs/link-collection.md)
  grouped by domain.

  ```bash
  python collect_links.py              # regenerate the source list
  python collect_links.py --check      # CI: exit non-zero if the file is stale
  ```

Run `verify_template.py --strict` clean and regenerate the source list before you open a pull
request. If you change anything under [`tools/`](tools/), also run the tests:

```bash
python -m pytest -q
```

## Style

- Language: English (source titles may stay in their original language).
- Markdown; links are relative and stay inside the repository.
- One topic per pull request.

Thanks for helping this artifact grow. 🙏
