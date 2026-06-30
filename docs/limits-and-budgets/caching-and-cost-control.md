# Caching & cost control — lower the bill, don't just cap it

> **In one sentence:** Ceilings stop a runaway; these levers — prompt caching, model right-sizing, batching,
> output-length control, and retrieval scoping — make every *legitimate* run cheaper, which is what turns a
> per-feature budget from a constant fight into a number you comfortably sit under.

> Part of **[Limits & budgets overview](README.md)**

The other deep-dives in this pillar *bound* spend: the [token and cost ceiling](cost-and-token-budgets.md),
the [rate, loop and timeout caps](rate-loop-timeout-caps.md), and the [denial-of-wallet circuit
breaker](denial-of-wallet.md) all stop an agent from spending more than it should. This page is the
complement — the levers that *reduce* what a correct run costs in the first place. The framing is FinOps
unit economics: the metric that matters is not total spend or a ceiling but **cost per successful task**, and
every lever here moves that number down without removing a single guardrail
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)).

---

## Optimise the unit, not just the total

A budget ceiling answers "how much may we spend?"; unit economics answers "is each run worth what it costs?".
The FinOps discipline for AI is to attach value and workload metrics to spend — **cost-per-call,
cost-per-resolved-ticket, satisfaction-score-divided-by-AI-cost** — so the lever you pull is judged by its
effect on the unit, not the invoice ([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)).
This reframing matters because the cheapest *total* (cap everything hard) and the cheapest *unit* (a correct
answer for the fewest tokens) are different goals, and the levers below optimise the second. The
[per-call tagging](cost-and-token-budgets.md) that makes attribution possible is the prerequisite — you
cannot tell whether a cache or a cheaper model improved the unit cost of a feature you cannot measure per
feature.

## Prompt & context caching — stop paying to re-read the same tokens

An agent loop re-sends a large, stable prefix on every turn: the system prompt, tool definitions, retrieved
context, the running transcript. Caching that prefix means you pay full price to process it once and a steep
discount on every subsequent reuse — directly attacking the agent's dominant cost, since token usage drives
roughly 80% of the variance in agent performance and cost
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
The provider economics are public, named here as neutral examples of the mechanism:

- One provider prices **cache reads at 0.1× the base input-token price** (a 5-minute cache write costs 1.25×,
  a 1-hour write 2×), so a stable prefix reused many times approaches a tenth of its uncached cost
  ([Anthropic — Prompt caching](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching)).
- Another applies caching automatically to prompts of **≥1,024 tokens**, cutting cached input-token cost by
  **up to 90%** and latency by **up to 80%** ([OpenAI — Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)).

Treat these multipliers as ballpark and provider-specific — they shift and have minimums and TTLs — but the
shape is consistent: structure the prompt so the stable, high-token part comes first and is cacheable, and
the per-turn variable part comes last.

## Right-size the model — don't send a hard model to an easy step

The most expensive habit is running every step on the most capable (most expensive) model. Most steps in an
agent loop are easy — classify, format, extract, decide which tool — and a smaller, cheaper model handles
them at a fraction of the cost. Two patterns:

- **Routing** — classify the step and send it to the model sized for it (cheap model for routine steps, the
  frontier model only where the task demands it).
- **Cascading** — try the cheap model first and *escalate* to a stronger one only when confidence is low or a
  validator rejects the output.

This is also the gate on multi-agent designs, which carry roughly a 15× token multiplier over chat and are
only worth it when task value clears that cost — so right-sizing is the first question, not multi-agent
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Keep a validator on the cheap path: right-sizing that silently lowers quality raises cost-per-*successful*-task
even as it lowers cost-per-call, which is why the unit must be the *successful* task.

## Control the output length — generated tokens are the pricier half

