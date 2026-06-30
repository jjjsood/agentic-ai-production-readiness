# Guardrails & safety — risk register

> **In one sentence:** These are the ways an adversary turns a working agent against its operator — each
> scored so you can sequence the hardening, and each tied to the layer that contains it, because the model
> itself is not a control.

The risks below share a root: untrusted input crosses a boundary the model cannot police, and the harm is
sized by how little stands behind it. Read the score as a priority sort, not a probability. For the
reasoning behind each control, see the
[Guardrails & safety overview](../docs/guardrails-and-safety/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, legal, safety).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **Indirect prompt injection** — malicious instructions in retrieved/ingested content (email, doc, web, ticket) hijack the agent's actions or exfiltrate data, with no attacker access to the user | 3 | 3 | 9 | Defense-in-depth: segregate untrusted content + detection guardrails + least-privilege/HITL + capability/control-flow defense — [Prompt-injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md), [EchoLeak](../docs/case-studies/echoleak-m365-copilot.md) |
| 2 | **Excessive agency / oversized blast radius** — a fooled or hallucinating agent reaches money, deletes, or prod writes it never needed | 3 | 3 | 9 | Least-capability tool surface, minimize permissions, HITL on high-impact actions, complete mediation — [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md), [Replit](../docs/case-studies/replit-database-deletion.md) |
| 3 | **Unfiltered output** — the agent ships profanity, defamation, or an off-policy/binding statement that speaks for the brand | 3 | 2 | 6 | Output guardrail on every customer-facing response; no binding commitments from free-form generation — [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md), [DPD](../docs/case-studies/dpd-chatbot.md), [Chevrolet](../docs/case-studies/chevrolet-dealership-chatbot.md) |
| 4 | **Improper output handling** — model output flows unvalidated into SQL/shell/browser/HTML and executes (OWASP LLM05) | 2 | 3 | 6 | Treat output as untrusted to the consumer: encode/escape/parameterize; never eval generated code on a trusted host — [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |
| 5 | **Unvalidated tool arguments** — a malformed or unauthorized tool call corrupts a downstream system or self-authorizes an action | 2 | 3 | 6 | Typed schema validation + complete mediation (authorize downstream with the user's permissions) before any side effect — [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |
| 6 | **Direct prompt injection / jailbreak** — a user rewrites the bot's policy via crafted input | 3 | 2 | 6 | Segregate system instructions from user text; refuse policy/commitment overrides — [Prompt-injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md), [Chevrolet](../docs/case-studies/chevrolet-dealership-chatbot.md) |
| 7 | **Tool / MCP supply-chain poisoning** — a poisoned tool *description* injects instructions with no execution, and agents rarely refuse | 2 | 3 | 6 | Treat connected tools as untrusted supply chain: pin/review descriptions, prefer vetted servers, authorize independently — [Memory & tool supply chain](../docs/guardrails-and-safety/memory-and-tool-supply-chain.md) |
| 8 | **Memory / context poisoning** — a poisoned write to long-term memory/RAG re-activates on a later, unrelated run, possibly in another user's session (OWASP ASI06) | 2 | 3 | 6 | Validate/quarantine memory writes, scope memory per session/user, tag provenance on stored context — [Memory & tool supply chain](../docs/guardrails-and-safety/memory-and-tool-supply-chain.md) |
| 9 | **Single-layer guardrail bypassed** — a content filter is treated as the defense and fails with no backstop | 2 | 3 | 6 | Layered defenses + contained blast radius so one bypass isn't catastrophic — [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md), [EchoLeak](../docs/case-studies/echoleak-m365-copilot.md) |
| 10 | **Unsandboxed untrusted code execution** — injected/hallucinated code runs with host access | 2 | 3 | 6 | Disposable, isolated sandbox (stronger than shared-kernel container) + egress allow-list — [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md) |
| 11 | **Untested defense regresses on change** — a prompt/model/config update silently breaks a guardrail; scored on the silent gap itself, not the row-3 output failures it can enable | 2 | 2 | 4 | Adversarial red-team gate + benchmark measurement on every change — [Prompt-injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md), [DPD](../docs/case-studies/dpd-chatbot.md) |
| 12 | **SSRF via a URL-fetching tool** — an injection points a `fetch_url`-style tool at the `169.254.169.254` cloud-metadata endpoint or an internal service, exfiltrating IAM credentials | 2 | 3 | 6 | Block private/reserved IP ranges by resolving host→IP (not string matching), re-validate redirects, prefer an egress proxy — [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md) |

---

## Sources

- **[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** (OWASP GenAI Security Project) — backs the direct/indirect injection risks (1, 6) and their mitigations.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — backs the blast-radius, complete-mediation, and tool-argument risks (2, 5).
- **[OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)** (OWASP GenAI Security Project) — backs improper output handling (LLM05), risk 4.
- **[MCPTox](https://arxiv.org/abs/2508.14925)** (arXiv) — backs the tool-description-poisoning supply-chain risk (7): 72.8% attack success, <3% refusal across real MCP servers (single study — see the deep-dive's hedge).
- **[OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — backs the memory/context-poisoning risk (8), ASI06.
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — backs the no-foolproof-defense premise behind layered defense and risk 8.
- **[CVE-2025-32711 (EchoLeak)](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711)** (Microsoft MSRC) — the chained-bypass exfiltration behind risks 1 and 8.
- **[MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)** (Anthropic / MCP) — the SSRF attack and block-private-ranges mitigation behind risk 12.

<!-- page-type: risk-register -->
