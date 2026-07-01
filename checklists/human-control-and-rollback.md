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

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Risk-rate every tool | Each tool rated (read/write, reversibility, permissions, financial impact); the rating drives whether it is gated | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md); [OpenAI — practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| ☐ | Approve before side effect | Irreversible/money-moving/record-mutating/external-send actions require human approval before the side effect, not after | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | Gate enforced in code | Gate enforced in code / the downstream system, not a "please ask first" instruction in the prompt | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | New tools approval-required | New mutating tools default approval-required, and graduate to autonomous only on evidence | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md) |

## Gate quality (against automation bias)

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Show dry-run diff | Gate presents the exact effect (rows, recipients, amounts, commands), not a paraphrase of intent | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md) |
| ☐ | Refusal as easy as approval | No default-yes, no pre-checked box, no buried reject | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md); [EU AI Act Art. 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Route at reviewable rate | Decision routed to someone who can evaluate it at the rate it arrives; a gate firing hundreds/hour is mis-scoped | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md) |
| ☐ | Record the decision | Approver, evidence shown, and decision recorded, per the human-oversight obligation | [HITL approval gates](../docs/human-control-and-rollback/hitl-approval-gates.md); [EU AI Act Art. 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |

## Staged rollout

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Deploy behind feature flag | Behaviour changes (prompt/model/tool/policy) ship behind a flag that separates *deployed* from *active* | — |
| ☐ | Shadow before serving | A new version runs in shadow (mirrored traffic, serving nothing) before any user sees it | — |
| ☐ | Canary vs control | A canary serves a small slice (e.g. ~5%), compared against a control by population, not just aggregate | [Google SRE — canarying](https://sre.google/workbook/canarying-releases/) |
| ☐ | Automated good/bad gates | Gates on error/refusal rate, tool-call distribution, latency, cost/request, and a quality signal advance or halt the rollout | [Google SRE — canarying](https://sre.google/workbook/canarying-releases/) |
| ☐ | Session-locked flag | Flag evaluation locked to the session, so a conversation doesn't flip versions mid-stream | — |

## Kill switch

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Real stop control | Halts the agent regardless of the model's cooperation — a flag/gateway outside the loop, not a prompt | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md); [EU AI Act Art. 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Flip to safe fallback | Kill switch flips to a deterministic path / unavailable state, not a crash | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |
| ☐ | Named owner + trigger | A named owner can trip it, with a documented trigger for when they must | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md); [NYC MyCity](../docs/case-studies/nyc-mycity-chatbot.md) |

## Versioning & rollback

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Version all four layers | Model, prompt, tools+scopes, policy/config pinned + versioned as one bundle with immutable IDs | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md); [EU AI Act Arts. 11–12](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |
| ☐ | Pin the model version | Model version pinned, not left to silent provider updates | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |
| ☐ | Test rollback pre-go-live | Rollback is a repoint to the last-good bundle, and the path is tested before go-live, not discovered during an incident | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |
| ☐ | Config ≠ data rollback | A plan to reverse (or a written, accepted record you *cannot* reverse) the data the agent mutated, distinct from repointing the bundle | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md) |
| ☐ | Auto-revert on failed gate | A failed eval/canary gate automatically reverts to the last-stable bundle, rather than waiting for a human to notice | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md); [Google SRE — canarying](https://sre.google/workbook/canarying-releases/) |
| ☐ | Human-verifiable recovery | Recovery to a known-good state is verifiable by the human, not asserted by the agent | [Kill switch & rollback](../docs/human-control-and-rollback/kill-switch-and-rollback.md); [Replit incident](../docs/case-studies/replit-database-deletion.md) |

## Separation of environments

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Dev/prod separation | Agent off production data by default; reaching production requires an explicit, gated promotion | [Replit incident](../docs/case-studies/replit-database-deletion.md) |

## Incident response (after the gate trips, the kill switch fires, the canary regresses)

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Written runbook + on-call | Runbook with pre-assigned roles; a named on-call paged on the documented trigger — response doesn't run on improvisation | [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md); [Google SRE — Incident Response](https://sre.google/workbook/incident-response/) |
| ☐ | Halt-first, diagnose-second | A still-acting agent is tripped to the safe fallback before root-cause analysis begins | [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md); [Google SRE — Incident Response](https://sre.google/workbook/incident-response/) |
| ☐ | Rollback-vs-forward rule | Written rule: roll back behaviour by default; forward-fix only the data damage a config repoint can't un-mutate | [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md) |
| ☐ | Tell affected users | What the agent did, who was hit, how you stopped/reversed it, and what they should do now — via a single owned channel | [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md); [Google SRE — Incident Response](https://sre.google/workbook/incident-response/) |
| ☐ | Blameless post-incident review | Produces two durable artifacts: a new eval/regression case for the input that broke, and a re-scored risk-register row with the added control | [Incident response & runbooks](../docs/human-control-and-rollback/incident-response-and-runbooks.md); [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/); [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) |

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 14 human oversight (interrupt via a "stop" button, awareness of automation bias) and Arts. 11–12 logging/version history, behind the gate-quality, kill-switch, and versioning rows.
- **[OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI) — "require a human to approve high-impact actions" and *complete mediation*, behind the approval-gate rows.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — tool risk-rating (read/write, reversibility, permissions, financial impact) behind the first approval-gate row.
- **[Canarying Releases](https://sre.google/workbook/canarying-releases/)** (Google SRE) — canary-vs-control, per-population comparison, gate-on-metrics, and gate-triggered automated revert behind the staged-rollout and auto-revert rows.
- **[Incident Response](https://sre.google/workbook/incident-response/)** (Google SRE Workbook) — pre-assigned roles, halt-/mitigate-first triage, and centralised stakeholder communication behind the incident-response rows.
- **[Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/)** (Google SRE) — the blameless-postmortem definition and principle behind the post-incident-review row.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the *Manage* function (respond, recover, feed lessons back) behind the eval-case-plus-risk-register output of the review row.

<!-- page-type: checklist -->
