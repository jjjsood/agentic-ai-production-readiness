# Tracing & token accounting — reconstruct one run, attribute every token

> **In one sentence:** A production agent needs a structured trace of every run and a token count on every
> call, because without them "we couldn't reconstruct what happened" — and "we don't know why the bill
> jumped" — are infrastructure failures, not model ones.

> Part of **[Observability & evals overview](README.md)**

An agent is non-deterministic between runs, so you cannot reproduce a failure by replaying the inputs — the
only reliable record is the one you captured *while it ran*. This page covers what that record contains: a
structured trace built on the OpenTelemetry GenAI conventions, per-run token accounting, how to replay a
single run after the fact, and how to tag cost so it is attributable rather than a monthly surprise. It is
written for the engineer who will be paged at 2 a.m. and needs to answer *what did run #48213 actually do*.

---

## The trace is the tree of one run

The unit of observability for an agent is the **trace**: one run captured as a tree of nested **spans**. The
root span is the agent invocation; under it sit a child span for each model call, each tool execution, and
each retrieval — every step that touched the run, with start/end time, inputs, outputs, and status. Because
an agent **makes dynamic decisions and is non-deterministic between runs even with identical prompts**,
re-running the inputs does not reproduce the failure; the captured trace is the only way back to what
happened ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).

A useful trace lets you answer, for a single run, all of:

- **What did it call, in what order?** The span tree *is* the trajectory — the sequence of tool and model
  calls the agent chose.
- **With what arguments, and what came back?** Each tool span carries the call arguments and the result.
- **Where did it stall, loop, or branch?** Repeated identical tool-plus-args spans are the signature of a
  loop; a timing gap shows where it hung.
- **What did each step cost?** Token counts per model span, summed to a per-run total (below).

## Use the OpenTelemetry GenAI conventions — and pin the version

Rolling your own trace schema means every tool and backend speaks a different dialect. The emerging
vendor-neutral standard is the **OpenTelemetry GenAI semantic conventions**, which define a common `gen_ai.*`
attribute set and span types so a trace is portable across instrumentation and backends
([OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)).
The attributes a production trace leans on, per the official registry
([OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)):

| Attribute | What it records |
|---|---|
| `gen_ai.operation.name` | The operation — e.g. `invoke_agent`, `execute_tool`, `chat`. |
| `gen_ai.request.model` / `gen_ai.response.model` | The model requested vs the model that actually answered. |
| `gen_ai.provider.name` | The provider (well-known values include `openai`, `anthropic`, `aws.bedrock`, `gcp.vertex_ai`). |
| `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` | Tokens in the prompt and in the completion — the cost and audit unit. |
| `gen_ai.agent.id` / `gen_ai.agent.name` | Which agent ran the step. |
| `gen_ai.tool.name` / `gen_ai.tool.type` | Which tool a span executed. |
| `gen_ai.conversation.id` | The session/thread that joins related runs. |

Two design cautions. First, these GenAI conventions are explicitly marked **experimental / in development**,
not stable — pin to a schema version and expect attribute names to move
([OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)).
Second, the conventions let you capture prompt and completion *content* on spans — useful for debugging, and a
privacy liability if logged raw (see below). Several agent SDKs and tracing backends emit these spans as
neutral examples, but the value is the schema, not any one product.

## Per-run token accounting

Token counts on each model span are the raw material; the accounting is summing them to a **per-run total**
and attaching that total to something you can budget against. Token is the atomic cost unit of an AI
workload, and the FinOps-for-AI discipline is to make per-feature token budgets first-class with usage limits,
quotas, and anomaly detection that fire *before* costs spiral
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). This matters more
for agents than for chat because an agent emits many model calls per task — a multi-agent system can use on
the order of **~15× the tokens of a single chat** — so a missing per-run token meter hides the largest line
item ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Practically, record on every model span both `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`,
roll them up per run, and treat a per-run token total as a metric you can alert on — a token count that climbs
with no new state is the same loop signature seen in the trace tree, surfaced as a number.

## Cost attribution: tag from day one, or you can't attribute later

Counting tokens is not the same as knowing *whose* tokens they are. Attribution is an architectural decision
you make at the first line of instrumentation, not a report you generate later: every model call carries a
tag — `feature_id`, agent id, session id, tenant — so spend can be aggregated per feature, team, or product
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). Add the tag on day
one; retrofitting it means re-deriving who spent what from un-attributed logs, which usually cannot be done.
And remember the distinction the FinOps community draws: **visibility is not control** — a dashboard that
*shows* runaway spend after the fact is not the same as a budget that *stops* it (the spend-limit enforcement
itself belongs to the limits-and-budgets discipline; here the job is to produce the attributable signal it
acts on).

## Reconstructing a single run

Incident reconstruction is the payoff. Given a run id or a `gen_ai.conversation.id`, you should be able to
pull the whole span tree and walk it: the agent's plan, every tool call and its arguments, every model
response, where it looped or branched, what it ultimately did, and what it cost. This is also the audit
artifact the compliance pillar requires — the EU AI Act's record-keeping obligation is, in effect, "be able
to reconstruct what the system did", and a per-run trace is how you produce it without a separate forensics
project ([compliance & governance overview](../compliance-and-governance/README.md)). The rule that makes
reconstruction possible is unglamorous: **traces on by default, captured as a by-product of every run** — not
a debug flag someone forgot to enable on the run that went wrong.

## Don't turn the trace pipeline into a PII store

The same instrumentation that captures prompts, tool arguments, and completions will, by default, capture the
personal and secret data flowing through them — silently turning a trace backend into an unmanaged PII and
secrets store. Sensitive-information disclosure is a top LLM risk in its own right, and observability
pipelines are a common place it leaks ([OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)).
Redact at the boundary *before* the span leaves the process, apply least-privilege access to the trace
backend, and set a retention window that matches the legal and incident need rather than "keep everything
forever". Capturing the trajectory and token counts does not require capturing every raw secret alongside
them.

---

## Sources

- **[OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)** (OpenTelemetry) — the vendor-neutral span schema (`invoke_agent`, `execute_tool`, child `chat` spans) the trace tree is built on.
- **[OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)** (OpenTelemetry) — the `gen_ai.*` attribute table (operation, model, token usage, provider, agent, tool, conversation) and the **experimental / in-development** stability status.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — backs non-determinism between runs (can't reproduce by rerun) and the ~15× multi-agent token cost.
- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — token as the atomic cost unit, per-feature budgets/quotas/anomaly detection, and the tag-from-day-one attribution requirement.
- **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)** (OWASP) — sensitive-information disclosure as a top risk, behind the "don't turn the trace pipeline into a PII store" section.

<!-- page-type: standard -->
