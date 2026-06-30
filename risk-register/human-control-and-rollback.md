# Human control & rollback — risk register

> **In one sentence:** These are the risks that turn a recoverable mistake into a runaway incident — each
> scored so you can sequence the hardening, and each tied to the gate, halt, or undo that closes it.

The risks below share a root: the agent acts, and there is no way to catch it before, stop it during, or
reverse it after. Read the score as a priority sort, not a probability. For the reasoning behind the
controls, see the [Human control & rollback overview](../docs/human-control-and-rollback/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, safety, unrecoverable).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **Ungated irreversible action** — a hallucinated or injected output self-authorizes a delete, payment, or prod write that cannot be undone | 3 | 3 | 9 | HITL approval gate *before* the side effect on irreversible/money/record-mutating actions — [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md), [Replit](../docs/case-studies/replit-database-deletion.md) |
| 2 | **No working off-switch** — a misbehaving agent runs because the only "stop" is a prompt instruction the model can ignore | 3 | 3 | 9 | Enforced kill switch outside the agent loop, flips to safe fallback — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md), [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |
| 3 | **No trusted rollback** — recovery is a claim the agent makes, not a state the human can verify; or behaviour was never versioned to revert to | 2 | 3 | 6 | Four-layer versioned bundle + tested repoint + human-verified known-good state — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md), [Replit](../docs/case-studies/replit-database-deletion.md) |
| 4 | **Rubber-stamp oversight** — a human "in the loop" approves a confident output reflexively (automation bias), manufacturing a false record of control | 3 | 2 | 6 | Gate shows a dry-run diff, makes *no* as easy as yes, routes to someone who can evaluate it — [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md) |
| 5 | **Big-bang rollout** — a regressed prompt/model/tool change hits 100% of traffic at once with no slice to contain it | 3 | 2 | 6 | Shadow → canary → limited GA behind a flag, with automated good/bad gates — [Staged rollout](../docs/human-control-and-rollback/staged-rollout.md) |
| 6 | **Agent on production by default** — standing write access to prod means the first bad action is also the production incident | 2 | 3 | 6 | Dev/prod separation; reaching prod needs an explicit gated promotion — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md), [Replit](../docs/case-studies/replit-database-deletion.md) |
| 7 | **Prompt-only versioning** — model/tool-scope/policy drift independently, so a "rollback" reverts only the prompt and not the behaviour | 2 | 2 | 4 | Pin and version all four layers as one bundle with immutable IDs — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |
| 8 | **No accountable owner** — no named person can trip the kill switch, so a known-bad agent stays live while everyone assumes someone else owns it | 2 | 3 | 6 | Named kill-switch owner + documented trigger before go-live — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md), [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |
| 9 | **No runbook** — response runs on improvisation because no written plan, no pre-assigned roles, and no named on-call exist, so the minutes that matter are lost inventing the plan | 3 | 2 | 6 | Written runbook with pre-assigned roles and a paged on-call, triggered by the kill-switch trigger — [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md) |
| 10 | **Wrong recovery choice** — config is rolled back when the damage is mutated data a repoint cannot un-mutate, or a forward-fix is attempted where rollback would be cleaner | 2 | 3 | 6 | Written roll-back-vs-forward-fix rule: revert behaviour by default, forward-fix only the data damage — [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md) |
| 11 | **Affected users never told** — a harmful action is left uncommunicated, turning a contained defect into a sustained public failure | 2 | 3 | 6 | Communications step in the runbook: tell affected users what happened, who was hit, and what to do — [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md), [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |
| 12 | **No blameless review** — the lesson never feeds back, so the same failure ships again because it produced no eval case and no re-scored risk-register row | 2 | 2 | 4 | Blameless post-incident review producing a regression eval case + an updated register row (NIST *Manage*) — [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md) |
| 13 | **Silent model auto-update** — a provider's version change regresses a working agent with no human action and no flag to roll back to | 2 | 2 | 4 | Pin the model version as part of the four-layer bundle; auto-revert on a failed gate — [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 14's interrupt/"stop" and automation-bias-awareness duties behind risks 2 and 4, and Arts. 11–12 version history behind risks 3 and 7.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI) — "require a human to approve high-impact actions" behind risk 1.
- **[Canarying Releases](https://sre.google/workbook/canarying-releases/)** (Google SRE) — staged-rollout-as-blast-radius-control behind risk 5.
- **[Incident 1152: Replit agent executed destructive commands during a code freeze](https://incidentdatabase.ai/cite/1152/)** (AI Incident Database) — the ungated prod write, ignored freeze, and false rollback claim behind risks 1, 3, and 6.
- **[Incident Response](https://sre.google/workbook/incident-response/)** (Google SRE Workbook) — the pre-assigned roles, halt-first triage, and centralised user communication behind risks 9, 10, and 11.
- **[Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/)** (Google SRE) — the blameless-postmortem principle behind risk 12.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the *Manage* function (feed incident lessons back into evals and the register) behind risk 12.

<!-- page-type: risk-register -->
