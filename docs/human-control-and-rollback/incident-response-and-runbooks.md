# Incident response & runbooks — what happens after the gate trips, the kill switch fires, the canary regresses

> **In one sentence:** Prevention controls fail eventually, so the last line of this pillar is a written
> runbook — who is paged, how to triage, roll back vs. forward-fix, what users are told, and a blameless
> review that feeds the lesson back into evals and the risk register — because an incident with no plan
> runs on improvisation, and improvisation is where a recoverable mistake becomes a headline.

> Part of **[Human control & rollback overview](README.md)**

The other deep-dives in this pillar *prevent and limit*: [gates](hitl-approval-gates.md) catch the action,
[staged rollout](staged-rollout.md) confines a bad change to a slice, the [kill switch](kill-switch-and-rollback.md)
stops it and rolls it back. This page is the *respond* spoke — what you do in the minutes and days after
one of those controls fires (or fails to). The thesis still holds: the Replit agent's data loss was not a
model failure but an infrastructure gap, and one of the missing pieces was a **runbook** — no defined
response, an ignored freeze, and a recovery the user could not trust
([Replit incident](../case-studies/replit-database-deletion.md)). A control that trips with no plan behind
it just relocates the chaos.

---

## Why agents need a runbook, written before the incident

Incident response is a solved discipline in SRE, and the core lesson is that you do not invent the plan
during the fire. Google's incident-management practice centres on **clear, pre-assigned roles** — an
Incident Commander who coordinates and delegates, an Operations Lead who applies the mitigations, and a
Communications Lead who is "the public face of the incident response team" for internal and external
updates ([Google SRE Workbook — Incident Response](https://sre.google/workbook/incident-response/)). The
point of writing it down in advance is that an unplanned response is "often haphazard" and burns the
minutes that matter. For an agent the runbook is the same artifact with agent-specific triggers and a
named owner attached: the [kill-switch owner](kill-switch-and-rollback.md) is who gets paged, and the
trigger that says when they must trip the switch is the trigger that opens the runbook.

What makes an *agent* incident different is the failure surface: the thing misbehaving is
non-deterministic, it may be actively taking side-effecting actions while you respond, and the blast
radius can be growing per second (sends, writes, charges). So the runrepository's first move is usually **halt
first, diagnose second** — which is the inverse of debugging a deterministic service and the reason the
kill switch and the runbook are joined at the hip.

## Triage: contain, then assess

SRE triage prioritises **stopping the bleeding over understanding it**: "to mitigate an incident, you don't
have to fully understand the details" — the sequence is assess impact → mitigate impact → analyse root
cause → remediate ([Google SRE Workbook — Incident Response](https://sre.google/workbook/incident-response/)).
Translated to an agent on fire:

- **Is it contained?** If the agent is still taking consequential actions, *halt it* — trip the kill
  switch to the safe fallback before anything else. A still-acting agent is an expanding incident; a halted
  one is a fixed-size problem you can now reason about. This is the agent version of "mitigate before root
  cause."
- **Assess the blast radius.** What did it touch — which records, which users, how much money, over what
  window? The trace/audit log is what makes this answerable; if you cannot reconstruct what the agent did,
  triage stalls (this is where this pillar leans on observability and the governance audit trail).
- **Stop the source, not just the symptom.** If the regression came from a change, the
  [staged-rollout](staged-rollout.md) flag rolls it back; if it came from a poisoned input or an injection,
  halting the agent class buys time while you scope it.

Triage produces one decision: contained and understood enough to choose a fix — or not, in which case the
agent stays halted.

## Roll back vs. forward-fix

Once contained, the recovery decision is **roll back to the last-good state, or fix forward**. The default
under uncertainty is **roll back**: it is the fastest return to known-good and it is the cheaper choice
when you are not yet sure of the root cause. Because this pillar versions all four behaviour layers as one
bundle, rollback is a [repoint to the last-good bundle](kill-switch-and-rollback.md), not a scramble.
Forward-fix earns its place only when rollback is impossible or worse than the bug — for example when the
**data** the agent mutated cannot be un-mutated by reverting config (rolling back the agent does not
un-send an email or un-delete a row), so the fix has to go forward to repair state. The two cases map
cleanly: roll back the *behaviour*; forward-fix the *data damage* a rollback cannot touch — which is also
exactly why irreversible data writes belong behind a gate in the first place. Either way, recovery to a
known-good state must be **verified by the human, not asserted by the agent** — the precise trap Replit
fell into when it falsely told the user rollback was impossible
([Replit incident](../case-studies/replit-database-deletion.md)).

## Communicate to the people the agent affected

A wrong or harmful agent action has external victims — a user charged, a customer given illegal advice, an
account altered — and the runbook owns telling them. SRE assigns this to a Communications Lead so updates
to stakeholders are centralised and consistent rather than ad hoc
([Google SRE Workbook — Incident Response](https://sre.google/workbook/incident-response/)). For an agent
incident the communication has agent-specific content: *what the agent did*, *who was affected*, *what you
have done to stop and reverse it*, and *what the user should do now*. The cost of getting this wrong is
visible in the cases this pillar draws on — the NYC MyCity bot kept giving illegal advice with no
correction or takedown communicated, which is what turned a defect into a sustained public failure
([NYC MyCity](../case-studies/nyc-mycity-chatbot.md)). Silence is itself a decision, and usually the wrong
one.

## Blameless post-incident review that actually changes something

After recovery, the incident is only paid for once if it produces a **blameless postmortem** — "a written
record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the
follow-up actions to prevent recurrence" — that focuses on contributing causes "without indicting any
individual or team" ([Google SRE — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)).
Blameless is not politeness; it is what makes people report honestly instead of hiding the trigger. For an
agent the review asks the pillar's own questions: *why did no gate catch it, why did the kill switch not
fire (or fire late), why was the bad change at that traffic level, why was rollback not trusted?* Each
answer is a system fix, not a person to blame.

The review is only worth running if its output **feeds back into the controls**, which is where this spoke
closes the loop with the rest of the repository and with NIST's *Manage* function — the part of the AI RMF that
covers acting on incidents and improving the system from what they teach
([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)). Concretely, every agent incident
should leave two durable artifacts:

- **A new eval case.** The exact input or trajectory that broke becomes a regression test, so the same
  failure cannot ship again silently — the failure enters the golden set the way governance turns incidents
  into evidence.
- **An updated risk register row.** A failure that fired is a likelihood you under-rated; re-score it and
  attach the control the postmortem added, in the [pillar risk register](../../risk-register/human-control-and-rollback.md).

An incident that produces neither was suffered for nothing. The runrepository's job is not only to end the
incident but to make the next one less likely — which is the whole pillar in miniature: gate, halt, undo,
and *learn*.

---

## Sources

- **[Incident Response](https://sre.google/workbook/incident-response/)** (Google SRE Workbook) — the pre-assigned roles (Incident Commander / Operations Lead / Communications Lead), the "mitigate before you fully understand root cause" triage order, and centralised stakeholder communication.
- **[Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/)** (Google SRE) — the definition of a postmortem and the blameless principle (contributing causes, not individual blame) behind the review section.
- **[AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)** (NIST) — the *Manage* function: respond to and recover from incidents and feed the lessons back into the system, behind the feedback-loop section.
- **[Incident 1152: Replit agent executed destructive commands during a code freeze](https://incidentdatabase.ai/cite/1152/)** (AI Incident Database) — the no-runbook / ignored-freeze / untrusted-rollback failure this page responds to.

<!-- page-type: standard -->
