# Limits & budgets — go-live checklist

> **In one sentence:** Every box below is a cap you can point at in code — if you cannot tick it, your
> agent has no enforced off-switch and the bill (or the side effects) are unbounded.

Run this before sign-off on any agent that calls a metered model, runs in a loop, or touches side-effecting
tools. A failed box is not an automatic blocker — it is a residual risk someone has to *accept in writing*.
For the why behind each theme, see the [Limits & budgets overview](../docs/limits-and-budgets/README.md).

---

## Token & cost budgets

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Per-run token/cost ceiling | Enforced; run terminates before the call that would breach it | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) |
| ☐ | Per-day feature/team budget | Enforced per feature/team; catches many cheap runs that each pass the per-run cap | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |
| ☐ | Per-tenant / per-user quota | Caps spend attributable to one identity | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) |
| ☐ | Count tokens from response | Token counts taken from the provider's response, not estimated from text length | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md) |
| ☐ | Input-size / request cap | Per-request token cap bounds how many tokens a single request can demand | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) |
| ☐ | Budget alerts before limit | Staged % thresholds fire before the hard limit is hit | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |
| ☐ | Spend anomaly alert | Flags spend diverging from baseline even while still under budget | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |

## Rate, loop & timeout caps

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Max-iteration ceiling | Bounds loop turns per run, sized to the task | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md); [Building effective agents](https://www.anthropic.com/research/building-effective-agents) |
| ☐ | Recursion-depth cap | Bounds sub-agent spawning / multi-agent fan-out | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |
| ☐ | Per-step timeout | Wraps each individual tool/model call | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |
| ☐ | Wall-clock timeout | Wraps the whole run | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |
| ☐ | Rate limits / quotas | Restrict requests per source entity per window | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md); [OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) |
| ☐ | No-progress detection | Breaks the loop on N repeated identical calls / no new state | [Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md) |

## Circuit breaker & denial-of-wallet

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Spend-rate circuit breaker | Trips to a hard stop on a rate spike / repeated calls / consecutive 429s — not only on latency or quality | [Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md) |
| ☐ | Monitor spend rate | Alerts on cost/spend rate, not just uptime/latency (DoW leaves availability alarms green) | [Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md); [arXiv — DoW](https://arxiv.org/abs/2508.19284) |
| ☐ | Safe open state | Breaker degrades gracefully / escalates to a human — does not crash | [Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md) |
| ☐ | Deliberate breaker reset | Resets on human ack or cool-down with the cause addressed — no auto-flap back into the runaway | [Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md) |

## Enforcement & side effects

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Caps enforced in code | Every cap lives in deterministic orchestration code, not asked of the model in a prompt | [OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) |
| ☐ | Cap mutating actions/run | Bound on mutating actions per run (the bill is often the least-bad outcome) | [Replit database deletion](../docs/case-studies/replit-database-deletion.md) |
| ☐ | Stable cost tag per call | feature/agent/session/tenant tag on every model/tool call, so cost is attributable and quotas are per-entity | [Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md); [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |

---

## Sources

- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — backs the rate-limit, quota, input-size, timeout/throttling, anomaly-detection, graceful-degradation, and enforce-outside-the-model rows.
- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — backs the max-iteration stopping-condition row.
- **[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — backs the tagging/attribution, per-feature budget, and anomaly-alert rows.
- **[A Comprehensive Review of Denial of Wallet Attacks](https://arxiv.org/abs/2508.19284)** (arXiv) — backs the "watch spend rate, not just uptime" row: DoW escalates cost without degrading availability.

<!-- page-type: checklist -->
