<h1 align="center">Agentic AI Production Readiness</h1>

<p align="center">
  A curated, source-backed field guide for taking AI agents from a working demo to a production
  process you can <em>operate, defend, and pass an audit on</em>.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: CC BY 4.0" src="https://img.shields.io/badge/license-CC%20BY%204.0-blue"></a>
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
</p>

<p align="center">
  <b>The demo was the easy part.</b> Running the thing in production — without it overspending,
  leaking, or failing an audit — is the part nobody hands you a playbook for. This is that playbook.
</p>


## Contents

- [Why this exists](#why-this-exists)
- [What this is — and isn't](#what-this-is--and-isnt)
- [How to use it](#how-to-use-it)
- [Structure](#structure)
  - [When to use agents](docs/when-to-use-agents/README.md)
  - [Limits & budgets](docs/limits-and-budgets/README.md)
  - [Guardrails & safety](docs/guardrails-and-safety/README.md)
  - [Observability & evals](docs/observability-and-evals/README.md)
  - [Human control & rollback](docs/human-control-and-rollback/README.md)
  - [Identity & access](docs/identity-and-access/README.md)
  - [Compliance & governance](docs/compliance-and-governance/README.md)
  - [Case studies](docs/case-studies/README.md)
  - [Checklists](checklists/)
  - [Risk register](risk-register/)
- [The compliance spine](#the-compliance-spine)
- [Contributing](#contributing)
- [How this was written](#how-this-was-written)
- [License](#license)


## Why this exists

An agent works in the demo, ships — then breaks in ways that have nothing to do with model quality: it
loops and burns a month's budget overnight, calls a tool it should never have had, or fails with no
trace, no stop switch, no way back. Then someone asks *prove you were in control*, and the team that
shipped it can't.

Across documented agent failures (2023–2026), the pattern repeats: **the failures that can be
attributed to a cause are overwhelmingly infrastructure gaps — missing limits, guardrails,
observability, identity boundaries, rollback paths — not model quality.** Roughly **88% of attributable
failures**, by this reading; treat it as order-of-magnitude, not a constant. OWASP ranks the top agent
risks as **[excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** and
**[unbounded consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)** — not
accuracy. Anthropic frames agent reliability as a
**[context-engineering problem](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**,
not a smarter-model problem. Reported AI incidents are climbing fast — a ballpark **233 in 2024, up
~56% year-on-year** ([Stanford HAI AI Index 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report/responsible-ai)).

<p align="center">
  <img src="figures/schematics/01-failure-attribution.svg" alt="Across documented agent failures (2023–2026), roughly 88% are attributable to infrastructure gaps, not model quality." width="460">
</p>

**You can already build the agent. The gap is hardening it for production — and producing the evidence
that you were in control.** This repo collects what actually breaks, organised around the
infrastructure that's missing when it does.

> Every number here is attached to a source, primary sources beat vendor blogs, and figures are
> ballpark — never constants. A claim that loses its source loses its place.

## What this is — and isn't

This is a **curated knowledge collection** — mental models, risks, checklists, and decision aids
organised around *what fails when it's missing*: the production infrastructure. A thinking aid for the
questions before go-live, not a framework, library, or turnkey system to install, a "build an agent in
framework X" tutorial, or a one-correct-answer oracle. It's mid-build, on purpose, and living — meant
to be argued with.

**Written for:** someone **accountable** for an agentic system that has to run reliably, within
acceptable risk — they can already build an agent; the gap is hardening it for production and
surviving audit. In practice:

- the senior/staff engineer embedding an agent feature into a real product
- the AI/ML engineer taking a working PoC into an unattended workflow
- the tech lead or architect signing off on go-live
- the product/platform/process owner wiring agents into processes that touch money or records
- the business owner judging whether agentic vs. deterministic is the sound call
- the consultant who needs defensible, evidence-based go/no-go criteria

**Probably not for:** a weekend-PoC tinkerer with no intent to run it for real, an intern building a
throwaway demo, a developer trying out tools for fun, a pure benchmark researcher, or a team on a
mature agent platform looking for an installable product — the hardening overhead here will outweigh
the value for these readers.

## How to use it

**Not** a linear manual — read the parts that match your role, your project phase, or the question in
front of you. The prose helps you ask better questions before you ship:

- What do I need to think about *before* putting an agent into production?
- Which risks do I have to assess — and which assumptions must I validate?
- Where does my chosen approach hit its limits?
- Which governance and compliance questions are still open?
- Where do I want **deterministic logic** instead of agentic flexibility?
- Which checks belong in front of a deployment, and which failure modes are realistic?

Checklists, risk templates, and scoring aids translate those questions into concrete work — a working
surface, not a verdict. Treat the whole repo as **alive**: models, tools, and regulation move fast, so
it's meant to be argued with — better approaches, new risks, counter-examples all welcome.
## Structure

The repository is **seven pillars** plus **cross-cutting artifacts**. The first pillar decides *whether
to use an agent at all*; the other six are the production infrastructure that choice obligates. Each
pillar is a chapter — an **overview hub** plus focused **deep-dive pages**, one per sub-topic — every
claim tied to a primary source, each page closing with its own **Sources** list.

### The seven pillars

| Pillar | What it covers |
|--------|----------------|
| **[When to use agents](docs/when-to-use-agents/README.md)** | The decision before the other six: agent vs. workflow vs. deterministic code — pick the least-agentic option that does the job. Deep-dives: the workflow/agent line, the signals that earn an agent, the cost of agency, multi- vs. single-agent, and when classical code wins outright. Read first. |
| **[Limits & budgets](docs/limits-and-budgets/README.md)** | The off-switch the cloud bill depends on: token/cost ceilings, rate/loop/timeout caps, and a spend-rate circuit breaker. Deep-dives: cost & token budgets, rate/loop/timeout caps, denial of wallet, and caching & cost control. Rule: a limit only counts if it's enforced in code outside the model. |
| **[Guardrails & safety](docs/guardrails-and-safety/README.md)** | Defense-in-depth for a model that can be fooled — the pillar an attacker tests on day one. The model can't reliably tell data from instructions, so safety has to come from layers around it. Deep-dives: prompt-injection defense, input/output/tool-argument filtering, sandboxing & blast radius, and the memory/tool-supply-chain attacks — plus how to *measure* injection defense. |
| **[Observability & evals](docs/observability-and-evals/README.md)** | If you can't trace it or measure it, you can't operate it — traces and token accounting for one run, regression suites and online evals for the whole population. Deep-dives: OpenTelemetry GenAI trace spans, offline eval suites, eval-in-production and the pass@1-vs-reliable gap, and FinOps cost attribution. |
| **[Human control & rollback](docs/human-control-and-rollback/README.md)** | The off-switch, the undo, and the gate that holds — decides how bad an incident gets after it starts. Three questions in order: approve before, stop while, roll back after. Deep-dives: HITL approval gates, staged rollout (shadow → canary → GA), kill switch & four-layer versioned rollback, and incident-response runbooks. |
| **[Identity & access](docs/identity-and-access/README.md)** | An agent is a new non-human identity holding real credentials — it should get only the keys the task needs. Deep-dives: per-agent identity (not a borrowed human session), the tool-permission matrix, scoped/short-lived secrets, and per-action audit logging. Where the other pillars get their teeth. |
| **[Compliance & governance](docs/compliance-and-governance/README.md)** | Proving you were in control — the pillar a regulator, auditor, or court actually tests. The other six are controls; this is the evidence they existed and worked. Deep-dives: the EU AI Act tier by tier, NIST AI RMF as a Govern/Map/Measure/Manage loop, and the artifact-by-artifact audit-evidence kit. |

### Cross-cutting artifacts

| Artifact | What it is |
|----------|------------|
| **[Case studies](docs/case-studies/README.md)** | Named real agents — wins, staged demos, shipped failures — each read back to the infrastructure that decided the outcome (Air Canada, Chevrolet, DPD, NYC MyCity, Replit, EchoLeak, Uber, and more). Across the failures, root cause is almost always infrastructure, not model quality. |
| **[Checklists](checklists/)** | One per pillar: terse, checkable go-live lines — a limit you can point at, a gate that can say no, a trace you actually keep. A working surface, not a verdict. |
| **[Risk register](risk-register/)** | One per pillar: failure modes scored by likelihood and impact, paired with the control that addresses each. Tells you what to fix first. |



## Contributing

Contributions welcome — a new source, a sharpened checklist line, a new incident pattern, or a
counter-argument. See [CONTRIBUTING.md](CONTRIBUTING.md) for the content rules, the source/citation
format, and the one-topic-per-PR convention.

There is a template per page type in [templates/](templates/): the standard
[page-template.md](templates/page-template.md) (deep-dives), plus
[pillar-overview-template.md](templates/pillar-overview-template.md),
[checklist-template.md](templates/checklist-template.md),
[risk-register-template.md](templates/risk-register-template.md), and
[case-study-template.md](templates/case-study-template.md).


## How this was written

This repository is a collaboration between AI and people: AI drafted breadth and structure, human
judgment decided what's true, relevant, and worth saying — every claim reviewed before it shipped. The
repository argues agents belong in production only with a human accountable in the loop; it was built
the same way.


## License

See [LICENSE](LICENSE) — Creative Commons Attribution 4.0.
