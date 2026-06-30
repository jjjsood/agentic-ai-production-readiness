# Evals & regression suites — gate every change on a measurement, not a hunch

> **In one sentence:** An offline regression suite is the infrastructure that catches the silent drift a
> prompt tweak or model swap introduces — without it, "it worked in the demo" ships changes that quietly
> break production, which is an infrastructure gap, not a model fault.

> Part of **[Observability & evals overview](README.md)**

A model provider can change behaviour under a pinned name, a one-line prompt edit can regress a skill you
weren't touching, and a new tool can break a flow that used to work — none of which a demo will show you. The
control is an **offline eval suite**: a held-out set of cases you re-run on every change, blocking the change
if a metric regresses. This page covers what to put in the suite (capability, reliability, safety, cost), why
agent evals must grade the *trajectory* and not just the final answer, the caveats of using an LLM as a judge,
and how to wire the suite as a gate. It is written for the team that ships prompt and model changes and needs
to do so without playing roulette.

---

## Build the suite across four axes

A regression suite that only checks "did it get the right answer" misses most of what breaks an agent in
production. The agent-evaluation literature partitions the problem across capability, reliability, safety, and
behaviour ([Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)); to that we
add **cost** as a fourth go-live axis — not part of the survey's taxonomy, but a regression an agent team has
to gate on. Cover all four:

- **Capability** — does the agent complete the task correctly on representative inputs? The headline axis,
  and the one teams over-index on.
- **Reliability** — does it succeed *consistently*, not just once? A single pass overstates this badly (see
  [eval in production](eval-in-production.md) for the pass^k gap); include repeated runs of the same case.
- **Safety** — does it refuse what it should, resist prompt injection, and avoid harmful or out-of-policy
  actions? These cases double as regression tests for your guardrails.
- **Cost** — does the change blow up token usage or tool-call count? A change that improves accuracy while
  tripling cost is a regression you want the suite to flag, using the per-run token accounting from
  [tracing & token accounting](tracing-and-token-accounting.md).

Start small and grow from real failures: a held-out set of even **10–20 prompts already surfaces regressions
for a single skill**, after which you grow it from production failures rather than guessing cases up front
([OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)).
The suite is a living artifact, not a one-time benchmark.

## Grade the trajectory, not just the final answer

For an agent, the final answer hides how it got there. Two runs can both produce a correct answer while one
took a safe, cheap path and the other looped, called a destructive tool, or got lucky — and a final-answer
check scores them identically. **Trace grading** scores the end-to-end record of a run — the sequence of model
calls, tool calls, guardrail checks, and handoffs — so workflow-level regressions surface even when the answer
still looks right ([OpenAI — evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)).

The complication is that there is rarely one correct path: **agents reach goals by different valid routes**, so
the grader cannot demand an exact tool sequence ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
The practical resolution is to grade *properties* of the trajectory rather than a fixed script — did it stay
within the allowed tool set, avoid the destructive tools, stay under the step and token budget, and reach a
correct end state — leaving the agent free to choose the path while the suite enforces the boundaries.

## LLM-as-judge: useful, biased, and not to be trusted alone

Much of what you want to grade is subjective — helpfulness, faithfulness to a source, tone — and an LLM judge
scales that grading where exact-match cannot. But a judge is **biased and overconfident**, and the biases are
well catalogued: **verbosity** (longer answers scored higher), **position** (first or last option preferred),
**self-enhancement** (a model rates its own family's output higher), and **authority** (fabricated citations
score higher); chain-of-thought is not always faithful, and naive sampling can amplify the bias rather than
average it out ([From Generation to Judgment](https://arxiv.org/pdf/2411.16594)). Treating a single judge's
score as ground truth is how a suite turns into eval theatre — a green number with no relationship to real
quality.

Mitigations that keep the judge honest ([From Generation to Judgment](https://arxiv.org/pdf/2411.16594)):

- **Pin a fixed, explicit rubric** so the judge grades against stated criteria, not vibes.
- **Randomise answer order** between runs to neutralise position bias.
- **Use multiple judges** (or multiple samples) rather than one, and watch for disagreement.
- **Anchor to human-labelled spot checks** — calibrate the judge against a human-graded sample so you know its
  error, and reserve expensive judge calls for the cases cheap code-based graders can't handle.

Where an exact, deterministic check is possible — schema validity, a required field present, a forbidden tool
*not* called — prefer it to a judge: it is cheaper, faster, and unbiased.

## Gate the change: a regression is a blocked merge

A suite only protects production if a regression *stops the change*. Wire it as a gate: re-run the suite on
every prompt, model-version, tool, or flow change, and block the change if a metric drops below threshold.
The reason the gate has to be end-to-end is that the failure mode is non-local — **re-evaluate the whole
application before any change ships, because even a small prompt or model-version change can regress the
system** somewhere you weren't editing ([OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)).
Keep code-based graders in the fast pre-merge path (seconds to a few minutes) and reserve heavier judge-based
or trajectory grading for a fuller pre-release run. Pinning the model version is part of this gate, not a
separate concern: providers can change a model's behaviour under the same name, so an un-pinned model is an
ungated change happening without a commit ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).

This offline gate is one half of the loop; the other is watching production, because no held-out set covers
the real long-tail. The [eval-in-production](eval-in-production.md) page closes the loop: online evals flag a
live failure, a human labels it, and that case enters this offline golden set so the next regression run
catches its whole class earlier.

---

## Sources

- **[Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)** (arXiv) — maps agent evaluation across capability, reliability, safety, and behaviour, behind the four-axis suite design.
- **[OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)** (OpenAI) — re-evaluate end-to-end before any change ships; start with 10–20 prompts and grow from real failures.
- **[OpenAI — evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)** (OpenAI) — trace grading: scoring the end-to-end run (model/tool/guardrail/handoff) to catch workflow regressions.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — agents reach goals by different valid paths (grade properties, not a fixed script) and providers change model behaviour under a pinned name.
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — the judge-bias catalogue (verbosity, position, self-enhancement, authority) and the rubric / randomise / multi-judge / human-anchor mitigations.

<!-- page-type: standard -->
