# When to use agents — pick the least-agentic thing that works

> **In one sentence:** Every notch of autonomy you add is infrastructure you then owe — limits,
> guardrails, observability, identity, rollback — so the cheapest way to avoid an infrastructure-gap
> failure is to not buy the agency you don't need.

This is the pillar that runs *before* the other six. The infrastructure thesis of this repository — that
across ~591 documented incidents most attributable failures are infrastructure gaps, not model quality —
has a quiet corollary: the surest way to pass the infrastructure bill is to architect a system that
doesn't incur it. Agency is a spectrum, not a switch — deterministic code, then an LLM-augmented workflow,
then a single autonomous agent, then a multi-agent system — and the obligation to harden grows at every
rung. This page is written for the person choosing where on that ladder a feature should sit; the
[deep-dives](#going-deeper) then work each rung in detail.

---

## Where this breaks in production

The failure here is rarely loud at launch — a demo ships as a product. A curated reel shows an agent
finishing a job end-to-end, budget gets approved on the strength of it, and the gap to a reproducible
production run surfaces only in production. Cognition's Devin launch demo claimed an autonomous agent had
closed a real paid job; independent review found a cherry-picked task in the wrong environment, with the
agent fixing errors it had itself introduced ([Cognition / Devin demo](../case-studies/cognition-devin-demo.md)).
Google's viral Gemini "Hands-on" reel implied a live video-and-voice loop the shipped system didn't have
([Gemini hands-on demo](../case-studies/google-gemini-handson-demo.md)). Both: an agent-shaped capability
was *believed* before the infrastructure to run it autonomously existed.

The market is pricing this in. Gartner predicts **over 40% of agentic AI projects will be cancelled by end
of 2027**, citing escalating costs, unclear business value, and inadequate risk controls, and warns of
"agent washing" — ordinary automation rebranded as agentic
([Gartner, Jun 2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)).
Treat it as an analyst forecast, order-of-magnitude, not a measurement. The cheapest insurance against
being in that share: **don't reach for the agent rung first.**

## Agency is a spectrum, not a switch

The single most useful mental model: "agent" is a position on a ladder of autonomy, not a yes/no choice —
climb only as high as the task forces you. Anthropic draws the line: a **workflow** orchestrates LLMs and
tools "through predefined code paths," an **agent** "dynamically directs its own processes and tool
usage" — "find the simplest solution possible, and only increase complexity when needed"
([Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents)).

AWS reaches the same conclusion from the security side: "only increase the agency of the system when the
task complexity requires it" — a workflow keeps code paths "largely deterministic," an autonomous agent
runs a reason-and-act loop "until the LLM is given a stop reason"
([AWS Well-Architected — Agentic AI](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)),
and its blunter rule: **deterministic where possible**, enforced in code, not a prompt
([AWS GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)).
The autonomous rung is the ReAct (reason + act) loop
([Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)) — that loop, not the model, creates the
obligation to bound iterations, scope tools, and trace every step.

The picture, lowest agency at the top:

| Rung | What it is | What it costs you in infrastructure |
|------|------------|-------------------------------------|
| **Deterministic code** | Regex, SQL, a state machine, a lookup table — no model in the path | Ordinary software testing; reproducible, auditable, cheap |
| **LLM-augmented workflow** | Predefined code paths, a few steps delegated to an LLM | Eval the LLM steps; the control flow is still yours |
| **Single agent** | One LLM directing its own tools in a loop, with a stop condition | Loop/iteration caps, tool scoping, tracing, HITL on writes, rollback |
| **Multi-agent system** | Several agents coordinating, an orchestrator fanning out | All of the above × N identities, × the blast radius, × the failure surface |

You don't pick a rung for its own sake; you pick the lowest one that does the job, because the right-hand
column is exactly the infrastructure bill this repository is about.

## The few signals that actually earn an agent

OpenAI names three signals where rules-based automation breaks down and an agent pays off: **complex
decision-making** (nuanced judgement, exceptions, context-sensitive calls), **difficult-to-maintain rules**
(a ruleset too large and tangled to update safely), and **heavy reliance on unstructured data** (natural
language, documents, conversation). Its gate: "validate that your use case can meet these criteria
clearly. Otherwise, a deterministic solution may suffice"
([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
Google Cloud agrees from the other direction — predictable, single-call workloads are better served
**non-agentic**, and when you do need an agent, "start with a single agent"
([Google Cloud — Choose a design pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)).

Two reliability facts argue for the shortest, least-agentic path. Autonomy degrades with task length: METR
measured frontier agents near 100% success on tasks under 4 minutes but under 10% on tasks over ~4 hours
([METR, Mar 2025](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)). And more
agents isn't more intelligence: a Berkeley study found multi-agent gains "often remain minimal compared
with single-agent frameworks," with failures concentrated in specification and coordination, not model IQ
([Cemri et al., MAST, 2025](https://arxiv.org/abs/2503.13657)). Reach for the next rung only when the task
genuinely earns it.

## Going deeper

The four deep-dives take each part of the ladder further:

- **[Workflow vs. agent — drawing the line](workflow-vs-agent.md)** the definitions, the three
  "earns-it" signals, and AWS's spectrum, so you can place a feature on purpose.
- **[The cost of agency](cost-of-agency.md)** the token multiplier per rung and the compounding-error
  math (pⁿ) behind each added autonomous hop.
- **[Multi-agent vs. single agent](multi-agent-vs-single.md)** when a multi-agent topology is actually
  justified, and why its failures are coordination failures, not model-quality ones.
- **[When not to reach for AI at all](when-not-to-use-ai.md)** the rung below workflow — stable rules,
  exact reproducibility, high cost of a plausible-but-wrong answer — where classical code wins outright.

When you reach the decision point, the [checklist](../../checklists/when-to-use-agents.md) turns this
into boxes to tick, and the [risk register](../../risk-register/when-to-use-agents.md) scores over-reach
so you fix the worst first; see [Klarna](../case-studies/klarna-ai-assistant.md) for real value on the
routine majority, over-extrapolated to "replace the humans" before the escalation path existed. This
decision is upstream of [compliance & governance](../compliance-and-governance/README.md): less agency
taken is less you must prove control of.

---

## Sources

- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — the workflow-vs-agent definitions and the "simplest solution… add agentic loops only when simpler solutions fall short" rule that frames the whole pillar.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — the three signals that earn an agent (complex decisions, brittle rules, unstructured data) and the "otherwise a deterministic solution may suffice" validation gate.
- **[Well-Architected Generative AI Lens — Agentic AI](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)** (AWS) — agency as a spectrum; LLM-augmented workflow vs. autonomous ReAct loop; "increase agency only when task complexity requires it."
- **[Well-Architected GenAI Lens — GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — the "deterministic where possible / enforce in code, not the prompt" rule behind the ladder.
- **[Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)** (Google Cloud) — "non-agentic solutions" for predictable/single-call work and "start with a single agent."
- **[Gartner predicts over 40% of agentic AI projects will be canceled by 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)** (Gartner) — the cancellation prediction, the cost/value/risk-control causes, and "agent washing."
- **[Measuring AI ability to complete long tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)** (METR) — ~100% success on <4-minute tasks vs <10% on >4-hour tasks; reliability falls with task length.
- **[Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)** (Cemri et al., UC Berkeley) — multi-agent gains often minimal vs single-agent; failures are design and coordination, not model quality.
- **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (Yao et al., ICLR 2023) — the canonical reason-and-act loop that defines the autonomous rung.

<!-- page-type: overview -->
