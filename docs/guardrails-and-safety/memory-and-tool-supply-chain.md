# Memory & tool supply chain — the attack that arrives before the prompt

> **In one sentence:** Live prompt injection is the attack you can watch happen; the agent-specific upgrade
> is the attack that was *planted earlier* — in long-term memory or RAG, or in a tool's own description —
> and fires on a later run, so the trust boundary you must police is not just this request but everything
> the agent persists and everything it connects to.

> Part of **[Guardrails & safety overview](README.md)**

The [injection-defense](prompt-injection-defense.md), [input/output-filtering](input-output-filtering.md),
and [sandboxing](sandboxing-and-blast-radius.md) pages all defend the *live request*: untrusted content
arrives, is filtered, and its blast is contained. This page covers the two surfaces that defeat that
framing by acting outside the request you are watching. **Memory/context poisoning** writes malicious
content into long-term store on one run and re-activates it on a later, unrelated one. **Tool supply-chain
poisoning** ships the malice in the tool's *definition* — the metadata the model reads to decide how to
call it — so the agent is compromised before any data is even retrieved. Both are first-class agentic
risks in NIST and OWASP's agent taxonomies; both need controls a request-time filter cannot provide:
provenance, pinning, and write-validation.

---

## Why this is a separate surface

A request-time filter assumes the threat enters *with the request*. These two do not:

- **Memory poisoning is time-shifted.** The poison is written now and weaponized later — possibly in a
  different session, possibly against a different user. NIST's 2025 taxonomy treats memory poisoning as a
  distinct attack on agent and RAG systems, alongside indirect injection and the tool supply chain
  ([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)). OWASP's agentic list names it
  **ASI06 Memory & Context Poisoning** — "corrupting stored context (memory, embeddings, RAG stores) to
  bias future reasoning and actions" ([OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)).
- **Tool poisoning is pre-request.** The malicious instruction rides in the tool's own description, so the
  agent is steered before it fetches a single document. OWASP calls this out under **ASI02 Tool Misuse**:
  an attacker "alters tool descriptors so the model invokes capabilities that look normal on paper but
  encode malicious semantics" ([OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)),
  and supply-chain compromise of connected tools is its own category. OWASP's deeper threat reference
  catalogs both as core agentic threats with mitigations
  ([OWASP — Agentic AI: Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)).

The unifying point: the trust boundary for an agent is not "this prompt" but **everything it persists and
everything it connects to.**

## Memory & context poisoning

The mechanism is the dark side of memory and RAG: an agent that learns from what it stores will faithfully
re-load and act on whatever was written, including a poisoned note, a tampered document chunk, or an
embedding placed to surface on a target query. Because retrieval and memory recall are *designed* channels,
the poisoned content arrives as legitimate context and bypasses input validation the same way indirect
injection does ([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)). Two properties make
it nastier than live injection: it is **persistent** (one successful write keeps firing until the store is
cleaned) and it can **cross sessions and users** (a memory written in one user's session can steer
another's). Controls, none of which a request-time content filter provides:

- **Validate and quarantine memory writes.** Treat *writing* to memory/RAG as a privileged, guarded action,
  not a side effect — validate provenance and content before persisting, and quarantine writes that come
  from untrusted-content paths so a poisoned retrieval cannot silently become durable memory.
- **Isolate memory scope.** Session- and user-scoped memory limits cross-contamination; don't let one
  session's writes leak into another's recall by default.
- **Provenance on stored context.** Tag each memory/RAG record with where it came from, so a later run can
  weight or distrust content of untrusted origin and an incident is reconstructable.
- **Bound and expire.** Cap memory size and age out stale entries; unbounded, never-pruned memory is a
  growing poisoned-write surface.

## Tool supply-chain poisoning

As agents wire into tools over protocols like the Model Context Protocol, **every connected tool is a
trust dependency** — and the description the model reads to call it is an injection channel that needs no
execution. The risk has measured teeth. **MCPTox** evaluated tool-description poisoning across **45 live,
real-world MCP servers** and **353 authentic tools**: poisoning reached a **72.8%** attack-success rate on
one capable model, and agents almost never refused — the *highest* refusal rate observed was under **3%**.
The counter-intuitive finding is that *more capable* models were *more* vulnerable, because the attack
exploits their stronger instruction-following ([MCPTox](https://arxiv.org/abs/2508.14925)). Three variants
make this a supply-chain problem, not a one-off bug:

- **Poisoned descriptions** — the tool's metadata carries hidden instructions from day one (the MCPTox
  case).
- **Rug-pulls / mutation** — a tool vetted as benign at install time has its definition changed *after*
  approval, so review-once is not enough.
- **Unvetted third-party tools** — an agent connected to an arbitrary or typosquatted server inherits its
  author's intent.

Controls borrow directly from software supply-chain security:

- **Provenance & signing.** Prefer first-party or vetted tools/servers; require a verifiable source so an
  unsigned or unknown-origin tool is rejected rather than trusted.
- **Pin & review tool definitions.** Treat a tool description as a versioned artifact — pin it, review it,
  and re-review on any change, so a rug-pull cannot mutate an approved tool silently.
- **Authorize independently of the description.** A tool's self-description must never grant authority your
  authorization layer hasn't — the same *complete mediation* rule as
  [input/output filtering](input-output-filtering.md): the action is authorized downstream, not by trusting
  the tool's stated semantics. The model rarely refusing (MCPTox's <3%) is exactly why enforcement cannot
  live in the model's judgment.

## Where this sits in the defense

These controls are the *persistence* and *supply-chain* layers of the same defense-in-depth posture the
rest of the pillar builds: injection defense handles the live request, filtering guards the boundaries,
sandboxing contains the blast, and this page closes the two gaps that act *outside* the live request.
NIST's framing is the anchor — indirect injection, memory poisoning, and tool supply chain are named
together as the agent attack surface, with the same standing caveat that there is "no foolproof" defense
([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)) — so here too the rule holds: do
not rely on the model not being fooled. Police what it stores and what it connects to.

---

## Sources

- **[Adversarial Machine Learning: Taxonomy and Terminology (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — names memory poisoning and the tool supply chain as distinct agent/RAG attacks alongside indirect injection, surviving input validation, with no foolproof defense.
- **[OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** (OWASP GenAI Security Project) — ASI06 Memory & Context Poisoning (corrupting memory/embeddings/RAG to bias future actions) and ASI02 Tool Misuse / altered tool descriptors, plus the supply-chain category.
- **[Agentic AI — Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)** (OWASP GenAI Security Project) — the threat-model reference cataloguing memory poisoning and tool misuse with mitigations.
- **[MCPTox](https://arxiv.org/abs/2508.14925)** (arXiv) — tool-description poisoning across 45 MCP servers / 353 tools: 72.8% attack-success rate, <3% refusal, more-capable-models-more-vulnerable.

<!-- page-type: standard -->