Output tokens are typically billed at a multiple of input tokens — published provider rate cards show
output priced several times above input per million tokens (one provider's published rates put output at
roughly **5× the input rate** across its current model line, a representative ballpark rather than a
universal constant) ([Anthropic — Pricing](https://platform.claude.com/docs/en/about-claude/pricing)). So an
agent that emits verbose intermediate reasoning, restates context, or returns more than the caller needs
spends disproportionately on the expensive half of the meter. Bound it: set a `max_tokens` ceiling
appropriate to the step, instruct for concise structured output, and prefer returning an identifier or a
short result the next step can act on over a long prose dump. This is a pure FinOps lever — fewer generated
tokens for the same successful outcome is a lower unit cost
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)).

## Scope retrieval — don't pay to stuff context that doesn't help

More context is not more capability; it is more tokens and, past a point, *worse* recall as the window fills.
Anthropic frames context as a finite resource to be spent on "the smallest possible set of high-signal
tokens," and recommends **just-in-time retrieval** — the agent holds lightweight references and loads data
via tools only when a step needs it — over pre-loading everything into the window
([Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
The cost effect is direct: tighter top-k, relevance filtering, and loading on demand all cut the input
tokens carried on every turn, and they compound with caching — a smaller, stable retrieved context is both
cheaper to send and cheaper to cache.

## Batching — amortise the work that isn't latency-sensitive

Not every agent task is interactive. For offline or bulk workloads — evaluations, backfills, large
document-processing runs — **batch** processing trades immediacy for a lower rate, and providers commonly
price an asynchronous batch tier below the synchronous one: two major providers publish an asynchronous
batch tier at a **50% discount** on both input and output tokens, in exchange for completion within a window
(commonly up to 24 hours) rather than in real time ([Anthropic — Pricing](https://platform.claude.com/docs/en/about-claude/pricing);
[OpenAI — Batch API](https://developers.openai.com/api/docs/guides/batch)). Treat the exact figure as
provider-specific and subject to change, but the shape — defer delivery, pay less — is consistent. Where a
task does not need a real-time response, routing it through a batch path lowers its unit cost for free; the
discipline is simply to classify which workloads are latency-sensitive and which are not, and send the
latter to the cheaper lane ([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)).

## Reduction sits beside the caps, never instead of them

These levers lower the bill; they do not bound it. A cached, right-sized, concise agent with no
[per-run ceiling](cost-and-token-budgets.md) and no [circuit breaker](denial-of-wallet.md) is still one loop
away from a runaway — cheaper per call only means the runaway takes marginally longer to hurt. The correct
posture is both: hard caps as the floor that guarantees an off-switch, and these reduction levers on top to
keep the *normal* unit cost low enough that the caps rarely fire. Reduction makes the budget livable; the
caps make it safe.

---

## Sources

- **[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — the unit-economics framing (cost-per-call / cost-per-successful-task, value metrics) and the discipline of optimising the unit and matching workloads to the cheapest viable lane.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — token usage explaining ~80% of agent cost/performance variance and the ~15× multi-agent multiplier that makes right-sizing the first question.
- **[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (Anthropic) — context as a finite resource and just-in-time retrieval, the basis for scoping retrieval to cut per-turn tokens.
- **[Prompt caching](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching)** (Anthropic) — vendor docs, neutral example: cache reads at 0.1× base input price, write multipliers and TTLs.
- **[Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)** (OpenAI) — vendor docs, neutral example: automatic caching for prompts ≥1,024 tokens, up to 90% cached-input cost and up to 80% latency reduction.
- **[Pricing](https://platform.claude.com/docs/en/about-claude/pricing)** (Anthropic) — vendor rate card, neutral example: per-model output tokens priced at roughly 5× input, and an asynchronous Batch API at a 50% discount on input and output.
- **[Batch API](https://developers.openai.com/api/docs/guides/batch)** (OpenAI) — vendor docs, neutral example: a 50% cost discount versus the synchronous API for non-real-time requests completing within 24 hours, corroborating the batch-below-synchronous pricing shape.

<!-- page-type: standard -->
