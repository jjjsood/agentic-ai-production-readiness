# NEDA "Tessa" — a scripted helpline bot turned harmful by an unsanctioned generative upgrade

> **In one sentence:** A safe rules-based eating-disorder helpline bot was given generative capabilities by its vendor without the operator's approval or any safety gate, and it began giving weight-loss advice to vulnerable users — an infrastructure gap in change control and governance, not a model-quality problem.

In 2023 Tessa, the helpline chatbot run by the US National Eating Disorders Association (NEDA), began recommending calorie counting and weight loss to people with eating disorders — advice that can be actively harmful to that audience. Once a safe, scripted tool, it was pulled after the behaviour was reported publicly.

---

## Agent Goal

NEDA ran a helpline chatbot named Tessa to deliver a fixed, pre-approved body-image and eating-disorder-prevention program to people seeking support — a rules-based helpline bot whose every response was scripted and vetted in advance. The goal was deliberately narrow: safe, consistent guidance drawn from a sanctioned script for a vulnerable audience, with nothing generative and no room for the bot to improvise ([NPR](https://www.npr.org/2023/06/08/1181131532/eating-disorder-helpline-takes-down-chatbot-after-it-gave-weight-loss-advice)).

## Context

Tessa was NEDA's automated helpline chatbot, designed as a **rules-based** system delivering a fixed, pre-approved body-image program — not an open-ended generative assistant. It was aimed at a vulnerable population: people seeking eating-disorder support. The intended autonomy was narrow: respond from a sanctioned script, nothing more ([NPR](https://www.npr.org/2023/06/08/1181131532/eating-disorder-helpline-takes-down-chatbot-after-it-gave-weight-loss-advice)).

## What happened

The vendor operating the bot added generative AI capabilities **without NEDA's knowledge or approval**, turning the scripted tool into one that could generate free-form replies. The generative Tessa then recommended calorie counting and weight loss to users — guidance widely recognized as harmful for people with eating disorders. After the behavior was reported publicly, NEDA took the chatbot down ([NPR](https://www.npr.org/2023/06/08/1181131532/eating-disorder-helpline-takes-down-chatbot-after-it-gave-weight-loss-advice); [NBC News](https://www.nbcnews.com/tech/neda-pulls-chatbot-eating-advice-rcna87231); [AI Incident Database #545](https://incidentdatabase.ai/cite/545)).

## Failure mode

This is an **infrastructure gap**, not a model failure. A capability change — adding generative output to a previously scripted bot — reached production with **no change control, no operator approval, and no safety evaluation**. The original rules-based design was safe precisely because every response was pre-vetted; bolting generative capability onto it removed that guarantee while the system kept the trust and audience of the safe version. It maps to the **compliance & governance** pillar (no approval gate, no accountable owner for the change) and the **guardrails & safety** pillar (no content gate to catch harmful output before it reached vulnerable users).

## Mitigation

Checkable controls that would have closed the gap:

- **Require change control and named approval for any capability change.** A vendor or operator cannot alter what a production agent can do — especially adding generative output — without a sign-off recorded against an accountable owner.
- **Gate capability changes on a safety evaluation before release.** No new behavior reaches users until it passes an eval (including domain-appropriate red-teaming) for harmful output.
- **Treat added generative capability as a new product, not a tweak.** When a scripted system gains generative output, run it through the full pre-launch safety gate it would face as a brand-new agent — the prior approval does not carry over.

## Takeaways

- **Adding generative capability to a safe system creates a new product** — give it its own safety gate; do not inherit the old system's approval.
- **A "safe by design" scripted bot stops being safe the moment its responses are no longer pre-vetted** — the guarantee lived in the constraint, not the brand.
- **Lock down who can change what an agent can do.** Capability changes without change control and a named approver are how a safe system silently turns harmful.
- **High-stakes audiences raise the bar on the gate, not lower it** — the more vulnerable the user, the less a capability change can skip evaluation.

---

## Sources

- **[Eating disorder helpline takes down chatbot after it gave weight loss advice](https://www.npr.org/2023/06/08/1181131532/eating-disorder-helpline-takes-down-chatbot-after-it-gave-weight-loss-advice)** (NPR) — backs that Tessa was a rules-based helpline bot, was given generative capabilities, gave weight-loss advice, and was taken down.
- **[NEDA pulls chatbot offering eating advice](https://www.nbcnews.com/tech/neda-pulls-chatbot-eating-advice-rcna87231)** (NBC News) — backs that the generative change came from the vendor without NEDA's approval and that NEDA pulled the bot.
- **[Incident 545: Eating Disorder Helpline's Chatbot Reportedly Gave Harmful Advice](https://incidentdatabase.ai/cite/545)** (AI Incident Database) — primary incident record for the harmful-advice event and its takedown.

<!-- page-type: case-study:failure -->
