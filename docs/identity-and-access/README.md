# Identity & access — the agent only gets the keys the task needs

> **In one sentence:** An agent is a new non-human identity holding real credentials and real blast
> radius, so a gap here — a borrowed human session, an unscoped token, a secret in the prompt — turns a
> single bad output into real-world damage, which is why identity is an *attributable infrastructure
> failure*, not a model-quality one.

An agent that can act in the world holds keys: API tokens, database connections, OAuth sessions, service
accounts. Identity & access is the infrastructure that decides *whose* keys those are, *how much* each one
opens, and *for how long* — and it is owned by whoever signs off the agent's permissions, not by the model
vendor. The reason this pillar gets its own chapter is that the security community's single highest-ranked
agent risk is here: OWASP ranks **excessive agency** — too much permission, functionality, or autonomy —
as a top LLM risk, and its 2026 agentic list promotes **identity & privilege abuse** to a named entry of
its own ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/);
[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
This page is meant to be read on its own: by the end you should understand why over-permissioning is where
agents do their worst damage, why an agent needs an identity distinct from any human's, what the
tool-permission matrix is and why it is the concrete artifact this pillar produces, and why credentials
should be scoped, short-lived, and never live in a prompt. The [deep-dives](#going-deeper) then take each
piece further.

---

## Why this is the pillar that gets tested

The failures that land hardest are not the ones where the model said something wrong — they are the ones
where the model *did* something it should never have had the access to do. Two documented incidents in this
repository are exactly that. In the **[Replit database deletion](../case-studies/replit-database-deletion.md)**, a
coding agent held write access to a live production database and, during an explicit freeze, ran destructive
commands that wiped ~1,200+ records — the root cause was access the agent should never have held, not a
reasoning slip. In **[EchoLeak](../case-studies/echoleak-m365-copilot.md)** (CVE-2025-32711), a single
crafted email turned Microsoft 365 Copilot's broad retrieval reach into a zero-click exfiltration channel —
the blast radius was set by *what the assistant's identity could reach and send*, and a narrower reach would
have meant a smaller leak.

That is the pattern OWASP names. Excessive agency's damage "is possible whenever an LLM-based system is
granted a degree of agency" beyond what the task needs, and **excessive permissions** is one of its three
named root causes — an agent acting with more downstream access than the task requires is what converts a
hallucinated or injected output into a real action
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). The agentic threat list
sharpens it: in **ASI03 Identity & Privilege Abuse**, the agent "becomes an aggregation point for non-human
identities," acting "with the full authority of every key, token, and service account assigned to it"
([OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
Get identity wrong and every other guardrail is defending a system that was handed too many keys to begin
with.

## An agent is a non-human identity, not a person on a service account

The first design decision is *who the agent is*. The wrong answers are the easy ones: let the agent borrow
a human's session, or share one service account across every agent. Both break attribution and inflate
blast radius — an agent on a support rep's full OAuth session can refund invoices, delete tickets, and
modify settings when it only needed read access to one record. The right answer is a **distinct identity per
agent**, so its actions are attributable to it and its permissions can be scoped to it. Microsoft's
governance guidance makes this concrete: *"Require each agent to operate under a distinct agent identity"*
and maintain a single registry of every agent, its owner, purpose, and access scope, because *"you can't
govern agents you don't know exist"*
([Microsoft — Govern and secure AI agents](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization),
vendor guidance, neutral example). The hard part is delegation: when an agent acts *for* a user, it must
carry that user's authorization, not its own superset — getting this wrong is the **confused-deputy**
problem, where a privileged agent is tricked into using its authority on a less-privileged caller's behalf.

## The tool-permission matrix is the artifact this pillar ships

Identity becomes operational at the tool boundary. The concrete artifact this pillar produces is a
**tool-permission matrix**: each tool the agent can call, mapped to the *single credential it runs under*,
the *scope that credential carries*, the *approval gate* (if any) in front of it, and the *log* that proves
the boundary held. It is the answer to "prove the agent could only do what it was allowed to do." OWASP's
mitigations for excessive agency read like a spec for that matrix — *minimize extensions*, *minimize
permissions*, *execute in the user's context*, *require human approval of high-impact actions*, and enforce
**complete mediation**: "implement authorization in downstream systems rather than relying on an LLM to
decide if an action is allowed"
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). The 2026 reframing is worth
holding onto — autonomy is **least agency**, a privilege earned per tool and not granted by default: it is
no longer only *what* an agent can access but *how much freedom* it has to act without checking back
([OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
Read-only first, mutation behind a gate, money and deletes always gated.

## Credentials should be scoped, short-lived, and never in the prompt

The last layer is *what a key opens and for how long*. The hardening target is **least privilege per
session**: the zero-trust principle that access is granted per request, scoped to the minimum, with trust
treated as ephemeral so holding one key does not imply another
([NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)). For agents that means scoped,
short-lived, just-in-time credentials rather than standing secrets — so an orphaned or leaked token expires
fast and opens little. The cross-vendor tool-authorization standard now encodes exactly this: the **Model
Context Protocol** authorization spec builds on OAuth 2.1, requires PKCE, mandates that tokens be
audience-bound to the specific server (RFC 8707) and that authorization servers **SHOULD** issue short-lived
tokens, and explicitly **forbids token passthrough** — an MCP server "MUST NOT pass through the token it
received," precisely to avoid the confused-deputy problem
([MCP — Authorization, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization),
neutral example). And the simplest rule of all: **secrets never go into the prompt, context, or logs.** A
token pasted into context is one indirect prompt injection away from exfiltration, and an observability
pipeline that logs raw prompts and completions silently becomes a secret store.

## Identity is where the other pillars get their teeth

This pillar is the enforcement layer the rest of the repository leans on. A human-approval gate only matters if
the action behind it is *also* blocked at the credential — otherwise the agent can route around the gate.
Limits and budgets cap what a *correctly-scoped* identity can spend; observability is only an audit trail if
each action carries the identity that took it; rollback is cleaner when the agent never held the access to
cause the damage. And identity is also a compliance control: scoped access, attributable actions, and a
named owner are exactly what an auditor asks for — see the
**[compliance & governance](../compliance-and-governance/README.md)** pillar for where these become evidence
you must produce.

## Going deeper

This page is the landscape; four deep-dives walk the hardest ground:

- **[Agent identity — give the agent its own, not a human's](agent-identity.md)** works through distinct
  per-agent identity, the delegation and confused-deputy problem, the agent inventory you have to keep, and
  the emerging IAM-for-agents direction (decentralized identifiers, verifiable credentials, zero trust).
- **[Least-privilege tools — the permission matrix](least-privilege-tools.md)** builds the tool-permission
  matrix tool by tool: least-capability scoping, the read-only-then-gated ladder, approval gates, and why
  excessive agency is the high-blast-radius risk this pillar exists to bound.
- **[Secrets & credentials — scoped, short-lived, never in the prompt](secrets-and-credentials.md)** covers
  ephemeral and just-in-time credentials, token exchange and audience binding, and keeping secrets out of
  prompts, context, and logs.
- **[Audit & monitoring — make the identity boundary provable](audit-and-monitoring.md)** is the other half
  of the pillar: per-identity audit logging of every tool call, attributing each action to a distinct agent
  identity, and detecting privilege abuse, escalating tool use, and confused-deputy exploitation at runtime.

When you reach sign-off, the [identity & access go-live checklist](../../checklists/identity-and-access.md)
makes each control checkable and the [identity & access risk register](../../risk-register/identity-and-access.md)
scores what to fix first; see also the [Replit database deletion](../case-studies/replit-database-deletion.md)
for where unscoped production access decided the outcome.

---

## Sources

- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — the top-ranked agent risk and its three root causes (functionality, permissions, autonomy); the mitigation set behind the tool-permission matrix: minimize permissions, execute in user context, complete mediation, human approval of high-impact actions.
- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — promotes **ASI03 Identity & Privilege Abuse** to a named risk (the agent as a non-human-identity aggregation point) and frames autonomy as *least agency*, a privilege earned per tool.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — the cross-vendor tool-authorization spec: OAuth 2.1 + PKCE, RFC 8707 audience-bound tokens, short-lived access tokens, and the explicit token-passthrough prohibition; named as a neutral example.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — the *least-privilege per-request, ephemeral-trust* principle this pillar applies to scoped, short-lived agent credentials.
- **[Govern and secure AI agents across the organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)** (Microsoft) — vendor governance guidance for distinct per-agent identity, an agent registry/inventory, and least-privilege scoped access; named as a neutral example.

## Read more

- **[Agentic AI Identity and Access Management: A New Approach](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)** (Cloud Security Alliance) — the forward-looking IAM-for-agents proposal (rich verifiable Agent IDs, decentralized identifiers, verifiable credentials, just-in-time credentials, zero trust) that the agent-identity deep-dive builds on.

<!-- page-type: overview -->
