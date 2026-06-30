# DoorDash voice self-service — routine Dasher calls resolved without a human

> **In one sentence:** A voice IVR for delivery-driver support works at scale not because of a bigger model, but because it gates low-confidence calls to live agents and holds latency under a hard budget — infrastructure, not model quality, carried it.

DoorDash runs a voice agent that resolves routine Dasher support calls end-to-end in production, at high volume and low latency, handing the rest off to live agents. What makes it hold up isn't a bigger model — it's two controls: low-confidence calls route to humans, and latency stays under a hard budget.

---

## Agent Goal

DoorDash built a voice agent to resolve routine Dasher phone-support calls end-to-end without a human — understanding natural speech, handling the common requests, and escalating only what it couldn't to live agents. The outcome it was built for was lower support cost and a smaller transfer rate, while holding response latency low enough (≤2.5s) for the exchange to feel like a real phone conversation ([AWS case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/)).

## Context

The system answers Dasher phone support automatically: an IVR that understands natural speech, resolves routine requests, and escalates the rest. It is built on Amazon Connect + Bedrock + Claude 3 Haiku and runs unattended for the calls it can handle, with a defined handoff to human agents for the calls it cannot. It fields **hundreds of thousands of Dasher calls per day** at **≤2.5s** response latency ([AWS case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/)).

## What happened

In production the voice agent cut agent transfers by ~**49%**, lifted first-contact resolution by ~**12%**, and saved ~**$3M** year-on-year in operating cost ([AWS case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/), [Anthropic DoorDash one-sheeter](https://assets.anthropic.com/m/53dbf4b0b4e5ab42/original/Anthropic-DoorDash-case-study-one-sheeters.pdf)). These are single-vendor figures — treat them as order-of-magnitude, not audited constants.

## What worked

- **An explicit escalation path.** Low-confidence calls route to live agents rather than being forced through the automated flow, so the agent only owns the calls it can actually resolve ([AWS case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/)).
- **An enforced latency budget.** The ≤2.5s response target drove the model choice: the faster Claude 3 Haiku was selected to stay inside it, making latency a design constraint rather than an afterthought ([AWS case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/)).
- **Built-in abuse handling.** The system includes prompt-injection and abusive-language handling, so adversarial or off-script callers don't derail it ([Anthropic DoorDash one-sheeter](https://assets.anthropic.com/m/53dbf4b0b4e5ab42/original/Anthropic-DoorDash-case-study-one-sheeters.pdf)).

## Takeaways

- Gate low-confidence interactions to a human by default; let the agent own only what it can resolve, and measure the transfer rate as the control's effectiveness.
- Treat latency as a hard budget that constrains model choice — pick the fastest model that meets quality, not the largest.
- Build prompt-injection and abuse handling into any open-input channel before launch, not after the first incident.
- Read single-vendor success metrics as ballpark direction, not audited proof; confirm the *infrastructure* claims before copying the numbers.

---

## Sources

- **[DoorDash voice self-service case study](https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/)** (AWS) — call volume, ≤2.5s latency, ~49% fewer transfers, ~12% FCR lift, ~$3M YoY savings, the escalation path, and the Haiku latency-driven model choice.
- **[Anthropic DoorDash case study one-sheeter (PDF)](https://assets.anthropic.com/m/53dbf4b0b4e5ab42/original/Anthropic-DoorDash-case-study-one-sheeters.pdf)** (Anthropic) — the production deployment and the built-in prompt-injection / abusive-language handling.

<!-- page-type: case-study:success -->
