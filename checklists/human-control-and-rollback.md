# Human control & rollback — go-live checklist

> **In one sentence:** Every box below is a way to gate, halt, or undo an autonomous action — if you
> cannot tick it, an incident has no off-ramp and you are betting on the model not misbehaving.

Run this before sign-off on any agent that can take a consequential action — money, deletes, record
writes, external sends. A failed box is not an automatic blocker; it is a residual risk someone has to
**accept in writing**, knowing that this pillar is the difference between an incident that stops and one
that runs until someone notices. For the why behind each theme, see the
[Human control & rollback overview](../docs/human-control-and-rollback/README.md).

---

## Approval gates (gate the irreversible)

- [ ] Every tool is **risk-rated** (read/write, reversibility, permissions, financial impact) and the rating drives whether it is gated. ([HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md))
- [ ] Irreversible, money-moving, record-mutating, and external-send actions **require human approval before the side effect**, not after.
- [ ] The gate is **enforced in code / the downstream system**, not a "please ask first" instruction in the prompt.
- [ ] New mutating tools default to **approval-required**, and graduate to autonomous only on evidence.

## Gate quality (against automation bias)

- [ ] The gate presents a **dry-run diff** of the exact effect (rows, recipients, amounts, commands) — not a paraphrase of intent.
- [ ] **Refusal is as easy as approval** — no default-yes, no pre-checked box, no buried reject.
- [ ] The decision is routed to **someone who can evaluate it at the rate it arrives**; a gate firing hundreds of times an hour is mis-scoped.
- [ ] The **approver, the evidence shown, and the decision are recorded**, per the human-oversight obligation. ([EU AI Act Art. 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng))

## Staged rollout

- [ ] Agent behaviour changes (prompt / model / tool / policy) ship **behind a feature flag** that separates *deployed* from *active*.
- [ ] A new version runs in **shadow** (mirrored traffic, serving nothing) before any user sees it.
- [ ] A **canary** serves a small slice (e.g. ~5%) and is compared **against a control by population**, not just aggregate. ([Google SRE — canarying](https://sre.google/workbook/canarying-releases/))
- [ ] **Automated good/bad gates** on error/refusal rate, tool-call distribution, latency, cost/request, and a quality signal advance or halt the rollout.
- [ ] Flag evaluation is **locked to the session**, so a conversation does not flip versions mid-stream.

## Kill switch

- [ ] A **real stop control** halts the agent **regardless of the model's cooperation** — a flag/gateway outside the agent's loop, not a prompt. ([Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md))
- [ ] The kill switch flips to a **safe fallback** (deterministic path / unavailable state), not a crash.
- [ ] A **named owner** can trip it, with a **documented trigger** for when they must. ([NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md))

## Versioning & rollback

- [ ] **All four behaviour layers** — model, prompt, tools+scopes, policy/config — are pinned and versioned **as one bundle** with immutable IDs.
- [ ] The **model version is pinned**, not left to silent provider updates.
- [ ] **Rollback is a repoint** to the last-good bundle, and the path has been **tested before go-live**, not discovered during an incident.
- [ ] **Config rollback ≠ data rollback** — there is a plan to reverse (or a written, accepted record that you *cannot* reverse) the **data the agent mutated**, distinct from repointing the behaviour bundle. ([Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md))
- [ ] A failed eval/canary gate **automatically reverts** to the last-stable bundle, rather than waiting for a human to notice. ([Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md))
- [ ] Recovery to a known-good state is **verifiable by the human**, not asserted by the agent. ([Replit incident](../docs/case-studies/replit-database-deletion.md))

## Separation of environments

- [ ] **Dev/prod separation** keeps the agent off production data by default; reaching production requires an explicit, gated promotion. ([Replit incident](../docs/case-studies/replit-database-deletion.md))

## Incident response (after the gate trips, the kill switch fires, the canary regresses)

- [ ] A **written runbook** exists with pre-assigned roles, and a **named on-call** is paged on the documented trigger — response does not run on improvisation. ([Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md))
- [ ] Triage is **halt-first, diagnose-second** — a still-acting agent is tripped to the safe fallback before root-cause analysis begins. ([Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md))
- [ ] A **roll-back-vs-forward-fix rule** is written down: roll back the behaviour by default; forward-fix only the data damage a config repoint cannot un-mutate. ([Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md))
- [ ] **Affected users are told** — what the agent did, who was hit, what you did to stop and reverse it, and what they should do now — through a single owned channel, not ad hoc. ([Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md))
- [ ] A **blameless post-incident review** runs and produces two durable artifacts: a new **eval/regression case** for the input that broke, and a re-scored **risk-register row** with the added control. ([Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md))

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 14 human oversight (interrupt via a "stop" button, awareness of automation bias) and Arts. 11–12 logging/version history, behind the gate-quality, kill-switch, and versioning lines.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI) — "require a human to approve high-impact actions" and *complete mediation*, behind the approval-gate lines.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — tool risk-rating (read/write, reversibility, permissions, financial impact) behind the first approval-gate line.
- **[Canarying Releases](https://sre.google/workbook/canarying-releases/)** (Google SRE) — canary-vs-control, per-population comparison, gate-on-metrics, and gate-triggered automated revert behind the staged-rollout and auto-revert lines.
- **[Incident Response](https://sre.google/workbook/incident-response/)** (Google SRE Workbook) — pre-assigned roles, halt-/mitigate-first triage, and centralised stakeholder communication behind the incident-response lines.
- **[Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/)** (Google SRE) — the blameless-postmortem definition and principle behind the post-incident-review line.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the *Manage* function (respond, recover, feed lessons back) behind the eval-case-plus-risk-register output of the review line.

<!-- page-type: checklist -->
