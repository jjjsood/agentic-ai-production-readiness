# Compliance & governance — risk register

> **In one sentence:** These are the risks that turn a working agent into a liability — each scored so you
> can sequence the hardening, and each tied to the control that closes it.

The risks below share a root: the agent runs, but the organisation cannot *demonstrate* it was in
control. Read the score as a priority sort, not a probability. For the reasoning behind the controls, see
the [Compliance & governance overview](../docs/compliance-and-governance/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, legal, safety).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **Misclassified risk tier** — a high-risk system run as if minimal, skipping the entire obligation set | 2 | 3 | 6 | Written, reasoned tier classification before go-live — [EU AI Act](../docs/compliance-and-governance/eu-ai-act.md) |
| 2 | **Operator disowns the output** — relying on "the AI said it", which has already failed in tribunal | 3 | 3 | 9 | Treat every agent output as the org's own statement; grounding + sign-off — [Air Canada](../docs/case-studies/air-canada-chatbot.md) |
| 3 | **No reconstructable trace** — can't show what a given run did when asked | 3 | 3 | 9 | Automatic, structured, queryable logging on by default, retained ≥6 months — [Audit evidence](../docs/compliance-and-governance/audit-evidence.md) |
| 4 | **No review gate** — a harmful agent ships or stays online because no one owns the stop decision | 2 | 3 | 6 | Named owner + recorded go-live sign-off + intervene/stop control — [NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md), [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |
| 5 | **Stale governance** — assessment done once, never revisited after a capability change | 3 | 2 | 6 | Re-review trigger on new tool / prompt / model swap (continuous RMF loop) — [NIST AI RMF](../docs/compliance-and-governance/nist-ai-rmf.md) |
| 6 | **Missing transparency disclosure** — users not told they are dealing with AI | 2 | 2 | 4 | Visible AI disclosure at the point of interaction — [EU AI Act](../docs/compliance-and-governance/eu-ai-act.md) |
| 7 | **Excessive agency** — the agent acts outside its permitted scope (a tool/credential it should never have reached), the agent-defining failure | 3 | 3 | 9 | Tool-permission matrix: each tool scoped to one credential behind an approval gate, with logs proving the boundary held — [Compliance & governance overview](../docs/compliance-and-governance/README.md) |
| 8 | **Inherited-regime breach** — an agent processes personal data with no lawful-basis / DSAR path, breaching GDPR (72-hour breach clock; fines to €20M / 4% — [Reg. (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng), Arts. 33 & 83) | 2 | 3 | 6 | Identify inherited overlays (GDPR / SOC 2 / HIPAA / PCI) at classification and wire their controls — [Compliance & governance overview](../docs/compliance-and-governance/README.md) |
| 9 | **Poor high-risk data governance** — biased or low-quality training/grounding data in a high-risk system | 2 | 3 | 6 | Data-governance controls on data quality and bias before go-live (EU AI Act Art. 10) — [EU AI Act](../docs/compliance-and-governance/eu-ai-act.md) |
| 10 | **Premature log destruction** — logs exist but are purged before the legal/incident window closes, leaving no trace when questioned | 2 | 3 | 6 | Tie retention to the legal/incident window, not storage cost; keep ≥6 months minimum — [Audit evidence](../docs/compliance-and-governance/audit-evidence.md) |

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — the tier, logging, and transparency obligations behind risks 1, 3, and 6.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the Govern ownership and continuous-loop controls behind risks 4 and 5.
- **[*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html)** (BC Civil Resolution Tribunal) — the holding that the operator owns its agent's output, behind risk 2.
- **[General Data Protection Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)** (EUR-Lex / Official Journal) — the 72-hour breach clock (Art. 33) and €20M / 4% fine ceiling (Art. 83) behind the inherited-regime breach, risk 8.
- **[OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)** (OWASP) — *excessive agency* as the agent-defining risk behind risk 7.

<!-- page-type: risk-register -->
