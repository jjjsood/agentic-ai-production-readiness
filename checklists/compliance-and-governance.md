# Compliance & governance — go-live checklist

> **In one sentence:** Each box below is something an auditor could ask you to show — if you cannot tick
> it honestly, you cannot yet prove you were in control.

Run this before sign-off on any agent that touches real users, money, records, or decisions. A failed box
is not a blocker by itself — it is a residual risk someone has to *accept in writing*. For the why behind
each theme, see the [Compliance & governance overview](../docs/compliance-and-governance/README.md).

---

## Classification & ownership

- [ ] The system's EU AI Act risk tier is **written down with reasoning** (unacceptable / high / limited / minimal). ([EU AI Act](../docs/compliance-and-governance/eu-ai-act.md))
- [ ] A **named owner** is accountable for the agent's risk — a person, not a team alias.
- [ ] A one-page **agent policy** exists (purpose, allowed tools, prohibited uses) and was approved before go-live.
- [ ] **Inherited regimes are identified** — if the agent touches personal data, money, health, or cardholder data, the applicable overlay (GDPR DSAR path / automated-decision limits / 72-hour breach clock, SOC 2, HIPAA, PCI DSS) is listed and owned. ([Compliance & governance overview](../docs/compliance-and-governance/README.md))

## Transparency

- [ ] Users are **told they are interacting with AI**, per the limited-risk transparency duty. ([EU AI Act, Art. 50](../docs/compliance-and-governance/eu-ai-act.md))
- [ ] **AI-generated content is labelled** as such where Art. 50 requires it. ([EU AI Act, Art. 50](../docs/compliance-and-governance/eu-ai-act.md))
- [ ] The disclosure is visible at the point of interaction, not buried in terms.

## Documentation (if high-risk)

- [ ] The **Annex IV technical documentation** dossier is started and assigned an owner. ([EU AI Act](../docs/compliance-and-governance/eu-ai-act.md))
- [ ] A **data-governance** note covers training/grounding data quality and known bias.
- [ ] If you run an ISO/IEC 42001 AIMS, a **Statement of Applicability** records which controls are included or excluded, with reasons. ([Audit evidence](../docs/compliance-and-governance/audit-evidence.md))

## Logging & evidence

- [ ] **Automatic logging is on by default**, structured, and queryable to reconstruct a single run. ([Audit evidence](../docs/compliance-and-governance/audit-evidence.md))
- [ ] Log **retention** meets at least the EU AI Act Art. 12 6-month floor and matches your legal/incident window. ([Audit evidence](../docs/compliance-and-governance/audit-evidence.md))
- [ ] Risk assessments and **evaluation/red-team results are dated and stored**, not left in terminal history.

## Human oversight & sign-off

- [ ] A **tool-permission matrix** exists: each tool scoped to one credential and behind an approval gate, with logs proving the boundary held — bounding *excessive agency*. ([Compliance & governance overview](../docs/compliance-and-governance/README.md))
- [ ] A human can **understand, intervene, and stop** the agent on a consequential action. ([NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md))
- [ ] The **go-live sign-off is recorded** — who approved, against which evidence, on what date.
- [ ] A **re-review trigger** is defined for capability changes (new tool, new prompt, model swap).

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — backs the risk-tier, transparency, Annex IV documentation, Art. 12 logging (≥6 months), and Art. 14 human-oversight lines.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — backs the ownership/Govern and re-review (continuous loop) lines.
- **[OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)** (OWASP) — backs treating *excessive agency* (tool-permission matrix, tool scope, stop control) as a first-class governance risk.
- **[General Data Protection Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)** (EUR-Lex / Official Journal) — backs the inherited-regime line: DSAR rights, automated-decision limits, the 72-hour breach clock (Art. 33), and the €20M / 4% fine ceiling (Art. 83).
- **[ISO/IEC 42001 explained — what it is](https://www.iso.org/home/insights-news/resources/iso-42001-explained-what-it-is.html)** (ISO) — the official, non-paywalled overview behind the Statement-of-Applicability line.

<!-- page-type: checklist -->
