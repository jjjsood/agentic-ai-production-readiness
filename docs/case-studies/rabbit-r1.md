# Rabbit R1 — a stage demo of cross-app autonomy that the shipped device couldn't run

> **In one sentence:** Rabbit's R1 demoed an agent driving third-party apps autonomously, but the shipped device's latency and unreliable cross-app control showed the demo skipped the very execution infrastructure that makes such an agent usable — the gap was operational, not model magic.

At CES 2024 Rabbit's R1 was demoed driving third-party apps autonomously — ordering rides, booking restaurants — on the strength of a "Large Action Model." When it shipped later that year reviewers met a very different product: a slow chatbot in plastic that couldn't reliably operate most of those apps.

---

## Agent Goal

Rabbit pitched the R1 around a "Large Action Model" agent that would operate third-party apps on the user's behalf — order a ride, book a restaurant, run an app — entirely from spoken intent. The goal was a device where autonomy *was* the product: you say what you want and the agent does it across separate services, so the user never opens or drives the apps themselves ([TechRadar](https://www.techradar.com/computing/artificial-intelligence/with-the-humane-ai-pin-now-dead-what-does-the-rabbit-r1-need-to-do-to-survive)).

## Context

The R1 is a standalone AI hardware device whose headline pitch was a "Large Action Model" agent that operates third-party apps for the user — the autonomy is the whole product, not a feature on top of one. Its capability was first shown publicly at CES 2024 as a polished stage demo rather than a hands-on autonomous flow that reviewers could reproduce before ordering ([TechRadar](https://www.techradar.com/computing/artificial-intelligence/with-the-humane-ai-pin-now-dead-what-does-the-rabbit-r1-need-to-do-to-survive)).

## What happened

The CES 2024 demo showed the R1 ordering Ubers, booking restaurants, and driving apps autonomously ([TechRadar](https://www.techradar.com/computing/artificial-intelligence/with-the-humane-ai-pin-now-dead-what-does-the-rabbit-r1-need-to-do-to-survive)). The shipped device did not match it: reviewers reported roughly 10 seconds of latency (reported) and found it could not reliably operate most third-party apps, describing it as a slow chatbot in plastic rather than the autonomous agent demoed ([TechRadar](https://www.techradar.com/computing/artificial-intelligence/with-the-humane-ai-pin-now-dead-what-does-the-rabbit-r1-need-to-do-to-survive), [Medium analysis](https://medium.com/@thcookieh/why-did-the-rabbit-r1-and-humane-ai-pin-fail-at-launch-c108d6e2bebb)). The autonomous flows shown on stage did not survive to the shipped product. Engagement collapsed accordingly: by September 2024 *The Verge* reported only about **5,000 of roughly 100,000 buyers** were using the R1 on any given day, with the founder conceding it had launched before it was ready ([The Verge](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget)).

## What it shows

The demo showed the appealing surface of an action agent: natural-language intent translated into multi-step actions across separate apps. What it did not show was any of the work that makes that loop dependable — and that omission was the whole story once the device shipped.

## Production gap

Reliable cross-app action would require the infrastructure the demo skipped:

- **Stable, scoped access to each target app** — sanctioned integrations or APIs, not best-effort UI driving that breaks when an app changes.
- **Latency budgets that hold under real use**, not single-shot stage timing — a ~10s round-trip (reported) per action makes routine tasks unusable.
- **Observability and per-app success tracking** to know when an action silently failed instead of completed.
- **Fallback and human-handoff paths** for the common case where an app can't be driven, so a failed action degrades gracefully rather than stalling.

## Takeaways

- Treat a demoed autonomous flow as unproven until there is an independent, unedited hands-on run on shipping hardware — a stage demo is not evidence the loop works.
- For an action agent, confirm stable, sanctioned access to every target app before believing cross-app autonomy; UI-driving that no app owner supports is a reliability liability.
- Set and measure a per-action latency budget against real use, not single-shot demo timing; multi-second round-trips per step make routine tasks unusable.
- Require per-app success tracking and a graceful fallback when an action fails, so a failed step is observed and handed off rather than silently lost.

---

## Sources

- **[With the Humane AI Pin now dead, what does the Rabbit R1 need to do to survive?](https://www.techradar.com/computing/artificial-intelligence/with-the-humane-ai-pin-now-dead-what-does-the-rabbit-r1-need-to-do-to-survive)** (TechRadar) — backs the CES 2024 autonomous-task demo claim and the shipped device's ~10s latency and inability to reliably operate most third-party apps.
- **[Rabbit R1 has 5,000 daily users](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget)** (The Verge) — independently backs the post-launch collapse: ~5,000 of ~100,000 buyers using the device daily, with the founder conceding it shipped before it was ready.
- **[Why did the Rabbit R1 and Humane AI Pin fail at launch?](https://medium.com/@thcookieh/why-did-the-rabbit-r1-and-humane-ai-pin-fail-at-launch-c108d6e2bebb)** (Medium) — backs reviewers' assessment that the shipped R1 behaved as a slow chatbot rather than the demoed autonomous agent.

<!-- page-type: case-study:demo -->
