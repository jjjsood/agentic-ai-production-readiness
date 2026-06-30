# Staged rollout — shadow → canary → limited GA, so a bad change hits a slice, not everyone

> **In one sentence:** Rolling a change out gradually behind automated good/bad gates is the cheapest way
> to bound blast radius — a 5% canary caps a bad release at ~5% of traffic instead of 100%, which is the
> whole point of not shipping an agent change to everyone at once.

> Part of **[Human control & rollback overview](README.md)**

An agent change — a new prompt, a swapped model, an added tool, a tweaked policy — is a behaviour change
to a non-deterministic system, and the demo never hits the long-tail input, the injection, or the loop
that production will. Staged rollout is the discipline of exposing that change to **progressively more
traffic, with a gate at each step**, so a regression is caught while it is still cheap and contained. This
page takes the SRE rollout curve — shadow → canary → limited GA — and puts it in agent terms: what to
measure at each stage, how the math bounds the damage, and why every step stays behind a flag with a
kill-switch path.

---

## Why gradual, not all-at-once

This is settled SRE practice, not an AI-specific invention. Google defines **canarying** as "a partial and
time-limited deployment of a change in a service and its evaluation," sending the change to a small slice
of traffic while the rest serves as an unchanged **control**, so defects show up before all of production
is affected ([Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/)).
Almost all Google rollouts proceed gradually with verification steps rather than flipping to 100%
([Google SRE Book — Reliable product launches](https://sre.google/sre-book/reliable-product-launches/)).
The reason is arithmetic: with a 5% canary, a change that produces a 20% error rate raises the *overall*
error rate by only ~1%, spending your error budget in proportion to exposure rather than all at once
([Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/)). Blast radius
is set by the size of the slice, and the slice is yours to choose.

## The rollout curve for an agent

| Stage | What runs | What you compare | Gate to advance |
|-------|-----------|------------------|-----------------|
| **Shadow** | New version runs on **duplicated live traffic** but serves nothing to users | New vs. current on tool-call patterns, error/refusal rate, output length, latency, cost/request | No user-visible regression in the mirrored comparison |
| **Canary** | Small real-traffic slice (e.g. ~5%) actually served; the rest is the control | Canary vs. control on the same metrics, broken down **by population** | Automated good/bad gates green over a representative window |
| **Limited GA** | Progressively widen — e.g. 5% → 25% → 50% → 100% | Each step against the prior, watching the same gates | No regression at each widening; full ramp only after sustained green |

**Shadow mode** is where an agent change earns the most cheaply: because nothing is served, you can compare
the new version's behaviour to production on real inputs at zero user risk — does it call different tools,
refuse more, run longer, cost more? **Canary** then exposes a real slice and compares it against the
control, and Google's own guidance is to break monitoring down **by population**, because aggregate
system metrics often mask a canary problem entirely
([Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/)). Then widen
in steps, never in one jump.

## What to gate on for an agent

Pick the **top few metrics** that clearly indicate a problem, are attributable to *this* change, and
correlate with real user impact — Google warns against tracking more than a dozen, since beyond that the
signal blurs ([Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/)).
For an agent, the high-signal set is:

- **Error / refusal / fallback rate** — a spike means the change broke or over-restricted behaviour.
- **Tool-call distribution** — a shifted pattern (new tool fired far more, a write tool appearing where it
  should not) is an early sign of a behaviour change the change did not intend.
- **Latency percentiles and cost per request** — agents amplify both; a regression here is a budget
  incident waiting to happen.
- **Quality / task-success signal** — sampled trace grading on the canary, plus cheap implicit signals
  like thumbs-down and regeneration rate.

The gates should be **automated** — a human deciding "looks fine" at each step does not scale and reintroduces
the bias problem. Tie advancement (and rollback) to thresholds on these metrics, not to a person's
impression.

## Keep every stage behind a flag — and keep the off-ramp

The mechanism that makes staged rollout safe is the **feature flag** that decouples *deployed* from
*active*: the new version ships dormant, gets switched on for 5% → 25% → 100%, and — critically — can be
switched **off** to a safe fallback at any point. That same flag is the kill switch (see
[kill switch & rollback](kill-switch-and-rollback.md)); staged rollout and the off-switch are the same
control turned up and down. Release engineers and SREs co-own both the canary and the rollback path, by
design, so the person ramping the change owns the way back too
([Google SRE Book — Release engineering](https://sre.google/sre-book/release-engineering/)).

Two agent-specific cautions — engineering judgement extending the SRE practice to a conversational,
non-deterministic system rather than claims drawn from a single source:

- **Lock flag evaluation to the session, not the request.** A conversational agent that flips between the
  old and new version mid-conversation produces incoherent behaviour and unattributable metrics; pin the
  version for the whole session so the canary comparison is clean.
- **Never roll out to 100% by silence.** "No alerts fired" over a short window is not the same as "the
  change is good" — give each stage a window proportional to your traffic so the gate metrics actually
  accumulate signal before you widen ([Google SRE Workbook — Canarying Releases](https://sre.google/workbook/canarying-releases/)).

## Staged rollout is also how autonomy graduates

The rollout curve is not only for code changes; it is how a *capability* earns trust. A new mutating tool
can ship in [planning-only mode](hitl-approval-gates.md) (proposing, never committing), then canary the
autonomous version to a small slice with the gates above watching for the wrong action, then widen as
evidence accumulates — and snap back to gated mode instantly if a gate trips. This is the maturity ladder
from the overview made operational: a tool moves from human-*in*-the-loop toward monitored autonomy **on
the rollout curve**, with the same off-ramp the rest of the pillar provides. The change that does *not*
get this treatment — shipped straight to all traffic, no shadow, no canary, no flag — is the one the NYC
MyCity and Replit incidents share: a behaviour reached every user with no slice to contain it and no
verified way back ([NYC MyCity](../case-studies/nyc-mycity-chatbot.md),
[Replit incident](../case-studies/replit-database-deletion.md)).

---

## Sources

- **[Canarying Releases](https://sre.google/workbook/canarying-releases/)** (Google SRE) — the definition of canary as a partial, time-limited deployment vs. a control; the 5%-canary blast-radius math; the "top few metrics," per-population breakdown, and window-sizing guidance.
- **[Reliable product launches at scale](https://sre.google/sre-book/reliable-product-launches/)** (Google SRE) — that gradual rollout with verification steps is the default, not the exception.
- **[Release engineering](https://sre.google/sre-book/release-engineering/)** (Google SRE) — that release engineers and SREs co-own canarying and the rollback path.

<!-- page-type: standard -->
