# Goldman Sachs × Cognition Devin — an autonomous coder boxed into a supervised pilot

> **In one sentence:** Inside a regulated bank, Devin only became useful once it was wrapped in mandatory human oversight, low-blast-radius scope, and existing review/CI — the infrastructure carried it, not raw autonomy.

Goldman Sachs put Cognition's Devin into production engineering work — the same agent behind a debunked 2024 launch demo — and got real value from it. It works here for one reason: it is supervised, not unattended. Treat the figures below as ballpark operator/vendor numbers, and the deployment as an early production pilot, **not** a finished rollout.

---

## Agent Goal

Goldman Sachs deployed Devin as an autonomous software engineer to take on lower-risk maintenance — legacy-code migration, refactoring, debugging — working alongside its human engineers in a "hybrid workforce." The bank wanted the agent to absorb the repetitive, well-scoped work and lift engineering throughput, citing a rough 3–4× productivity target on those tasks (operator figure, ballpark) while people kept supervising every output ([Fortune](https://fortune.com/2025/07/14/goldman-sachs-ai-powered-software-engineer-devin-new-employee-increase-productivity-fears-of-job-replacement/), [CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)).

## Context

Devin runs as an autonomous coding agent inside Goldman Sachs, a regulated bank, scoped to lower-risk maintenance work rather than greenfield or high-stakes systems. CIO Marco Argenti described **hundreds of Devin instances** in use, with possible scaling to thousands, citing roughly **3–4× productivity** versus prior tools — vendor/operator figures, treated as ballpark ([CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)). The autonomy is real but bounded: engineers stay in the loop on every task.

## What happened

From 2025, Goldman deployed Devin into a hybrid human-plus-agent engineering model on maintenance tasks — migration, refactoring, debugging ([Fortune](https://fortune.com/2025/07/14/goldman-sachs-ai-powered-software-engineer-devin-new-employee-increase-productivity-fears-of-job-replacement/)). Cognition reports the same agent running in engineering teams at other firms including Santander and Nubank ([Cognition](https://cognition.ai/blog/devin-annual-performance-review-2025)). The status is consistently described as an early production / supervised pilot — explicitly not a completed enterprise-wide rollout.

## What worked

- **Mandatory human oversight.** Engineers scope each task into prompts and verify every output; the agent does not ship work unreviewed.
- **Low-blast-radius scope.** Work is confined to maintenance — migration, refactoring, debugging — not high-stakes or irreversible changes.
- **Existing controls absorb it.** Devin's output runs through the bank's existing code-review and CI pipeline, so the agent inherits the same gates as a human contributor.

## Takeaways

- Box an autonomous agent into a narrow, low-blast-radius scope before trusting it in production — bounded tasks fail cheaply.
- Require a human to scope the task and verify each output; treat unattended autonomy as the exception, not the default.
- Route agent output through the review/CI controls you already enforce on humans, rather than building a separate, weaker path for the agent.
- The same product can be overhyped vapor in a demo and genuinely useful in production — the difference is the supervision wrapper, not the model.

---

## Sources

- **[Goldman Sachs is piloting Devin, the AI software engineer](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)** (CNBC) — CIO Marco Argenti on hundreds of Devin instances and ~3–4× productivity (operator figures, ballpark).
- **[Goldman Sachs is testing an AI software engineer named Devin](https://fortune.com/2025/07/14/goldman-sachs-ai-powered-software-engineer-devin-new-employee-increase-productivity-fears-of-job-replacement/)** (Fortune) — the hybrid human-plus-agent model and the maintenance scope.
- **[Devin Annual Performance Review 2025](https://cognition.ai/blog/devin-annual-performance-review-2025)** (Cognition — vendor) — the same agent running in engineering teams at firms including Santander and Nubank.

<!-- page-type: case-study:success -->
