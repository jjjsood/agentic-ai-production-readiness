# McDonald's × IBM AI Drive-Thru — voice ordering pulled after a multi-year pilot

> **In one sentence:** A drive-thru voice agent failed in noisy real-world audio *and* had no confidence-gated handoff to catch its own bad orders — a partly model-quality case that still turns on the missing human-control infrastructure.

After a roughly three-year pilot across 100+ US drive-thrus, McDonald's ended its IBM voice-ordering partnership in June 2024 as misorders went viral — nine sweet teas on one order, bacon piled onto an ice cream. It is the case in this collection that leans most honestly on genuine model limits — but the controls that would have contained those limits were missing.

---

## Agent Goal

McDonald's and IBM built an automated voice-ordering system to take drive-thru orders, unattended — the agent capturing each customer's spoken order accurately enough to send straight to the kitchen with no staff member involved. The goal was to automate the order-taking station across many locations, freeing crew for other work and speeding the line; getting orders right on noisy, real-world audio was the bar it had to clear ([ACS Information Age](https://ia.acs.org.au/article/2024/mcdonald-s-bins-ai-drive-thru-after-errors-go-viral.html)).

## Context

The system took drive-thru orders by voice — an unattended, customer-facing agent operating in one of the noisiest input environments a speech model meets: overlapping voices, road noise, varied accents, menu jargon. McDonald's ran it as a pilot at **100+ US locations** over a **~3-year** partnership with IBM before deciding whether to scale it ([AI Incident Database #475](https://incidentdatabase.ai/cite/475), [ACS Information Age](https://ia.acs.org.au/article/2024/mcdonald-s-bins-ai-drive-thru-after-errors-go-viral.html)).

## What happened

In **June 2024** McDonald's ended the IBM voice-ordering partnership after a ~3-year pilot. Viral clips showed misorders the system never caught — e.g. **nine sweet teas** added to one order, and **bacon piled onto an ice cream**. Accuracy **reportedly plateaued around 80–85%** (ballpark, as reported), short of what unattended ordering needs ([AI Incident Database #475](https://incidentdatabase.ai/cite/475), [ACS Information Age](https://ia.acs.org.au/article/2024/mcdonald-s-bins-ai-drive-thru-after-errors-go-viral.html)).

## Failure mode

This is a **mixed** root cause, and worth stating honestly — unlike most cases here, model quality is genuinely part of the story:

- **Model-quality limit (real):** speech recognition in noisy drive-thru audio — accents, background and road noise, simultaneous speakers — is a hard problem, and the system hit a quality plateau a bigger or better-tuned model alone might not have cleared.
- **Infrastructure gap (the containable part):** there was **no reliable confidence threshold and no human handoff** to catch low-confidence orders before they reached the customer. A model that is sometimes wrong is survivable; a model that is sometimes wrong *with no gate to catch it* is not.

The containable half maps to the **human-control-and-rollback** pillar: an unattended agent operating on uncertain input needs a confidence-gated path back to a human, not just a more accurate model.

## Mitigation

Concrete, checkable controls — none of which require a better model:

- Compute a per-order **confidence score** and define a threshold below which the order is not auto-committed.
- Route low-confidence orders to a **human handoff** (staff confirmation) before they reach the kitchen/customer — confidence-gated HITL, not silent auto-accept.
- Require **order read-back / confirmation** on the customer-facing path so a misorder is caught at the point of input.
- Track misorder rate as a **production eval metric** with a rollback trigger, so a quality plateau is observed before it goes viral, not after.

## Takeaways

- In messy real-world input, design the **handoff** before the model: a confidence-gated HITL path beats chasing a few more accuracy points.
- An agent on uncertain input needs a **confidence threshold** that decides auto-commit vs. human review — "usually right" is not a deployment control.
- Even a real model-quality limit is survivable if low-confidence outputs are **caught and contained**; it becomes an incident only when nothing catches them.
- Measure the **failure rate in production** with a rollback trigger, so the decision to pull is yours, not the public's.

---

## Sources

- **[AI Incident Database #475](https://incidentdatabase.ai/cite/475)** (Responsible AI Collaborative) — catalogs the McDonald's/IBM drive-thru voice-ordering failures and the viral misorders.
- **[McDonald's bins AI drive-thru after errors go viral](https://ia.acs.org.au/article/2024/mcdonald-s-bins-ai-drive-thru-after-errors-go-viral.html)** (ACS Information Age) — reports the June 2024 end of the IBM partnership, the ~3-year/100+-location pilot, and the reported ~80–85% accuracy plateau.

<!-- page-type: case-study:failure -->
