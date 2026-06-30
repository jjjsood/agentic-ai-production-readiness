# When to use agents — pick the least-agentic thing that works

> **In one sentence:** Every notch of autonomy you add is infrastructure you then owe — limits,
> guardrails, observability, identity, rollback — so the cheapest way to avoid an infrastructure-gap
> failure is to not buy the agency you don't need.

This is the pillar that runs *before* the other six. The infrastructure thesis of this repository — that across
~591 documented incidents most attributable failures are infrastructure gaps, not model quality — has a
quiet corollary: the surest way to pass the infrastructure bill is to architect a system that doesn't
incur it. Agency is a spectrum, not a switch — deterministic code, then an LLM-augmented workflow, then a
single autonomous agent, then a multi-agent system — and the obligation to harden grows at every rung. This
page is written for the person choosing where on that ladder a feature should sit. By the end you should be
able to draw the line between a workflow and an agent, name the few signals that genuinely *earn* an agent,
see why the agent rung is a real and order-of-magnitude bill, and recognise the rung below workflow where
deterministic code wins outright. The [deep-dives](#going-deeper) then work each of those in detail.

---

## Why this is the pillar that gets tested

The failure here is rarely loud at launch — it is a demo that shipped as a product. A curated reel shows an
agent finishing a job end-to-end, the budget gets approved on the strength of it, and the gap between *that
run* and a reproducible production run is discovered only in production. Cognition's launch demo for Devin,
the "first AI software engineer," claimed an autonomous agent had closed a real paid job; independent review
found a cherry-picked task run in the wrong environment, with the agent fixing errors it had itself
introduced — the gap was evidence and scope, not a smarter model
([Cognition / Devin demo](../case-studies/cognition-devin-demo.md)). Google's viral Gemini "Hands-on" reel
implied a live video-and-voice loop the shipped system did not have; the missing piece was the serving and
latency infrastructure, not the model ([Gemini hands-on demo](../case-studies/google-gemini-handson-demo.md)).
The pattern in both: an agent-shaped capability was *believed* before the infrastructure to run it
autonomously existed.

The market is already pricing this in. Gartner predicts **over 40% of agentic AI projects will be cancelled
by the end of 2027**, naming escalating costs, unclear business value, and inadequate risk controls — and
warning of "agent washing," ordinary automation rebranded as agentic
([Gartner, Jun 2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)).
Treat the figure as an analyst *forecast*, not a measurement, and as an order-of-magnitude signal rather
than a constant: the claim is that a large share of agent projects will not survive contact with their own
cost and risk. The discipline this pillar teaches is the cheapest insurance
against being in that share — **don't reach for the agent rung first.**

## Agency is a spectrum, not a switch

The single most useful mental model is that "agent" is not a yes/no choice but a position on a ladder of
autonomy, and you should climb only as high as the task forces you. Anthropic draws the load-bearing line:
a **workflow** orchestrates LLMs and tools "through predefined code paths," while an **agent** is a system
where the LLM "dynamically directs its own processes and tool usage." The guidance is explicit — "find the
simplest solution possible, and only increase complexity when needed," adding agentic loops "only when
simpler solutions fall short," because agentic systems "trade latency and cost for better task performance"
([Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents)).

AWS frames the same continuum and reaches the same conclusion from the security side: agency exists on a
spectrum, and "it's important to only increase the agency of the system when the task complexity requires
it" — an LLM-augmented workflow keeps code paths "largely deterministic" with a few LLM-decided steps, while
an autonomous agent runs a reason-and-act loop "until the LLM is given a stop reason"
([AWS Well-Architected — Agentic AI](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/agentic-ai.html)).
Its blunter rule is to be **deterministic where possible** and to enforce a boundary in code, not in a
prompt ([AWS GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)).
The autonomous rung is the ReAct (reason + act) loop in the foundational sense
([Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)) — and that loop, not the model, is what creates
the obligation to bound iterations, scope tools, and trace every step.

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

If a workflow is the default, what flips the decision toward an agent? OpenAI names three signals where
rules-based automation breaks down and an agent starts to pay off: **complex decision-making** (nuanced
judgement, exceptions, context-sensitive calls, e.g. a refund weighed against loyalty and dispute history);
**difficult-to-maintain rules** (a ruleset grown so large and tangled that updates are costly and
error-prone); and **heavy reliance on unstructured data** (interpreting natural language, extracting meaning
from documents, conversing). Its validation gate is the sentence to keep: "validate that your use case can
meet these criteria clearly. Otherwise, a deterministic solution may suffice"
([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
Google Cloud says the same from the other direction — if a workload is "predictable or highly structured, or
if it can be executed with a single call to an AI model," a **non-agentic** solution (summarise, translate,
classify) is more cost-effective; and when you do need an agent, "start with a single agent"
([Google Cloud — Choose a design pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)).

Two reliability facts sit underneath those signals and argue for the shortest, least-agentic path that
works. First, autonomy degrades with task length: METR measured frontier agents at "almost 100% success
rate on tasks taking humans less than 4 minutes, but [succeeding] less than 10% of the time on tasks taking
more than around 4 hours" ([METR, Mar 2025](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)).
The longer and more open-ended the autonomous run, the weaker the case for it *today*. Second, more agents
is not more intelligence: a Berkeley study of multi-agent systems found that gains "often remain minimal
compared with single-agent frameworks," and that the failures are concentrated in specification and
inter-agent coordination — design problems, not model-IQ problems
([Cemri et al., MAST, 2025](https://arxiv.org/abs/2503.13657)). That is the infrastructure thesis restated
at the architecture level: reach for the next rung only when the task genuinely earns it.

## Going deeper

The four deep-dives take each part of the ladder further:

- **[Workflow vs. agent — drawing the line](workflow-vs-agent.md)** works the core distinction in detail:
  Anthropic's workflow/agent definitions, OpenAI's three "an agent earns it" signals and validation gate,
  and AWS's agency-as-a-spectrum with its deterministic-where-possible rule — so you can place a feature on
  the ladder on purpose.
- **[The cost of agency](cost-of-agency.md)** makes the economic case concrete: an agent uses on the order
  of several times the tokens of a single chat call and a multi-agent system roughly an order of magnitude
  more, and the compounding-error math (pⁿ) shows why each added autonomous hop also costs reliability.
- **[Multi-agent vs. single agent](multi-agent-vs-single.md)** works the topmost rung — when a multi-agent
  topology is actually justified (parallelisable, separable-context, loosely-coupled work) versus a single
  agent or a workflow, why its capability gains are often minimal, and why its failures are coordination
  failures rather than model-quality ones.
- **[When not to reach for AI at all](when-not-to-use-ai.md)** is the rung below workflow: the signals —
  stable rules, exact reproducibility, a cheap correct deterministic solution, high cost of a
  plausible-but-wrong answer — where classical code wins outright and an LLM is the wrong tool.

When you reach the decision point, the [when-to-use-agents checklist](../../checklists/when-to-use-agents.md)
turns each of these into a box you can honestly tick before you commit to a rung, and the
[when-to-use-agents risk register](../../risk-register/when-to-use-agents.md) scores the failures of
*over-reaching* so you fix the worst first; see [Klarna](../case-studies/klarna-ai-assistant.md) for a
deployment that delivered real value on the routine majority and then over-extrapolated to "replace the
humans" before the escalation path existed — the over-reach this pillar exists to prevent. This decision is
upstream of the [compliance & governance](../compliance-and-governance/README.md) pillar: the less agency
you take, the less you have to prove you were in control of.

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
