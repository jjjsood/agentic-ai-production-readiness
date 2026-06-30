# Rate, loop & timeout caps — bound the loop, not just the bill

> **In one sentence:** Token budgets bound how much an agent may spend; rate, loop, and timeout caps bound
> how many times and how long it may run — the iteration ceiling, wall-clock limit, and no-progress
> stopping condition that turn an open-ended loop into one with a guaranteed exit.

> Part of **[Limits & budgets overview](README.md)**

An agent is a loop: plan, call a tool, observe, repeat. The defining property of a loop is that it does not
stop on its own — it stops when a condition says so. A budget cap stops it on *cost*; this page is about the
caps that stop it on *behaviour*: too many iterations, too long, too many requests, or no forward progress.
These are the controls that catch the classic agent runaway — re-calling the same tool on an ambiguous
result forever — which a cost cap would also eventually catch, but only after the spend, and never as
cleanly.

---

## Stopping conditions are mandatory, not optional

The single most important design rule for an agent loop is that it must carry an explicit stopping
condition. Anthropic states it plainly: give an agent "a maximum number of iterations to maintain control"
([Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents)). An
agent loop without a hard iteration ceiling is not a bounded program; it is a program that runs until an
external limit — a rate limit, a timeout, an exhausted budget, or a human — stops it. The whole of this page
is the set of conditions that should stop it *first*, by design, in your own code.

## The four caps and what each stops

Each cap targets a distinct failure; production loops layer all four because each catches what the others
miss ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)):

| Cap | Bounds | The failure it stops |
|-----|--------|----------------------|
| **Max-iteration / recursion ceiling** | Number of loop turns (and depth of sub-agent spawning) per run | The infinite loop and recursive fan-out — the agent that keeps acting with no new state. |
| **Per-step timeout** | Wall-clock for a single tool/model call | A hung dependency or a call that never returns. |
| **Wall-clock (per-run) timeout** | Total elapsed time for the whole run | The slow grind that stays under the iteration cap but runs for hours. |
| **Rate limit** | Requests per entity per time window | Retry storms and API exhaustion; the parallel-request abuse a per-run cap can't see. |

### Iteration and recursion ceilings

Set a hard maximum on loop turns sized to the task — a task that should take ~10 steps does not need 2,000,
so a ceiling well above the expected count but far below "unbounded" catches the runaway without tripping on
normal variance. For agents that spawn sub-agents, cap **recursion depth** too: multi-agent fan-out is a
common runaway shape, where one agent spawning helpers that spawn helpers multiplies the loop. When the
ceiling is hit, the run halts and surfaces the partial state — it does not silently continue.

### Step and wall-clock timeouts

A loop can be under its iteration ceiling and still never end if one call hangs, so wrap **each** call in a
per-step timeout, and wrap the **whole run** in a wall-clock budget. The two are different controls: the
per-step timeout kills a stuck dependency; the wall-clock timeout kills a run that is making slow,
legitimate-looking progress for far longer than its value justifies. OWASP names both — "set timeouts and
throttle processing for resource-intensive operations to prevent prolonged resource consumption"
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).

### Rate limits and quotas

Rate limiting bounds how often a single source can drive work, which neither the iteration cap nor the
timeout addresses — those govern one run, while a rate limit governs the *frequency of runs and calls*
across an entity. OWASP's mitigation is explicit: "apply rate limiting and user quotas to restrict the
number of requests a single source entity can make in a given time period"
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). This is also the front
line against the parallel-request flavour of [denial of wallet](denial-of-wallet.md): one expensive request
is a budget problem; a thousand cheap requests a second is a rate problem.

## No-progress detection — the loop that runs but cycles

The subtlest runaway is the agent that is busy but not progressing: it re-issues the same tool call with the
same arguments on an empty or ambiguous result, climbing the step count while the state never changes. A
plain iteration ceiling eventually catches it, but a sharper control catches it sooner — **no-progress
detection**: track recent tool-call signatures (tool name plus arguments) and the resulting state, and break
the loop when N consecutive turns produce no new state or repeat an identical call. The general direction is
sourced — Anthropic's guidance to give an agent "a maximum number of iterations to maintain control"
([Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents)) — but
the specific signature-tracking mechanism described here is the authors' practitioner heuristic, not a
control named in a standard; treat the threshold N and the matching logic as engineering judgement to tune,
not a fixed rule. It pairs naturally with **idempotency on side-effecting tools**: a stochastic agent may
retry a call that timed out, or fire the same call in parallel when it is unsure, so a non-idempotent
`charge_card` can apply the effect twice — design side-effecting tools around an idempotency key so a repeated
call collapses to a single effect rather than N duplicate writes. Anthropic frames a tool as a contract with a
*non-deterministic* caller that may invoke it incorrectly or repeatedly, which is exactly the failure mode to
design out ([Anthropic — Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

## Enforce caps deterministically, outside the model

Every cap on this page must live in the orchestration code, not the prompt. "Stop after 25 steps" written
into a system prompt is a suggestion a stochastic model can lose track of, be argued out of by an injected
instruction, or simply ignore. The enforceable version is a counter and a clock the runtime owns: the
**iteration count is incremented by the loop, the timeout is measured by the runtime, the rate limit is
checked by the gateway** — and the check that ends the loop runs *before* the next metered call is
dispatched, not after. This is the same rule the whole pillar turns on: a limit the model is merely asked to
respect is not a limit ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).
The Replit incident is the cost of getting this wrong — a freeze stated in the prompt did not bind the
agent's actions because it was a request, not an enforced block
([Replit database deletion](../case-studies/replit-database-deletion.md)).

## Fail closed, and degrade gracefully

When a cap fires, the run should stop in a *safe* state, not an arbitrary one. Two principles: **fail
closed** — a hit ceiling halts and escalates rather than defaulting to "continue"; and **degrade
gracefully** — under load or at a quota boundary, prefer partial functionality (a queued response, a
fallback, a clear refusal) over either a hard crash or a silent overspend
([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)). A cap that, when breached,
dumps the user into an error with no recovery is a cap that teams disable; one that returns a clean "this
took too long, here's what I have, escalating to a human" is one they keep on.

---

## Sources

- **[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP GenAI Security Project) — the named controls: rate limiting and per-entity quotas, input-size limits, timeouts and throttling on resource-intensive operations, limiting queued/total actions, and graceful degradation under load.
- **[Building effective agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic) — the primary recommendation that an agent loop carry "a maximum number of iterations to maintain control," the basis for the iteration-ceiling rule.
- **[Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** (Anthropic) — tools as contracts with a non-deterministic caller that may call them incorrectly or repeatedly: the basis for making side-effecting tools idempotent; named as a neutral example.

<!-- page-type: standard -->
