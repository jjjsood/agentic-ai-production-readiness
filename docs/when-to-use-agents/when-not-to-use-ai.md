# When not to reach for AI at all — the rung below workflow

> **In one sentence:** Below the lowest agentic rung is plain deterministic code, and for a large class of
> tasks it is not just cheaper but *more correct* — putting an LLM in that path adds stochastic risk and an
> infrastructure bill to a problem that had neither.

> Part of **[When to use agents overview](README.md)**

The autonomy ladder has a rung beneath "LLM-augmented workflow": no model in the path at all. It is easy to
forget once a team has decided "we're doing AI," but the question that should come first is whether the task
needs a language model to begin with. For a stable, structured, reproducible problem, classical code — a
regex, a SQL query, a state machine, a lookup table, a small classifier — wins outright on cost, latency,
reproducibility, and auditability. Reaching past it for an LLM imports non-determinism and the whole
infrastructure obligation of this repository into a problem that had neither.

---

## The signals that say "use classical code"

Each of these favours deterministic code or classical ML over an LLM. If two or more hold, the LLM is almost
certainly the wrong rung. The unifying primary rule is AWS's: be **deterministic where possible**, and
enforce behaviour in code rather than asking a model to comply
([AWS GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)).

- **The rules are stable and few.** They fit a decision table a human can read and a unit test can pin. An
  LLM here trades a verifiable artefact for a probabilistic one. This is the inverse of OpenAI's
  "difficult-to-maintain rules" signal: brittle, sprawling rules can earn an agent; small, stable ones do
  not ([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
- **Exact reproducibility is required.** When the same input must give the same output — for correctness, or
  to be defensible in an audit — a stochastic generator is the wrong primitive. Even at temperature 0 an LLM
  is only *near*-deterministic in practice: production inference endpoints are typically not batch-invariant,
  so as server load (and thus batch size) varies, identical inputs can produce different outputs — the
  primary reason most inference endpoints are nondeterministic
  ([Thinking Machines Lab — Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)).
  Reproducibility is therefore an argument *against* the LLM rung, not something to expect from it by default.
- **A cheap, correct deterministic solution already exists.** If a regex, a SQL query, a state machine, or a
  lookup already solves it, an LLM is strictly worse — slower, costlier, and fallible where the existing
  code is exact. Google Cloud makes the positive case directly: predictable, highly structured, or
  single-call work is more cost-effective as a **non-agentic** solution
  ([Google Cloud — Choose a design pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)).
- **A plausible-but-wrong answer is expensive.** LLMs fail *fluently* — a confident, well-formatted wrong
  answer is the dangerous failure mode, because it passes a casual eye. Where that cost is high, you want a
  system that fails loudly and predictably, not one that hallucinates persuasively. Air Canada's bot
  inventing a refund policy is the canonical version: a fluent wrong answer the operator was held liable for
  ([Air Canada chatbot](../case-studies/air-canada-chatbot.md)).
- **The path is high-volume and latency-sensitive.** When per-call model cost and tail latency dominate the
  budget, a deterministic path — which typically runs orders of magnitude faster and cheaper than a model
  call, the exact margin depending on workload and model (illustrative, not a measured figure) — beats a
  model call on every axis that matters.

## Why "just add AI" is a net-negative trade here

Putting an LLM into a deterministic-shaped problem doesn't only fail to add value; it *subtracts* it, on
several axes at once. You trade an exact answer for a probabilistic one. You trade the low, predictable
latency and cost of a code path for a model call's latency and token cost (the gap is typically large but
workload-dependent — illustrative, not a measured figure). And — most relevant to this repository — you trade a
piece of code that needs only ordinary software testing for one that now needs the full agentic
infrastructure stack: guardrails against bad output, observability to reconstruct what it did, limits so it
can't run away, and a rollback path. OWASP's **Excessive Agency** and **Unbounded Consumption** are the
named failure surfaces you've just opted into ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/),
[OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). The infrastructure thesis
of this repository applies in reverse: the surest way to avoid an infrastructure-gap failure on a task is to keep
the task on a rung that doesn't require the infrastructure.

## Where the LLM does earn its place

This is not an argument against LLMs — it is an argument for matching the tool to the task. The genuine
signals are the mirror image of the list above and are covered in
[workflow vs. agent](workflow-vs-agent.md): nuanced or exception-heavy judgement, rulesets too large and
volatile to maintain by hand, and heavy reliance on unstructured language or documents
([OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
The discipline is sequential: first ask whether deterministic code does the job; if not, whether an
LLM-augmented workflow does; only then whether the task earns an autonomous agent. Each rung you can decline
is infrastructure you never have to build, harden, observe, and be able to roll back.

## Sources

- **[Well-Architected GenAI Lens — GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — "deterministic where possible": enforce in code, not the prompt — the rule behind this whole page.
- **[Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)** (Google Cloud) — predictable / highly structured / single-call work is more cost-effective as a non-agentic solution.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — the three signals that *do* earn an agent, the mirror image of the "use classical code" signals here.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP) — the agency-related failure surface an unneeded LLM/agent opts into.
- **[OWASP LLM10: Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP) — the consumption-related failure surface an unneeded LLM/agent opts into.
- **[Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)** (Thinking Machines Lab) — why inference endpoints are nondeterministic even at temperature 0: production kernels are not batch-invariant, so varying server load changes identical-input outputs.

<!-- page-type: standard -->
