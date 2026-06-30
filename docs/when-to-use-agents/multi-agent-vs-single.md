# Multi-agent vs. single agent — the topology you have to earn

> **In one sentence:** Splitting one agent into many multiplies the token bill, the coordination surface,
> and the failure modes roughly an order of magnitude — so multi-agent is a topology you justify against
> real parallelism, not a default you reach for because "more agents sounds smarter."

> Part of **[When to use agents overview](README.md)**

Once a feature has earned the agent rung, a second architecture choice follows: one agent, or several
coordinating ones? It is tempting to treat multi-agent as the natural next step up in capability, but it is
better understood as the most expensive rung on the autonomy ladder — the one that multiplies every cost the
single-agent rung already carries. This page sets out what multi-agent actually costs, why its failures are
coordination failures rather than model-quality ones, and the narrow signals that genuinely earn it, so you
default to the simplest topology that works.

---

## What multi-agent costs over a single agent

The token bill is the first and bluntest cost, and it scales with the topology. Anthropic, reporting on its
own multi-agent research system, gives the primary anchors: "**agents typically use about 4× more tokens
than chat interactions**," and "**multi-agent systems use about 15× more tokens than chats**"
([Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
So moving from a single agent to multi-agent is itself roughly a further ~4× step on top of the single-agent
rung — and that multiple is structural: every additional agent has its own context, its own tool calls, and
its own loop, plus the orchestration traffic between them. That sets a hard gate Anthropic states directly:
"for economic viability, multi-agent systems require tasks where the value of the task is high enough to pay
for the increased performance." The per-task value has to clear an order-of-magnitude-higher bar before the
topology makes sense; treat the figures as ballpark anchors, not constants.

The second cost is coordination overhead, which is also where the reliability goes. A single agent keeps all
state in one context; a multi-agent system must pass context between agents, keep them aligned on a shared
goal, and merge their results — and each of those seams is a new place to fail. This is why adding agents
does not buy back the reliability that the [compounding-error math](cost-of-agency.md) takes away: more
agents means more autonomous steps and more inter-agent handoffs, not fewer.

## The gains are often minimal — and the failures are coordination failures

The strongest reason to default away from multi-agent is empirical. A UC Berkeley study analysed seven
multi-agent frameworks across 200+ tasks and 1000+ traces and found that multi-agent "performance gains…
often remain minimal compared with single-agent frameworks" — i.e. the extra agents frequently do not earn
their cost in capability ([Cemri et al., MAST, 2025](https://arxiv.org/abs/2503.13657)). More importantly,
the study located *where* multi-agent systems break: it catalogued 14 failure modes in three buckets —
**specification and system design (~44%)**, **inter-agent misalignment (~32%)**, and **task verification
(~24%)**. Read those buckets back: the dominant failures are about how the system was *designed and
coordinated*, not about how smart the underlying model is. That is the repository's infrastructure thesis sharpened
to the topology level — multi-agent systems fail on design and coordination infrastructure, so adding a more
capable model does not fix them, and adding more agents enlarges exactly the surface that fails.

The security view agrees that the surface grows. Each agent is a separate non-human identity with its own
tools and blast radius, so a multi-agent system multiplies the **Excessive Agency** surface
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)) and the **Unbounded
Consumption** surface ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)) —
runaway loops are commonly multi-agent fan-out — across N identities instead of one. More agents is more to
scope, observe, bound, and be able to stop.

## The narrow signals that earn multi-agent

Default to a single agent, and split only when a clear signal forces it. OpenAI's guidance is to maximise a
single agent's tools and prompts before splitting into multiple agents
([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)),
and Google Cloud's is the same: "start with a single agent," because multi-agent "requires additional
evaluation, security, reliability, and cost considerations"
([Google Cloud — Choose a design pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)).
Anthropic names the conditions under which the topology actually pays — and the conditions under which it is
the *worse* choice ([Anthropic — multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system)):

| Signal | Multi-agent fits when… | Single agent is better when… |
|--------|------------------------|------------------------------|
| **Parallelism** | The work splits into independent subtasks that can run at the same time | The steps are sequential and depend on each other |
| **Context size** | The information exceeds a single context window and separates cleanly per agent | Everything fits one window, or the agents would all need the same shared context |
| **Coupling** | Subtasks are loosely coupled — agents rarely need each other's intermediate state | Subtasks are tightly coupled, with heavy inter-agent dependencies (e.g. most coding) |

The pattern is: multi-agent earns its bill on **parallelisable, separable-context, loosely-coupled** work —
broad research fan-out is Anthropic's own example — and is the wrong tool for **sequential, shared-context,
tightly-coupled** work, where the coordination cost is pure overhead. Anthropic's sub-agent pattern is worth
the contrast: there, sub-agents exist to isolate context and return a distilled summary to a single
orchestrator, not because "more agents = smarter." If the justification for a second agent is capability
rather than parallelism or context separation, it is usually the wrong reason.

## Deciding the topology

- **Exhaust the single agent first.** Maximise its tools and prompts before splitting — most tasks that feel
  like multi-agent are a single agent with better tools ([OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), [Google Cloud](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)).
- **Require genuine parallelism or context overflow.** Split only when subtasks are independent and run
  concurrently, or when the information genuinely exceeds one context window and separates cleanly
  ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).
- **Reject it for coupled or shared-context work.** Sequential, interdependent, or shared-context tasks are
  the documented poor fit — the coordination cost buys nothing ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system); [MAST](https://arxiv.org/abs/2503.13657)).
- **Clear the ~15× bill.** The per-task value must justify roughly an order of magnitude more tokens than a
  chat call, plus the multiplied infrastructure — N identities, N tool scopes, N blast radii to observe and
  bound ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).

The discipline is the pillar's discipline applied one rung higher: pick the simplest topology that works,
because every agent you add is more of the infrastructure this repository is about, and the failures the data
records are coordination failures, not model-quality ones.

## Sources

- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — the ~4×/~15× token anchors, the economic-viability gate, and the fit/poor-fit signals (parallelism, context size, coupling) for multi-agent.
- **[Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)** (Cemri et al., UC Berkeley) — gains often minimal vs single-agent; 14 failure modes in three buckets (design ~44%, misalignment ~32%, verification ~24%), i.e. coordination failures, not model quality.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — maximise a single agent's tools and prompts before splitting into multiple agents.
- **[Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)** (Google Cloud) — "start with a single agent"; multi-agent adds evaluation, security, reliability, and cost considerations.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP) — the agency/blast-radius surface that multiplies across multiple agent identities.
- **[OWASP LLM10: Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP) — the runaway-cost surface that multi-agent fan-out amplifies.

<!-- page-type: standard -->
