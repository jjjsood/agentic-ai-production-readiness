# Identity & access — go-live checklist

> **In one sentence:** Each box below is a way you've narrowed the agent's blast radius — if you can't tick
> it, the agent is holding more access, for longer, in more places than the task needs.

Run this before sign-off on any agent that holds a credential, calls a tool, or acts on a real system. A
failed box is not an automatic blocker — it is a residual risk someone has to *accept in writing*. For the
why behind each theme, see the [Identity & access overview](../docs/identity-and-access/README.md).

---

## Agent identity

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Distinct agent identity | Runs under its own identity — not a human's session, not a shared service account | [Agent identity](../docs/identity-and-access/agent-identity.md) |
| ☐ | Agent registry entry | Owner, purpose, run-as identity, and access scope recorded in an inventory | [Agent identity](../docs/identity-and-access/agent-identity.md); [Microsoft governance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization) |
| ☐ | Act in user context | When acting for a user, carries that user's authorization — not a standing superset | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | Re-consent on forwarding | Forwarding to a third party triggers re-consent / a fresh audience-bound token; caller's token never replayed onward (confused-deputy defense) | [Agent identity](../docs/identity-and-access/agent-identity.md); [MCP authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) |
| ☐ | Re-review scope on change | Scope re-reviewed when tools, prompt, or purpose change — not only at launch (the mover step) | [Agent identity](../docs/identity-and-access/agent-identity.md) |
| ☐ | De-provisioning path | Retiring an agent revokes its credentials, leaving none live | [Agent identity](../docs/identity-and-access/agent-identity.md) |

## Tool permissions (the matrix)

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Tool-permission matrix | Each tool mapped to its credential, scope, risk tier, gate, and log location | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md) |
| ☐ | Least-capability credential | Read-only where it needn't write; narrowed to specific resources, not "the whole database" | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | No open-ended tools | No arbitrary shell / arbitrary HTTP unless explicitly justified and gated | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | Gate before side effect | Every mutating / money / delete / external action gated, firing before the side effect | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | Authorize downstream | Authorization enforced downstream (complete mediation); the LLM never decides whether an action is allowed | [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md); [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| ☐ | No default prod access | Prod write access blocked at the credential, not just asked against in the prompt | [Replit deletion](../docs/case-studies/replit-database-deletion.md) |

## Secrets & credentials

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Scoped, short-lived creds | Scoped and just-in-time, not standing, broad, or shared across agents | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md); [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) |
| ☐ | Audience-bound tokens | Downstream tokens audience-bound and not passed through upstream; a separate token is obtained | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md); [MCP authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) |
| ☐ | Credential rotation | Every credential rotates on a defined schedule; prefer automatic over a human-pasted secret | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md); [MCP01](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure) |
| ☐ | No cross-env reuse | A staging-scoped credential cannot open production | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md) |
| ☐ | Prefer managed identity | Platform-managed identity preferred over human-handled secrets where the runtime offers it | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md); [Microsoft governance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization) |
| ☐ | No secret in prompt | No secret in any prompt or the context window; secrets live in the runtime, fetched at call time | [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md); [MCP01](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure) |

## Audit & monitoring

| Done | Control | Pass criterion / metric | Source |
|------|---------|-------------------------|--------|
| ☐ | Per-call audit record | Agent identity, credential/scope, resource, gate decision, on-behalf-of subject, outcome + timestamp on every tool call | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Deny + alert escalation | Out-of-scope action/resource/tool call rejected at the boundary, and the denial itself raises a signal | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Detect anomalous tool use | Spike in a high-risk tool, a never-before-called tool, or a climbing rate of gated actions raises an alert | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Surface confused-deputy | Token presented to a wrong-audience service, or a privileged identity acting on unexpected on-behalf-of, is flagged | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Redact before logging | Secrets and PII redacted before the audit log is written; the trace store never becomes a secret/PII store | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Lock down log backend | Access to the trace/log backend is least-privilege — the audit trail is a sensitive system | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| ☐ | Retain audit logs ≥6mo | Retained long enough to reconstruct operation — meets the EU AI Act Art. 12 ≥6-month floor for high-risk systems | [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md); [EU AI Act Art. 12](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |

---

## Sources

- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — backs the least-capability, no-open-ended-tools, human-approval, and complete-mediation rows.
- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — backs treating identity & privilege abuse (distinct identity, no inherited/cached credentials) as a first-class risk.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — backs the audience-bound, no-passthrough, short-lived-token rows; named as a neutral example.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — backs least-privilege-per-session scoped, short-lived credentials.
- **[MCP01:2025 — Token Mismanagement and Secret Exposure](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure)** (OWASP) — MCP-specific backing for the scoped/short-lived-credential and no-secret-in-prompt rows: hardcoded keys and over-long/un-rotated tokens as the top MCP risk.
- **[Govern and secure AI agents across the organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization)** (Microsoft) — backs the distinct-identity, agent-registry, and managed-identity rows; named as a neutral example.
- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 12 automatic logging and the ≥6-month retention floor behind the audit-log retention row.

<!-- page-type: checklist -->
