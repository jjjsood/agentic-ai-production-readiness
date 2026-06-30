# Checklist Template — a checkable go-live list for one pillar

A **checklist** turns a pillar's prose into work a reader can actually do before go-live: one checkable
line per control, grouped by theme, each line sharp enough that "done / not done" is unambiguous. It
lives at `checklists/<pillar>.md` and carries the marker `<!-- page-type: checklist -->` as its **last
line**.

> **In one sentence:** Every line is a box a reader can honestly tick or not — vague advice does not
> belong on a checklist.

A checklist is the hands-on counterpart to a [pillar overview](pillar-overview-template.md): the overview
explains *why*, the checklist says *what to verify*. Link the two from the overview's "Where this
connects" section.

---

## What makes a good checklist line

- **Checkable, not vague.** "Per-run token ceiling enforced and alerting on breach" — not "manage costs".
  A reader must be able to point at the thing that satisfies it.
- **One control per line.** If a line bundles two things, split it.
- **Sourced where it makes a claim.** A line that asserts a standard or a number carries its link, same
  as any other page (the standards referenced go in `## Sources`).
- **Ordered by theme, then by what you'd check first.** Group with H2/H3 headings a reader recognises.

## The skeleton (copy this)

```markdown
# <Pillar> — Go-live checklist

> **In one sentence:** <what passing this whole list buys you, in production terms>

<Lead: what this checklist covers, when to run it (pre-go-live / pre-change / audit prep), and how to
read a failed box. 2–3 sentences. Point back to the pillar overview for the why.>

---

## <Theme 1>

- [ ] <Checkable control — a reader can verify this is true.>
- [ ] <Checkable control with a source where it claims a standard.> ([OWASP …](URL))

## <Theme 2>

- [ ] <Checkable control.>
- [ ] <Checkable control.>

---

## Sources
<!-- Required: the standards / primary sources the checklist lines reference. -->
- **[Title](URL)** (Publisher) — which lines it backs.

<!-- page-type: checklist -->
```

The fixed order is:
**H1 → callout → lead → `---` → themed `## sections` of `- [ ]` lines → `---` → `## Sources` →
`<!-- page-type: checklist -->`.**

## What the verifier checks

- **`## Sources` is present and non-empty** — same as every repository page.
- **The page carries `- [ ]` checkbox lines** — a "checklist" with no checkable boxes is flagged
  (warning). The boxes are the point.

Everything else (theme grouping, ordering) is convention, not enforced — keep it readable.

## Inherited content rules

From [CONTRIBUTING.md](../CONTRIBUTING.md) and [page-template.md](page-template.md):

- **Every number/claim needs a source link.** No source → drop the number.
- **Checklist lines must be checkable**, not vague — this template exists to enforce exactly that.
- **Be terse** — one line, one control.
- **Neutral on tools** — name them as examples, never promote.
- **Links stay inside the repository and are relative.** Never link to the tooling layer
  (`research-toolkit/`, `research/`, `.claude/`, `tools/`).

## Sources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — the "checklist lines must be checkable" rule.

<!-- page-type: standard -->
