# Eval in production — pass@1 is not reliability, so keep measuring after launch

> **In one sentence:** A single passing run overstates reliability, and an offline suite can't see the real
> long-tail — so quality has to be measured *in production* on live traffic, or wrong outputs sit undetected,
> which is the attributable failure this pillar exists to prevent.

> Part of **[Observability & evals overview](README.md)**

The most expensive measurement mistake is to evaluate an agent once, watch it pass, and call it reliable.
Production needs the agent to succeed *every* time on the *same* task under real, repeated, sometimes
adversarial traffic — a much higher bar than "succeeded once in a demo". This page covers why single-shot
success (pass@1) overstates reliability through the **pass^k / consistency gap** and Sierra's τ-bench, what an
**online eval** loop looks like, and how to monitor quality drift on live traffic before users do it for you.
It is written for the team that has shipped and now owns keeping the agent good.

---

## pass@1 ≠ reliable: the consistency gap

Benchmarks usually report **pass@1** — the probability a single attempt succeeds. Production cares about a
different number: will the agent succeed on *every* attempt at the same task, not just one. The metric for
that is **pass^k** — the probability the agent succeeds on all *k* independent trials of the same task — and
the gap between the two is large. Sierra's **τ-bench**, a tool-agent-user benchmark in real-world retail and
airline domains, found a state-of-the-art function-calling agent (gpt-4o) scored **under 50% pass@1**, and its
**pass^8 fell below 25%** in the retail domain — an agent that succeeds once will frequently fail
when asked to do the same thing eight times ([τ-bench](https://arxiv.org/abs/2406.12045)). The benchmark's own
conclusion is the operating lesson: there is an urgent need for agents that **act consistently and follow
rules reliably**, because single-trial success does not deliver it ([τ-bench](https://arxiv.org/abs/2406.12045)).

The production consequence is direct: a one-off green eval is not a green light. The Devin launch demo is the
cautionary version of this — a single curated run presented as proof of capability, which independent review
took apart ([Cognition Devin demo](../case-studies/cognition-devin-demo.md)). The same agent earned trust at
Goldman Sachs only once every output was reviewed and routed through existing CI — i.e. measured *repeatedly*
rather than trusted *once* ([Goldman Sachs × Devin](../case-studies/goldman-sachs-devin.md)). Reliability is a
property of the population of runs, and you only see the population by measuring in production.

## Online evals: a smoke detector on live traffic

Offline suites measure the cases you thought of; production serves the ones you didn't. **Online evals** close
that gap by scoring live traffic — sampling real traces and grading them asynchronously, off the user's
critical path so they add no latency, as a continuous smoke detector for degradation rather than a launch
gate. The grading reuses everything from the offline suite — the same rubric, the same trajectory-property
checks, the same calibrated LLM-as-judge with its known biases and human-anchored spot checks
([From Generation to Judgment](https://arxiv.org/pdf/2411.16594)) — applied to sampled production runs instead
of a held-out set. Because grading runs on the captured trace, it depends entirely on the tracing from
[tracing & token accounting](tracing-and-token-accounting.md): no trace, no online eval.

A few signals are nearly free and worth wiring first, because they are direct user verdicts on quality:
thumbs-down rates, regeneration / retry rates, and escalation-to-human rates. A rising rate on any of these is
an early degradation signal that needs no judge model at all. This triad is the authors' operating guidance
rather than a cited standard — treat it as a cheap first layer under the calibrated grading above, not a
substitute for it.

## Monitoring quality drift

Online evals produce a stream of scores; monitoring turns that stream into an alarm. The pattern is the SRE
one applied to quality: establish a **baseline** for your key metrics — task success rate, refusal rate,
trajectory-property pass rate, tool-error rate, cost per run — then alert on a sustained deviation from it.
Watch for drift from three sources in particular: a **silent provider model update** (behaviour changes under
a pinned name), input distribution shift (real traffic diverging from your eval set), and slow regressions
that no single change caused. The reason this loop is non-negotiable is the failure mode it prevents: NYC's
MyCity bot produced illegal regulatory advice and was **left online still producing it** after the problem was
public — there was no quality-monitoring loop watching production outputs, so wrong answers simply
accumulated unseen ([NYC MyCity](../case-studies/nyc-mycity-chatbot.md)). Undetected wrong outputs in
production are exactly what this loop exists to surface.

## Close the loop back to offline

Online and offline evals are one system, not two. The mature loop is **self-improving**: an online eval (or a
thumbs-down spike) flags a live failure → a human labels it → the labelled case enters the offline golden set
→ the [regression suite](evals-and-regression-suites.md) catches that whole class of failure on the next
change, *before* it ships again. Production becomes the source of new test cases, and the offline gate gets
stronger every time production teaches it something. A team that only runs offline evals is testing yesterday's
failures; a team that closes this loop is continuously importing today's.

This is also where observability and evals meet rollback and governance. When monitoring flags a regression,
the response is a fast, tested rollback to the last known-good pinned config — owned by the human-control &
rollback discipline — and the captured traces and eval results are the audit record the
[compliance & governance](../compliance-and-governance/README.md) pillar requires you to retain. Measuring in
production is what makes both possible.

---

## Sources

- **[τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)** (Sierra) — the pass@1 (<50%) vs pass^8 (<25%, retail) consistency gap and the call for consistent, rule-following agents.
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — the judge biases and human-anchoring carried into online grading.

<!-- page-type: standard -->
