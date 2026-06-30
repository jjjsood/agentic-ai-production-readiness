# Page Template — one shared structure for the repository

Most pages in this repo follow the **same spine** so a reader always knows where to look:
the claim up top, the body in the middle, the receipts at the bottom. This file is the
template to copy. Important pages may deviate (see [When to deviate](#when-to-deviate)),
but the structure stays recognisable — and **every page ends with its sources**.

> **In one sentence:** Same skeleton on every page → predictable to read, easy to trust,
> because the numbers are sourced where they appear.

---

## The skeleton (copy this)

```markdown
# <Page Title> — <short tagline, optional>

> **In one sentence:** <core claim of this page; tie to the 88%-infra thesis where it fits>

<Lead: what this page is, who it's for, why it matters. 2–4 sentences.>

---

## <Section 1>
## <Section 2>
<!-- as many H2 sections as the topic needs; use tables and checkable lists per the content rules -->

---

## Sources
<!-- Required. Primary sources backing the numbers/claims ON THIS PAGE. -->
- **[Title](URL)** (Publisher) — which claim on this page it backs.

## Read more
<!-- Optional. Only topic-specific links that add real value beyond this page.
     NOT a back-link to the README or other generic repo docs, NOT loosely-related
     links. If every link is generic or off-topic, drop the whole section. -->
- **[Title](URL)** (Publisher) — what this *specifically* adds for this topic.

<!-- page-type: standard -->
```

The fixed order is always:
**H1 + tagline → one-sentence callout → lead → `---` → body H2s → `---` → `## Sources` →
`## Read more` → `<!-- page-type: standard -->`.**

## Minimal variant (short pages)

For a small page, drop the `> **In one sentence:**` callout and keep the rest:

```markdown
# <Page Title>

<Lead: 1–3 sentences.>

## <Section>
...

## Sources
- **[Title](URL)** (Publisher) — what it backs.

<!-- page-type: standard -->
```

## The page-type marker

Every page ends with a page-type marker so tooling can tell page kinds apart without guessing
from the path. It is the **last line** of the file; a page with no marker is treated as
`standard`.

- **`<!-- page-type: standard -->`** — the default spine on this page. No extra requirements. **A
  pillar deep-dive is a `standard` page** living at `docs/<pillar>/<slug>.md`; it opens with a one-line
  breadcrumb up to its hub (`> Part of **[<Pillar> overview](README.md)**`) and is otherwise the spine.
- **`<!-- page-type: overview -->`** — a pillar hub at `docs/<pillar>/README.md`; turns on the
  sub-topic-map + orphan checks in [pillar-overview-template.md](pillar-overview-template.md).
- **`<!-- page-type: checklist -->`** — a go-live checklist at `checklists/<pillar>.md`; expects
  `- [ ]` lines, see [checklist-template.md](checklist-template.md).
- **`<!-- page-type: risk-register -->`** — a scored risk table at `risk-register/<pillar>.md`, see
  [risk-register-template.md](risk-register-template.md).
- **`<!-- page-type: case-study:failure -->`** (or `:success`, `:demo`) — a case study; turns
  on the core-section checks in [case-study-template.md](case-study-template.md).

## The two trailing sections

These are the point of the shared structure — they make claims checkable instead of asserted.

- **`## Sources` — required on every page.** Lists the **primary** sources that back the
  numbers and claims *on this page*. If a number has no source here, the number does not
  belong on the page (per [CONTRIBUTING.md](../CONTRIBUTING.md)). Prefer primary sources
  (Anthropic Engineering, OWASP, NIST, FinOps Foundation, arXiv, official docs) over vendor
  blogs. Each line says *which* claim it supports.
- **`## Read more` — optional, and earn its place.** Only links that are **specific to this
  page's topic** and add **real value beyond what the page already says**. Explicitly **not**
  for: a back-link to the README or other generic repo docs (the README already maps to every
  page — a return link on each page is noise), and **not** for loosely-related material. If a
  link would only be there to look thorough, leave it out. If every candidate link is generic
  or off-topic, **omit the whole section** — an absent `Read more` is the normal case, not a
  gap.

Both use the literature line format from `CONTRIBUTING.md`:
`**[Title](URL)** (Publisher) — one sentence on *why* relevant.`

`Sources` and `Read more` are deliberately distinct: Sources prove what this page *claims*;
Read more points the reader *onward*. A link can appear in both if it does both jobs.

## When to deviate

The spine is the default, not a straitjacket. Structured page types keep their own body
shape **but still end with `## Sources` (required) and `## Read more` (optional)**:

| Page type | Keeps its own shape | Still required |
|-----------|---------------------|----------------|
| **Pillar overview** | Standalone chapter prose that links every deep-dive in the directory as a reading path (no status table), marked `<!-- page-type: overview -->` — see [pillar-overview-template.md](pillar-overview-template.md) | `## Sources`; must link ≥1 deep-dive (orphan check) |
| **Risk register** | Scoring legend + risk table, marked `<!-- page-type: risk-register -->` — see [risk-register-template.md](risk-register-template.md) | `## Sources` for any cited figures |
| **Checklists** | Checkbox lines grouped by theme, marked `<!-- page-type: checklist -->` — see [checklist-template.md](checklist-template.md) | `## Sources` for the standards referenced (e.g. OWASP) |
| **Case study** | Core sections (Agent Goal → Context → What happened → Takeaways) plus type-specific ones for failure/success/demo, marked `<!-- page-type: case-study:<type> -->` — see [case-study-template.md](case-study-template.md) | `## Sources` for every cited figure |
| **README** | Landing-page layout (pillar table, how-to-use, literature list) | the literature list *is* its sources |

If a page needs to break the spine for a real reason, that is allowed — keep it close to the
template and never drop `Sources`.

## Inherited content rules

The template does not replace the rules in [CONTRIBUTING.md](../CONTRIBUTING.md); it carries them:

- **Every number/claim needs a source link.** No source → drop the number.
- **Order of magnitude, not false precision** — label figures as ballpark.
- **Be terse** — one sharp sourced sentence beats three.
- **Checklist lines must be checkable**, not vague.
- **Neutral on tools** — name them as examples, never promote.
- **Links stay inside the repository and are relative.** Never link from a repository page to the
  tooling layer (`research-toolkit/`, `.claude/`).

## Sources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — the content rules and literature
  line format this template enforces.

<!-- No `## Read more` here on purpose: the only candidate would be a generic back-link to the
     README, which is exactly what the rule above forbids. Absent section = correct. -->
