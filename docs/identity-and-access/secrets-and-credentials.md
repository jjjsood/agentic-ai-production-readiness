# Secrets & credentials — scoped, short-lived, never in the prompt

> **In one sentence:** A credential an agent holds should open the smallest thing for the shortest time, be
> issued just-in-time and audience-bound, and never live in a prompt, the context window, or a log — because
> a standing, broad, or logged secret turns one leak or injection into lasting access.

> Part of **[Identity & access overview](README.md)**

The last layer of identity & access is the credential itself: *what a key opens and for how long*, and
*where the key is allowed to exist*. The two failure modes are durability (a standing, broad token that
keeps opening doors long after the task is done) and exposure (a secret that ends up somewhere an attacker
or an injection can read it — the prompt, the context, the logs). This page covers the hardening target —
scoped, short-lived, just-in-time credentials with audience-bound token exchange — and the hard rule that
secrets stay out of the model's view.

---

## The target: least privilege per session, not standing secrets

The principle to apply is **least privilege per request with ephemeral trust**: access granted to the
minimum needed, re-evaluated each session, so holding one key never implies another and no access is
permanent ([NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)). For agents that translates to a
"tier-zero" posture: **no standing credentials, no unscoped tokens, no secrets shared across agents.** A
short-lived, narrowly-scoped, just-in-time token is the goal because it shrinks both dimensions of risk at
once — a token that opens little and expires fast means an orphaned, leaked, or injected credential has a
small blast radius and a short window. Standing secrets are the opposite: a long-lived broad token found in
a repo is a permanent skeleton key, which is precisely the shape of the
**[Replit database deletion](../case-studies/replit-database-deletion.md)** failure, where the agent reached
production through access it should never have held in standing form.

The contrast in one line: **standing + broad + shared = maximum blast radius for the longest time; ephemeral
+ scoped + per-agent = minimum blast radius for the shortest time.**

This is now codified MCP-specifically: OWASP's MCP risk catalog ranks **token mismanagement and secret
exposure** as its top MCP risk — keys hardcoded into client, server, or tool configuration, and tokens whose
lifetime outlives the session or carries no enforced rotation — and prescribes exactly this target: *issue
short-lived, scoped tokens aligned with least privilege* and *require token renewal for every new MCP session*
([OWASP MCP01:2025](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure)).
The standing static key an agent loads at startup is the precise anti-pattern it names.

## Just-in-time issuance and token exchange

"Short-lived and scoped" is a property you have to *issue*, not hope for. Two mechanisms make it real:

- **Just-in-time (JIT) issuance.** Mint a credential at the moment the agent needs it, scoped to the
  specific operation, with a short expiry — rather than handing the agent a long-lived secret at startup. A
  high-privilege operation gets a token that exists only for that operation and then expires.
- **Token exchange / scope reduction.** When an agent needs to call a downstream service, it should obtain a
  *new* token for that specific service, audience-bound and scoped down — not reuse or forward the token it
  already holds. The Model Context Protocol authorization spec encodes this directly: it builds on **OAuth
  2.1**, requires **PKCE** on the authorization-code flow, mandates **resource indicators (RFC 8707)** so a
  token is bound to the one server it's meant for, and requires servers to "validate that access tokens were
  issued specifically for them as the intended audience." Critically, it **forbids token passthrough** — "the
  MCP server **MUST NOT** pass through the token it received from the MCP client"; an upstream call uses a
  separate token from the upstream authorization server. And it advises short lifetimes: authorization
  servers "**SHOULD** issue short-lived access tokens to reduce the impact of leaked tokens"
  ([MCP — Authorization, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization),
  neutral example).

Audience binding plus no-passthrough is what stops a leaked or borrowed token from being replayed against a
*different* service — the credential-level defense against the confused-deputy problem covered in the
[agent-identity](agent-identity.md) deep-dive.

## Standard credential governance still applies

Agents don't get an exemption from the hygiene every non-human identity needs. Carry it over:

- **Rotation and expiry** on every credential the agent can hold; prefer issuance mechanisms where rotation
  is automatic over secrets a human pastes once and forgets.
- **No cross-environment reuse** — a credential scoped to staging must not open production, so an agent in a
  test environment can't reach live data.
- **De-provisioning on retirement** — when an agent is decommissioned, its credentials are revoked, not left
  live. This is the leaver half of the agent lifecycle the inventory tracks (see
  [agent-identity](agent-identity.md)).
- **Prefer platform-managed identity over handled secrets** where available, to remove the secret a human
  would otherwise store, paste, or leak — Microsoft's guidance is to *"mandate the use of managed identities
  … to eliminate credential management risks"*
  ([Microsoft — Govern and secure AI agents](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization),
  vendor guidance, neutral example).

## The hard rule: secrets never enter the prompt, context, or logs

Scoping and rotation are undone instantly if the secret is sitting somewhere the model — or an attacker —
can read it. Two places teams leak secrets without noticing:

- **In the prompt or context window.** A token pasted into the system prompt or pulled into context is now
  one **indirect prompt injection** away from exfiltration: the same untrusted content that can hijack an
  agent's actions can ask it to read back whatever is in its context, and a retrieval assistant turns any
  ingested email, document, or web page into a potential injection vector. The
  **[EchoLeak](../case-studies/echoleak-m365-copilot.md)** incident is the worked example of context being
  turned into an egress channel with no user interaction. Secrets belong in the execution environment the
  tool runs in, fetched at call time — never in the text the model sees.
- **In the logs.** Observability is a pillar of production readiness, but an observability pipeline that logs
  raw prompts and completions silently becomes a secret-and-PII store. Redact secrets and sensitive values
  **at the boundary, before they are written**, and put least-privilege access controls on the log backend
  itself — the trace store is a sensitive system, not a dumping ground. (This is the sensitive-information
  disclosure risk OWASP catalogs alongside excessive agency
  ([OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)).)

The discipline is simple to state and easy to violate under deadline: **a credential the model can read is a
credential the model can leak.** Keep secrets in the runtime, audience-bound and short-lived, and out of
every surface the model or a logger can see.

## Sources

- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — least-privilege per-request access with ephemeral, per-session trust: the principle behind scoped, short-lived, no-standing-secret agent credentials.
- **[MCP01:2025 — Token Mismanagement and Secret Exposure](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure)** (OWASP) — the top-ranked MCP risk: hardcoded keys and over-long/un-rotated tokens, with the "short-lived scoped tokens, renew per session" remediation that corroborates the no-standing-secret target.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — OAuth 2.1 + PKCE, RFC 8707 audience-bound tokens, short-lived access tokens, and the explicit token-passthrough prohibition behind scope-reduced token exchange; named as a neutral example.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — the "minimize permissions" mitigation behind scoping a credential to least capability.
- **[Govern and secure AI agents across the organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)** (Microsoft) — managed identities to eliminate handled secrets, and scoped service accounts per tool; named as a neutral example.
- **[LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)** (OWASP GenAI Security Project) — the risk that a credential or PII in a prompt, context window, or log surfaces in model output: why secrets stay out of every surface the model or a logger can read.
- **[EchoLeak — zero-click exfiltration in M365 Copilot](../case-studies/echoleak-m365-copilot.md)** (this repository) — why anything in the model's context (including a secret) is reachable by an indirect prompt injection.

<!-- page-type: standard -->
