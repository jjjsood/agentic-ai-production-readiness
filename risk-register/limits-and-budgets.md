# Limits & budgets — risk register

> **In one sentence:** These are the risks of an agent with no enforced off-switch — runaway cost, runaway
> loops, and the irreversible side effects they commit — each scored so you can sequence the hardening and
> tied to the cap that closes it.

The risks below share a root: the agent runs, and nothing in deterministic code stops it before cost,
iterations, or side effects spiral. Read the score as a priority sort, not a probability. For the reasoning
behind each control, see the [Limits & budgets overview](../docs/limits-and-budgets/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, safety, unrecoverable).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **No per-run ceiling** — a stuck or looping run consumes tokens/dollars unbounded until something external stops it | 3 | 3 | 9 | Enforced per-run token/cost ceiling that terminates before the next call — [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) |
| 2 | **Infinite / no-progress loop** — agent re-calls the same tool on an ambiguous result, "running" but cycling | 3 | 2 | 6 | Max-iteration ceiling + no-progress detection; wall-clock timeout — [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |
| 3 | **Runaway commits irreversible side effects** — a loop sends emails, writes rows, or deletes data before any stop fires | 2 | 3 | 6 | Enforced cap on mutating actions per run — [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) (evidence: [Replit database deletion](../docs/case-studies/replit-database-deletion.md)) |
| 4 | **Denial of wallet** — an attacker (or bug) escalates cost while availability stays green, so outage alarms never fire | 2 | 3 | 6 | Spend-rate circuit breaker + monitoring on cost rate, not just uptime — [Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md) |
| 5 | **Limit enforced only in the prompt** — "stop after N / don't spend > \$X" ignored, lost, or injected away | 3 | 3 | 9 | Deterministic enforcement in orchestration code, before the metered call — [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |
| 6 | **One tenant drains the budget** — no per-entity quota, so a single user/key consumes the whole allowance | 2 | 2 | 4 | Per-tenant quota + per-call tagging for attribution — [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) |
| 7 | **No cost attribution** — spend is one undifferentiated number; can't allocate, budget per feature, or justify a multi-agent design | 3 | 1 | 3 | Stable tag (feature/agent/session/tenant) on every call from day one — [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) |
| 8 | **Cost spirals on legitimate runs** — no caching, an oversized model on easy steps, unscoped retrieval, and unbounded output make every correct run cost far more than it should | 3 | 2 | 6 | Reduction levers — prompt caching, model right-sizing/routing, `max_tokens`, scoped retrieval, batching — to lower cost per successful task — [Caching & cost control](../docs/limits-and-budgets/caching-and-cost-control.md) |
| 9 | **Oversized input** — a single request demands a huge token volume (large pasted context, adversarial padding), blowing per-call cost or context before any per-run tally reacts | 2 | 2 | 4 | Input-size / per-request token cap enforced before the call — [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)) |

---

## Sources

- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — the risk class (DoS, economic loss, denial of wallet) and the rate-limit/quota/timeout/input-size/anomaly controls behind risks 1, 2, 4, 6, and 9.
- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — the max-iteration stopping condition behind risk 2.
- **[A Comprehensive Review of Denial of Wallet Attacks](https://arxiv.org/abs/2508.19284)** (arXiv) — the cost-escalation-without-outage threat behind risk 4.
- **[Replit AI agent deletes a production database](https://incidentdatabase.ai/cite/1152/)** (AI Incident Database) — the unbounded-side-effect failure behind risk 3.

<!-- page-type: risk-register -->
