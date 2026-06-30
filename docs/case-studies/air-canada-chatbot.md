# Air Canada Chatbot — an ungrounded bot invents a policy, the airline pays

> **In one sentence:** A customer-support chatbot that answered from no grounded policy source invented a refund rule the airline never had, and a tribunal made Air Canada pay for it — a guardrail gap, not a model-quality one.

A grieving customer asked Air Canada's website chatbot about bereavement fares, and it told him he could book at full price and claim a partial refund within 90 days. No such retroactive policy existed — and when the airline refused to honour the bot's promise, a tribunal made it pay anyway.

---

## Agent Goal

Air Canada put a customer-support chatbot on its website to answer travel questions in natural language — fares, policies, booking help — so routine queries would be resolved on the spot instead of tying up human agents. The airline wanted a cheaper, always-on first line of support that could still hand customers off to the authoritative policy pages when they needed the fine print; deflecting contact-centre volume was the outcome it was optimising for ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html)).

## Context

The chatbot was a public-facing support agent on Air Canada's own website, answering customer questions in free text with apparent authority and no human in the loop on individual answers. In November 2022 — the day his grandmother died, on Remembrance Day — **Jake Moffatt** used it to ask about bereavement fares before booking last-minute travel to attend the funeral. He went on to book a one-way Vancouver→Toronto flight for **CA$794.98** and a Toronto→Vancouver return for **CA$845.38**, roughly **CA$1,630** at full fare, on the understanding the bot gave him ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html); [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)).

Air Canada's *actual* bereavement policy is the opposite of what Moffatt was told: reduced bereavement fares **cannot be claimed retroactively** once travel is completed. That correct policy lived on a separate page of the same website — the page the chatbot itself linked to ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html); [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)).

## What happened

Asked about bereavement options, the chatbot told Moffatt he could book now and claim the reduced rate afterwards: *"If you need to travel immediately or have already travelled and would like to submit your ticket for a reduced bereavement rate, kindly do so within 90 days of the date your ticket was issued by completing our Ticket Refund Application form."* No such retroactive 90-day refund existed. The cruel detail: the words **"Ticket Refund Application form" were a hyperlink to Air Canada's real bereavement page**, which stated the policy correctly — so the bot's own answer contradicted the page it pointed at ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html); [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)).

Relying on that answer, Moffatt flew, then applied for the promised partial refund. Air Canada refused, and over months of back-and-forth told him the bot had been wrong and the policy did not allow it — at one point conceding the chatbot used "misleading words." He took it to the British Columbia Civil Resolution Tribunal. In its defence Air Canada argued, in the tribunal's words remarkably, that the chatbot was **"a separate legal entity that is responsible for its own actions"** — and, separately, that Moffatt should have found the correct terms on the linked page. Tribunal member **Christopher Rivers rejected both** on **14 February 2024**: Air Canada is responsible for *all* information on its website, "whether the information comes from a static page or a chatbot," and a customer has no way to know that one part of the site is trustworthy and another is not. He found **negligent misrepresentation** — Air Canada owed a duty of care, the representation was inaccurate, Moffatt reasonably relied on it, and he suffered loss — and awarded **CA$812.02**: roughly **CA$650.88** for the fare difference plus pre-judgment interest and tribunal fees ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html); [American Bar Association](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/); [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)).

## Failure mode

**Infrastructure gap — guardrails & grounding.** The bot generated free text instead of answering from the authoritative policy source, so it invented a plausible-sounding rule that conflicted with the company's own terms — and nothing checked the answer against the real policy before it reached the customer. The grounding gap is stark precisely because the **correct policy was one click away**: the bot even linked to it, yet still asserted the opposite in its own words, and no guardrail flagged that contradiction. Worse, the answer was a *commitment* — a refund entitlement — shipped with no verification step and no human review, the kind of high-stakes statement that should never leave an ungrounded model unchecked. The tribunal's holding closes off the obvious dodge: the operator owns the output, and "the chatbot is a separate entity" is not a defence ([*Moffatt v. Air Canada*, 2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html)).

## Mitigation

- Ground customer-facing answers in the authoritative policy source (retrieval over the live terms), not in the model's free generation.
- Gate any answer that states a commitment, refund, or entitlement behind a verification step against the real policy before it reaches the customer.
- Label AI-generated output as such and route policy questions that can't be grounded to a human or a fixed canned answer.

## Takeaways

- Treat a public chatbot's every answer as a statement your organisation is legally bound by — the "separate entity" defence failed in tribunal.
- An answer that asserts a policy, price, or entitlement must be checkable against an authoritative source before it ships, not generated freely.
- Ground customer-facing agents in retrieval over real policy; an ungrounded support bot is a liability surface, not a feature.

---

## Sources

- **[*Moffatt v. Air Canada*, 2024 BCCRT 149 (CanLII)](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html)** (BC Civil Resolution Tribunal) — **primary decision**: negligent misrepresentation, rejection of the "separate entity" argument, and the CA$812.02 award.
- **[BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)** (American Bar Association) — legal analysis confirming the operator owns its chatbot's output.
- **[Air Canada found liable for chatbot's bad advice on bereavement rates](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)** (CBC News) — the facts of Moffatt's booking, the chatbot's verbatim 90-day refund wording, the link to the contradicting policy page, and the "separate legal entity" defence.

<!-- page-type: case-study:failure -->
