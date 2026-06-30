# Identity & access — go-live checklist

> **In one sentence:** Each box below is a way you've narrowed the agent's blast radius — if you can't tick
> it, the agent is holding more access, for longer, in more places than the task needs.

Run this before sign-off on any agent that holds a credential, calls a tool, or acts on a real system. A
failed box is not an automatic blocker — it is a residual risk someone has to *accept in writing*. For the
why behind each theme, see the [Identity & access overview](../docs/identity-and-access/README.md).

---

## Agent identity

- [ ] The agent runs under its **own distinct identity** — not a human's session and not a shared service account. ([Agent identity](../docs/identity-and-access/agent-identity.md))
- [ ] Every agent is in a **registry/inventory** with owner, purpose, the identity it runs as, and its access scope. ([Microsoft governance guidance](../docs/identity-and-access/agent-identity.md))
- [ ] When the agent acts **for a user**, it carries that user's authorization — not a standing superset. ([OWASP LLM06 — execute in user context](../docs/identity-and-access/least-privilege-tools.md))
- [ ] Forwarding a delegated action to a **third-party service triggers re-consent / a fresh audience-bound token** — the agent never replays the caller's token onward (confused-deputy defense). ([Agent identity](../docs/identity-and-access/agent-identity.md))
- [ ] An agent's scope is **re-reviewed when its tools, prompt, or purpose change** — not only at first launch (the mover step of the lifecycle). ([Agent identity](../docs/identity-and-access/agent-identity.md))
- [ ] A **de-provisioning path** exists: retiring an agent revokes its credentials, leaving none live.

## Tool permissions (the matrix)

- [ ] A **tool-permission matrix** exists: each tool mapped to its credential, scope, risk tier, gate, and log location. ([Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md))
- [ ] Every tool runs on a **least-capability credential** — read-only where it doesn't need to write; narrowed to specific resources, not "the whole database". ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- [ ] **No open-ended tools** (arbitrary shell / arbitrary HTTP) unless explicitly justified and gated. ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- [ ] Every **mutating / money / delete / external** action sits behind an approval gate that fires **before** the side effect. ([OWASP LLM06 — human approval](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- [ ] Authorization is enforced **downstream (complete mediation)** — the LLM never decides whether an action is allowed. ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- [ ] The agent has **no path to production data by default** — write access to prod is blocked at the credential, not just asked against in the prompt. ([Replit deletion](../docs/case-studies/replit-database-deletion.md))

## Secrets & credentials

- [ ] Credentials are **scoped and short-lived / just-in-time**, not standing, broad, or shared across agents. ([Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md))
- [ ] Downstream tokens are **audience-bound** and **not passed through** to upstream APIs (a separate token is obtained). ([MCP authorization spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization))
- [ ] Every credential the agent can hold **rotates** on a defined schedule (prefer automatic rotation over a human-pasted secret). ([Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md))
- [ ] **No cross-environment credential reuse** — a staging-scoped credential cannot open production. ([Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md))
- [ ] **Platform-managed identity is preferred** over human-handled secrets wherever the runtime offers it. ([Microsoft governance guidance](../docs/identity-and-access/secrets-and-credentials.md))
- [ ] **No secret appears in any prompt or the context window** — secrets live in the runtime, fetched at call time. ([Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md))

## Audit & monitoring

- [ ] Every tool call writes a **per-call identity audit record** — agent identity, credential/scope used, resource touched, gate decision, on-behalf-of subject, and outcome + timestamp. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] **Scope-escalation attempts are denied at the boundary and alerted** — an out-of-scope action, resource, or tool call is rejected, and the denial is itself a signal. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] **Anomalous or escalating tool use is detected at runtime** — a spike in a high-risk tool, a never-before-called tool, or a climbing rate of gated actions raises an alert. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] **Confused-deputy / audience-mismatch rejections are surfaced** — a token presented to a service it wasn't issued for, or a privileged identity acting on unexpected on-behalf-of requests, is flagged. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] **Secrets and PII are redacted before the audit log is written** — the trace store never becomes a secret/PII store. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] Access to the **trace/log backend is least-privilege** — the audit trail is a sensitive system, not a dumping ground. ([Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md))
- [ ] Audit logs are **retained long enough to reconstruct the system's operation** — meeting the EU AI Act Art. 12 ≥6-month floor for high-risk systems. ([EU AI Act Art. 12](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng))

---

## Sources

- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — backs the least-capability, no-open-ended-tools, human-approval, and complete-mediation lines.
- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — backs treating identity & privilege abuse (distinct identity, no inherited/cached credentials) as a first-class risk.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — backs the audience-bound, no-passthrough, short-lived-token lines; named as a neutral example.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — backs least-privilege-per-session scoped, short-lived credentials.
- **[MCP01:2025 — Token Mismanagement and Secret Exposure](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure)** (OWASP) — MCP-specific backing for the scoped/short-lived-credential and no-secret-in-prompt lines: hardcoded keys and over-long/un-rotated tokens as the top MCP risk.
- **[Govern and secure AI agents across the organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)** (Microsoft) — backs the distinct-identity, agent-registry, and managed-identity lines; named as a neutral example.
- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 12 automatic logging and the ≥6-month retention floor behind the audit-log retention line.

<!-- page-type: checklist -->
