# Observability & evals — go-live checklist

> **In one sentence:** Each box below is something you should be able to point at and demonstrate — if you
> can't, you can't yet *see* what your agent does or *prove* it still works.

Run this before sign-off on any agent that touches real users, money, or records, and again before any
prompt, model, or flow change. A failed box is not an automatic blocker — it is a residual risk someone has to
accept in writing. For the why behind each theme, see the
[Observability & evals overview](../docs/observability-and-evals/README.md).

---

## Tracing & reconstruction

- [ ] **Structured tracing is on by default** for every run — agent, model, tool, and retrieval spans captured automatically, not behind a debug flag. ([Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md))
- [ ] Spans follow the **OpenTelemetry GenAI `gen_ai.*` conventions** and are pinned to a schema version (the conventions are still experimental). ([OpenTelemetry GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/))
- [ ] A **single run is reconstructable** from a run/conversation id — full span tree, tool arguments and results, model responses, end state.
- [ ] **Trace retention is set to a stated window** that covers the incident-review period and meets the applicable record-keeping floor — for an EU high-risk system that floor is **at least six months** of automatic logs (defer the exact figure to the [EU AI Act deep-dive](../docs/compliance-and-governance/eu-ai-act.md)).

## Token accounting & cost attribution

- [ ] **Input and output token counts are recorded on every model call** (`gen_ai.usage.input_tokens` / `output_tokens`) and summed to a per-run total. ([OpenTelemetry GenAI registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/))
- [ ] Every call carries an **attribution tag** (feature / agent / session / tenant) so spend aggregates per feature — added from day one, not retrofitted. ([FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/))
- [ ] **Anomaly alerting on per-run token total and cost** fires before spend spirals, not after the invoice.
- [ ] **A financial-anomaly alert watches spend-rate and per-tenant cost spikes** to catch denial-of-wallet / runaway-loop abuse, which availability monitoring never fires on. ([Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md))
- [ ] **Cost per *successful* task is baselined per feature/tenant** and is a regression axis in the suite — so a change that lifts accuracy while doubling cost-per-success is caught. ([Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md))

## Privacy of the observability pipeline

- [ ] **PII and secrets are redacted at the boundary** before a span leaves the process — the trace backend is not an unmanaged PII store. ([OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/))
- [ ] Access to the trace/eval backend is **least-privilege** — only roles that need raw spans can read them.
- [ ] **Content-capture (prompts/completions) is a deliberate, bounded choice** — captured on purpose with a defined scope and retention, not logged in full by default.

## Offline eval / regression suite

- [ ] A **held-out regression suite** exists covering capability, reliability, safety, and cost cases. ([Agent-eval survey](https://arxiv.org/abs/2507.21504))
- [ ] The suite **grades the trajectory** (tool set, order properties, budget adherence, end state), not only the final answer. ([Agent evals](https://developers.openai.com/api/docs/guides/agent-evals))
- [ ] **Reliability is tested by repetition** — the same case is run multiple times, not scored on a single pass.
- [ ] LLM-as-judge graders use a **fixed rubric and randomised answer order** to blunt verbosity/position bias. ([LLM-as-judge biases](https://arxiv.org/pdf/2411.16594))
- [ ] LLM-as-judge verdicts are **anchored against human-labelled spot checks** (and multiple judges where it matters), not a single judge trusted blindly. ([LLM-as-judge biases](https://arxiv.org/pdf/2411.16594))

## Gating changes

- [ ] The suite **runs as a gate on every prompt, model, tool, or flow change** and blocks the change on a metric regression. ([OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices))
- [ ] The **model version is pinned** so a silent provider update is treated as a change that must pass the gate.
- [ ] Fast code-based graders run pre-merge; heavier judge/trajectory grading runs pre-release.

## Eval in production

- [ ] **Online evals sample live traces** and score them asynchronously, off the user's critical path. ([Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md))
- [ ] **User-verdict signals** (thumbs-down, regeneration, escalation-to-human rates) are tracked as early degradation alarms.
- [ ] **Quality metrics have a baseline and alert on sustained drift** — task success, refusal, trajectory-pass, tool-error, cost per run.
- [ ] The loop is **closed back to offline**: a flagged production failure is labelled and added to the golden set so the next regression run catches its class. ([Evals & regression suites](../docs/observability-and-evals/evals-and-regression-suites.md))

---

## Sources

- **[OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)** (OpenTelemetry) — backs the structured-tracing, `gen_ai.*` convention, and span-reconstruction lines.
- **[OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)** (OpenTelemetry) — backs the per-call token-usage attribute lines and the experimental-status caveat.
- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — backs the attribution-tag and per-run anomaly-alert lines.
- **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)** (OWASP) — backs the redaction / least-privilege observability-pipeline lines.
- **[Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)** (arXiv) — backs the four-axis (capability/reliability/safety/cost) suite line.
- **[OpenAI — evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)** (OpenAI) — backs the trajectory-grading line.
- **[OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)** (OpenAI) — backs the gate-on-every-change line.
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — backs the LLM-as-judge mitigation line.

<!-- page-type: checklist -->
