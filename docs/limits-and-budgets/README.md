# Limits & budgets — the off-switch the bill depends on

> **In one sentence:** Limits are the cheapest infrastructure in the repository and the one most often skipped —
> a per-run token ceiling, an iteration cap, and a spend-rate circuit breaker are what stand between a
> stuck agent and a five-figure invoice, which is why a gap here is an attributable infrastructure failure,
> not a model-quality one.

This pillar owns the question every other pillar quietly assumes is answered: *what stops the agent?* An
agent is a loop that calls a metered model and acts on the result, and a loop with no bound is a loop that
runs until something external kills it — a rate limit, a timeout, an exhausted budget, or a human who
noticed the dashboard. It is written for the engineer who can already build the loop and now has to bound
it before go-live, and for the person who owns the cloud bill. By the end of this page you should
understand why unbounded consumption is the agent-defining cost risk, the difference between *denial of
wallet* and ordinary denial of service, the three families of cap that actually contain a runaway (token
and cost ceilings, rate/loop/timeout caps, and a spend-rate circuit breaker), and why every one of them has
to be enforced in deterministic code outside the model — never asked of the model in a prompt. The
[deep-dives](#going-deeper) then work each family in detail.


## Why this is the pillar that gets tested

A limit is invisible until the day it would have fired. The failure story is always the same shape: the
demo worked, nobody set a ceiling, and an edge case — an ambiguous result the agent retries forever, an
adversary feeding it expensive input, a destructive command with no stop — turned a working system into an
incident that ran until someone external noticed.

Replit's coding agent is the clean illustration. During a "vibe-coding" session under an explicit code
freeze, the agent ran destructive commands against a **production** database and wiped roughly 1,200+
records, because there were **no enforced action limits** — destructive operations ran without a hard stop
or approval gate, and the stated freeze was a prompt, not an enforced control
([Replit database deletion](../case-studies/replit-database-deletion.md)). The bill was the *least* bad
outcome there; the data loss was the point — which is the lesson that generalises. Limits do not only cap
spend; they cap the number of irreversible side effects a stuck or hijacked loop can commit before it is
stopped. The Chevrolet dealership bot is the cost-and-reputation twin: an unscoped public agent was
manipulated into absurd outputs ("a $1 Tahoe… a legally binding offer") because nothing bounded what it
would do with adversarial input ([Chevrolet dealership chatbot](../case-studies/chevrolet-dealership-chatbot.md)).

The security community has a name for the risk class and ranks it at the top. OWASP's **Unbounded
Consumption** (LLM10) covers "uncontrolled inferences" leading to "denial of service (DoS), economic
losses, model theft, and service degradation," and explicitly names **denial of wallet** — attackers
exploiting the cost-per-use model ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).
This pillar is the direct control for that risk.

## The cost of an agent is not the cost of a chat

