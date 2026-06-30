# Cost & FinOps attribution — make every token answer to a feature, a tenant, and a task

> **In one sentence:** Counting tokens is observability; knowing *whose* tokens they are and *what they
> bought* is FinOps — and without that attribution a runaway agent drains the budget silently, because the
> service stays up while the bill climbs, which is an infrastructure blind spot, not a model fault.

> Part of **[Observability & evals overview](README.md)**

The [tracing & token accounting](tracing-and-token-accounting.md) page captures *how many* tokens each run
spent. This page is the next step: turning those counts into **attribution** — spend tagged per feature,
tenant, user, and run — and into **unit economics** — cost per *successful task*, not per call. It also covers
surfacing cost regressions in CI and production, and the *visibility* half of denial-of-wallet detection (the
*enforcement* half — hard budgets, kill switches, spend-rate circuit breakers — lives in the limits & budgets
pillar; this page produces the signal that pillar acts on). It is written for whoever owns the agent's bill
and has to explain it.

---

## Visibility is not control — but you can't control what you can't attribute

The FinOps community draws a sharp line: a dashboard that *shows* spend is not a budget that *stops* it.
Enforcement is its own discipline. But attribution is the precondition for both — you cannot set a per-feature
budget, bill a tenant, or even know which agent ran away if every model call lands in one undifferentiated
pile. The FinOps-for-AI workstream makes token the atomic cost unit and per-feature token budgets a
first-class concept, backed by usage limits, quotas, and anomaly detection
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). This page builds the
*visibility* layer that makes the enforcement layer possible; the kill switch itself belongs elsewhere.

## Tag every call, from day one

Attribution is an architectural decision made at the first line of instrumentation, not a report generated
later. Every model call should carry the tags you will one day want to slice by — typically `feature_id`,
agent id, `tenant_id`, user id, and a run/session id — so spend aggregates cleanly along each axis
([FinOps Foundation — FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)). These ride alongside
the per-call token counts already on the span; the OpenTelemetry GenAI conventions give you the token figures
(`gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`) and the session join
(`gen_ai.conversation.id`) in a vendor-neutral schema, and your attribution tags sit beside them as additional
span attributes ([OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)).
The reason "from day one" is load-bearing: retrofitting a `tenant_id` onto historical un-attributed calls
usually cannot be done — the information to reconstruct who spent what is simply gone. An un-tagged call is a
cost you can total but never assign.

Useful slices the tags unlock:

| Axis | The question it answers |
|---|---|
| Per **feature** | Which capability is the cost centre — and is it worth its spend? |
| Per **tenant / customer** | Are we losing money on a specific account; can we bill usage back? |
| Per **user** | Is one user (or one abuser) driving disproportionate spend? |
| Per **run / session** | What did this single incident cost — the per-run total from [tracing](tracing-and-token-accounting.md). |

## Unit economics: cost per *successful task*, not per call

Cost-per-call is the wrong denominator for an agent, because an agent makes *many* calls per task — a
multi-agent system can use on the order of **~15× the tokens of a single chat**, so a cheap-looking per-call
cost hides an expensive per-task one ([Anthropic — multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
Worse, averaging cost over *all* runs flatters you by counting failures as if they delivered value. The metric
we recommend — the authors' synthesis of the FinOps unit-economics view, not a named standard — is **cost per
successful task**: total spend (including the runs that looped, retried, or failed) divided by the tasks that
actually succeeded. This is where cost and evals meet: "success" is defined by the
[eval](evals-and-regression-suites.md) layer, so unit economics is only as trustworthy as your eval grading.
Tracking it surfaces failures the accuracy metric alone hides — a change that lifts task success while
doubling cost per successful task is an economic regression, even though every quality dashboard is green.

## Surface cost regressions in CI and production

Cost is a regression axis like capability or safety, and it belongs in the [regression
suite](evals-and-regression-suites.md): a change that triples token usage or tool-call count should fail the
gate even if it improves the answer. The denominator there is the same one — cost per successful task on a
held-out set — so a prompt or model swap that quietly inflates spend is caught before it ships, not on the
next invoice.

In production, the same signal feeds the monitoring baseline alongside the quality metrics from [eval in
production](eval-in-production.md): baseline the per-feature and per-tenant cost-per-successful-task, and alert
on sustained drift. A model-version change, a prompt edit, or a shift in input mix can move cost without
moving accuracy, and a cost baseline is what makes that movement visible.

## The visibility half of denial-of-wallet

The failure this attribution exists to catch is **denial-of-wallet**: an attacker (or a runaway loop)
exploiting the pay-per-use model to inflate spend. What makes it dangerous is precisely why observability has
to cover it — unlike a denial-of-service attack, a denial-of-wallet attack **escalates cost without impacting
service operation**, so the application keeps serving normally while the bill climbs, and conventional
availability-focused monitoring never fires ([A Comprehensive Review of Denial of Wallet Attacks](https://arxiv.org/abs/2508.19284)).
The detection signal is therefore a *financial* anomaly, not an availability one: a spend-rate or
per-tenant-cost spike against baseline, surfaced by the attribution above. OWASP catalogues this under
unbounded consumption and names anomaly detection on unusual consumption as a control
([OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)). This page produces that anomaly
signal; the **limits & budgets** pillar owns what happens next — the hard per-run and per-tenant ceilings, the
spend-rate circuit breaker, and the kill switch that turns a detected runaway off. Visibility here, enforcement
there; you need both, and neither substitutes for the other.

---

## Sources

- **[FinOps for AI](https://www.finops.org/wg/finops-for-ai-overview/)** (FinOps Foundation) — token as the atomic cost unit, per-feature budgets, the tag-every-call attribution requirement, and visibility-vs-control behind this page's spine.
- **[OpenTelemetry — GenAI attribute registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)** (OpenTelemetry) — the `gen_ai.usage.*` token attributes and `gen_ai.conversation.id` that attribution tags ride alongside.
- **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** (Anthropic) — the ~15× multi-agent token cost behind "cost per call is the wrong denominator".
- **[A Comprehensive Review of Denial of Wallet Attacks in Serverless Architectures](https://arxiv.org/abs/2508.19284)** (arXiv) — denial-of-wallet escalates cost without disrupting availability, so availability monitoring misses it — the detection blind spot behind the financial-anomaly signal.
- **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)** (OWASP) — unbounded consumption and anomaly-detection-on-consumption as the named control class.

<!-- page-type: standard -->
