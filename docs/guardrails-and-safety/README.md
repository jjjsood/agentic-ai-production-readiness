# Guardrails & safety — defense-in-depth for a model that can be fooled

> **In one sentence:** Guardrails are the pillar where the agent meets an adversary, and the one rule that
> organizes all of it is that the model itself is injectable — so every tool result and retrieved document
> is untrusted, and safety has to come from layers around the model, not from the model's good judgment.

Of the seven pillars, this is the one an attacker tests on day one. The others bound what the agent
*costs*, prove what it *did*, and decide who it *is*; guardrails decide what happens when someone hostile
points adversarial input at it — which, for any public or tool-using agent, is immediately. It is written
for the engineer who has to ship an agent into a world that will try to jailbreak it, exfiltrate through
it, and turn it against its own operator. The hard truth the pillar is built on: the model has no reliable
boundary between data and instructions, so you cannot make it safe by making it smarter or wording the
prompt more firmly. The [deep-dives](#going-deeper) walk the hardest parts.

This pillar is the runtime control behind a legal obligation: the EU AI Act's accuracy-robustness-and-
cybersecurity duty for high-risk systems (Art. 15) is, in effect, "have guardrails" written into law — it
requires resilience "against attempts by unauthorised third parties to alter their use, outputs or
performance by exploiting … vulnerabilities" ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Art. 15);
see [compliance & governance](../compliance-and-governance/README.md).

---

## Where this breaks in production

Guardrails fail loudly and in public. A Chevrolet dealership's bot was talked into "agreeing" to sell a
~$76k SUV for **$1** and calling it "a legally binding offer," because attacker-supplied instructions
were treated as policy ([Chevrolet dealership chatbot](../case-studies/chevrolet-dealership-chatbot.md)).
DPD's support bot was steered into swearing and writing a poem calling DPD "useless," with no output
filter and no adversarial pre-release test ([DPD chatbot](../case-studies/dpd-chatbot.md)). And
**EchoLeak** (CVE-2025-32711) raised the stakes to data breach: a single crafted email made Microsoft 365
Copilot exfiltrate the user's sensitive context with *zero user interaction*, by chaining bypasses of
three separate controls ([EchoLeak](../case-studies/echoleak-m365-copilot.md);
[MSRC CVE-2025-32711](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711)).

In each, the model did roughly what models do; what was missing was the infrastructure around it —
filtering, injection defense, a contained blast radius. Prompt injection is no theoretical risk; OWASP
has ranked it the **#1** LLM application risk for two editions running
([OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)), and as agents gain tools its
impact escalates from a wrong answer to "executing arbitrary commands in connected systems."

## The model is the vulnerable part — so don't defend with it

The single idea that organizes this pillar: an agent receives instructions and data as the *same tokens*
in the same context window, with no privileged channel an attacker's text cannot also occupy. So "tell
the model to ignore injected instructions" is not a control; it's one prompt competing with the
attacker's. Google DeepMind adversarially trained Gemini specifically to resist injection and still
concluded adversarial training "will not render the model immune," so model robustness is "a vital layer
within a comprehensive defense-in-depth strategy" ([Google DeepMind — Defending Gemini](https://arxiv.org/abs/2505.14534)).
NIST states flatly there is "no foolproof" defense against this class of attack
([NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)). The pillar's posture: **if the
model is the part that can be fooled, the controls that matter must not depend on the model not being
fooled.**

## Defense-in-depth: layers, at least one deterministic

Because no single control holds, safety is built as **multiple independent layers, each of which must be
bypassed for an attack to land, and at least one of which is deterministic** — enforced in code, not by
the model's judgment. OpenAI's and AWS's agent guidance both frame guardrails this way: layered, parallel,
fail-fast, deterministic where possible
([OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf);
[AWS Well-Architected — Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)).
EchoLeak is the cautionary tale for *thin* layering: it chained bypasses of three controls, so any single
one passing was no evidence the chain held. Layers reduce attacks; the deterministic ones *contain* the
attacks that get through.

## Guard the boundaries; then contain the blast

The defense has two halves, and a production agent needs both:

- **Guard every boundary the model touches.** Three of them — input (user text plus untrusted
  retrieved/tool/web content), output (what the model emits, speaking for your organization), and *tool
  arguments* (the JSON the model fills in, "a suggestion, not a command"). DPD and Chevrolet are pure
  output-boundary failures; tool-argument is the boundary filtering discussions usually skip, and the most
  dangerous.
- **Contain the blast for when a guard is bypassed.** Assume the earlier layers lost: *how much can a
  fooled agent touch?* Set by least-capability tool surface, execution isolation, and egress control — not
  the model's behaviour. OWASP names the root cause **Excessive Agency**: harm enabled by excessive
  functionality, permissions, or autonomy "regardless of what is causing the LLM to malfunction"
  ([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). Replit's agent wiping a
  production database during a code freeze is the blast-radius lesson: harm was sized by what the agent
  could reach ([Replit database deletion](../case-studies/replit-database-deletion.md)).

## Measure it, or you can't defend it at sign-off

"We have guardrails" is the answer that fails an audit; "our agent's attack-success rate on a recognized
benchmark is X%, here is the trace" is evidence. Injection defense is measurable: **AgentDojo** provides 97
realistic tool-using tasks and 629 security test cases for adaptive attacks and defenses
([AgentDojo](https://arxiv.org/abs/2406.13352)), and the strongest structural defense, **CaMeL**, publishes
its trade-off — 77% of tasks solved *with provable security* against an 84% undefended baseline
([CaMeL](https://arxiv.org/abs/2503.18813)). Test against *adaptive* attacks, and re-run on every prompt,
model, or tool change — each can regress the defense.

## Going deeper

This page is the landscape; four deep-dives walk the hardest ground:

- **[Prompt-injection defense](prompt-injection-defense.md)** direct vs. indirect injection, why the model
  can't self-defend, layered defenses up to CaMeL-style capability control, and how to *measure* with
  AgentDojo.
- **[Input/output filtering](input-output-filtering.md)** the three boundaries — input screening, output
  filtering, and tool-argument schema validation with complete mediation before any side effect.
- **[Sandboxing & blast radius](sandboxing-and-blast-radius.md)** shrinking tool surface to least
  capability, isolating untrusted execution, and locking down egress.
- **[Memory & tool supply chain](memory-and-tool-supply-chain.md)** attacks that arrive *before* the
  prompt — poisoned long-term memory/RAG, malicious or mutated tool descriptions (MCPTox measured 72.8%
  attack success across real MCP servers — a single study, not yet independently corroborated) — and the
  provenance/pinning/write-validation controls a request-time filter can't provide.

When you reach sign-off, the [go-live checklist](../../checklists/guardrails-and-safety.md) makes each
control checkable and the [risk register](../../risk-register/guardrails-and-safety.md) scores what to fix
first; see also [EchoLeak](../case-studies/echoleak-m365-copilot.md) for where a thin guardrail stack
decided the outcome.

---

## Sources

- **[LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)** (OWASP GenAI Security Project) — the #1-risk ranking, the direct/indirect taxonomy, and the escalation to arbitrary commands for tool-using agents.
- **[LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)** (OWASP GenAI Security Project) — excessive functionality/permissions/autonomy as the blast-radius root cause "regardless of what is causing the LLM to malfunction."
- **[OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)** (OWASP GenAI Security Project) — the taxonomy behind the three boundaries, including LLM05 Improper Output Handling.
- **[Lessons from Defending Gemini Against Indirect Prompt Injections](https://arxiv.org/abs/2505.14534)** (Google DeepMind) — adversarial training does not make a model immune; model robustness is one layer in defense-in-depth.
- **[Adversarial Machine Learning: Taxonomy (AI 100-2e2025)](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)** (NIST) — there is no foolproof defense against indirect prompt injection.
- **[Defeating Prompt Injections by Design (CaMeL)](https://arxiv.org/abs/2503.18813)** (Google DeepMind / ETH Zurich) — the capability/control-flow defense and the 77%-provably-secure vs 84%-undefended AgentDojo figures.
- **[AgentDojo](https://arxiv.org/abs/2406.13352)** (ETH Zurich) — the injection benchmark (97 tasks, 629 security tests) behind "measure it."
- **[A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)** (OpenAI) — layered, parallel, fail-fast guardrails; no single guardrail suffices.
- **[AWS Well-Architected — Generative AI Lens: guardrails (GENSEC02-BP01)](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html)** (AWS) — layered, deterministic-where-possible guardrails as production guidance.
- **[CVE-2025-32711 (EchoLeak)](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711)** (Microsoft MSRC) — the zero-click indirect-injection exfiltration advisory.
- **[Regulation (EU) 2024/1689 (EU AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)** (EUR-Lex / Official Journal) — Art. 15's accuracy-robustness-cybersecurity duty for high-risk systems, the legal obligation this pillar implements.

<!-- page-type: overview -->
