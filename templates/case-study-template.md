# Case Study Template — one shape, three types

A **case study** page documents one real agent deployment and ties what happened back to the
thesis: most attributable agent outcomes turn on **infrastructure, not model quality**. Three
types share this one shape:

- **`failure`** — an agent went wrong (or nearly did); the missing piece was infrastructure.
- **`success`** — a deployment that worked; *which* infrastructure carried it.
- **`demo`** — an impressive demo and the production gap between it and a real deployment.

> **In one sentence:** Every case study keeps the same core — Agent Goal → Context → What happened →
> Takeaways — and adds the optional sections its type needs, so the reader always sees *which
> infrastructure factor* decided the outcome.

This file is the template to copy for any page under `docs/case-studies/`. A case study page
carries the marker `<!-- page-type: case-study:<type> -->` as its **last line**, where `<type>`
is `failure`, `success`, or `demo`; the verifier keys off it to enforce the core sections.

---

## Core sections (always required)

Every case study, whatever its type, must have these — the verifier errors if one is missing
(`## Sources` is required on every repository page already):

| Section | What it carries |
|---------|-----------------|
| **`## Agent Goal`** | The heart of the page: *what the operator built the agent to achieve.* Written as full sentences with a subject — "X deployed the agent to…", "The agent was meant to…" — naming **who** ran it, **what job** it was given, and the **target outcome** it was optimising for (deflect support volume, ship code, close drive-thru orders). **Introduce the agent on first mention** — indefinite ("a support chatbot", "an AI coding agent") or named-and-described ("a chatbot named Tessa") — this is the reader's entry point, so never open with "the chatbot" as if they already know what it is. 2–3 sourced sentences; the yardstick everything below is measured against, never a bare imperative fragment. **It must add the intent the lead only hinted at — not paraphrase the lead.** |
| **`## Context`** | Where it ran, its autonomy and scale, the controls around it. Sourced facts, not background colour. |
| **`## What happened`** | The events in order. Facts with source links; no speculation. Order of magnitude, not false precision. |
| **`## Takeaways`** | 2–4 checkable lessons a reader can apply to their own stack. Each line stands on its own. |
| **`## Sources`** | Primary sources for the claims on this page (required). |

## Type-specific sections (optional, add what fits)

Each type drops in the sections that make its point. These are **recommended, not enforced** —
use the ones that carry the story:

| Type | Marker | Add these sections |
|------|--------|--------------------|
| **failure** | `case-study:failure` | **`## Failure mode`** (root cause as an infrastructure gap, named to a pillar) · **`## Mitigation`** (concrete, checkable controls that close it) |
| **success** | `case-study:success` | **`## What worked`** (the infrastructure/controls that carried the deployment — limits, guardrails, observability, identity, rollback) |
| **demo** | `case-study:demo` | **`## What it shows`** (the capability demonstrated) · **`## Production gap`** (the infrastructure a real deployment would still need) |

Whichever type, the failure/success/demo all land on the same point: the **infrastructure**
decided the outcome, not the model.

## The skeleton (copy this)

```markdown
# <Case Study Title> — <one-line outcome>

> **In one sentence:** <the agent, the infrastructure factor, the outcome — tie to the 88%-infra thesis>

<Lead: the hook — name the system in a clause, then what notably happened and why it matters.
Do NOT restate the purpose (that is `Agent Goal`) or the setup detail (that is `Context`);
those sections must not read as a paraphrase of this lead. 2–4 sentences.>

---

## Agent Goal

<What the operator built the agent to achieve. Full sentences with a subject — "X deployed the agent to…" / "The agent was meant to…" — naming who ran it, the job it was given, and the target outcome. Introduce the agent on first mention (indefinite or named-and-described), never "the chatbot" as if the reader already knows it. 2–3 sourced sentences.>

## Context

<Where it ran, how much autonomy and scale it had, the controls around it.>

## What happened

<The events in order, sourced. No speculation.>

<!-- Add the section(s) for this type:
     failure → ## Failure mode + ## Mitigation
     success → ## What worked
     demo    → ## What it shows + ## Production gap                       -->

## Takeaways

<2–4 checkable lessons for the reader's own stack.>

---

## Sources

- **[Title](URL)** (Publisher) — which claim in this case it backs.

## Read more
<!-- Optional. Only topic-specific links that add real value beyond this case.
     NOT a generic back-link to the README, NOT loosely-related links.
     If every candidate is generic or off-topic, drop the whole section. -->
- **[Title](URL)** (Publisher) — what this *specifically* adds for this case.

<!-- page-type: case-study:failure -->
```

The fixed order is:
**H1 + tagline → callout → lead → `---` → Agent Goal → Context → What happened → (type sections) →
Takeaways → `---` → `## Sources` → `## Read more` *(optional — see rule below)* →
`<!-- page-type: case-study:<type> -->`.**

`## Read more` is optional and has to **earn its place**: only links specific to this case
that add real value beyond the page. **Not** a back-link to the README (it already maps to
every case) and **not** loosely-related material. If every candidate link is generic or
off-topic, omit the whole section — an absent `Read more` is the normal case, not a gap.

## The page-type marker

Every repository page ends with a page-type marker so tooling can tell page kinds apart without
guessing from the path. It is the **last line** of the file; a page with no marker is treated
as `standard`.

- **Case study:** `<!-- page-type: case-study:failure -->` (or `:success`, `:demo`) — turns on
  the core-section checks above. A bare `case-study` is accepted; an unknown subtype is flagged.
- **Standard page:** `<!-- page-type: standard -->` — the default spine (see
  [page-template.md](page-template.md)); no extra section requirements.

## Inherited content rules

This template adds sections; it does not replace the rules in
[CONTRIBUTING.md](../CONTRIBUTING.md):

- **Every number/claim needs a source link.** No source → drop the number.
- **Order of magnitude, not false precision** — label figures as ballpark.
- **Be terse** — one sharp sourced sentence beats three.
- **Takeaway lines must be checkable**, not vague.
- **Neutral on tools** — name them as examples, never promote.
- **Links stay inside the repository and are relative.** Never link from a repository page to the
  tooling layer (`research-toolkit/`, `research/`, `.claude/`, `tools/`).

## Sources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — the content rules and literature
  line format this template enforces.

## Read more

- **In this repo:** [page-template.md](page-template.md) — the standard page spine this
  case study shape extends.
<!-- Generic README back-link deliberately dropped here — it would only pad, per the rule above. -->

<!-- page-type: standard -->
