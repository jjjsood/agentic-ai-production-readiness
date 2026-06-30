# NIST AI RMF as an operating model — the loop that runs under the law

> **In one sentence:** The EU AI Act tells you *what evidence* to produce; NIST's AI Risk Management
> Framework tells you *how to run the risk loop* that generates it — Govern, Map, Measure, Manage.

> Part of **[Compliance & governance](README.md)**

The AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1) is voluntary and US-origin, but it is the
most usable *operating model* in the governance toolkit: four functions you can actually run a team on,
rather than a checklist you sign once. It pairs naturally with the [EU AI Act](eu-ai-act.md) (the legal
floor) and [ISO/IEC 42001](https://www.iso.org/standard/81230.html) (the certifiable shell) — the RMF is
the verb between them.

---

## The four core functions

NIST structures the framework as four functions, with **Govern as the cross-cutting one that informs the
other three** ([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)):

| Function | The question it answers | For an agent, concretely |
|----------|-------------------------|--------------------------|
| **Govern** | Who owns AI risk, under what policy and culture? | A named owner, a written agent policy, an approval gate before go-live. |
| **Map** | What is the context and what could go wrong? | The agent's purpose, its tools and blast radius, the misuse and failure modes. |
| **Measure** | How do we quantify and track the risk? | Eval suites, red-team results, cost/latency/error telemetry, drift checks. |
| **Manage** | How do we act on what we measured? | Prioritised mitigations, limits, rollback paths, residual-risk acceptance. |

**Govern is the part teams skip and regulators check.** Map/Measure/Manage are recognisably engineering;
Govern is the ownership, policy, and sign-off that makes the other three repeatable instead of heroic —
and it is exactly what was missing in the [NYC MyCity](../case-studies/nyc-mycity-chatbot.md) failure,
where no one owned the decision to leave a law-breaking bot online.

## Why it fits agents well

The RMF is a *loop*, not a gate: you Map, Measure, Manage, and feed results back through Govern,
continuously. Agents need exactly that, because their risk surface moves — a new tool, a new prompt, a
model upgrade all change the blast radius. A one-time assessment goes stale the first time you add a
capability; the RMF's continuous framing is built for that.

## The Generative AI Profile

NIST extended the framework to LLMs and agents with the **Generative AI Profile (NIST AI 600-1)**,
published **26 July 2024** ([NIST AI 600-1, PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). It maps the
generative-AI-specific risks — confabulation, prompt-injection, data leakage, harmful outputs — onto the
four functions and suggests concrete actions. For an agent team it is the more directly applicable
document: start from the Profile's risk list, not the abstract core.

## How to use it without drowning

- **Stand up Govern first** — name an owner and write a one-page agent policy before you touch Map. The
  framework is worthless if no one is accountable for running it.
- **Use Map/Measure to feed your [audit evidence](audit-evidence.md)** — the artifacts the loop produces
  (risk maps, eval results) are the same artifacts the [EU AI Act](eu-ai-act.md) wants documented. Run
  the loop once, satisfy both.
- **Re-enter the loop on every capability change** — treat "added a tool" or "swapped the model" as a
  trigger to re-Map and re-Measure, not a silent config edit.

## Sources

- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — primary source for the Govern / Map / Measure / Manage core functions and Govern as cross-cutting.
- **[Generative AI Profile (NIST AI 600-1, PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)** (NIST) — the binding Generative AI Profile document itself (published 26 July 2024), mapping generative-AI risks onto the four functions.
- **[AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/)** (NIST AI Resource Center) — the navigable core, categories, and subcategories behind the four functions.

<!-- page-type: standard -->
