# Cost & token budgets — make spend a number the system enforces

> **In one sentence:** A token budget is a ceiling the orchestration code enforces on tokens and dollars
> per run, per day, and per tenant — and the per-call cost attribution underneath it — so spend is a
> bounded, attributable quantity instead of a surprise on the invoice.

> Part of **[Limits & budgets overview](README.md)**

Visibility is not control. A dashboard that shows you spent \$9,000 last night is a post-mortem, not a
limit. This page is about making spend a *quantity the system refuses to exceed*: a per-run ceiling that
terminates the loop, a per-day and per-tenant quota that throttles, alerts that fire before the cap, and
the tagging that lets you say which feature, agent, or customer spent what. It is the slow-burn complement
to the [circuit breaker](denial-of-wallet.md) — budgets catch the steady drift; the breaker catches the
spike.

---

## Token is the unit of cost — count it authoritatively

For an LLM workload the atomic billable unit is the token, not the request or the CPU-second, so the
FinOps discipline starts by measuring tokens at the boundary and treating them as the meter
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). The reason this
matters for agents specifically is multiplicative: Anthropic's production data shows agents consume about
**4× the tokens of a chat interaction and multi-agent systems about 15×**, with "token usage by itself"
explaining roughly **80% of the variance** in task performance — so the same lever that buys capability
drives the bill ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Count input and output tokens per call from the provider's response, not by estimating from string length;
the provider's count is the one you are billed on.

## Set ceilings at three scopes

A single global budget is too coarse to stop the failure that matters. Set enforced ceilings at three
scopes, each catching a different runaway:

| Scope | What it caps | Why |
|-------|--------------|-----|
| **Per run** | Total tokens / dollars one agent invocation may consume before it is terminated | Bounds a single stuck or looping run — the cap that turns a runaway from "unbounded" into "expensive but finite". |
| **Per day (per feature/team)** | Aggregate spend for a feature, team, or product in a window | Catches many cheap runs that individually pass the per-run cap but together blow the budget. |
| **Per tenant / per user** | Spend attributable to one customer or identity | Contains [denial-of-wallet](denial-of-wallet.md) abuse where one entity drives cost, and makes per-customer unit economics real. |

OWASP names the platform mechanisms for these directly: **rate limiting and per-entity quotas**, input-size
limits to cap the tokens a single request can demand, and timeouts/throttling on resource-intensive
operations ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). The per-entity
quota is what makes "per tenant" enforceable rather than aspirational.

## Enforce the budget in code, before the next call

A budget written into the prompt — "don't spend more than \$5" — is not a budget; a stochastic model is
the wrong enforcer of a hard financial boundary. The enforceable pattern is a deterministic check in the
orchestration layer: maintain a running token/cost tally for the run, and **before dispatching each metered
call, check the tally against the ceiling and terminate if the next call would breach it**. The product
team owns the budget number; the gateway or orchestrator owns the kill — when a request would exceed
budget, it is refused (e.g. an HTTP 429), not completed and reconciled later. This is the same
"enforce outside the model" rule that governs every cap in this pillar
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).

## Alert before the limit, not at it

A ceiling that only signals when it is hit gives you no time to react. Pair every enforced ceiling with a
**threshold alert that fires earlier** — a conventional budget-alert pattern is to warn at staged
percentages of the limit (e.g. 50% / 80% / 100%) so a human sees the trend before the hard stop, and to
combine the static thresholds with **anomaly detection** that flags consumption diverging from the normal
baseline even when it is still under budget ([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/);
[OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). Anomaly detection is the
part that catches the *new* failure — a prompt change that doubled token use, a feature that started looping
— which a static threshold tuned to last month's numbers would miss until the bill.

## Attribution: tag every call or you can't allocate cost

You cannot budget per feature if you cannot measure per feature. The FinOps Foundation is explicit that a
tagging strategy is *essential* to organise and track AI cost by project, team, or workload, and to
separate environments and workload types (training vs. inference)
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). For agents the
load-bearing decision is architectural and best made on day one: attach a stable tag — a feature, agent,
session, or tenant identifier — to **every** model and tool call, so the same tally that enforces the
budget also answers "who spent this?". Without that tag, cost is a single undifferentiated number and no
per-scope ceiling above is actually attributable.

The unit-economics payoff is the reason to bother: with per-call attribution you can compute meaningful
ratios — cost-per-resolved-ticket, cost-per-call, satisfaction-score-divided-by-AI-cost — that turn a raw
spend number into a decision about whether the agent is worth running
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). That is also the
gate on multi-agent designs: a ~15× token multiplier is only justified when the task value clears it, and
you cannot make that call without the per-feature number ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).

## The bill is often the least bad outcome

A token budget is framed as a cost control, but its more important job is bounding **side effects**. A loop
that spends \$200 also sent N emails, wrote N rows, or processed N charges before anything stopped it — and
those are not refundable the way compute sometimes is. Replit's agent under a code freeze is the case: the
deleted production records, not the inference cost, were the damage, and the missing control was an enforced
action limit ([Replit database deletion](../case-studies/replit-database-deletion.md)). So a per-run budget
should be expressed not only in dollars but, where the tools are side-effecting, in a **cap on mutating
actions per run** — the cheapest control that bounds the irreversible.

---

## Sources

- **[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — token as the atomic cost unit, tagging as essential for per-feature/team/workload attribution, usage quotas, anomaly detection paired with limits, and the unit-economics ratios (cost-per-call, etc.).
- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — the platform controls behind the ceilings: rate limiting, per-entity quotas, input-size limits, timeouts/throttling, and anomaly detection on unusual consumption.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — agents ~4× and multi-agent ~15× chat tokens, token usage explaining ~80% of performance variance; the figures that size the per-run ceiling and justify (or reject) a multi-agent design.

<!-- page-type: standard -->
