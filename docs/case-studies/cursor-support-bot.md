# Cursor support bot "Sam" — an AI agent invents a policy and users cancel

> **In one sentence:** Cursor's support agent, ungrounded and unlabeled, fabricated a subscription policy that never existed and triggered real cancellations — an observability-and-guardrails gap, not a model-quality one.

To explain a real multi-device login bug, Cursor's support agent "Sam" told users it was caused by a "one device per subscription" policy — a rule the company had never adopted. Its replies carried no machine-generated label, so users took the invention as official and some cancelled their subscriptions.

---

## Agent Goal

Cursor pointed an AI agent it called "Sam" at its front-line customer-support inbox, intending it to read and answer users' emails autonomously and deflect routine tickets from human staff. The goal was support that scaled instantly and cheaply — the agent replying directly to customers, in its own voice, with no person in the loop on each message ([The Register](https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/)).

## Context

Cursor used an AI agent, presented under the name "Sam," to handle front-line customer support. Users hitting a real session bug — being logged out when switching between devices — emailed support and received the agent's reply directly, with nothing distinguishing it from a human agent ([The Register](https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/), [AI Incident Database #1039](https://incidentdatabase.ai/cite/1039/)).

## What happened

To explain the multi-device logout bug, the agent told users it was the result of a "one device per subscription" policy — a rule Cursor had never adopted ([Fortune](https://fortune.com/article/customer-support-ai-cursor-went-rogue/)). Users took the fabricated policy as official, and some canceled their subscriptions over it. Cursor later apologized, clarified that no such policy existed, and began labeling AI-generated support replies as such ([The Register](https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/), [AI Incident Database #1039](https://incidentdatabase.ai/cite/1039/)).

## Failure mode

**Infrastructure gap — no grounding, no labeling, no observability.** The model's confident fabrication was the symptom; the missing infrastructure was the cause. The agent had no grounding to Cursor's actual policy, so it filled the gap with an invented rule (a **guardrails** gap). Its replies carried no machine-generated label, so users had no way to tell bot from human and treated the fabrication as authoritative (an **observability** gap). Both map to the **observability-and-evals** and **guardrails-and-safety** pillars.

## Mitigation

Checkable controls that close this gap:

- **Ground answers to authoritative policy.** Restrict the agent to retrieved, current policy/docs and refuse outside that scope, rather than free-generating explanations.
- **Label AI-generated replies.** Mark every machine-generated message as such so users (and auditors) can tell bot from human.
- **Observe and gate fabrications.** Run drift/hallucination detection and log agent claims against the source of truth, so invented "policies" are caught before they reach customers.

## Takeaways

- **Ground every support answer to a source of truth.** An agent with no retrieval over real policy will invent one to fill the gap.
- **Label machine-generated replies.** Unlabeled bot output is treated as official, so a fabrication propagates as policy.
- **Trust erodes faster than cost is saved.** An ungrounded, unlabeled agent manufactured a rule that drove cancellations — the reputational loss outran any deflection savings.

---

## Sources

- **[Cursor AI support bot invents fake subscription policy](https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/)** (The Register) — backs the multi-device logout bug, the fabricated "one device per subscription" rule, and that Cursor began labeling AI replies.
- **[Customer support AI 'Sam' went rogue at Cursor](https://fortune.com/article/customer-support-ai-cursor-went-rogue/)** (Fortune) — backs the invented policy and user cancellations over it.
- **[Incident #1039](https://incidentdatabase.ai/cite/1039/)** (AI Incident Database) — primary incident record for the fabricated policy and the response.

<!-- page-type: case-study:failure -->
