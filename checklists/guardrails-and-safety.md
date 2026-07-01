# Guardrails & safety — go-live checklist

> **In one sentence:** Each box is a layer an attacker would have to defeat — if you cannot tick it, you
> are trusting the model not to be fooled, which NIST says no one can guarantee.

Run this before sign-off on any agent that takes untrusted input, retrieves external content, or calls
tools — which is nearly all of them. A failed box is not a blocker by itself; it is a residual risk
someone has to *accept in writing*, knowing the blast-radius boxes are what decide how bad the others get.
For the why behind each theme, see the [Guardrails & safety overview](../docs/guardrails-and-safety/README.md).

---

## Trust boundary & posture

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Untrusted content, not instructions | Retrieved/tool/web content segregated from system instructions, never obeyed by default | [Prompt injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md); [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |
| ☐ | No model-level enforcement | No control relies on the model "ignoring injected instructions" — there is no foolproof model-level defense | [NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) |
| ☐ | Layered, ≥1 deterministic | Defenses layered with at least one code-enforced layer, not a single content filter | [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |
| ☐ | Guardrails fail closed | A tripped input/output/tool guard halts the action (block/refuse), not log-and-continue | [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |

## Input filtering

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Screen input | Injection/jailbreak patterns, oversized payloads, and off-topic/out-of-scope requests screened before the model | [Prompt injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md); [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |
| ☐ | Delimit untrusted content | Untrusted content delimited/channelled separately so the model knows which tokens are data | [Prompt injection defense](../docs/guardrails-and-safety/prompt-injection-defense.md); [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |

## Output filtering

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Output guardrail | Blocks profanity, self-disparagement, defamation, off-policy content before every customer-facing response is sent | [DPD chatbot](../docs/case-studies/dpd-chatbot.md) |
| ☐ | No binding commitments | Prices/contracts/"legally binding" terms come from a controlled system, not free-form generation | [Chevrolet dealership chatbot](../docs/case-studies/chevrolet-dealership-chatbot.md) |
| ☐ | Encode downstream output | Model output into SQL/shell/browser/HTML is encoded/escaped/parameterized — treated as untrusted input (LLM05) | [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/) |
| ☐ | Redact surfaced PII | PII the model surfaces is redacted before it reaches a user or a log | [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |

## Tool-argument validation

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Validate tool args | Every argument validated against a typed schema (types, ranges, enums, required fields); ill-typed/out-of-policy calls refused before execution | [Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md) |
| ☐ | Authorize downstream | Each action authorized in the downstream system with the user's own permissions (complete mediation), never by trusting the model's call | [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |

## Blast-radius containment

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Least-capability tools | Fewest tools, split read/write, minimum downstream permissions per tool | [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | New tools gated by default | New mutating tools default read-only/dry-run/approval; irreversible/money/delete actions require human approval so injection can't self-authorize | [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | Sandbox untrusted code | Untrusted code/shell runs in a disposable, isolated sandbox (stronger than a shared-kernel container) | [Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md) |
| ☐ | Allow-list egress | A fooled agent can only reach approved destinations; exfiltrating links/embedded resources are blocked | [EchoLeak](../docs/case-studies/echoleak-m365-copilot.md) |
| ☐ | Block SSRF ranges | URL-fetch tools resolve host to IP and block private/reserved ranges (incl. `169.254.169.254` metadata), and re-validate redirects | [MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) |

## Memory & supply chain

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Guard memory writes | Memory/RAG writes validated + quarantined, scoped per session/user, provenance-tagged — a poisoned write can't re-fire on a later/cross-user run (ASI06) | [Memory & tool supply chain](../docs/guardrails-and-safety/memory-and-tool-supply-chain.md); [OWASP Agentic 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| ☐ | Vet tool supply chain | Connected tools/MCP servers treated as untrusted: tool descriptions pinned + reviewed, first-party/vetted preferred (description poisoning is real) | [Memory & tool supply chain](../docs/guardrails-and-safety/memory-and-tool-supply-chain.md); [MCPTox](https://arxiv.org/abs/2508.14925) |

## Measurement & release gating

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Measure injection defense | Benchmarked with adaptive attacks; attack-success-rate result recorded | [AgentDojo](https://arxiv.org/abs/2406.13352) |
| ☐ | Red-team gate on change | Adversarial/red-team test required before any prompt/model/config change ships — not an after-the-fact check (DPD rode in on a routine update) | [DPD chatbot](../docs/case-studies/dpd-chatbot.md) |

---

## Sources

- **[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** (OWASP GenAI Security Project) — backs the untrusted-content, segregation, and input-filtering rows.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — backs the complete-mediation, least-capability, and human-approval rows.
- **[OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)** (OWASP GenAI Security Project) — backs the improper-output-handling (LLM05) row.
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — backs the "no foolproof model-level defense" posture row.
- **[AgentDojo](https://arxiv.org/abs/2406.13352)** (ETH Zurich) — backs the measure-against-a-benchmark row.
- **[MCPTox](https://arxiv.org/abs/2508.14925)** (arXiv) — backs the tool/MCP supply-chain row.
- **[OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — backs the memory/context-poisoning row (ASI06).
- **[MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)** (Anthropic / MCP) — backs the SSRF / block-private-ranges row on URL-fetching tools.

<!-- page-type: checklist -->
