# Audit evidence — proving you were in control

> **In one sentence:** "Prove you were in control" is answered with an *evidence pack* you accumulate
> while the agent runs — not a story you assemble after it fails — which is why the gap that sinks teams
> is evidence that was never recorded, not controls that were never built.

> Part of **[Compliance & governance](README.md)**

This is the page the whole pillar points at. The [EU AI Act](eu-ai-act.md) sets the legal floor and
[NIST AI RMF](nist-ai-rmf.md) runs the loop; both produce **artifacts**, and those artifacts are what an
auditor, regulator, or court actually inspects. The discipline is simple to state and hard to retrofit:
**generate the evidence continuously, keep it, and be able to find it.**

---

## Why evidence beats good intentions

When [Air Canada](../case-studies/air-canada-chatbot.md)'s bot invented a refund policy, the tribunal's
holding was that the operator owns the output — being well-meaning was no defence. When an agent
[deleted a production database at Replit](../case-studies/replit-database-deletion.md), part of what made
it a crisis was the absence of a trustworthy trace and rollback path. In an audit the asymmetry is
brutal: **a control you cannot evidence did not, for the record, exist.** The work is to make "we were in
control" a query against stored artifacts, not a recollection.

## The evidence pack

Six artifact classes cover most of what a high-risk agent must be able to produce. Most map directly to a
named EU AI Act obligation and to a NIST function:

| Evidence | What it is | Anchored in |
|----------|------------|-------------|
| **Technical documentation** | The system dossier: purpose, design, data, controls, limitations | EU AI Act Art. 11 + **Annex IV** (nine sections) |
| **Automatic logs / traces** | Per-run records of inputs, tool calls, decisions, outputs | EU AI Act Art. 12 — retained **≥ 6 months** |
| **Risk records** | The risk assessment, the residual-risk acceptance, who signed it | NIST **Map** / **Manage**; EU AI Act Art. 9 |
| **Evaluation & red-team results** | Eval suite runs, adversarial tests, the dates and verdicts | NIST **Measure** |
| **Human-oversight & sign-off records** | Who approved go-live, who can intervene, the gate decisions | EU AI Act Art. 14; NIST **Govern** |
| **Version & change history** | Model versions, prompt/tool changes, with timestamps | ISO/IEC 42001 documented information |

If you can produce these six on demand, you can answer almost any "prove it" question. If you cannot, the
quality of your actual controls is, evidentially, beside the point.

## Retention — keep it long enough to matter

The EU AI Act sets a floor for automatic logs of **at least six months**, but the right horizon is "as
long as the system could plausibly be questioned" ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Art. 12). A liability claim or a regulatory inquiry can land long after an
interaction, so tie retention to your legal and incident-response windows, not to log-storage cost.

## The one rule that prevents the scramble

**Evidence must be a by-product of operation, not a project after an incident.** Logging that is off by
default, risk assessments written once and never revisited, eval results that live in someone's terminal
history — all reconstruct into nothing under audit. Wire the pack into how the agent runs:

- **Log by default, structured, and queryable** — Art. 12 logs are worthless if you cannot search them
  to reconstruct a specific run.
- **Date and store every risk and eval artifact** — an undated assessment proves nothing about *when* you
  knew what.
- **Record the sign-off, not just the decision** — who approved go-live, against which evidence, on what
  date; the [checklist](../../checklists/compliance-and-governance.md) is where that gate is made explicit.

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — technical documentation (Art. 11 + Annex IV), automatic record-keeping and the ≥6-month log-retention floor (Art. 12), risk management (Art. 9), human oversight (Art. 14).
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the Map / Measure / Manage / Govern functions that produce the risk, evaluation, and sign-off artifacts.
- **[ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)** (ISO) — the "documented information" and change-control expectations behind version history as auditable evidence.
- **[ISO/IEC 42001 explained — what it is](https://www.iso.org/home/insights-news/resources/iso-42001-explained-what-it-is.html)** (ISO) — the official, non-paywalled overview of the AI management system standard, for readers without access to the priced text.

<!-- page-type: standard -->
