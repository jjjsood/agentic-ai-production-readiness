# When to use agents — risk register

> **In one sentence:** These are the risks of *over-reaching* on the autonomy ladder — taking more agency
> than the task needs — each scored so you can sequence the decision, and each closed by dropping a rung or
> pricing the one you keep.

The risks below share a root: the system works in a demo, so a higher autonomy rung is adopted than the task
requires — and the cost, reliability, and infrastructure bills of that rung arrive later, in production.
Read the score as a priority sort, not a probability. For the reasoning behind the controls, see the
[When to use agents overview](../docs/when-to-use-agents/README.md); every control below also resolves to a
tickable line in the [When to use agents checklist](../checklists/when-to-use-agents.md), so a high-score
risk maps to a concrete go-live gate.

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, trust, schedule) · 3 severe (cancelled programme, liability, unrecoverable cost).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **Demo mistaken for evidence** — a curated reel approves a build the production conditions never matched | 3 | 3 | 9 | Require a reproducible run before committing a rung — [Cognition / Devin demo](../docs/case-studies/cognition-devin-demo.md), [Gemini hands-on](../docs/case-studies/google-gemini-handson-demo.md) |
| 2 | **Agent where a workflow would do** — autonomy chosen for a pre-mappable task, importing the full infra bill for no gain | 3 | 2 | 6 | Validate against the three signals; pick the lowest rung that works — [Workflow vs. agent](../docs/when-to-use-agents/workflow-vs-agent.md) |
| 3 | **AI where classical code would do** — an LLM put into a stable, reproducible, deterministic-shaped path | 3 | 2 | 6 | Deterministic-where-possible; prefer non-agentic solutions for structured work — [When not to reach for AI](../docs/when-to-use-agents/when-not-to-use-ai.md) |
| 4 | **Fluent-but-wrong answer ships** — on a path where a plausible, well-formatted wrong output is costly, the LLM fails *fluently* and passes a casual eye (operator held liable) | 2 | 3 | 6 | Keep high-cost-of-error paths on a system that fails loudly/predictably, not one that hallucinates persuasively — [When not to reach for AI](../docs/when-to-use-agents/when-not-to-use-ai.md), [Air Canada chatbot](../docs/case-studies/air-canada-chatbot.md) |
| 5 | **Runaway cost from over-agency** — token spend at ~4×/~15× the chat baseline with no value to clear it | 2 | 3 | 6 | Price the per-task value against the rung's token multiple before adopting it — [Cost of agency](../docs/when-to-use-agents/cost-of-agency.md) |
| 6 | **Compounding-error collapse** — a long autonomous chain whose pⁿ reliability falls below usable | 3 | 2 | 6 | Minimise autonomous steps; keep runs short-horizon; humans on the steps that matter — [Cost of agency](../docs/when-to-use-agents/cost-of-agency.md) |
| 7 | **Premature multi-agent** — splitting into agents before a single agent's tools are exhausted, multiplying identities and failure surface for minimal gain | 2 | 2 | 4 | Single agent first; justify each added agent against real parallelism — [Multi-agent vs. single](../docs/when-to-use-agents/multi-agent-vs-single.md), [MAST](https://arxiv.org/abs/2503.13657) |
| 8 | **Deflection oversold as replacement** — the agent handles the routine majority, then is scaled past a missing escalation path | 2 | 3 | 6 | Design and observe the human handoff before scaling; deflection ≠ replacement — [Klarna](../docs/case-studies/klarna-ai-assistant.md) |
| 9 | **Cancelled programme / agent washing** — escalating cost, unclear value, weak risk controls, or ordinary automation rebranded as "agentic" kill the project late | 2 | 3 | 6 | Decision written with reasoning; value and infra costed up front; confirm the work is genuinely agentic, not rebranded automation — [When to use agents overview](../docs/when-to-use-agents/README.md) |

---

## Sources

- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — the ~4×/~15× token multiples behind risks 4 and 6.
- **[Measuring AI ability to complete long tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)** (METR) — reliability falls with task length, behind risk 5.
- **[Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)** (Cemri et al., UC Berkeley) — multi-agent gains often minimal vs single-agent, behind risk 6.
- **[Gartner predicts over 40% of agentic AI projects will be canceled by 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)** (Gartner) — the cancellation-on-cost/value/risk prediction behind risk 8.
- **[Well-Architected GenAI Lens — GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — deterministic-where-possible, the control behind risks 2 and 3.

<!-- page-type: risk-register -->
