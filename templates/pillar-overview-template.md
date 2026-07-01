# Pillar Overview Template — the standalone chapter a pillar opens with

A **pillar overview** is the hub at `docs/<pillar>/README.md`, but it is **not a project README**. It is a
*standalone chapter*: a reader who reads only this page comes away understanding the whole pillar — what it
is, why a gap there breaks production, the mental models, and the lay of the land — and is then pointed to
the deep-dives that take each piece further. It is breadth that stands on its own; the deep-dives are depth.

> **In one sentence:** The overview teaches the whole pillar in one read and reads like a book chapter, not
> a table of contents — it links onward to every deep-dive, but the links are a reading path inside the
> prose, never a build-status tracker.

This file is the template to copy for any `docs/<pillar>/README.md`. The page carries the marker
`<!-- page-type: overview -->` as its **last line**; the verifier keys off it to require that the overview
links every deep-dive in its own directory.

---

## What an overview owes the reader

1. **Stand alone.** A reader who only reads the overview should understand what the pillar is, why it
   fails when missing, the core concepts, and how the pieces fit — without opening a single deep-dive. The
   body is real, sourced chapter prose, not a summary that defers everything to the spokes.
2. **Read like a chapter, not a README.** No "Status" columns, no "🚧 planned / ✅ done" markers, no
   project-progress framing. **Build/roadmap status belongs in the root `README.md` pillar table, not
   here.** The overview is content; it only mentions a deep-dive once that deep-dive exists to link to.
3. **Point onward as a reading path.** Every deep-dive in the directory is linked — woven into the prose
   or gathered in a short "Going deeper" section as full sentences ("**[X](x.md)** works through …"), not
   a bare index. A deep-dive nothing links to is an orphan the verifier errors on.
4. **Connect outward, briefly.** Fold the pillar's checklist, risk register, and illustrative case studies
   into the narrative where they belong — typically a closing line — so the chapter joins up with the
   hands-on artifacts and the real incidents.

## The skeleton (copy this)

```markdown
# <Pillar Name> — <short tagline>

> **In one sentence:** <core claim of this pillar; tie to the 88%-infra thesis where it fits>

<Lead: what this pillar is, who is accountable for it, why a gap here is what actually breaks in
production, and — in a sentence — what this page covers so it reads as self-contained. 3–5 sentences.>

---

## Where this breaks in production

<The failure story: what goes wrong in production when this infrastructure is absent or weak, ideally
through a named case study or two. Sourced. The motivation the rest of the chapter answers.>

## <Core concept section(s)>

<The long-form heart of the overview — the mental models, terms, trade-offs, and the key framework(s) a
reader needs to think about the pillar clearly. Use as many H2/H3 sections as the topic needs, with real
section titles (not a generic "Core concepts"). Sourced prose; tables where they genuinely help. This is
the part that lets the overview stand on its own.>

## Going deeper

<A short reading path into the deep-dives, as full sentences — every `*.md` in this directory linked here
or earlier in the prose. No status column.>

- **[<Deep-dive A title>](<slug-a>.md)** <verb-led clause on what it takes further>.
- **[<Deep-dive B title>](<slug-b>.md)** <…>.

<Closing line that connects outward, in prose:> When you reach sign-off, the
[<Pillar> go-live checklist](../../checklists/<pillar>.md) makes each control checkable and the
[<Pillar> risk register](../../risk-register/<pillar>.md) scores what to fix first; see also
[<Case A>](../case-studies/<slug>.md) for where this gap decided the outcome.

---

## Sources
<!-- Required. Primary sources backing the numbers/claims in the overview prose. -->
- **[Title](URL)** (Publisher) — which claim on this page it backs.

## Read more
<!-- Optional. Topic-specific further reading that adds value beyond the deep-dives.
     NOT a back-link to the README, NOT loosely-related links. Omit if every candidate is generic. -->
- **[Title](URL)** (Publisher) — what this *specifically* adds for the pillar.

<!-- page-type: overview -->
```

The fixed order is:
**H1 + tagline → callout → lead → `---` → `## Where this breaks in production` → one or more
real core-concept sections → `## Going deeper` (links every deep-dive + connects outward) → `---` →
`## Sources` → `## Read more` *(optional)* → `<!-- page-type: overview -->`.** Section *titles* are yours
to choose — write the ones the topic needs; the spine above is the rhythm, not a fill-in form.

## Linking every deep-dive is load-bearing

The one structural rule the verifier enforces for an overview, because it is what keeps a growing chapter
wired together:

- **The overview must link to at least one deep-dive in its directory.** A hub with no spokes is flagged.
- **It must link *every* deep-dive in the directory.** A `*.md` in `docs/<pillar>/` the overview does not
  link to is an **orphan** (verifier error `orphan-page`). When you add a deep-dive, link it here in the
  same change — in the prose or the "Going deeper" list.
- **Presentation is prose, not a status table.** Links are full sentences a reader follows as a path; the
  verifier checks that the link exists, not its format, so there is no reason to fall back to an index
  table — and never a "Status" column (that is the root README's job).

## How a deep-dive relates back (breadcrumb)

Each deep-dive page (a `standard` page under `docs/<pillar>/`) opens with a one-line breadcrumb up to
this hub:

```markdown
> Part of **[<Pillar> overview](README.md)**
```

This is meaningful chapter navigation, **not** the forbidden generic back-link to the root README (that
rule is about the landing page, not chapter hubs). A deep-dive missing its breadcrumb is a warning, not
an error — but add it.

## Inherited content rules

This template adds a shape; it does not replace the rules in [CONTRIBUTING.md](../CONTRIBUTING.md) or the
spine in [page-template.md](page-template.md):

- **Every number/claim needs a source link.** No source → drop the number.
- **Order of magnitude, not false precision** — label figures as ballpark.
- **Be terse** — one sharp sourced sentence beats three. The overview is long because it is *complete*,
  not because it is padded.
- **Neutral on tools** — name them as examples, never promote.
- **Links stay inside the repository and are relative.** Never link from a repository page to the tooling layer
  (`research-toolkit/`, `research/`, `.claude/`, `tools/`).

## Sources

- **[page-template.md](page-template.md)** (this repo) — the standard spine this overview shape extends.
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** (this repo) — the content rules this template carries.

<!-- page-type: standard -->
