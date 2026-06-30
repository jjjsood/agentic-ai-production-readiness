# Agent identity — give the agent its own, not a human's

> **In one sentence:** An agent is a non-human identity, so it needs its own distinct, attributable, scoped
> identity — not a borrowed human session and not a shared service account — or its actions can't be
> attributed, scoped, or revoked.

> Part of **[Identity & access overview](README.md)**

Before you scope a single tool, decide *who the agent is*. The cheap path — let the agent reuse a human's
login, or run every agent under one shared service account — is also the path that inflates blast radius and
destroys attribution. This page makes the case for a distinct identity per agent, works through the hardest
part (delegation and the confused-deputy problem), explains the inventory you have to keep, and surveys the
emerging IAM-for-agents direction.

---

## An agent is a non-human identity

An agent that calls tools holds credentials and acts on systems — it is a **non-human identity (NHI)** in
exactly the way a service account or a CI/CD bot is, and it needs to be treated as one. The agentic threat
list puts the danger plainly: an agent "becomes an aggregation point for non-human identities" and acts
"with the full authority of every key, token, and service account assigned to it," merging multiple
permissions into one execution point
([OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
That aggregation is the risk: whatever the agent's identity can touch is reachable by *any* output the model
produces — including a hallucinated or injected one.

The two anti-patterns to design out:

- **Borrowing a human session.** If the agent runs on a human's full OAuth session, it inherits everything
  that human can do, not the slice the task needs. Microsoft's guidance is explicit that when an agent acts
  on a user's behalf it should *inherit that user's permissions* for the specific data in play, not a
  standing superset — *"an internal helpdesk agent … shows an employee only their own HR record"*
  ([Microsoft — Govern and secure AI agents](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization),
  vendor guidance, neutral example).
- **Sharing one identity across agents.** A shared account means no action can be attributed to a specific
  agent and no agent's access can be revoked without breaking the others. Microsoft's rule: *"Require each
  agent to operate under a distinct agent identity"* so actions are attributable and enforceable
  ([Microsoft](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)).

## Delegation and the confused-deputy problem

The genuinely hard problem is **delegation**: an agent rarely acts purely as itself — it acts *for* a user,
or one agent calls another. The failure mode is the **confused deputy**: a more-privileged component is
tricked into using its authority on behalf of a less-privileged caller. In agent terms, a low-privilege
agent (or an injected instruction) sends a request to a high-privilege agent that "trusts the request
blindly" and executes it with its own elevated rights. The MCP authorization spec calls this out by name and
ties it to two concrete mistakes: accepting tokens that were not issued for you (audience-validation
failure), and **token passthrough** — forwarding a token unchanged to a downstream service, which lets the
downstream API "incorrectly trust the token as if it came from the MCP server"
([MCP — Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization),
neutral example).

The defenses are structural, not prompt-level:

- **Carry the caller's authority, not your own.** When the agent acts for a user, the downstream action runs
  in *that user's* security context — OWASP's "execute extensions in the user's context" mitigation
  ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).
- **Audience-bind every token.** A token issued for service A must be rejected by service B; MCP requires
  servers to "validate that access tokens were issued specifically for them as the intended audience"
  (RFC 8707) ([MCP — Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)).
- **Never pass a token through.** When the agent calls an upstream API it acts as a *separate* OAuth client
  with a *separate* token — the spec's "MUST NOT pass through the token it received" rule exists exactly to
  stop the confused deputy ([MCP — Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)).
- **Re-consent on dynamic delegation.** An intermediary using a shared client ID must get explicit user
  consent before forwarding to a third party, rather than silently reusing a prior authorization
  ([MCP — Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)).

## You can't govern an agent you can't see — the inventory

Distinct identities are only useful if you know which ones exist. Untracked or "shadow" agents are the
governance equivalent of orphaned service accounts: nobody owns them, nobody scoped them, nobody will
notice when they misbehave. The baseline control is an **agent registry** — a single inventory recording,
for every agent, its identity, owner, purpose, platform, and access scope. Microsoft states the rule
bluntly: *"You can't govern agents you don't know exist,"* and recommends recording every agent in one
organizational inventory with ownership and access scope tracked
([Microsoft — Govern and secure AI agents](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization),
neutral example). The registry is also where the lifecycle lives: an agent identity gets *created* with
scoped access, *reviewed* when its tools or prompt change, and *de-provisioned* when the agent is retired —
the same joiner/mover/leaver discipline any non-human identity needs, so an agent that is decommissioned
doesn't leave a live credential behind.

A workable inventory row captures at least: agent ID · owner (a person) · purpose · the identity it runs as
· the tools/scopes it holds · its approval gates · last review date.

## Where agent IAM is heading

Today most agents authenticate with OAuth clients, managed identities, or service accounts retrofitted from
human-and-app IAM — which is workable but strained, because agents are more numerous, more ephemeral, and
delegate more fluidly than the identities those systems were built for. The forward-looking proposal is a
purpose-built IAM for agents. The Cloud Security Alliance argues that *"traditional identity and access
management (IAM) protocols, designed for static applications and human users, can't keep up,"* and sketches
the building blocks: **rich, verifiable Agent IDs**, identities managed with **decentralized identifiers
(DIDs)** and **verifiable credentials (VCs)**, **just-in-time** context-aware access, and a **zero-trust**
posture throughout
([CSA — Agentic AI IAM: A New Approach](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)).
The underlying principle is not new — it is **zero trust** applied to a non-human identity: NIST defines it
as enforcing "least privilege per-request access decisions" with trust treated as ephemeral, re-evaluated
per session rather than granted once
([NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)). Treat the specific mechanisms (DIDs, VCs)
as an emerging direction to track, not a settled standard to adopt blindly; the durable takeaway is that an
agent's identity should be distinct, verifiable, scoped, and short-lived.

## Sources

- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — **ASI03 Identity & Privilege Abuse**: the agent as a non-human-identity aggregation point acting with the full authority of every assigned key/token/account.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — the "execute extensions in the user's context" mitigation behind carrying the caller's authority, not the agent's own.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — the confused-deputy section, audience-bound tokens (RFC 8707), the token-passthrough prohibition, and dynamic-delegation re-consent; named as a neutral example.
- **[Govern and secure AI agents across the organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)** (Microsoft) — distinct per-agent identity, the agent registry/inventory ("you can't govern agents you don't know exist"), and inheriting the user's permissions on delegation; named as a neutral example.
- **[Agentic AI Identity and Access Management: A New Approach](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)** (Cloud Security Alliance) — the IAM-for-agents direction: verifiable Agent IDs, decentralized identifiers, verifiable credentials, just-in-time access, zero trust.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — least-privilege per-request access with ephemeral, per-session trust, the principle under agent zero-trust.

<!-- page-type: standard -->
