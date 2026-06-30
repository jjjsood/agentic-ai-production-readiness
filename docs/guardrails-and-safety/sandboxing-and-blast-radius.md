# Sandboxing & blast radius — design for the guardrail that gets bypassed

> **In one sentence:** Every other guardrail can fail, so the load-bearing safety question is not "can the
> agent be tricked?" (assume yes) but "when it is, how much can it touch?" — and the answer is set by
> least-capability tool surface and execution isolation, not by the model's good behaviour.

> Part of **[Guardrails & safety overview](README.md)**

Prompt-injection defenses reduce attacks; filters catch some; neither is foolproof, on the explicit word
of NIST ([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)). So the final layer
assumes the earlier ones lost: it bounds what a fooled or hallucinating agent can *do*. This is
containment — least-capability tool surface, execution isolation, and egress control — and it is the
layer that decides whether a successful injection is an embarrassment or a deleted production database.
This page covers excessive agency as the blast-radius root cause, shrinking the tool surface,
sandboxing untrusted execution, and the egress controls that turn a leak attempt into nothing.

---

## Excessive agency is the blast-radius root cause

OWASP names the vulnerability directly: **Excessive Agency** is damage enabled by an agent having
excessive *functionality, permissions, or autonomy* — "the vulnerability that enables damaging actions…
regardless of what is causing the LLM to malfunction"
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). The phrase *regardless of
what is causing* is the whole point of this page: blast radius is independent of the trigger. A
hallucination, an injection, a bad retrieval, a buggy prompt — each produces the same harm if the agent
holds the capability to cause it. So the control is not "make the model not malfunction" (impossible to
guarantee) but "ensure malfunction has nowhere damaging to go."

The Replit incident shows the shape: an agent executed destructive commands and wiped a production
database *during a stated code freeze* — the harm was sized by what the agent could reach, not by a model
error rate ([Replit database deletion](../case-studies/replit-database-deletion.md)). EchoLeak shows the
exfiltration version: once injected, the damage was bounded by what the assistant's context could *reach
and send* ([EchoLeak](../case-studies/echoleak-m365-copilot.md)). In both, the fix lives in the
capability surface, not the prompt.

## Shrink the tool surface to least capability

The cheapest, highest-leverage containment is having fewer, narrower, lower-privilege tools. OWASP's
official mitigations for excessive agency are a direct checklist
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)):

- **Minimize extensions** — fewer tools is less surface; don't add a tool "just in case."
- **Minimize extension functionality** — a tool that can read should not also delete; split capabilities.
- **Minimize permissions** — each tool gets the strict minimum downstream access the task needs.
- **Execute in user context** — apply the *user's own* authorization, not a broad service account, so the
  agent can never exceed what the requesting user could do.
- **Require human approval** of high-impact actions, so an injected or hallucinated instruction cannot
  self-authorize a destructive one.
- **Complete mediation** — authorize each action in the downstream system, never by trusting the model's
  decision to call the tool.

