# Observability & evals — risk register

> **In one sentence:** These are the risks that turn a working agent into one you can neither debug, cost, nor
> trust — each scored so you can sequence the hardening, and each tied to the control that closes it.

The risks below share a root: the agent runs, but you cannot *see* a single run or *measure* the population of
runs, so failures stay invisible until users or the invoice surface them. Read the score as a priority sort,
not a probability. For the reasoning behind the controls, see the
[Observability & evals overview](../docs/observability-and-evals/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, legal, safety).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **No reconstructable trace** — an incident happens and there's no way back to what the agent did, because runs weren't captured and can't be reproduced | 3 | 3 | 9 | Structured `gen_ai.*` tracing on by default; single run reconstructable from a run id — [Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md) |
| 2 | **Undetected wrong outputs in production** — bad answers accumulate unseen because nothing monitors live quality (left online despite known failures) | 3 | 3 | 9 | Online evals + user-verdict signals + baseline drift alerting — [Eval in production](../docs/observability-and-evals/eval-in-production.md), [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |
| 3 | **Demo trusted as proof of reliability** — a single passing run ships, then fails in production (pass@1 ≫ pass^8) | 3 | 3 | 9 | Repeat-run reliability testing + eval gate before ship — [Eval in production](../docs/observability-and-evals/eval-in-production.md), [Cognition Devin demo](../docs/case-studies/cognition-devin-demo.md) |
| 4 | **Silent regression on change** — a prompt tweak or model-version swap quietly breaks a flow with no gate to catch it | 3 | 2 | 6 | Held-out regression suite gating every change; pinned model version — [Evals & regression suites](../docs/observability-and-evals/evals-and-regression-suites.md) |
| 5 | **Unattributable cost** — token spend can't be tied to a feature/agent because calls were never tagged; runaway loops invisible until the invoice | 3 | 2 | 6 | Tag every call from day one + cost-per-successful-task unit economics + financial-anomaly alerting — [Cost & FinOps attribution](../docs/observability-and-evals/cost-and-finops-attribution.md) |
| 6 | **Eval theatre** — a green headline score from a single biased LLM judge or an overfit set hides real regressions | 2 | 2 | 4 | Trajectory grading + fixed rubric + multi-judge + human-anchored spot checks — [Evals & regression suites](../docs/observability-and-evals/evals-and-regression-suites.md) |
| 7 | **Observability pipeline becomes a PII store** — prompts, tool args, and completions logged raw turn the trace backend into an unmanaged sensitive-data store | 2 | 3 | 6 | Redact at the boundary before the span leaves; least-privilege backend access; bounded retention — [Tracing & token accounting](../docs/observability-and-evals/tracing-and-token-accounting.md) |
| 8 | **Open eval loop** — online evals (or a thumbs-down spike) flag a live failure but it never re-enters the offline golden set, so the same class of failure recurs change after change | 2 | 2 | 4 | Close the loop: label the flagged production failure and add it to the golden set so the next regression run catches its class — [Evals & regression suites](../docs/observability-and-evals/evals-and-regression-suites.md), [checklist "closed back to offline"](../checklists/observability-and-evals.md) |

---

## Sources

- **[OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)** (OpenTelemetry) — the trace schema behind the reconstruction control in risk 1.
- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — token accounting and attribution tagging behind risk 5.
- **[τ-bench](https://arxiv.org/abs/2406.12045)** (Sierra) — the pass@1-vs-pass^k consistency gap behind risk 3.
- **[From Generation to Judgment: Opportunities and Challenges of LLM-as-a-Judge](https://arxiv.org/pdf/2411.16594)** (arXiv) — the LLM-as-judge biases behind the eval-theatre control in risk 6.
- **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)** (OWASP) — sensitive-information disclosure behind risk 7.

<!-- page-type: risk-register -->
