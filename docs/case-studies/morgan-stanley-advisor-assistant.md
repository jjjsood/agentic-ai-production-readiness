# Morgan Stanley AI Assistant — a grounded internal agent that advisors actually use

> **In one sentence:** Morgan Stanley's advisor assistant works not because the model is special but because the infrastructure around it carries it — retrieval grounding in a vetted corpus, a scope that takes no client-facing action, and a human who reviews every output before it reaches a client.

Morgan Stanley's internal AI assistant for wealth advisors did what most pilots never do — it reached broad, daily use across the firm. The reason isn't a special model; it's the infrastructure around it: retrieval grounding in a vetted corpus, a scope that takes no client-facing action, and a human reviewing every output before it reaches a client.

---

## Agent Goal

Morgan Stanley built an internal AI assistant so its wealth-management advisors could query the firm's vetted research library in natural language — having the agent surface and synthesize answers instead of an advisor hunting through ~100,000 proprietary documents by hand. The goal was to put the whole research corpus at an advisor's fingertips while keeping every answer grounded in approved internal material, never open-ended generation ([OpenAI case study](https://openai.com/index/morgan-stanley/)).

## Context

The agent is an internal retrieval assistant for wealth-management advisors that answers natural-language questions against the firm's vetted research library of roughly **~100,000 proprietary documents** ([OpenAI case study](https://openai.com/index/morgan-stanley/)), order of magnitude. It is scoped to internal knowledge: it surfaces and synthesizes the firm's own research and takes no autonomous client-facing action. Follow-on tools built on the same partnership — Debrief, which drafts meeting notes back into the CRM, and AskResearchGPT — extend the same grounded, internal pattern ([Morgan Stanley — Debrief launch](https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch), [Morgan Stanley — AskResearchGPT](https://www.morganstanley.com/press-releases/morgan-stanley-research-announces-askresearchgpt)).

## What happened

The Assistant moved into real, broad use rather than staying a pilot. Roughly **>98% of advisor teams** actively use it, and advisor access to the document set rose from about **~20% to ~80%** — both ballpark figures from the firm and its vendor ([Morgan Stanley — Debrief launch](https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch), [CNBC](https://www.cnbc.com/2024/06/26/morgan-stanley-openai-powered-assistant-for-wealth-advisors.html)). The Debrief and AskResearchGPT tools then shipped on the same footing ([OpenAI case study](https://openai.com/index/morgan-stanley/)).

## What worked

Three infrastructure choices, not raw model quality, carried the deployment:

- **Retrieval grounding in a vetted corpus** — answers are grounded in the firm's own approved research library rather than the model's open-ended generation, which constrains what it can assert ([OpenAI case study](https://openai.com/index/morgan-stanley/)).
- **Scope limits** — the agent is confined to internal knowledge and takes no autonomous client-facing action, keeping its blast radius inside the firm ([Morgan Stanley — Debrief launch](https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch)).
- **Human review on the client-facing step** — an advisor reviews and edits any output before it reaches a client, so a person owns the final word ([OpenAI case study](https://openai.com/index/morgan-stanley/)).

## Takeaways

- Ground a knowledge agent in an authoritative, vetted internal corpus instead of open generation — retrieval is the control that makes the output defensible.
- Scope the agent to internal knowledge and forbid autonomous client-facing action, so its blast radius stays inside the firm.
- Put a human review/edit step on any output that reaches a customer, and treat that human as the accountable last word.

---

## Sources

- **[OpenAI case study — Morgan Stanley](https://openai.com/index/morgan-stanley/)** (OpenAI) — backs the ~100,000-document corpus, the retrieval grounding, the human review-before-client step, and the follow-on tools.
- **[AI at Morgan Stanley — Debrief launch](https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch)** (Morgan Stanley) — backs the >98% advisor-team adoption, the ~20%→~80% access rise, and the internal-only scope.
- **[Morgan Stanley Research announces AskResearchGPT](https://www.morganstanley.com/press-releases/morgan-stanley-research-announces-askresearchgpt)** (Morgan Stanley) — backs the AskResearchGPT follow-on tool on the same grounded pattern.
- **[Morgan Stanley's OpenAI-powered assistant for wealth advisors](https://www.cnbc.com/2024/06/26/morgan-stanley-openai-powered-assistant-for-wealth-advisors.html)** (CNBC) — independent reporting backing the adoption and access figures.

<!-- page-type: case-study:success -->
