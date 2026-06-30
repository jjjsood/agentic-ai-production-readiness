# Audit & monitoring — make the identity boundary provable

> **In one sentence:** Scoping an agent's access only matters if you can *prove* the boundary held and
> *notice* when it's being tested — so every tool call must be logged with the identity, credential, scope,
> and action behind it, and privilege abuse must be detectable at runtime, not reconstructed after the
> damage.

> Part of **[Identity & access overview](README.md)**

The other deep-dives in this pillar *grant and scope* access — a distinct identity, a least-capability tool
matrix, short-lived credentials. This page is the other half: *watching and proving*. A boundary you can't
observe is a boundary you can't defend in an audit and can't see being breached in real time. Identity is
where this pillar meets the **observability & evals** pillar (the trace infrastructure) and the
**[compliance & governance](../compliance-and-governance/README.md)** pillar (where these logs become the
evidence you must produce). This page covers per-identity audit logging, attributing every action to a
distinct agent identity, and detecting privilege abuse, escalating tool use, and confused-deputy
exploitation while it's happening.

---

## Log the identity boundary, not just the action

A trace that says "an invoice was refunded" is an operational log. An *identity* audit log says **which
agent identity, running under which credential, with which scope, took which action, against which
resource, and whether a gate approved it.** That fuller record is what proves the boundary held — or shows
exactly where it didn't. The fields to capture on every tool call:

| Field | Why it's in the audit record |
|-------|------------------------------|
| Agent identity | Attributes the action to a distinct, named non-human identity, not "the system". |
| Credential / scope used | Shows the action ran inside its granted scope (or escaped it). |
| Action + arguments | What was actually attempted, including parameters that bound blast radius. |
| Resource touched | Which downstream object — the basis for least-privilege review. |
| Gate decision | Whether an approval gate fired and who/what approved. |
| On-behalf-of subject | The user the agent was acting for, if delegated — the confused-deputy check. |
| Outcome + timestamp | Success/denied, and when — the reconstruction spine. |

This is the identity-flavored version of the audit trail compliance frameworks already require. The EU AI
Act mandates automatic logging that lets you reconstruct a high-risk system's operation, retained for a
period appropriate to use and **at least six months**
([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Art. 12); NIST's AI RMF
treats accountability and transparency — including the traceability needed to document and reconstruct how an
outcome was produced — as a core trustworthiness characteristic
([NIST AI RMF 1.0 (AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)). Identity logging
is what makes those records *attributable*: without the identity-and-scope fields, a trace can tell you an
action happened but not that it was authorized.

## Attribution requires a distinct identity to attribute to

Per-identity logging only works if there is a distinct identity per agent to log against — which is why the
[agent-identity](agent-identity.md) decision is load-bearing here. An agent on a shared service account or a
borrowed human session produces an **attribution gap**: the log can't say *which* agent acted, so abuse
hides in aggregate and revocation breaks every agent at once. OWASP names this directly in **ASI03 Identity
& Privilege Abuse** — when an agent reuses cached or inherited credentials, "it acts with the full authority
of every key, token, and service account assigned to it," and the action can't be cleanly traced back to a
specific actor
([OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
Distinct identity is therefore both a *prevention* control (scoped, revocable) and a *detection* control
(attributable). The same lifecycle inventory that tracks agents also tells you which identities *should* be
active, so an action from a retired or unknown identity is itself a signal.

One discipline carries over from the [secrets](secrets-and-credentials.md) page: the audit log is a
sensitive system. Redact secrets and PII **before** they're written, and put least-privilege access on the
log backend — an audit trail that quietly stores credentials or personal data becomes the next breach
surface rather than the evidence of control. This is the **sensitive-information disclosure** risk OWASP
catalogs alongside excessive agency: an observability pipeline logging raw prompts and completions silently
becomes a secret-and-PII store
([OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)).

## Detect privilege abuse and escalation at runtime

Logging proves the boundary after the fact; monitoring catches it being tested in the moment. The point of
the per-identity record is that it makes anomalies *legible* — you can baseline what each agent identity
normally does and alert when it deviates. Signals worth watching, mapped to the threats this pillar bounds:

- **Scope escalation** — an identity attempting actions, resources, or tools outside its granted scope. In a
  zero-trust posture this should be *denied at the boundary* (trust is per-request and ephemeral, so an
  out-of-scope call is rejected, not reasoned about — [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)),
  but the denied attempt is itself the alert.
- **Anomalous or escalating tool use** — a sudden spike in a high-risk tool, a new tool an identity has
  never called, or a climbing rate of gated actions: the runtime fingerprint of a hijacked agent or an
  excessive-agency failure trying to ride the credentials it holds.
- **Confused-deputy exploitation** — a privileged identity acting on a stream of low-privilege or unexpected
  on-behalf-of requests, or a token presented to a service it wasn't issued for. The structural defense is
  audience binding (a token "issued specifically for them as the intended audience", RFC 8707) and the
  token-passthrough prohibition ([MCP — Authorization, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)) —
  and a *rejected* audience-mismatched token is exactly the event to alert on.
- **Off-hours or out-of-pattern access** — an identity acting at a time or volume unlike its baseline, the
  classic non-human-identity compromise tell.

CSA frames this as continuous, identity-centric oversight — its agentic IAM approach pairs scoped, verifiable
agent identities with *"real-time monitoring"* of agent behavior rather than a one-time grant
([CSA — Agentic AI IAM: A New Approach](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)).
The detections route into the same place a human-control kill switch lives: an identity tripping these
signals is a candidate to suspend or revoke, fast.

## Where this connects

This page is the seam between three pillars. The **observability & evals** pillar owns the trace plumbing —
the spans, the token accounting, the structured pipeline — and this pillar adds the identity/credential/scope
fields that make a trace *provable* rather than merely informative. The
**[compliance & governance](../compliance-and-governance/README.md)** pillar is where these logs become
audit evidence: the retained, reconstructable record that you were in control. And the human-control &
rollback pillar consumes the detections, turning an anomaly into a suspend-or-revoke decision. The durable
rule: **generate the identity evidence as a by-product of running the agent, not as a forensic exercise after
it fails.**

## Sources

- **[OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — **ASI03 Identity & Privilege Abuse**: cached/inherited credentials and the attribution gap that per-identity logging closes; the privilege-abuse signals to detect.
- **[Special Publication 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)** (NIST) — per-request, ephemeral-trust access: out-of-scope calls are denied at the boundary, and the denial is the signal.
- **[Agentic AI Identity and Access Management: A New Approach](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)** (Cloud Security Alliance) — scoped, verifiable agent identities paired with real-time monitoring of agent behavior.
- **[Model Context Protocol — Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)** (Anthropic / MCP) — audience-bound tokens (RFC 8707) and the token-passthrough prohibition behind detecting confused-deputy exploitation; named as a neutral example.
- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 12 automatic logging and the ≥6-month retention floor behind the reconstructable audit record.
- **[AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)** (NIST) — accountability and transparency, including traceability, as a core trustworthiness characteristic: documenting and reconstructing how an outcome was produced.
- **[LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)** (OWASP GenAI Security Project) — the sensitive-information-disclosure risk the audit log itself can create: redact secrets and PII before they are written, least-privilege the log backend.

<!-- page-type: standard -->
