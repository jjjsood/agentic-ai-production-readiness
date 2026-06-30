# The cost of agency — what choosing "agent" actually costs

> **In one sentence:** Moving up the autonomy ladder buys flexibility with two currencies — tokens and
> reliability — and both bills scale steeply enough that "agent" should be a deliberate purchase, not a
> default.

> Part of **[When to use agents overview](README.md)**

The case for picking the least-agentic option is usually argued on principle; this page argues it on the
invoice. Choosing the agent rung commits you to more tokens per task, a larger failure surface to harden,
and a reliability tax that compounds with every autonomous hop. None of these are model-quality problems —
they are the predictable economics of autonomy, and they are why a large share of agent projects do not
survive their own cost. Read the figures here as order-of-magnitude anchors, not constants.

---

## The token bill scales with the rung

Autonomy is paid for in tokens, and the multiple is large. Anthropic, reporting on its own multi-agent
research system, gives the cleanest primary anchors: "**agents typically use about 4× more tokens than chat
interactions**," and "**multi-agent systems use about 15× more tokens than chats**"
([Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
The mechanism is structural, not wasteful: each loop iteration, retry, tool call, and context reload is more
tokens, and a multi-agent system multiplies that across several agents plus the orchestration between them.

That sets a hard economic gate. Anthropic states it plainly: "for economic viability, multi-agent systems
require tasks where the value of the task is high enough to pay for the increased performance"
([Anthropic — multi-agent system](https://www.anthropic.com/engineering/multi-agent-research-system)).
A single chat call that costs *x* becomes roughly *4x* as an agent and roughly *15x* as a multi-agent
system — so the per-task value has to clear that higher bar before the rung makes sense. Anthropic also
names the poor fits: tasks needing shared context across agents, heavy inter-agent dependencies, or little
parallelisable work (most coding) are *worse* on the multi-agent rung, not better. The OWASP risk that names
the open-ended version of this bill is **Unbounded Consumption** — uncontrolled inference driving economic
loss and "denial of wallet" ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)) —
and the agency that opens it is **Excessive Agency** ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).
The thrift is the architecture choice: a rung you don't climb is a multiple you never pay.

## The reliability bill — compounding error

The second currency is reliability, and it compounds. If an autonomous task is a chain of *n* steps that
each succeed independently with probability *p*, the end-to-end success rate is **pⁿ** — the product of the
per-step reliabilities. This is canonical reliability math (the reliability of a series system is the
product of its parts), so it needs no vendor source; it is a derivation, not a claim. Worked at a generous
95% per step:

| Steps in the chain | End-to-end success (0.95ⁿ) |
|--------------------|----------------------------|
| 1 | ~95% |
| 5 | ~77% |
| 10 | ~60% |
| 20 | ~36% |

Two things make production worse than the table. First, steps are not independent: an error at step 2
poisons step 3 onward, so real degradation outruns pⁿ. Second, demos hide the chain by showing two or three
clean steps; production tasks are five or more over messy input — the exact gap that made a curated launch
demo collapse under independent review in the [Cognition / Devin demo](../case-studies/cognition-devin-demo.md).
Every notch up the autonomy ladder adds steps the model takes unsupervised, which is why the math favours
the least-agentic rung: fewer autonomous hops means a higher *pⁿ*.

The empirical evidence lines up with the arithmetic. METR measured frontier agents at "almost 100% success
rate on tasks taking humans less than 4 minutes, but [under] 10% of the time on tasks taking more than
around 4 hours," with the 50%-reliability time horizon doubling roughly every seven months
([METR, Mar 2025](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)).
Reliability falls systematically as the autonomous run gets longer — so a long, open-ended agent loop is the
expensive *and* fragile choice today. And adding agents does not buy the reliability back: a Berkeley study
found multi-agent gains "often remain minimal compared with single-agent frameworks," with failures
concentrated in specification and inter-agent coordination — design and infrastructure, not model IQ
([Cemri et al., MAST, 2025](https://arxiv.org/abs/2503.13657)).

## The third bill — the infrastructure you now owe

Tokens and reliability are the metered costs; the standing cost is the infrastructure each rung obligates.
The moment a feature becomes an autonomous agent, it needs the controls the rest of this repository is about —
loop and iteration caps, a spend ceiling, scoped credentials, tracing on every tool call, human approval on
irreversible actions, and a rollback path — and a multi-agent system needs each of those replicated across
more identities with a larger blast radius. This is the connection back to the repository's thesis: the
attributable failures are infrastructure gaps, so choosing a higher rung *is* choosing to take on more of
the infrastructure that, when missing, is what fails. The market has put a number on the consequence —
Gartner predicts **over 40% of agentic AI projects will be cancelled by the end of 2027**, on escalating
costs, unclear value, and inadequate risk controls
([Gartner, Jun 2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)).
Treat it as an analyst *forecast* rather than a measurement, and as an order-of-magnitude signal: the
prediction is that a lot of agent projects will be cancelled for reasons that trace back to taking on more
agency than the task — and the budget — could carry.

## How to decide on the invoice

- **Price the task before the rung.** Estimate the per-task value, then check it clears the multiple — on
  the order of ~4× a chat call for an agent and ~15× for multi-agent ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)). If the value doesn't clear it, drop a rung.
- **Count the autonomous steps.** More unsupervised hops means a lower *pⁿ*; prefer the shortest chain that
  does the job, and keep humans on the steps that matter.
- **Justify multi-agent against the parallelism.** It pays only when work genuinely parallelises and exceeds
  one context window; for shared-context or tightly-coupled work, a single agent is cheaper *and* more
  reliable ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system); [MAST](https://arxiv.org/abs/2503.13657)).
- **Add the infrastructure into the estimate.** The agent's bill includes the limits, observability, and
  rollback it now requires — not just its tokens.

## Sources

- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — the primary token anchors (~4× chat for agents, ~15× for multi-agent), the economic-viability gate, and the multi-agent poor-fit cases.
- **[Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)** (Cemri et al., UC Berkeley) — multi-agent gains often minimal vs single-agent; failures concentrated in specification and coordination.
- **[Measuring AI ability to complete long tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)** (METR) — ~100% success on <4-minute tasks vs <10% on >4-hour tasks; reliability falls with autonomous task length.
- **[Gartner predicts over 40% of agentic AI projects will be canceled by 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)** (Gartner) — the cancellation prediction on cost, value, and risk-control grounds.
- **[OWASP LLM10: Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP) — the runaway-cost / denial-of-wallet failure mode the token bill opens.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP) — the excess-autonomy surface that drives the consumption and reliability bills.

## Read more

- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — frames the same trade-off qualitatively ("agents trade latency and cost for better task performance"), the principle behind the numbers on this page.

<!-- page-type: standard -->
