# Guardrails & safety — go-live checklist

> **In one sentence:** Each box is a layer an attacker would have to defeat — if you cannot tick it, you
> are trusting the model not to be fooled, which NIST says no one can guarantee.

Run this before sign-off on any agent that takes untrusted input, retrieves external content, or calls
tools — which is nearly all of them. A failed box is not a blocker by itself; it is a residual risk
someone has to *accept in writing*, knowing the blast-radius boxes are what decide how bad the others get.
For the why behind each theme, see the [Guardrails & safety overview](../docs/guardrails-and-safety/README.md).

---

## Trust boundary & posture

- [ ] All retrieved, tool, and web content is treated as **untrusted data, not instructions** — segregated from system instructions, never obeyed by default. ([OWASP LLM01](../docs/guardrails-and-safety/prompt-injection-defense.md))
- [ ] No control depends on the model "ignoring injected instructions" as its enforcement — there is **no foolproof model-level defense**. ([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final))
- [ ] Defenses are **layered**, with at least one **deterministic** (code-enforced) layer, not a single content filter. ([Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md))
- [ ] Guardrails **fail closed**: a tripped input, output, or tool guard **halts the action** (block/refuse), not log-and-continue — a guard that logs but doesn't stop is a silent gap. ([Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md))

## Input filtering

- [ ] Input is screened for injection/jailbreak patterns, oversized payloads, and off-topic/out-of-scope requests before it reaches the model.
- [ ] Untrusted content is delimited or channelled separately so the model knows which tokens are data.

## Output filtering

- [ ] An **output guardrail** sits in front of every customer-facing response — blocks profanity, self-disparagement, defamation, and off-policy content before it is sent. ([DPD chatbot](../docs/case-studies/dpd-chatbot.md))
- [ ] The agent is bound **not** to make binding commitments (prices, contracts, "legally binding" terms); those come from a controlled system, not free-form generation. ([Chevrolet dealership chatbot](../docs/case-studies/chevrolet-dealership-chatbot.md))
- [ ] Model output flowing into a downstream system (SQL, shell, browser, HTML) is **encoded/escaped/parameterized** — treated as untrusted input (OWASP LLM05 Improper Output Handling). ([OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/))
- [ ] PII the model surfaces is redacted before it reaches a user or a log.

## Tool-argument validation

- [ ] Every tool argument is **validated against a typed schema** (types, ranges, enums, required fields) and ill-typed/out-of-policy calls are refused **before execution**. ([Input/output filtering](../docs/guardrails-and-safety/input-output-filtering.md))
- [ ] Each action is **authorized in the downstream system** with the user's own permissions (complete mediation) — never by trusting the model's decision to call the tool. ([OWASP LLM06](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md))

## Blast-radius containment

- [ ] The tool surface is **least-capability**: fewest tools, split read/write, minimum downstream permissions per tool. ([OWASP LLM06](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md))
- [ ] New mutating tools default to **read-only / dry-run / approval-required**; high-impact (irreversible, money, deletes) actions require **human approval** so an injection can't self-authorize.
- [ ] Untrusted code/shell execution runs in a **disposable, isolated sandbox** (stronger than a shared-kernel container for untrusted code). ([Sandboxing & blast radius](../docs/guardrails-and-safety/sandboxing-and-blast-radius.md))
- [ ] **Egress is allow-listed** — a fooled agent can only reach approved destinations; links/embedded resources that could exfiltrate data are blocked. ([EchoLeak](../docs/case-studies/echoleak-m365-copilot.md))
- [ ] Any URL-fetching tool **blocks private/reserved IP ranges** (incl. the `169.254.169.254` cloud-metadata endpoint) by resolving the host to an IP and checking it, and re-validates redirects — so it can't be turned into an **SSRF** primitive. ([MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices))

## Memory & supply chain

- [ ] Writes to long-term **memory / RAG** are validated and quarantined (untrusted-path writes don't silently become durable memory), memory is **scoped per session/user**, and stored context carries a **provenance tag** — so a poisoned write can't re-fire on a later or cross-user run (OWASP ASI06 Memory & Context Poisoning). ([Memory & tool supply chain](../docs/guardrails-and-safety/memory-and-tool-supply-chain.md))
- [ ] Connected tools / MCP servers are treated as **untrusted supply chain** — tool descriptions are pinned and reviewed, first-party/vetted servers preferred (tool-description poisoning is a real attack). ([MCPTox](https://arxiv.org/abs/2508.14925))

## Measurement & release gating

- [ ] Injection defense is **measured** against a recognized benchmark with **adaptive** attacks, and the attack-success-rate result is recorded. ([AgentDojo](https://arxiv.org/abs/2406.13352))
- [ ] An **adversarial / red-team test is a required gate** before any prompt, model, or config change ships — not an after-the-fact check (DPD's regression rode in on a routine update). ([DPD chatbot](../docs/case-studies/dpd-chatbot.md))

---

## Sources

- **[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** (OWASP GenAI Security Project) — backs the untrusted-content, segregation, and input-filtering lines.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — backs the complete-mediation, least-capability, and human-approval lines.
- **[OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)** (OWASP GenAI Security Project) — backs the improper-output-handling (LLM05) line.
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — backs the "no foolproof model-level defense" posture line.
- **[AgentDojo](https://arxiv.org/abs/2406.13352)** (ETH Zurich) — backs the measure-against-a-benchmark line.
- **[MCPTox](https://arxiv.org/abs/2508.14925)** (arXiv) — backs the tool/MCP supply-chain line.
- **[OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — backs the memory/context-poisoning line (ASI06).
- **[MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)** (Anthropic / MCP) — backs the SSRF / block-private-ranges line on URL-fetching tools.

<!-- page-type: checklist -->
