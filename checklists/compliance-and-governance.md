# Compliance & governance — go-live checklist

> **In one sentence:** Each box below is something an auditor could ask you to show — if you cannot tick
> it honestly, you cannot yet prove you were in control.

Run this before sign-off on any agent that touches real users, money, records, or decisions. A failed box
is not a blocker by itself — it is a residual risk someone has to *accept in writing*. For the why behind
each theme, see the [Compliance & governance overview](../docs/compliance-and-governance/README.md).

---

## Classification & ownership

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Write down risk tier | EU AI Act risk tier (unacceptable / high / limited / minimal) recorded with reasoning | [EU AI Act](../docs/compliance-and-governance/eu-ai-act.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Named accountable owner | A person, not a team alias, is accountable for the agent's risk | [NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md); [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) |
| ☐ | One-page agent policy | Purpose, allowed tools, prohibited uses — approved before go-live | — |
| ☐ | Identify inherited regimes | Applicable overlay listed + owned (GDPR DSAR / automated-decision limits / 72-hour breach clock, SOC 2, HIPAA, PCI DSS) | [Compliance & governance overview](../docs/compliance-and-governance/README.md); [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) |

## Transparency

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Disclose AI to users | Users told they are interacting with AI, per the limited-risk transparency duty | [EU AI Act, Art. 50](../docs/compliance-and-governance/eu-ai-act.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Label AI-generated content | AI-generated content labelled where Art. 50 requires it | [EU AI Act, Art. 50](../docs/compliance-and-governance/eu-ai-act.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Disclosure at point of use | Disclosure visible at the point of interaction, not buried in terms | [EU AI Act, Art. 50](../docs/compliance-and-governance/eu-ai-act.md) |

## Documentation (if high-risk)

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Start Annex IV dossier | Annex IV technical-documentation dossier started and assigned an owner | [EU AI Act](../docs/compliance-and-governance/eu-ai-act.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Data-governance note | Covers training/grounding data quality and known bias | — |
| ☐ | Statement of Applicability | If running an ISO/IEC 42001 AIMS, records which controls are included/excluded, with reasons | [Audit evidence](../docs/compliance-and-governance/audit-evidence.md); [ISO/IEC 42001](https://www.iso.org/home/insights-news/resources/iso-42001-explained-what-it-is.html) |

## Logging & evidence

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Automatic logging by default | On by default, structured, and queryable to reconstruct a single run | [Audit evidence](../docs/compliance-and-governance/audit-evidence.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Retention ≥6-month floor | Log retention meets at least the EU AI Act Art. 12 6-month floor and matches your legal/incident window | [Audit evidence](../docs/compliance-and-governance/audit-evidence.md); [EU AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Store dated eval results | Risk assessments and evaluation/red-team results dated and stored, not left in terminal history | — |

## Human oversight & sign-off

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Tool-permission matrix | Each tool scoped to one credential and behind an approval gate, with logs proving the boundary held — bounding *excessive agency* | [Compliance & governance overview](../docs/compliance-and-governance/README.md); [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) |
| ☐ | Human can stop it | A human can understand, intervene, and stop the agent on a consequential action | [NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md); [EU AI Act Art. 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Record go-live sign-off | Who approved, against which evidence, on what date | — |
| ☐ | Define re-review trigger | Re-review defined for capability changes (new tool, new prompt, model swap) | [NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md); [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) |

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — backs the risk-tier, transparency, Annex IV documentation, Art. 12 logging (≥6 months), and Art. 14 human-oversight rows.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — backs the ownership/Govern and re-review (continuous loop) rows.
- **[OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)** (OWASP) — backs treating *excessive agency* (tool-permission matrix, tool scope, stop control) as a first-class governance risk.
- **[General Data Protection Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)** (EUR-Lex / Official Journal) — backs the inherited-regime row: DSAR rights, automated-decision limits, the 72-hour breach clock (Art. 33), and the €20M / 4% fine ceiling (Art. 83).
- **[ISO/IEC 42001 explained — what it is](https://www.iso.org/home/insights-news/resources/iso-42001-explained-what-it-is.html)** (ISO) — the official, non-paywalled overview behind the Statement-of-Applicability row.

<!-- page-type: checklist -->
