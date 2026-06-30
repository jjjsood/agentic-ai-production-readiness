# Limits & budgets — go-live checklist

> **In one sentence:** Every box below is a cap you can point at in code — if you cannot tick it, your
> agent has no enforced off-switch and the bill (or the side effects) are unbounded.

Run this before sign-off on any agent that calls a metered model, runs in a loop, or touches side-effecting
tools. A failed box is not an automatic blocker — it is a residual risk someone has to *accept in writing*.
For the why behind each theme, see the [Limits & budgets overview](../docs/limits-and-budgets/README.md).

---

## Token & cost budgets

- [ ] A **per-run token/cost ceiling** is enforced; the run terminates before the call that would breach it. ([Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md))
- [ ] A **per-day budget per feature/team** is enforced (catches many cheap runs that pass the per-run cap).
- [ ] A **per-tenant / per-user quota** caps spend attributable to one identity. ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/))
- [ ] Tokens are counted from the **provider's response**, not estimated from text length.
- [ ] An **input-size / per-request token cap** bounds how many tokens a single request can demand. ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/))
- [ ] **Budget alerts fire before the limit** (e.g. staged % thresholds). ([FinOps for AI](../docs/limits-and-budgets/cost-and-token-budgets.md))
- [ ] An **anomaly alert** flags spend diverging from baseline even while under budget. ([FinOps for AI](../docs/limits-and-budgets/cost-and-token-budgets.md))

## Rate, loop & timeout caps

- [ ] A **max-iteration ceiling** bounds loop turns per run, sized to the task. ([Building effective agents](https://www.anthropic.com/research/building-effective-agents))
- [ ] A **recursion-depth cap** bounds sub-agent spawning (multi-agent fan-out).
- [ ] A **per-step timeout** wraps each individual tool/model call. ([Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md))
- [ ] A **wall-clock timeout** wraps the whole run. ([Rate, loop & timeout caps](../docs/limits-and-budgets/rate-loop-timeout-caps.md))
- [ ] **Rate limits / quotas** restrict requests per source entity per window. ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/))
- [ ] **No-progress detection** breaks the loop on N repeated identical calls / no new state.

## Circuit breaker & denial-of-wallet

- [ ] A **spend-rate circuit breaker** trips to a hard stop on a rate spike (or repeated calls / consecutive 429s), not only on latency or quality. ([Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md))
- [ ] Monitoring watches **cost/spend rate**, not just uptime/latency (denial of wallet leaves availability alarms green). ([arXiv — DoW](https://arxiv.org/abs/2508.19284))
- [ ] The breaker has a **safe open state** (graceful degradation / human escalation), not a crash. ([Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md))
- [ ] The breaker resets **deliberately** (human ack or cool-down with the cause addressed), not auto-flap back into the runaway. ([Denial of wallet](../docs/limits-and-budgets/denial-of-wallet.md))

## Enforcement & side effects

- [ ] Every cap is enforced in **deterministic orchestration code**, not asked of the model in a prompt. ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/))
- [ ] Side-effecting agents carry a **cap on mutating actions per run** (the bill is often the least bad outcome). ([Replit database deletion](../docs/case-studies/replit-database-deletion.md))
- [ ] Every model/tool call carries a **stable tag** (feature/agent/session/tenant) so cost is attributable and quotas are per-entity. ([Cost & token budgets](../docs/limits-and-budgets/cost-and-token-budgets.md))

---

## Sources

- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — backs the rate-limit, quota, input-size, timeout/throttling, anomaly-detection, graceful-degradation, and enforce-outside-the-model lines.
- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — backs the max-iteration stopping-condition line.
- **[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — backs the tagging/attribution, per-feature budget, and anomaly-alert lines.
- **[A Comprehensive Review of Denial of Wallet Attacks](https://arxiv.org/abs/2508.19284)** (arXiv) — backs the "watch spend rate, not just uptime" line: DoW escalates cost without degrading availability.

<!-- page-type: checklist -->
