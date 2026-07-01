# Checklist Template — a checkable go-live list for one pillar

A **checklist** turns a pillar's prose into work a reader can actually do before go-live: one checkable
row per control, grouped by theme, each row sharp enough that "done / not done" is unambiguous. Controls
are laid out as a **table** — `Done | Control | Pass criterion / metric | Source` — so the tick box, the
≤5-word control name, the verifiable metric, and the backing source each get their own column. It
lives at `checklists/<pillar>.md` and carries the marker `<!-- page-type: checklist -->` as its **last
line**.

> **In one sentence:** Every line is a box a reader can honestly tick or not — vague advice does not
> belong on a checklist.

A checklist is the hands-on counterpart to a [pillar overview](pillar-overview-template.md): the overview
explains *why*, the checklist says *what to verify*. Link the two from the overview's "Where this
connects" section.

---

## What makes a good checklist row

- **Control ≤5 words.** The `Control` column is a short handle — "Per-run token ceiling", not a sentence.
- **The metric is checkable, not vague.** "Cost cap configured; run aborts before the call that would
  breach it" — not "manage costs". A reader must be able to point at the thing that satisfies it.
- **One control per row.** If a row bundles two things, split it.
- **Sourced in the `Source` column.** Where a row asserts a standard or a number, cite it — internal
  deep-dive **and**, where it strengthens the claim, the external primary source (`; `-separated). Every
  external URL used also goes in `## Sources`.
- **Ordered by theme, then by what you'd check first.** Group with H2/H3 headings a reader recognises.

## The skeleton (copy this)

```markdown
# <Pillar> — Go-live checklist

> **In one sentence:** <what passing this whole list buys you, in production terms>

<Lead: what this checklist covers, when to run it (pre-go-live / pre-change / audit prep), and how to
read a failed box. 2–3 sentences. Point back to the pillar overview for the why.>

---

## <Theme 1>

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | <≤5-word control> | <verifiable condition a reader can point at> | [<deep-dive>](URL); [<primary>](URL) |
| ☐ | <≤5-word control> | <verifiable condition> | — |

## <Theme 2>

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | <≤5-word control> | <verifiable condition> | [<source>](URL) |

---

## Sources
<!-- Required: the standards / primary sources the checklist rows reference. -->
- **[Title](URL)** (Publisher) — which rows it backs.

<!-- page-type: checklist -->
```

The fixed order is:
**H1 → callout → lead → `---` → themed `## sections`, each a `Done | Control | Pass criterion / metric |
Source` table with `☐` rows → `---` → `## Sources` → `<!-- page-type: checklist -->`.**

## What the verifier checks

- **`## Sources` is present and non-empty** — same as every repository page.
- **The page carries checkbox rows** — either `- [ ]` bullets or a table whose rows carry a `☐`/`☑`
  (or `[ ]`) cell. A "checklist" with no checkable boxes is flagged (warning). The boxes are the point.

Everything else (theme grouping, ordering) is convention, not enforced — keep it readable.

## Inherited content rules

From [CONTRIBUTING.md](../CONTRIBUTING.md) and [page-template.md](page-template.md):

- **Every number/claim needs a source link.** No source → drop the number.
- **Checklist rows must be checkable**, not vague — this template exists to enforce exactly that.
- **Be terse** — one row, one control.
- **Neutral on tools** — name them as examples, never promote.
- **Links stay inside the repository and are relative.** Never link to the tooling layer
  (`research-toolkit/`, `research/`, `.claude/`, `tools/`).

## Sources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — the "checklist lines must be checkable" rule.

<!-- page-type: standard -->
