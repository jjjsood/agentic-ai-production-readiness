# NYC MyCity Chatbot — official advice bot tells businesses to break the law

> **In one sentence:** A city government's official business-advice bot gave illegal regulatory advice and was left running afterward — a grounding and governance gap, not a model gap, the kind that accounts for the bulk of attributable agent failures.

Within weeks of launch, New York City's official "MyCity" small-business chatbot was shown to confidently advise illegal actions — telling employers they could take a cut of workers' tips and landlords they could reject tenants paying with housing vouchers. It stayed online and kept giving such guidance even after the problem was widely reported.

---

## Agent Goal

New York City launched an official chatbot, MyCity, as a small-business assistant — a public bot answering owners' questions on labor, housing, and regulatory rules directly, drawing on 2,000+ pages of city material. The city wanted to make government guidance instantly accessible in plain language, so an owner could ask a question and get an authoritative answer instead of digging through statutes and agency pages ([The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law)).

## Context

The MyCity chatbot was the City of New York's official, public-facing assistant for small-business questions — labor, housing, and regulatory guidance. It ran on Microsoft Azure and was trained on 2,000+ pages of city information, giving direct answers to business owners with no human review gate between the model and the user. ([The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law))

## What happened

In late March 2024, testing showed the bot advising actions that violate the law: that employers could take a cut of workers' tips, and that landlords could reject tenants paying with housing vouchers — both illegal. The advice was delivered with confidence and no warning, on exactly the regulated domains the tool was meant to help with. ([The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law))

Days later, a follow-up found the chatbot still active and still producing the same kind of illegal guidance despite widespread evidence of the problem. There was no rapid takedown and no clear owner who pulled it. ([The Markup / THE CITY](https://themarkup.org/artificial-intelligence/2024/04/02/malfunctioning-nyc-ai-chatbot-still-active-despite-widespread-evidence-its-encouraging-illegal-behavior))

## Failure mode

An **infrastructure gap**, not a model-quality one — and it maps to the **compliance & governance** and **guardrails & safety** pillars:

- **No domain grounding to authoritative law.** The bot generated regulatory advice without being grounded in the actual statutes it was answering about, so wrong answers read as authoritative.
- **No review gate for high-stakes answers.** High-consequence regulatory output went straight to users with no verification or human-in-the-loop check.
- **Weak governance kept it running.** Once failures surfaced, nothing forced a shutdown — no kill switch, no named owner accountable for pulling it.

## Mitigation

Concrete, checkable controls that close the gap:

- Ground regulatory answers in authoritative, current law (retrieval over verified statute/regulation text), and refuse or escalate when no grounded source backs the answer.
- Put a review gate in front of high-consequence answers (legal, financial, housing, labor) — human-in-the-loop or hard refusal, not free-form generation.
- Wire a kill switch with a **named governance owner** who can take the system offline, and a documented trigger for when they must.

## Takeaways

- In regulated advice domains, treat ungrounded generation as a defect: every answer must trace to authoritative source text or be refused.
- Gate high-consequence output behind human review — confidence in the response is not evidence it is lawful.
- Name an owner and a kill switch before launch; "still online despite known failures" is a governance failure, not a model one.

---

## Sources

- **[NYC's AI Chatbot Tells Businesses to Break the Law](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law)** (The Markup) — backs the Azure platform, 2,000+ pages of training, and the illegal advice on tips and voucher tenants.
- **[Malfunctioning NYC AI Chatbot Still Active Despite Widespread Evidence It's Encouraging Illegal Behavior](https://themarkup.org/artificial-intelligence/2024/04/02/malfunctioning-nyc-ai-chatbot-still-active-despite-widespread-evidence-its-encouraging-illegal-behavior)** (The Markup / THE CITY) — backs that the bot was left online and still producing illegal guidance after the findings.

<!-- page-type: case-study:failure -->
