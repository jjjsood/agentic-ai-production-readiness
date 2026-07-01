# Observability & evals — go-live checklist

> **In one sentence:** Each box below is something you should be able to point at and demonstrate — if you
> can't, you can't yet *see* what your agent does or *prove* it still works.

Run this before sign-off on any agent that touches real users, money, or records, and again before any
prompt, model, or flow change. A failed box is not an automatic blocker — it is a residual risk someone has to
accept in writing. For the why behind each theme, see the
[Observability & evals overview](../docs/observability-and-evals/README.md).

---

## Tracing & reconstruction

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Tracing on by default | Agent, model, tool, and retrieval spans captured automatically for every run, not behind a debug flag | [Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md); [OpenTelemetry GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) |
| ☐ | OTel gen_ai spans | Spans follow the OpenTelemetry GenAI `gen_ai.*` conventions, pinned to a schema version (still experimental) | [OpenTelemetry GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) |
| ☐ | Reconstruct a single run | From a run/conversation id: full span tree, tool arguments + results, model responses, end state | [Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md) |
| ☐ | Trace retention window set | Stated window covering the incident-review period; the EU high-risk floor is ≥6 months of automatic logs | [EU AI Act deep-dive](../docs/compliance-and-governance/eu-ai-act.md) |

## Token accounting & cost attribution

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Record token counts | input/output token counts on every model call (`gen_ai.usage.input_tokens`/`output_tokens`), summed to a per-run total | [OpenTelemetry GenAI registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) |
| ☐ | Attribution tag per call | feature/agent/session/tenant tag on every call so spend aggregates per feature — added day one, not retrofitted | [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |
| ☐ | Alert on per-run spend | Anomaly alerting on per-run token total and cost fires before spend spirals, not after the invoice | [Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md); [FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/) |
| ☐ | Watch DoW spend-rate | Financial-anomaly alert on spend-rate and per-tenant cost spikes catches denial-of-wallet / runaway loops that availability monitoring never fires on | [Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md) |
| ☐ | Baseline cost per success | Cost per *successful* task baselined per feature/tenant and a regression axis — catches a change that lifts accuracy while doubling cost-per-success | [Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md) |

## Privacy of the observability pipeline

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Redact at the boundary | PII and secrets redacted before a span leaves the process; the trace backend isn't an unmanaged PII store | [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) |
| ☐ | Least-privilege trace access | Only roles that need raw spans can read the trace/eval backend | [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) |
| ☐ | Bounded content capture | Prompt/completion capture is a deliberate choice with defined scope + retention, not logged in full by default | — |

## Offline eval / regression suite

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Held-out regression suite | Covers capability, reliability, safety, and cost cases | [Agent-eval survey](https://arxiv.org/abs/2507.21504) |
| ☐ | Grade the trajectory | Grades tool set, order properties, budget adherence, end state — not only the final answer | [OpenAI — agent evals](https://developers.openai.com/api/docs/guides/agent-evals) |
| ☐ | Test reliability by repetition | The same case is run multiple times, not scored on a single pass | — |
| ☐ | Judge: fixed rubric | LLM-as-judge uses a fixed rubric and randomised answer order to blunt verbosity/position bias | [LLM-as-judge biases](https://arxiv.org/pdf/2411.16594) |
| ☐ | Anchor judge to humans | Judge verdicts anchored against human-labelled spot checks (multiple judges where it matters), not a single judge trusted blindly | [LLM-as-judge biases](https://arxiv.org/pdf/2411.16594) |

## Gating changes

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Gate every change | Suite runs as a gate on every prompt/model/tool/flow change and blocks the change on a metric regression | [OpenAI — eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) |
| ☐ | Pin the model version | Model version pinned so a silent provider update is treated as a change that must pass the gate | — |
| ☐ | Fast pre-merge, heavy pre-release | Fast code-based graders run pre-merge; heavier judge/trajectory grading runs pre-release | — |

## Eval in production

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Sample live traces | Online evals sample live traces and score them asynchronously, off the user's critical path | [Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md) |
| ☐ | Track user-verdict signals | thumbs-down, regeneration, and escalation-to-human rates tracked as early degradation alarms | — |
| ☐ | Baseline + drift alerts | Task success, refusal, trajectory-pass, tool-error, and cost per run have a baseline and alert on sustained drift | — |
| ☐ | Close the loop offline | A flagged production failure is labelled and added to the golden set so the next regression run catches its class | [Evals & regression suites](../docs/observability-and-evals/evals-and-regression-suites.md) |

---

## Sources

- **[OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)** (OpenTelemetry) — backs the structured-tracing, `gen_ai.*` convention, and span-reconstruction rows.
- **[OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)** (OpenTelemetry) — backs the per-call token-usage attribute rows and the experimental-status caveat.
- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — backs the attribution-tag and per-run anomaly-alert rows.
- **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)** (OWASP) — backs the redaction / least-privilege observability-pipeline rows.
- **[Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)** (arXiv) — backs the four-axis (capability/reliability/safety/cost) suite row.
- **[OpenAI — evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)** (OpenAI) — backs the trajectory-grading row.
- **[OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)** (OpenAI) — backs the gate-on-every-change row.
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — backs the LLM-as-judge mitigation rows.

<!-- page-type: checklist -->
