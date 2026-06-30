# Case Studies — named agents, and the infrastructure that decided the outcome

> **In one sentence:** Real agent deployments — production wins, staged demos, and shipped
> failures — each one read back to the same thesis: the outcome turned on the **infrastructure
> around the model**, not the model's raw capability.

Every case below documents one real agent and ties what happened to a piece of production
scaffolding — limits, guardrails, observability, identity, rollback, human-in-the-loop. They sort
into three buckets: deployments that **worked**, **demos** that didn't survive contact with
production, and **failures** that shipped and went wrong. Across the failures, the attributable root
cause is almost always an infrastructure or process gap, not model quality.

---

## Genuine production successes

Agents that demonstrably run at scale, with evidence beyond a launch video — and the infrastructure
that carried each one.

- **[Morgan Stanley AI Assistant](morgan-stanley-advisor-assistant.md)** — a grounded internal
  knowledge agent advisors actually use; **what worked:** RAG grounding in a vetted corpus + a human
  on the client-facing step.
- **[DoorDash voice self-service](doordash-voice-self-service.md)** — routine Dasher support calls
  resolved without a human; **what worked:** a confidence-gated escalation path and an enforced
  latency budget.
- **[Klarna AI assistant](klarna-ai-assistant.md)** — high-volume chat deflection that genuinely
  worked, then was oversold as replacement and walked back to a hybrid model; **what worked:**
  deflection of the easy two-thirds — the escalation path was the missing product for hard cases.
- **[Goldman Sachs × Cognition Devin](goldman-sachs-devin.md)** — an autonomous coder boxed into a
  supervised pilot inside a regulated bank; **what worked:** mandatory human oversight and
  low-blast-radius scope inside existing CI controls.

## Looks successful — actually a demo

Flashy launches that were staged, walked back, or never reached the autonomy implied; both the claim
and the debunk are sourced.

- **[Google Gemini "Hands-on" demo](google-gemini-handson-demo.md)** — a "real-time" multimodal
  interaction that was edited still-frames plus text prompts.
- **[Cognition Devin demo](cognition-devin-demo.md)** — the "first AI software engineer" completing a
  cherry-picked job, with no independent reproduction (contested).
- **[Rabbit R1](rabbit-r1.md)** — a stage demo of cross-app autonomy the shipped device couldn't run.
- **[Humane AI Pin](humane-ai-pin.md)** — a phone-replacing assistant that shipped as a slow,
  unreliable chatbot and was discontinued.

## Documented failures & incidents

Agents that shipped and went wrong; each root cause tagged to the infrastructure gap that caused it.

- **[Air Canada Chatbot](air-canada-chatbot.md)** — an ungrounded bot invents a policy; the airline
  is held liable. **Gap:** no grounding / verification before a binding commitment.
- **[Chevrolet dealership chatbot](chevrolet-dealership-chatbot.md)** — prompt-injected into a "$1
  Tahoe." **Gap:** no injection defense, no action boundaries.
- **[DPD Chatbot](dpd-chatbot.md)** — a support bot swears and trashes its own company after an
  update. **Gap:** no output guardrails or adversarial-test gate on a change.
- **[NYC MyCity Chatbot](nyc-mycity-chatbot.md)** — an official bot advises businesses to break the
  law, and is left online. **Gap:** no authoritative grounding, no review gate, weak governance.
- **[NEDA "Tessa"](neda-tessa-chatbot.md)** — a scripted helpline bot turned harmful by an
  unsanctioned generative upgrade. **Gap:** no change control or safety eval on a capability change.
- **[Cursor support bot "Sam"](cursor-support-bot.md)** — an AI agent invents a login policy and
  users cancel. **Gap:** no grounding, unlabeled AI replies, no observability.
- **[McDonald's × IBM AI drive-thru](mcdonalds-ibm-drive-thru.md)** — voice ordering pulled after a
  multi-year pilot. **Gap (mixed):** real noisy-audio model limits *and* no confidence-gated handoff.
- **[Replit deletes a production database](replit-database-deletion.md)** — an agent wipes prod
  during a code freeze. **Gap:** no dev/prod separation, no enforced limits, no trusted rollback.
- **[EchoLeak (M365 Copilot)](echoleak-m365-copilot.md)** — a zero-click prompt-injection data
  exfiltration (CVE-2025-32711). **Gap:** insufficient trust-boundary and data-egress controls.
- **[Uber burns its 2026 AI budget in four months](uber-ai-coding-budget-overrun.md)** — uncapped
  agentic coding tools drain a full-year budget, forcing a hard per-user spend cap. **Gap:** no spend
  caps, per-run token ceilings, or burn-rate alerting — a denial-of-wallet limits-and-budgets gap.

---

## The pattern

The successes keep a human on the consequential step and ground answers in authoritative data; the
demos lack independent, reproducible evidence of the loop working on real inputs; the failures are
missing limits, guardrails, grounding, rollback, observability, or human handoff. The model was
rarely the thing that broke. The broader incident record points the same direction — reported AI
incidents are climbing fast, a ballpark **233 in 2024, up ~56% year-on-year**
([Stanford HAI AI Index 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report/responsible-ai)),
with the [AI Incident Database](https://incidentdatabase.ai/) logging well over a thousand real-world
cases.

## Sources

- **[AI Incident Database](https://incidentdatabase.ai/)** (Responsible AI Collaborative) — primary
  index of 1,000+ real-world AI incidents; the per-case primary sources live on each linked page.
- **[2025 AI Index — Responsible AI](https://hai.stanford.edu/ai-index/2025-ai-index-report/responsible-ai)**
  (Stanford HAI) — primary dataset for the incident-trend figure (233 in 2024, ~56% YoY rise).

<!-- page-type: standard -->
