# Uber Burns Its 2026 AI Budget in Four Months — agentic coding tools with no per-user spend cap

> **In one sentence:** Agentic coding assistants ran uncapped across thousands of engineers and drained a full-year budget in roughly a third of the year — a denial-of-wallet failure caused by missing spend limits, not by anything the models did wrong.

Uber gave its engineers agentic coding tools like Claude Code and Cursor and told them to use AI "as much as possible," with internal leaderboards ranking usage — then watched its entire 2026 AI budget burn out by around April. In June 2026 the company imposed a hard **$1,500-per-month cap per employee per agentic coding tool** to stop the bleed ([Bloomberg](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs), [TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)). The runaway was financial, not functional: the tools worked as designed, and that was the problem.

---

## Agent Goal

Uber rolled out agentic coding assistants — software such as Anthropic's Claude Code and Cursor that plan and execute multi-step coding work, not just autocomplete a line — to its engineering organization and actively pushed adoption, encouraging staff to lean on AI "as much as possible" and ranking usage on internal leaderboards ([The Information, via TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)). The target outcome was developer-productivity uplift across the workforce; the budget set in 2025 assumed a level of consumption that the agentic-tool rollout blew straight past ([Simon Willison](https://simonwillison.net/2026/Jun/3/uber-caps-usage/)).

## Context

The tools ran across Uber's large engineering organization on metered, pay-per-token pricing, where each agentic run — a chain of tool calls, file reads, edits, and re-checks — resends accumulated context to the model and bills for it. There was **no per-user or per-tool spend limit** in place when the rollout began; the only governance signal pushed in the opposite direction, telling engineers to use the tools more and gamifying that usage ([TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/), [Bloomberg](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs)).

## What happened

Uber exhausted its **full 2026 AI budget within roughly four months** — by about April — because real consumption far outran the 2025 projection ([Simon Willison](https://simonwillison.net/2026/Jun/3/uber-caps-usage/), [TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)). In June 2026 the company responded by capping spend at **$1,500 per month per employee per agentic coding tool**, tracked on an internal dashboard with approval-based exceptions ([Bloomberg](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs)). Uber was not alone: peer companies moved to spending controls in the same window, and an AI consultant told Axios of a client that ran up an unverified, eye-watering bill — reportedly on the order of **$500 million in a single month** — after setting *no* usage limits on employee AI licenses, a figure to treat as an anecdotal order-of-magnitude claim, not a confirmed accounting line ([Axios, via Tech Startups](https://techstartups.com/2026/05/28/company-accidentally-spent-500-million-on-claude-ai-in-one-month-after-forgetting-usage-limits/)). The pattern is the named failure class OWASP catalogues as **Unbounded Consumption**, which explicitly includes "denial of wallet" — uncontrolled inference draining a budget through pay-per-use pricing ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).

## Failure mode

A textbook **limits & budgets** infrastructure gap, not a model-quality failure — the models did exactly what they were asked, and the cost ran away because nothing bounded it:

- **No per-user or per-tool spend cap** — consumption could grow without a ceiling, so thousands of small overruns compounded into a budget-wide blowout ([Bloomberg](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs)).
- **No per-run token ceiling** — agentic runs resend accumulated context every step, so an unbounded multi-step session costs far more than a single prompt, with nothing capping the per-task spend ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).
- **No anomaly alerting on burn rate** — the overspend surfaced only when the annual budget was already gone, four months in, rather than when the daily run-rate first diverged from plan ([TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)).
- **Governance pushed the wrong way** — leaderboards and "use it as much as possible" incentivised volume with no opposing cost signal, so the only feedback loop amplified spend ([The Information, via TechCrunch](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)).

## Mitigation

The fixes are infrastructural and generalize to any team running metered LLM or agent workloads — most are exactly what OWASP recommends for Unbounded Consumption ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)):

- **Hard spend caps per user and per tool**, enforced at the billing/gateway layer with approval-based exceptions — the control Uber ultimately shipped ([Bloomberg](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs)).
- **A per-run token ceiling and loop/step limit** so a single agentic task cannot spiral through unbounded re-checks; cap max tokens and tool-call depth per run ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).
- **Burn-rate anomaly alerting** on a cost dashboard that fires when daily spend diverges from plan — days in, not months in ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).
- **Quotas tied to cumulative token usage, not just request counts**, since per-request limits do not bound a long, expensive agentic run ([OWASP LLM10:2025](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).

## Takeaways

- On metered LLM or agent tooling, an uncapped budget is a question of *when* it runs away, not *if* — set a hard per-user and per-tool spend cap before rollout, not after the overrun.
- A per-request limit does not bound an agentic run; cap cumulative tokens, tool-call depth, and per-task spend, because each step resends the whole accumulated context.
- Alert on burn rate, not just on the final bill — if the first signal of an overspend is the budget being gone, the observability for cost is missing.
- Adoption incentives without a cost signal optimise for the runaway; pair any "use AI more" push with an enforced ceiling so the only feedback loop is not the one that amplifies spend.

---

## Sources

- **[Uber Caps Usage of AI Tools Like Claude Code to Manage Costs](https://www.bloomberg.com/news/articles/2026-06-02/uber-caps-usage-of-ai-tools-like-claude-code-to-cut-costs)** (Bloomberg) — the $1,500/month per-employee, per-tool cap, the dashboard tracking, and the agentic coding tools (Claude Code, Cursor) involved.
- **[Uber caps employee AI spending after blowing through budget in four months](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/)** (TechCrunch) — the four-month budget burn, the "use it as much as possible" push and usage leaderboards (reporting The Information), and the cap details.
- **[Uber Caps Usage of AI Tools Like Claude Code to Manage Costs](https://simonwillison.net/2026/Jun/3/uber-caps-usage/)** (Simon Willison) — corroborates the four-month budget burn and the 2025 projection that demand outran, with per-engineer cost analysis.
- **[LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** (OWASP Gen AI Security Project) — the named failure class and "denial of wallet" definition, plus the mitigations: token-based quotas, spend caps, monitoring, and graceful degradation.

## Read more

- **[Company spent $500 million on Claude in one month after forgetting usage limits](https://techstartups.com/2026/05/28/company-accidentally-spent-500-million-on-claude-ai-in-one-month-after-forgetting-usage-limits/)** (Tech Startups, relaying Axios) — the unverified, anecdotal extreme of the same uncapped-consumption pattern; treat the figure as order-of-magnitude, not a confirmed accounting line.

<!-- page-type: case-study:failure -->
