# When to use agents — decision checklist

> **In one sentence:** Every box you can tick is a reason you are on the *lowest* autonomy rung that does
> the job — and every notch of agency you decline is infrastructure you never have to build and defend.

Run this before committing a feature to an autonomy rung — ideally before any agent code is written, and
again whenever you are tempted to climb (workflow → single agent → multi-agent). A failed box is not an
automatic veto; it is a residual reason to drop a rung, or to accept the higher rung's bill in writing. For
the why behind each theme, see the [When to use agents overview](../docs/when-to-use-agents/README.md).

---

## Should this be AI at all?

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Rules not stable-and-few | Rules wouldn't fit a decision table a test can pin (if they would, use code) | [When not to reach for AI](../docs/when-to-use-agents/when-not-to-use-ai.md) |
| ☐ | No exact reproducibility need | Same-input-same-output isn't a correctness/audit constraint (LLMs are only near-deterministic even at temp 0; endpoints aren't batch-invariant, so load changes identical-input outputs) | [Thinking Machines — Defeating Nondeterminism](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) |
| ☐ | No deterministic solution exists | No cheap, correct regex/SQL/state-machine/lookup already solves it outright | — |
| ☐ | Not latency/volume-critical | Not high-volume-and-latency-critical such that per-call model cost and tail latency dominate | — |

## Workflow or agent?

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Not a fixed decision tree | Task can't be pre-mapped as a fixed decision tree; if it can, a workflow (predefined code paths) is chosen over an agent | [Workflow vs. agent](../docs/when-to-use-agents/workflow-vs-agent.md) |
| ☐ | One agent-earning signal holds | Tick the specific signal below — don't nod at the set | [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | ↳ Complex decision-making | Nuanced, exception-heavy, context-sensitive judgement (e.g. a refund weighed against loyalty and dispute history) | [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | ↳ Difficult-to-maintain rules | A ruleset so large/tangled that updates are costly and error-prone | [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | ↳ Unstructured-data reliance | Interpreting natural language, extracting meaning from documents, conversing | [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | Boundaries enforced in code | Boundaries that must hold are enforced in code, not in the prompt (deterministic where possible) | [AWS GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html) |
| ☐ | Lowest sufficient rung | The chosen rung is the lowest that meets the requirement; agency was increased only because complexity required it | [AWS — Agentic AI](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html) |
| ☐ | Genuinely needs agency | Not ordinary automation rebranded ("agent washing"); earns the agent rung against the signals, not the marketing | [Gartner — cancellation forecast](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) |

## Single agent or multi-agent?

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Exhaust the single agent | A single agent's tools and prompts are exhausted before adding a second agent | [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | Justify multi-agent | Justified by genuine parallelism / context exceeding one window, not "more agents = smarter" — gains often minimal vs single-agent | [MAST](https://arxiv.org/abs/2503.13657) |
| ☐ | Not shared-context work | Work isn't shared-context or tightly inter-dependent (where multi-agent is the *worse* fit) | [Anthropic — multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system) |

## Does the value clear the bill?

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Value clears token multiple | Per-task value clears the token multiple of the rung (order of ~4× a chat call for an agent, ~15× for multi-agent) | [Anthropic — multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system) |
| ☐ | Bound autonomous steps | Unsupervised steps bounded; each hop justified against its pⁿ reliability cost (each step ~95% → ~60% over 10 hops, ~36% over 20) | — |
| ☐ | Short-horizon run | The autonomous run is short-horizon, not a multi-hour open-ended loop where reliability collapses | [METR](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) |
| ☐ | Cost includes infrastructure | Limits, guardrails, observability, scoped identity, rollback are in the cost estimate, not assumed free | — |

## Evidence before commitment

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Reproducible run, not demo | Decision rests on a reproducible run, not a curated demo reel | [Cognition / Devin demo](../docs/case-studies/cognition-devin-demo.md) |
| ☐ | Design the handoff path | Where the agent handles a subset, the escalation/handoff for the rest is designed before scaling — deflection is not replacement | [Klarna](../docs/case-studies/klarna-ai-assistant.md) |
| ☐ | Write down the decision | The rung decision is written down with its reasoning, so a later "why is this an agent?" has an answer | — |

---

## Sources

- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — backs the simplest-rung-first and single-agent-first rows.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — backs the ~4×/~15× token-multiple and multi-agent-poor-fit rows.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — backs the three agent-earning signals and exhaust-a-single-agent-first.
- **[Well-Architected GenAI Lens — Agentic AI / GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — backs "deterministic where possible" and "increase agency only when complexity requires it."
- **[Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)** (Cemri et al., UC Berkeley) — backs the "multi-agent gains often minimal" row.
- **[Measuring AI ability to complete long tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)** (METR) — backs the short-horizon row.
- **[Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)** (Thinking Machines Lab) — backs the "near-deterministic even at temperature 0" reproducibility row.
- **[Gartner predicts over 40% of agentic AI projects will be canceled by 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)** (Gartner) — backs the "agent washing / genuinely agentic" gate.

<!-- page-type: checklist -->
