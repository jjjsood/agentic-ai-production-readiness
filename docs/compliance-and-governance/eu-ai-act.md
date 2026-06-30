# The EU AI Act for agentic systems — find your tier, then produce the evidence

> **In one sentence:** The EU AI Act turns "prove you were in control" into binding law with fines up to
> €35M or 7% of turnover, and the size of your obligation is set almost entirely by which *risk tier*
> your agent lands in.

> Part of **[Compliance & governance](README.md)**

Regulation (EU) 2024/1689 — the AI Act — is the first horizontal AI law, and it is risk-tiered: the
heavier your system's potential to harm, the heavier the evidence and control burden. For an agent
operator the practical work is two steps: **classify the system honestly, then build the documentation
the tier demands.** This page is the map; the [audit-evidence](audit-evidence.md) page is the kit.

---

## The four risk tiers

The Act sorts AI systems by risk, and the obligations scale with the tier
([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)):

| Tier | What it means | Your obligation |
|------|---------------|-----------------|
| **Unacceptable** | Banned practices (e.g. social scoring, most real-time biometric ID) — Article 5 | Do not deploy. |
| **High-risk** | Systems in regulated products or the Annex III areas (hiring, credit, essential services, justice, …) | The full control + documentation set (below). |
| **Limited** | Systems that interact with people or generate content | **Transparency**: tell users they are dealing with AI / that content is AI-generated. |
| **Minimal** | Everything else | No specific obligations. |

**Classifying is the first governance act.** An agent that screens job applicants is high-risk; one that
drafts your own meeting notes is minimal. The same model, wired into different processes, carries wildly
different legal weight — so the decision belongs in writing, with reasons.

## What "high-risk" actually obligates

For a high-risk system the Act names a concrete control set — and each item is something you must be able
to *show*, not just assert ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)):

- **Risk management system** (Art. 9) — a continuous, documented process across the lifecycle.
- **Data governance** (Art. 10) — training/validation data quality and bias controls.
- **Technical documentation** (Art. 11 + **Annex IV**) — the full dossier; Annex IV lists nine sections
  covering the system end-to-end.
- **Record-keeping / automatic logging** (Art. 12) — logs over the system's lifetime, retained for a
  period appropriate to use and **at least six months**.
- **Transparency to deployers** (Art. 13) and **human oversight** (Art. 14) — a person must be able to
  understand, intervene, and stop the system.
- **Accuracy, robustness, cybersecurity** (Art. 15), under a **quality management system** (Art. 17).

These map almost one-to-one onto the other pillars in this repository: Art. 12 is **observability**, Art. 14 is **human control & rollback**, Art. 15 is **guardrails**. The Act is, in effect, a legally-enforced version of the infrastructure thesis.

## The phased timeline

Obligations switch on in stages from the Act's entry into force on **1 August 2024**
([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Art. 113):

| Date | What applies |
|------|--------------|
| **2 Feb 2025** | Prohibited practices (Art. 5) + AI-literacy duty (Art. 4). |
| **2 Aug 2025** | General-purpose AI (GPAI) model obligations + the penalty regime. |
| **2 Aug 2026** | High-risk obligations for Annex III systems. |
| **2 Aug 2027** | High-risk obligations for regulated-product systems; GPAI models placed before Aug 2025. |

Treat these as *the legal dates*, ballpark for planning: the high-risk timeline is under active
simplification debate in 2026, so confirm against the current consolidated text before you bet a roadmap
on a specific day.

## Penalties

Fines are tiered by what you got wrong ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Art. 99):

- **Prohibited practice:** up to **€35M or 7%** of total worldwide annual turnover, whichever is higher.
- **Other obligation breaches** (incl. high-risk): up to **€15M or 3%**.
- **Incorrect/misleading information** to authorities: up to **€7.5M or 1%**.

The "whichever is higher" is the sting for large operators; the percentage, not the cap, is what bites.

## What an agent operator should do first

- **Write down your tier and the reasoning** — most agents are *limited* (transparency) or *minimal*,
  but the few that touch Annex III areas carry the full burden, and guessing is not a defence.
- **If high-risk, start the Annex IV dossier and Art. 12 logging now** — both are slow to retrofit; see
  [audit-evidence](audit-evidence.md).
- **If limited, ship the transparency disclosure** — label the agent as AI to its users; the cheapest
  obligation to meet and the most embarrassing to miss.

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — the primary legal text: risk tiers (Art. 5 / Annex III), the high-risk control set (Arts. 9–17, Annex IV), record-keeping (Art. 12, ≥6 months), the timeline (Art. 113), and the penalty ceilings (Art. 99).

## Read more

- **[EU AI Act — annotated text & implementation timeline](https://artificialintelligenceact.eu/implementation-timeline/)** (Future of Life Institute) — a navigable, article-by-article reading aid that tracks timeline changes; useful for orientation, but defer to the EUR-Lex text for anything binding.

<!-- page-type: standard -->