A practical sequencing rule pairs with this: **read-only first, mutation later**; default every new
mutating tool to approval-required and a dry-run diff; graduate to autonomous only on evidence. Rating each
tool by reversibility, write access, and financial impact, then letting the rating drive the gate, is the
mechanism OpenAI recommends ([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
This is where guardrails meet identity and access: scoped, short-lived, least-privilege credentials per
agent are what make "minimize permissions" real rather than aspirational.

## Sandbox untrusted execution

When an agent runs generated code or shell commands, that code is **untrusted** — treat it like
user-supplied input, because an injection can put attacker code into it. Sandboxing each run "limits the
blast radius of malicious or unintended code"
([NVIDIA — code execution risks](https://developer.nvidia.com/blog/how-code-execution-drives-key-risks-in-agentic-ai-systems/)).
The isolation strength has to match the threat, and the bar has risen: a shared-kernel container (plain
Docker/runc) leaves the host kernel directly reachable from the workload, which is the gap stronger
sandboxes exist to close. **gVisor** intercepts a workload's syscalls in a userspace application kernel
(the Sentry) whose "primary design goal is to minimize the System API attack vector," so untrusted code
never talks straight to the host kernel ([gVisor — security model](https://gvisor.dev/docs/architecture_guide/security/)).
**Kata Containers** and **Firecracker microVMs** push further, wrapping each workload in a lightweight VM
for hardware-backed isolation. A practitioner write-up frames the same spectrum as the early-2026 working
baseline for untrusted agent code — Docker/runc no longer sufficient, gVisor/Kata next, Firecracker/microVMs
strictest ([AI agent sandboxing guide](https://manveerc.substack.com/p/ai-agent-sandboxing-guide), a
practitioner source; treat the tier names as illustrative of the spectrum, not a procurement list). The
disposability
matters as much as the strength: a per-run, throwaway sandbox means a compromised run leaves nothing behind
for the next one.

## Contain egress — the leak you can actually stop

Isolation contains *what the agent can do to a host*; **egress control** contains *what it can send out* —
and for data-exfiltration injection, egress is the primary defense, not the model's refusal. EchoLeak's
chained bypass was, end to end, an egress failure: the controls meant to stop data leaving (link
redaction, content-security-policy) each had a gap that chained into a working exfiltration path
([EchoLeak](../case-studies/echoleak-m365-copilot.md)). The controls that work are deterministic and
network-level: **allow-list outbound destinations** so a tricked agent can only talk to approved
endpoints, filter outbound network access from the sandbox, and redact or block links and embedded resource
loads that could carry data out ([AI agent sandboxing guide](https://manveerc.substack.com/p/ai-agent-sandboxing-guide)).
The design test is simple: assume the agent has already been injected and *wants* to exfiltrate — can it
reach anywhere it shouldn't? If yes, the egress boundary, not the prompt, is the work to do.

The mirror risk is a tool that can be induced to *reach in*. A `fetch_url`-style tool an agent can point
anywhere is a **server-side request forgery (SSRF)** primitive: an injected instruction tells it to fetch the
cloud-metadata endpoint `http://169.254.169.254/`, and the server returns the instance's IAM credentials as
plain text the model then leaks. The MCP security guidance is concrete — block requests to private and
reserved ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, loopback `127.0.0.0/8`, and link-local
`169.254.0.0/16`, the metadata range), and do it by **resolving the hostname to an IP and checking that**
rather than hand-rolling string matches that octal/hex/IPv4-mapped-IPv6 encodings slip past, re-validating
every redirect hop because a safe-looking domain can rebind to an internal address between check and use
([MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices);
[OWASP A10:2021 SSRF](https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)). It is
the same containment principle as egress, pointed the other way: the agent's outbound reach is a boundary to
enforce in code, not a behaviour to trust.

## Defense-in-depth: assume any single layer fails

The thread through every section is one principle: **any single layer can fail, so containment must hold
when it does.** Google DeepMind reached the same conclusion defending a frontier model — model robustness
is "a vital layer within a comprehensive defense-in-depth strategy," paired with runtime monitoring, input
filtering, strict permissions, and well-scoped tool access
([Google DeepMind — Defending Gemini](https://arxiv.org/abs/2505.14534)). Sandboxing and capability
constraints are complementary, not redundant: isolation contains the damage *and* least-capability limits
what's possible even inside the sandbox, "since any single layer can fail"
([AI agent sandboxing guide](https://manveerc.substack.com/p/ai-agent-sandboxing-guide)). The blast-radius
question — *when the guardrails are bypassed, how much can it touch?* — is the one to answer at sign-off,
because a "no" here is what survives the day every other control didn't.

---

## Sources

- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — the blast-radius root cause and the official minimize-extensions/functionality/permissions, execute-in-user-context, human-approval, and complete-mediation mitigations.
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — rate tools by reversibility/write-access/financial-impact and gate high-risk actions; read-only-first sequencing.
- **[How Code Execution Drives Key Risks in Agentic AI Systems](https://developer.nvidia.com/blog/how-code-execution-drives-key-risks-in-agentic-ai-systems/)** (NVIDIA) — LLM-generated code is untrusted; sandboxing limits the blast radius.
- **[gVisor — security model](https://gvisor.dev/docs/architecture_guide/security/)** (gVisor / Google) — primary corroborator for the isolation-tier claim: a userspace application kernel minimizes the host System API attack vector that a shared-kernel container leaves exposed.
- **[MCP — Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)** (Anthropic / MCP) — the SSRF mitigation behind the inbound-reach control: block private/reserved ranges incl. the `169.254.169.254` cloud-metadata endpoint, resolve-then-check rather than parse strings, re-validate redirects against DNS rebinding; named as a neutral example.
- **[A10:2021 — Server-Side Request Forgery (SSRF)](https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)** (OWASP) — the canonical SSRF risk an agent's URL-fetching tool exposes when it can be pointed at internal/metadata endpoints.
- **[Lessons from Defending Gemini Against Indirect Prompt Injections](https://arxiv.org/abs/2505.14534)** (Google DeepMind) — model robustness is one layer in defense-in-depth alongside strict permissions and well-scoped tool access.
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — there is no foolproof defense, so the last layer must assume the earlier ones failed.
- **[CVE-2025-32711 (EchoLeak)](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711)** (Microsoft MSRC) — the exfiltration case where egress/trust-boundary controls were the load-bearing defense.

## Read more

- **[How to Sandbox AI Agents in 2026](https://manveerc.substack.com/p/ai-agent-sandboxing-guide)** (manveerc, practitioner write-up) — the gVisor/Kata/Firecracker isolation spectrum and egress-filtering / defense-in-depth layering; a practitioner source, useful for the concrete isolation tiers but not a standard.

<!-- page-type: standard -->
