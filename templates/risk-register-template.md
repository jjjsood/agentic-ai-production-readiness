# Risk Register Template — scored risks and the control that addresses each

A **risk register** lists a pillar's risks with a likelihood, an impact, a resulting score, and the
**control that addresses each** — so a reader can prioritise hardening work, not just read about it. It
lives at `risk-register/<pillar>.md` and carries the marker `<!-- page-type: risk-register -->` as its
**last line**.

> **In one sentence:** Each row is a risk you can rank and a control you can point to — a register is for
> deciding what to fix first, so every row carries a score and a named control.

The register is the third hands-on artifact beside the [overview](pillar-overview-template.md) (the why)
and the [checklist](checklist-template.md) (the what-to-verify); the register adds *which risks, how bad,
fix in what order*. Link all three from the overview's "Where this connects" section.

---

## Scoring legend (copy and keep)

A simple, defensible scale — order of magnitude, not false precision.

- **Likelihood (L):** 1 = rare · 2 = possible · 3 = likely (in a real unhardened deployment).
- **Impact (I):** 1 = contained / recoverable · 2 = serious (money, data, trust) · 3 = severe
  (regulatory, safety, unrecoverable).
- **Score = L × I** (1–9). Treat **6–9 as address-before-go-live**, 3–4 as plan-to-mitigate, 1–2 as
  accept-and-watch. The number is a sort key, not a guarantee.

## The skeleton (copy this)

```markdown
# <Pillar> — Risk register

> **In one sentence:** <the headline risk class this pillar carries, and what hardening buys you>

<Lead: what these risks share, how to read the score, and that the control column maps each risk to the
deep-dive / checklist line that closes it. 2–3 sentences.>

---

## Scoring

<!-- Copy the legend above so the page stands alone. -->
- **Likelihood (L):** 1 rare · 2 possible · 3 likely. **Impact (I):** 1 contained · 2 serious · 3 severe.
  **Score = L × I**; 6–9 = address before go-live.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | <The risk, stated as a failure that can happen.> | 3 | 3 | 9 | <The control that addresses it> — [deep-dive](../docs/<pillar>/<slug>.md) |

---

## Sources
<!-- Required: primary sources for any cited figure or named standard in the rows. -->
- **[Title](URL)** (Publisher) — which row/figure it backs.

<!-- page-type: risk-register -->
```

The fixed order is:
**H1 → callout → lead → `---` → `## Scoring` → `## Risks` (the table) → `---` → `## Sources` →
`<!-- page-type: risk-register -->`.**

## What the verifier checks

- **`## Sources` is present and non-empty** — same as every repository page.
- **The page carries a table** — a register with no risk table is flagged (warning). The table is the
  artifact.

Likelihood/impact justification is convention (state your reasoning in the row or lead), not enforced.

## Inherited content rules

From [CONTRIBUTING.md](../CONTRIBUTING.md) and [page-template.md](page-template.md):

- **Every number/claim needs a source link.** A cited figure in a row carries its source in `## Sources`.
- **Order of magnitude, not false precision** — the L×I score is a priority sort, not a probability.
- **Be terse** — one row, one risk, one control.
- **Neutral on tools** — controls name mechanisms, not products to buy.
- **Links stay inside the repository and are relative.** Never link to the tooling layer
  (`research-toolkit/`, `research/`, `.claude/`, `tools/`).

## Sources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — "justify L/I/score" for risk lines.

<!-- page-type: standard -->