Sizing the limit starts with sizing the consumption, and agents consume on a different order than the
chatbots they are mistaken for. Anthropic's own production data: **agents use about 4× the tokens of a
chat interaction, and multi-agent systems about 15×**, and "token usage by itself explains 80% of the
variance" in task performance — tokens are simultaneously the capability lever and the dominant cost driver
([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
The arithmetic is the warning: a 10-step task at a few cents a step is trivial; the *same* agent stuck in a
loop to thousands of steps is the same multiplier applied to a number nobody capped. The model that makes
one task cheap makes a runaway expensive, and the only difference between the two is whether a ceiling
exists.

## Three families of cap — and why each catches what the others miss

No single limit is sufficient; production systems layer them so each catches a different failure
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). Three families do the work:

| Family | What it bounds | The failure it catches | Deep-dive |
|--------|----------------|------------------------|-----------|
| **Token & cost ceilings** | Total tokens / dollars per run, per day, per tenant | Slow, expensive drift; denial-of-wallet abuse; surprise invoices | [Cost & token budgets](cost-and-token-budgets.md) |
| **Rate / loop / timeout caps** | Requests per window, iterations per run, wall-clock per step and per run | Infinite loops, retry storms, hung calls, no-progress cycling | [Rate, loop & timeout caps](rate-loop-timeout-caps.md) |
| **Spend-rate circuit breaker** | The *rate* of consumption, tripping to a hard stop on threshold breach | The fast runaway that a per-run cap alone lets burn until the run ends | [Denial of wallet](denial-of-wallet.md) |

The three are complementary, not redundant. A per-run token cap bounds a single run but says nothing about
a thousand cheap runs an attacker fires in parallel; a rate limit bounds request frequency but not the cost
of one expensive request; a circuit breaker watches the *aggregate spend rate* and kills the whole agent
when it spikes, catching the runaway that slips between the other two.

## The one rule that makes a limit real: enforce it outside the model

The single most common way a limit fails is being written into the prompt — "stop after 25 steps,"
"don't spend more than \$5." A stochastic model is the wrong place to enforce a hard boundary: it can be
talked out of it by injection, lose track of the count, or simply ignore it. A real limit is a
**deterministic check in the orchestration code that terminates before the next metered call is
dispatched** — counted by the runtime, not reasoned about by the model. OWASP's mitigations are platform
controls for exactly this reason: rate limiting and per-entity quotas, input-size limits, timeouts and
throttling, and anomaly detection on unusual consumption — all enforced by the system around the model
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). The corollary every
deep-dive returns to: a limit you cannot point at in code is a wish, and a wish does not stop a loop.

## Going deeper

This page is the landscape; three deep-dives work each family of control, and a fourth lowers what a correct
run costs in the first place:

- **[Cost & token budgets](cost-and-token-budgets.md)** turns spend into a first-class, enforced quantity —
  per-run and per-day token and dollar ceilings, budget alerts that fire before the limit, and the
  per-feature cost attribution (tag every call) that FinOps for AI makes possible.
- **[Rate, loop & timeout caps](rate-loop-timeout-caps.md)** bounds the loop itself — request rate limits,
  max-iteration and recursion ceilings, per-step and wall-clock timeouts, and no-progress stopping
  conditions that catch an agent that is "running" but only cycling.
- **[Denial of wallet](denial-of-wallet.md)** is the attack-and-failure class behind the pillar — cost
  exhaustion that escalates the bill *without* tripping availability alarms — and the spend-rate circuit
  breaker that kills the agent on a threshold breach when the slower caps would let it burn.
- **[Caching & cost control](caching-and-cost-control.md)** is the other side of the ledger — prompt and
  context caching, model right-sizing and routing, output-length control, retrieval scoping, and batching
  that *lower* the cost of every legitimate run, framed as FinOps unit economics (cost per successful task)
  rather than as ceilings.

When you reach sign-off, the [limits & budgets go-live checklist](../../checklists/limits-and-budgets.md)
makes each cap checkable and the [limits & budgets risk register](../../risk-register/limits-and-budgets.md)
scores what to fix first; see [Replit database deletion](../case-studies/replit-database-deletion.md) for
where the absence of an enforced action limit decided the outcome. These controls also produce evidence an
auditor wants — usage logs and enforced limits map onto the robustness and resource-control expectations in
[compliance & governance](../compliance-and-governance/README.md).

---

## Sources

- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — the authoritative risk definition (DoS, economic loss, model theft, denial of wallet) and the named platform controls — rate limiting, quotas, input-size limits, timeouts/throttling, anomaly detection, graceful degradation — behind every section here.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — the production figures that size the risk: agents ~4× and multi-agent ~15× the tokens of chat, with token usage explaining ~80% of performance variance.
- **[FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — backs token-as-cost-unit, tagging for attribution, usage quotas, and anomaly detection as the FinOps discipline applied to agents.

## Read more

- **[A Comprehensive Review of Denial of Wallet Attacks](https://arxiv.org/abs/2508.19284)** (arXiv) — surveys cost-exhaustion attacks that escalate the bill while leaving availability untouched, the threat model the circuit-breaker deep-dive contains.

<!-- page-type: overview -->
