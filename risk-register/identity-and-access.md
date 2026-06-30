# Identity & access — risk register

> **In one sentence:** These are the risks that turn a single bad output into real-world damage by giving the
> agent too much access, for too long, in too many places — each scored so you can sequence the hardening,
> and each tied to the control that closes it.

The risks below share a root: the agent holds more access than the task needs, and a hallucination, an
injection, or a logic error then rides that access into the real world. Read the score as a priority sort,
not a probability. For the reasoning behind the controls, see the
[Identity & access overview](../docs/identity-and-access/README.md).

---

## Scoring

- **Likelihood (L):** 1 rare · 2 possible · 3 likely (in a real, unhardened deployment).
- **Impact (I):** 1 contained · 2 serious (money, data, trust) · 3 severe (regulatory, legal, safety, unrecoverable).
- **Score = L × I** (1–9). **6–9 = address before go-live**, 3–4 = plan to mitigate, 1–2 = accept and watch.

## Risks

| # | Risk | L | I | Score | Control (and where it lives) |
|---|------|---|---|-------|------------------------------|
| 1 | **Unscoped production access** — agent holds write/delete access to prod it never needed; one bad call destroys live data | 3 | 3 | 9 | Read-only by default, write blocked at the credential, no prod path by default — [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md), [Replit deletion](../docs/case-studies/replit-database-deletion.md) |
| 2 | **Over-broad reach enables exfiltration** — broad data/identity scope turns one injection into a large leak | 3 | 3 | 9 | Minimize permissions; scope what the agent's identity can reach and send — [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md), [EchoLeak](../docs/case-studies/echoleak-m365-copilot.md) |
| 3 | **LLM is the authorization decision** — boundary enforced only by prompt wording, which an injection overrides | 3 | 3 | 9 | Complete mediation: authorize in the downstream system, never trust the model — [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md) |
| 4 | **Standing / leaked secret** — long-lived broad token (e.g. in a repo or prompt) becomes a permanent skeleton key | 2 | 3 | 6 | Scoped, short-lived, just-in-time credentials; secrets out of prompt/context/logs — [Secrets & credentials](../docs/identity-and-access/secrets-and-credentials.md) |
| 5 | **Confused deputy / token passthrough** — a privileged agent acts on a low-privilege (or injected) caller's request; a token is replayed against the wrong service | 2 | 3 | 6 | Carry the caller's authority; audience-bind tokens; never pass a token through — [Agent identity](../docs/identity-and-access/agent-identity.md), [MCP authorization spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) |
| 6 | **Borrowed / shared identity** — agent runs on a human's session or a shared account; actions unattributable, access un-revocable | 3 | 2 | 6 | Distinct identity per agent; registry with owner and scope — [Agent identity](../docs/identity-and-access/agent-identity.md) |
| 7 | **Ungated high-impact action** — money / send / delete runs autonomously, so an injected output self-authorizes | 2 | 3 | 6 | Approval gate before the side effect, sized to blast radius — [Least-privilege tools](../docs/identity-and-access/least-privilege-tools.md) |
| 8 | **Shadow / orphaned agent identity** — untracked agent or un-revoked credential after retirement | 2 | 2 | 4 | Agent registry + lifecycle de-provisioning — [Agent identity](../docs/identity-and-access/agent-identity.md) |
| 9 | **No audit trail / undetected privilege abuse** — the boundary held but there's no per-identity record to prove it, and scope escalation or confused-deputy exploitation goes unnoticed at runtime | 3 | 2 | 6 | Per-call identity audit record + runtime detection of scope escalation, anomalous tool use, and audience-mismatch rejections — [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |
| 10 | **Privilege escalation / scope creep over time** — an agent accumulates permissions, or a tool/credential is widened post-launch without re-review; the agent becomes an aggregation point that accrues authority | 2 | 2 | 4 | Re-review scope on tool/prompt/purpose change; registry + lifecycle controls — [Agent identity](../docs/identity-and-access/agent-identity.md), [Audit & monitoring](../docs/identity-and-access/audit-and-monitoring.md) |

---

## Sources

- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — the minimize-permissions, complete-mediation, and human-approval controls behind risks 1, 2, 3, and 7.
- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — **ASI03 Identity & Privilege Abuse** behind the borrowed/shared-identity, shadow-agent, and undetected-abuse / scope-creep risks (6, 8, 9, and 10): the agent as a non-human-identity aggregation point that accrues authority.
- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 12 automatic logging and the ≥6-month retention floor behind the per-identity audit-trail control for risk 9.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — audience binding and the token-passthrough prohibition behind risk 5; named as a neutral example.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — least-privilege-per-session, ephemeral-trust principle behind the scoped, short-lived credential control for risk 4.
- **[MCP01:2025 — Token Mismanagement and Secret Exposure](https://owasp.org/www-project-mcp-top-10/2025/MCP01-2025-Token-Mismanagement-and-Secret-Exposure)** (OWASP) — the top-ranked MCP risk (hardcoded keys, over-long/un-rotated tokens) that the standing/leaked-secret control for risk 4 addresses.

<!-- page-type: risk-register -->
