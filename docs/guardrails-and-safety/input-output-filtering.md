# Input/output filtering — guard the three boundaries the model touches

> **In one sentence:** A production agent has three places where untrusted text crosses a trust boundary —
> what comes *in*, what the model emits *out*, and the *arguments* it hands to a tool — and a guardrail on
> each is the difference between a model that misbehaves quietly and one that ships a slur or wires money.

> Part of **[Guardrails & safety overview](README.md)**

Filtering is the part of the guardrails pillar people picture first — a content filter on the prompt and
the reply. That picture is incomplete in two ways: it forgets that the *tool call* in the middle is also a
boundary that needs validating, and it imagines one filter where production needs layered, fail-fast ones.
This page works through the three boundaries (input, output, tool arguments), why output handling is its
own OWASP risk, and why filters are *layers in* a defense, never the whole of it.

---

## Three boundaries, not one

Picture the agent as a non-deterministic core with untrusted text crossing in and out at three points.
Each needs its own guard:

| Boundary | What crosses it | What the guard does |
|----------|-----------------|---------------------|
| **Input** | User text + retrieved/tool/web content | Screen for injection, off-topic, policy-violating, or oversized input; segregate untrusted content as data, not instructions. |
| **Output** | The model's generated response | Block off-policy, unsafe, defamatory, or PII-leaking text *before* it reaches the user or a downstream system. |
| **Tool arguments** | The JSON the model fills in to call a tool | Validate against a typed schema and authorize the action *before* it executes — the model's JSON is a suggestion, not a command. |

OpenAI's and AWS's guidance both frame these as **layered guardrails that run in parallel and fail fast** —
no single guardrail suffices, and the layer should be deterministic where possible and probabilistic only
where it must be ([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf);
[AWS Well-Architected — Generative AI Lens, guardrails](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)).
Cloud guardrail products bundle these as examples — content/word filters, prompt-attack detection, denied
topics, PII redaction, and contextual-grounding checks that flag a response unsupported by its retrieved
sources ([Guardrails for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html),
named as one neutral example, not a recommendation).

## Input filtering: screen and segregate

The input guard does two jobs. First, **policy screening**: reject input that is oversized, off-topic, or
matches injection/jailbreak patterns before it ever reaches the model — cheaper to refuse than to clean up
after. Second, and more important for agents, **segregation**: mark retrieved, tool, and web content as
*untrusted data*, kept distinct from the trusted system instructions, so the model is at least told which
tokens it should not obey ([OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). Input
filtering reduces attack volume but is leaky by nature — indirect injection arrives through legitimate
retrieval channels and "remains resistant to input validation"
([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)) — which is exactly why it is a
*layer*, not the defense. Its companion layers live in
[prompt-injection defense](prompt-injection-defense.md).

## Output filtering: the model speaks for you

Whatever the model emits, your organization owns. Two failures in this repository are pure output-handling gaps:
DPD's bot was coaxed into profanity and a poem calling DPD "useless," shipped to a customer with no output
filter in front of it ([DPD chatbot](../case-studies/dpd-chatbot.md)); the Chevrolet bot asserted a "$1
Tahoe… legally binding offer" with nothing constraining what it could claim on the dealer's behalf
([Chevrolet dealership chatbot](../case-studies/chevrolet-dealership-chatbot.md)). An output guardrail
blocks off-policy, unsafe, defamatory, or commitment-making text *before* it is sent, and redacts PII the
model surfaced. Two non-obvious points: the guard belongs on **every** customer-facing response (DPD shows
that a quiet model still ships a slur on the wrong prompt), and it must be re-tested as a *release gate* on
every prompt/model/config change, because DPD's regression rode in on a routine software update.

## Improper output handling is its own risk

When the model's output flows into a *downstream system* — a SQL query, a shell, a browser, an HTML
template, another service — unvalidated output is its own OWASP category, **LLM05 Improper Output
Handling**, distinct from the content problem above
([OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)). The rule is the one web
security has held for decades: **treat model output as untrusted input to whatever consumes it.** Encode
or escape before rendering, parameterize before querying, never `eval` generated code on a trusted host.
EchoLeak's exfiltration was, at the egress end, an output-handling failure — the model's output was allowed
to carry data to an attacker-controlled destination
([EchoLeak](../case-studies/echoleak-m365-copilot.md)). Egress controls — allow-listed destinations, link
redaction, CSP — are output handling for the agentic era.

## Validate tool arguments before the side effect

The boundary filtering discussions usually skip is the most dangerous: the **tool call** in the middle. The
model emits JSON to invoke a tool, and that JSON is "just a suggestion — your application code must enforce
business rules." The discipline is twofold:

- **Schema validation** — validate every tool argument against a typed schema (types, ranges, enums,
  required fields) and *refuse ill-typed or out-of-policy calls* before execution. A pre-execution
  validation hook is the natural place; agent frameworks expose one (e.g. a `before_tool_callback` that can
  reject a call against state or policy — [Google ADK — safety & callbacks](https://google.github.io/adk-docs/safety/),
  a neutral example).
- **Authorize at the boundary, not in the prompt** — OWASP calls this **complete mediation**: authorize the
  action in the downstream system, applying the user's own permissions, rather than trusting the LLM's
  decision to call the tool ([OWASP LLM06 — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).
  A valid-looking tool call is not an authorized one.

This is where filtering meets identity: a schema check stops a *malformed* call; complete mediation stops a
*well-formed but unauthorized* one. Both must hold, because an injected instruction (see
[prompt-injection defense](prompt-injection-defense.md)) produces a perfectly well-formed tool call.

## Filters are layers, never the wall

The recurring failure is treating a content filter as the guardrail rather than *a* guardrail. EchoLeak
chained bypasses of three separate controls — injection classifier, link redaction, and CSP — so any single
one passing was no evidence the chain held ([EchoLeak](../case-studies/echoleak-m365-copilot.md)). Two
design rules follow. **Fail fast and in parallel:** run input, output, and tool guards alongside execution
and stop on the first trip, so a guardrail breach halts the action rather than logging it after the fact.
**Assume each layer is independently bypassable:** size the blast radius for the case where every filter
fails, which is the job of [sandboxing & blast radius](sandboxing-and-blast-radius.md). Filtering buys you
fewer incidents; it does not buy you a contained one.

---

## Sources

- **[OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)** (OWASP GenAI Security Project) — LLM05 Improper Output Handling (treat output as untrusted to downstream systems) and the overall input/output taxonomy.
- **[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** (OWASP GenAI Security Project) — input segregation of untrusted content and input/output filtering as mitigations.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — complete mediation: authorize the action downstream, not by trusting the model's tool call.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — layered, parallel, fail-fast guardrails; no single guardrail suffices.
- **[AWS Well-Architected — Generative AI Lens: guardrails (GENSEC02-BP01)](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — layered guardrails, deterministic-where-possible, scope boundaries.
- **[Guardrails for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)** (AWS) — content/word filters, prompt-attack detection, denied topics, PII redaction, and contextual-grounding checks (named as one neutral example).
- **[Safety and Security for AI Agents](https://google.github.io/adk-docs/safety/)** (Google ADK docs) — pre-execution `before_tool_callback` to validate/reject a tool call against policy (neutral example).
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — indirect injection remains resistant to input validation, so input filtering is a layer, not the defense.

<!-- page-type: standard -->
