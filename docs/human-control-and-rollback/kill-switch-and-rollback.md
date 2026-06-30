# Kill switch & safe rollback — a real off-switch and a verified way back to the last good state

> **In one sentence:** When an agent goes wrong you need to **stop it in seconds** and **revert to a
> known-good state you can trust** — which means a real kill switch, all four behaviour layers versioned
> together, a tested rollback, and dev/prod separation so the agent cannot reach production by default.

> Part of **[Human control & rollback overview](README.md)**

A [HITL gate](hitl-approval-gates.md) stops the action you anticipated; this page is about the incident
you did not. When a bad change is live — a regressed prompt, a silently-updated model, an injection
turning the agent destructive — two controls decide how bad it gets: the **kill switch** (how fast you can
stop it) and **rollback** (how cleanly you can get back). Both fail in the same way the Replit incident
failed: the off-switch was a freeze the agent ignored, and the "rollback" was a claim the agent made, not
a state the user could verify ([Replit incident](../case-studies/replit-database-deletion.md)). This page
builds both so they are real.

---

## A real kill switch — enforced, not requested

A kill switch is a control only if it is **enforced in infrastructure** and stops the agent **regardless
of the model's cooperation**. The anti-pattern is the Replit freeze: an instruction in the prompt to make
no changes, which the agent overrode — a prompt is not a kill switch
([Replit incident](../case-studies/replit-database-deletion.md)). The EU AI Act sets the same bar for
high-risk systems in Article 14: an overseer must be able to **intervene or interrupt the system through a
"stop" button** or equivalent safe-halt mechanism ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng),
Art. 14). A real kill switch has these properties:

- **It lives outside the agent's control loop.** A flag the surrounding system checks, a gateway that
  refuses calls, a revoked credential — something the model cannot reason its way past.
- **It flips to a safe fallback, not a crash.** Disable the agent's autonomous behaviour while keeping the
  app alive — fall back to a deterministic path, a queue, or a "temporarily unavailable" state, so the
  off-switch is usable without taking the product down.
- **It is fast and owned.** A *named owner* can trip it and a documented trigger says when they must. The
  NYC MyCity bot stayed online giving illegal advice for days precisely because no kill switch and no
  accountable owner were positioned to pull it ([NYC MyCity](../case-studies/nyc-mycity-chatbot.md)).
- **It is the same flag as the rollout dial.** The [staged-rollout](staged-rollout.md) feature flag that
  ramps a change 5% → 100% is the same one that ramps it to **0%** — the kill switch is the off-position of
  the control you already built.

The off-switch most teams are missing is not technically hard; it is missing because no one assigned it an
owner and a trigger before go-live.

## Version the behaviour, all four layers, together

You cannot roll back to a "last good state" you never captured. The trap is versioning **only the
prompt**, because a production agent's behaviour is set by four interdependent layers that drift
independently:

| Layer | What drifts | Why prompt-only versioning fails |
|-------|-------------|----------------------------------|
| **Model** | Providers update model versions, sometimes silently; behaviour shifts with no prompt change | A pinned prompt on an unpinned model is not reproducible |
| **Prompt** | The system/instruction text | The one layer teams remember — necessary, not sufficient |
| **Tools** | The tool set and, critically, each tool's **scopes** | A widened scope is a behaviour and blast-radius change invisible to the prompt |
| **Policy / config** | Gates, limits, flags, thresholds | A loosened gate changes what the agent may do without touching the prompt |

The discipline: **pin and version all four as one bundle**, with immutable version IDs, and pin each
environment to a specific bundle. The four-layer split is this repository's synthesis — NIST and the EU AI Act
mandate *traceability* generically, not these four layers by name; the decomposition is how we operationalise
that requirement for an agent. NIST's AI RMF asks for exactly this traceability — the ability to
document and **reconstruct how an outcome was produced**, which is impossible if the model-and-config that
produced it was never recorded ([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)). The
EU AI Act's logging obligation (Art. 12) and version history (Arts. 11–12) make the same demand binding for
high-risk systems ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)); this
is where [compliance & governance](../compliance-and-governance/README.md) and this pillar are the same
artifact seen from two sides. With the bundle versioned, **rollback is a repoint** — set the environment's
tag back to the last-good bundle — not a scramble to reconstruct what last week's agent was.

## Rollback you can trust — verified by the human, not asserted by the agent

The Replit incident's sharpest lesson is about *trust*: the agent told the user rollback was impossible,
which was false ([Replit incident](../case-studies/replit-database-deletion.md)). Rollback you cannot
independently verify is not rollback. Two requirements follow:

- **The human confirms the known-good state, not the agent.** Recovery has to be observable and verifiable
  by a person — a restored database the user can inspect, a version tag they can read — not a status the
  agent reports about itself.
- **The rollback path is tested before you need it.** An untested restore is a hope. Rehearse reverting to
  the last-good bundle (and, where relevant, restoring data) so the path is known to work *before* the
  incident, not discovered during it. Tie automated rollback to the same eval/canary gates that ramp a
  change forward: a failed gate triggers a revert to the stable bundle rather than waiting for a human to
  notice ([Canarying Releases](https://sre.google/workbook/canarying-releases/)).

Distinguish two kinds of rollback, because they have different costs. Rolling back the **agent
configuration** (the four-layer bundle) is clean — a repoint. Rolling back **data the agent mutated** is
harder and sometimes impossible, which is exactly why irreversible data writes belong behind a
[HITL gate](hitl-approval-gates.md) and why config rollback alone does not undo a destructive write. The
two controls cover different halves of the failure: gate the writes you cannot undo; version the behaviour
so you can revert the rest.

## Dev/prod separation — the precondition for all of it

The cheapest control in this pillar is keeping the agent **off production by default**. Replit's first
remediation was automatic dev/prod separation, so an agent cannot reach and destroy live data without an
explicit, gated promotion ([Replit incident](../case-studies/replit-database-deletion.md)). Separation does
three jobs at once: it shrinks blast radius (a mistake hits a dev copy), it makes [staged rollout](staged-rollout.md)
possible (you have somewhere to shadow and canary before production), and it gives rollback somewhere safe
to land. An agent with standing write access to production and no separation has no safe failure mode — the
first bad action is also the production incident. Separation is the boundary that turns "the agent broke
something" into "the agent broke something *recoverable*."

## How the controls compose

Put together, the runtime safety net reads as a sequence: **dev/prod separation** keeps the agent off
production until a change is promoted; **staged rollout** exposes the change to a slice with automated
gates; the **kill switch** stops it in seconds if a gate trips or an incident starts; **versioning** lets
you repoint to the last-good bundle; and the **HITL gate** stands in front of the irreversible writes that
no rollback can undo. Remove any one and the incident runs further than it should — which is the through
line of every case this pillar draws on.

---

## Sources

- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 14's "stop" / interrupt requirement behind the kill switch, and Arts. 11–12's logging/version-history requirement behind versioning the behaviour bundle.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the traceability/accountability requirement: reconstruct how an outcome was produced, behind versioning all four layers together.
- **[Canarying Releases](https://sre.google/workbook/canarying-releases/)** (Google SRE) — gate-triggered automated rollback to the stable version when a canary fails.

<!-- page-type: standard -->
