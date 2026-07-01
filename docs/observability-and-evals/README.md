# Observability & evals — if you can't trace it and can't measure it, you can't operate it

> **In one sentence:** Observability and evals are the infrastructure that lets you answer *"what did the
> agent actually do, and is it still good enough?"* — and when that infrastructure is missing, "we
> couldn't reconstruct what happened" is the attributable failure, not the model.

A stochastic, tool-using agent makes different decisions on identical input and acts in the world between
those decisions, so the two questions that decide whether you can run it in production are *can you see one
run* and *can you measure the whole population of runs*. The first is **observability** — structured traces,
per-run token accounting, the ability to replay a single session end to end. The second is **evaluation** —
a regression suite that gates every change before ship, plus online evals that watch quality in production
after it. This pillar is written for the on-call engineer and the team lead who own the agent after launch:
they can build it; the gap is *knowing* what it did and *proving* it still works. The
[deep-dives](#going-deeper) take each piece down to the mechanics.


## Where this breaks in production

The recurring failure here is invisibility. A system works in the demo, ships without the means to *see*
or *measure* it in production, and then misbehaves where no one is looking. New York City's official
MyCity bot gave small businesses illegal regulatory advice and was **left online and still producing it**
after the problem was widely reported — no monitoring flagged the wrong outputs and no measurement loop
would have caught them ([NYC MyCity](../case-studies/nyc-mycity-chatbot.md)).

The other half is mistaking a *demo* for a *measurement*. Cognition's Devin launch reel implied an agent
had closed a real paid engineering job end-to-end; independent review found a cherry-picked task,
self-inflicted errors the agent then "fixed," and a swapped environment
([Cognition Devin demo](../case-studies/cognition-devin-demo.md)). The same product became genuinely
useful at Goldman Sachs only once wrapped in mandatory human review and routed through the bank's existing
CI — once its output was *measured* every time rather than trusted once
([Goldman Sachs × Devin](../case-studies/goldman-sachs-devin.md)).

There's a structural reason the gap is wide: an agent is **non-deterministic between runs, even with
identical prompts**, so you cannot reproduce a failure by re-running the inputs — without a captured trace
there is often no way back to what happened
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Observability makes a single run recoverable; evals make the whole population measurable. Neither is
optional once the agent acts on real users, money, or records.

## A trace is the unit of "what happened"

You cannot debug, cost, or audit what you cannot see, and for an agent the thing to see is the **trace**:
the full tree of one run — the agent invocation, each model call, each tool execution, each retrieval —
captured as nested spans with timing, arguments, results, and token usage on every span. The emerging
vendor-neutral schema is the **OpenTelemetry GenAI semantic conventions**, standardising `gen_ai.*`
attributes and span types like `invoke_agent` and `execute_tool`
([OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)).
These conventions are still **experimental / in development**, so pin to a schema version and expect
attribute churn
([OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)).
**Generate the trace as a by-product of every run, from day one** — retrofitting traces is how a runaway
loop stays invisible for days.

## Tokens are the atomic cost and the audit unit

The same span that records *what the model did* should record *what it cost*: input/output token counts
per call, summed per run and tagged to a feature, agent, or session so cost is attributable rather than a
mystery on the invoice — the FinOps-for-AI discipline applied to agents, token as the atomic cost unit,
with per-feature budgets and anomaly detection firing *before* spend spirals
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). It matters more
for agents than chat: a multi-agent system can use **~15× the tokens of a single chat**, so a missing
token meter is a missing smoke alarm on the largest line item
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Token accounting is two jobs at once — cost attribution and an auditor-readable per-run record — both from
the same instrumented span.

## Single-shot success overstates reliability

The most expensive measurement mistake is to evaluate an agent once, see it pass, and call it reliable. The
standard benchmark number — **pass@1**, the chance one attempt succeeds — does not capture whether the
agent succeeds *every* time on the *same* task, which production actually requires. Sierra's **τ-bench**
makes the gap concrete: a state-of-the-art function-calling agent (gpt-4o) scored **under 50% pass@1**, and
its **pass^k** fell **below 25% at k=8** in the retail domain — a model that succeeds once often fails
doing the same thing eight times ([τ-bench](https://arxiv.org/abs/2406.12045)). A green demo is not a
green light; measurement has to continue *into* production, testing reliability under real, repeated,
adversarial traffic.

## Evals are a loop, not a launch gate

Evaluation is two complementary loops, not one pre-launch checkbox. The **offline** loop is a held-out
regression suite — capability, reliability, safety, cost cases — re-run on every prompt, model, or flow
change, blocking the change if a metric regresses; the **online** loop samples live traces and scores them
asynchronously so quality drift is caught in production before users complain. A mature setup connects
them: online evals flag a failure, a human labels it, the case enters the offline golden set, and the next
regression run catches that class earlier. Two cautions: **agent evals must grade the trajectory, not just
the final answer** — agents reach goals by different valid paths, so scoring the end-to-end trace finds
workflow regressions a final answer-check misses
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
And **LLM-as-judge is biased and overconfident** — verbosity, position, self-enhancement, and authority
biases — so pin a fixed rubric, randomise answer order, and anchor with human-labelled spot checks
([From Generation to Judgment](https://arxiv.org/pdf/2411.16594)).

## Going deeper

This page is the landscape; four deep-dives take each layer down to the mechanics:

- **[Tracing & token accounting](tracing-and-token-accounting.md)** the OpenTelemetry `gen_ai.*` span tree,
  per-run token accounting, and reconstructing a single run after the fact.
- **[Evals & regression suites](evals-and-regression-suites.md)** the offline suite — capability,
  reliability, safety, cost cases, trajectory grading, LLM-as-judge caveats — and gating a change on evals.
- **[Eval in production](eval-in-production.md)** why pass@1 ≠ reliable via the pass^k gap and τ-bench,
  then online evals and monitoring quality drift on live traffic.
- **[Cost & FinOps attribution](cost-and-finops-attribution.md)** attributed spend per feature/tenant/run,
  unit economics, the cost-regression gate, and the visibility half of denial-of-wallet detection.

When you reach sign-off, the [go-live checklist](../../checklists/observability-and-evals.md) makes each
control checkable and the [risk register](../../risk-register/observability-and-evals.md) scores what to
fix first; see [NYC MyCity](../case-studies/nyc-mycity-chatbot.md) for where undetected wrong outputs left
in production decided the outcome. The evidence this pillar produces is also the audit record
[compliance & governance](../compliance-and-governance/README.md) requires you to keep.

---

## Sources

- **[OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)** (OpenTelemetry) — the vendor-neutral `gen_ai.*` span schema for agent/tool/LLM spans (`invoke_agent`, `execute_tool`) behind the "a trace is the unit" section.
- **[OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)** (OpenTelemetry) — the `gen_ai.*` attribute definitions (operation, model, token usage, provider, agent, tool, conversation) and their **experimental / in-development** status.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — backs agents being non-deterministic between runs (can't reproduce by rerun), the ~15× multi-agent token cost, and trajectory- (not just outcome-) based evaluation.
- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — token as the atomic cost unit, per-feature budgets, and anomaly detection behind the cost-attribution section.
- **[τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)** (Sierra) — the pass@1 (<50%) vs pass^8 (<25%, retail) consistency gap behind "single-shot success overstates reliability".
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — the LLM-as-judge bias catalogue (verbosity, position, self-enhancement, authority) behind the evals-loop caveat.

<!-- page-type: overview -->
