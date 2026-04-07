---
slug: panda-landing-page
created_utc: 20260407T192201Z
source_spec: .omx/specs/deep-interview-panda-landing-page.md
context_snapshot: .omx/context/panda-landing-page-20260407T190820Z.md
interview: .omx/interviews/panda-landing-page-20260407T191553Z.md
consensus_mode: RALPLAN-DR short
consensus_status: approved_with_improvements_applied
---

# RALPLAN Consensus Plan: PANDA Professor-Facing Landing Page

## Consensus Result
- Planner: favored pure static HTML/CSS landing page.
- Architect: APPROVE with improvements.
- Critic: APPROVE with required final-plan improvements.
- Applied improvements: README/guardrail notes, Vite migration triggers, tighter BU wording guardrails, no-full-nav verification, responsive visual verification gates.

## RALPLAN-DR Summary

### Principles
1. **Simple first version:** one page, minimal files, no framework unless justified.
2. **Professor-facing credibility:** technical, concise, academic/research-lab tone.
3. **Conversion-oriented:** primary path guides visitors to the Airtable section.
4. **Constraint-safe BU wording:** text-only BU endorsement/developed-at-BU wording; no logos/seals.
5. **Placeholder-friendly:** missing media/Airtable URL must not block delivery.

### Decision Drivers
1. Fast greenfield delivery with no unnecessary dependencies.
2. Clear professor/lab conversion flow toward Airtable.
3. Accurate technical positioning without overclaiming or expanding scope.

### Viable Options

#### Option A — Pure static HTML/CSS landing page (chosen)
- Files: `index.html`, `styles.css`, optional/likely `README.md`.
- Pros: smallest dependency footprint, easy to host, easy to edit, aligns with one-page scope.
- Cons: no built-in bundler/dev server, less structured if the site grows.

#### Option B — Minimal Vite app
- Pros: standard dev/build workflow, better if future interactivity/components arrive.
- Cons: adds dependency/tooling overhead not necessary for this first one-page scope.

#### Option C — Next.js/React app
- Pros: appropriate for larger multi-page marketing/app site.
- Cons: over-scoped for this single landing page and introduces unnecessary dependencies.

## ADR

### Decision
Build the first PANDA landing page as a pure static one-page site using `index.html`, `styles.css`, and likely `README.md` guardrails/replacement notes.

### Drivers
- Empty greenfield workspace.
- One-page landing page scope.
- No unnecessary dependencies.
- Primary purpose is professor-facing positioning and Airtable conversion.
- Missing media and Airtable URL should not block the first version.

### Alternatives considered
- Pure static HTML/CSS: chosen for simplicity and dependency avoidance.
- Minimal Vite: rejected for now; use only if migration triggers appear.
- Next.js/React: rejected as over-scoped.

### Why chosen
Static HTML/CSS satisfies the clarified acceptance criteria with the smallest maintainable surface area and lowest implementation overhead. It supports polished responsive design and a clear Airtable conversion flow without adding framework complexity.

### Consequences
- Verification relies on local static serving and manual checklist rather than build scripts.
- Future expansion may require migration to Vite if scope grows.
- Media and Airtable remain placeholder-based until the user provides real assets/URL.

### Follow-ups
- Replace Airtable placeholder with the real embed URL.
- Replace media placeholders with approved video/images.
- Revisit framework choice if migration triggers appear.
- Confirm legal/brand wording before adding any official BU assets or stronger claims.

## Implementation Plan

### Step 1 — Create minimal static files
Create:
- `index.html`
- `styles.css`
- `README.md` (replacement notes and guardrails)

Use semantic sections:
- `header.hero`
- `section#media`
- `section#functionality`
- `section#airtable`

A minimal text brand plus CTA is acceptable. Do not add multi-link full company navigation.

### Step 2 — Build hero and conversion path
Add:
- Professor-facing headline.
- Subheadline describing autonomous materials discovery and the robotics/fluid/electrochemistry/optical/AI loop.
- Text-only credibility line: “BU-endorsed technology developed at Boston University.”
- Primary CTA to `#airtable`.
- Optional secondary CTA to learn more on-page.

Avoid unless later approved:
- “official partnership”
- “licensed by BU”
- “Boston University-backed”
- BU logos or seals

### Step 3 — Add media placeholder section
Add a professional media section with:
- One video placeholder.
- Two or three image placeholders for platform, 96-well workflow, and characterization/results.
- Clear replacement notes that do not look broken.

### Step 4 — Add functionality section
Add short cards or grid content for:
- Robotic experimentation.
- Integrated measurement loop.
- AI/Bayesian experiment selection.
- 96-well plate throughput.
- Structured data generation.
- Modular/extensible hardware integrations.

### Step 5 — Add Airtable embed placeholder
Add `section#airtable` with:
- CTA copy inviting professors to share lab interest.
- Airtable embed placeholder if no real URL is available.
- Clear instructions in `README.md` for replacing the placeholder with Airtable iframe later.

### Step 6 — Responsive polish
Ensure:
- Hero CTA visible above the fold on desktop.
- Airtable section reachable from CTA on mobile.
- Media section does not overwhelm functionality.
- Typography/spacing/contrast are credible and professor-facing.

### Step 7 — Verify
Use the test spec at `.omx/plans/test-spec-panda-landing-page.md`.

## Acceptance Criteria
See `.omx/plans/prd-panda-landing-page.md` and `.omx/plans/test-spec-panda-landing-page.md` for full criteria. Key checks:
- Single page only.
- Required four sections present.
- CTA routes to Airtable.
- PANDA technical copy coverage complete.
- No full nav, booking calendar, pricing, Airtable field design, or BU logos/seals.
- Placeholders render intentionally.
- Responsive visual gates pass.

## Risks and Mitigations
1. **BU wording overclaim risk** — Use only approved text-only wording; prohibit logos/seals and stronger legal/partnership phrasing unless later approved.
2. **Generic placeholder risk** — Use intentional placeholder cards labeled around PANDA workflows.
3. **Incomplete Airtable risk** — Treat placeholder as an integration point and keep CTA flow testable.
4. **Static-page growth risk** — Migrate to Vite if multi-page, reusable component, analytics-heavy, interactive, or repeated asset-state needs emerge.
5. **Consumer-flashy tone risk** — Anchor copy in professor/lab language: throughput, structured data, Bayesian optimization, modular hardware, 96-well experimentation.

## Available-Agent-Types Roster
- `executor` — implement static landing page files.
- `designer` — refine visual hierarchy, layout, responsive polish.
- `writer` — polish professor-facing copy and README guidance.
- `test-engineer` — convert acceptance criteria into verification checklist if needed.
- `verifier` — run final claim validation and completion evidence.
- `code-reviewer` — review final diff for maintainability and scope control.
- `security-reviewer` — likely unnecessary unless embeds/scripts or third-party tracking are added.
- `git-master` — commit/PR packaging if requested.

## Follow-up Staffing Guidance

### Recommended `$ralph` path
Use `$ralph .omx/plans/ralplan-panda-landing-page.md` for a single-owner execution loop.
- Lane 1: `executor` / high — create `index.html`, `styles.css`, `README.md`.
- Lane 2: `verifier` / high — validate against PRD and test spec after implementation.
- Optional: `designer` / high — visual polish if first pass is too plain.

This is the preferred execution mode because the scope is small and tightly coupled.

### Optional `$team` path
Use `$team .omx/plans/ralplan-panda-landing-page.md` only if speed or parallel polish is more important than overhead.
Suggested lanes:
- `executor` / high — file implementation.
- `designer` / high — visual style and responsive polish guidance.
- `writer` / high — final professor-facing copy and README text.
- `verifier` / high — acceptance/test-spec validation.

## Launch Hints

Sequential:
```text
$ralph .omx/plans/ralplan-panda-landing-page.md
```

Coordinated team:
```text
$team .omx/plans/ralplan-panda-landing-page.md
```

OMX CLI team-style hint if using shell runtime:
```bash
omx team --task "Implement .omx/plans/ralplan-panda-landing-page.md with executor, designer, writer, verifier lanes; keep scope static HTML/CSS/README only unless a blocker requires escalation."
```

## Team Verification Path
Before shutdown, team execution should prove:
1. `index.html`, `styles.css`, and README/notes exist as planned.
2. Static page renders under local server.
3. PRD criteria pass.
4. Test spec content/prohibited-content checks pass.
5. Visual responsive gates pass at desktop and mobile widths.
6. No framework/dependency scaffold was added unless explicitly justified.

If team mode is used, a later Ralph/verifier pass should re-check final output against `.omx/plans/test-spec-panda-landing-page.md` and collect final evidence.

## Changelog: Improvements Applied from Reviews
- Added README/guardrail file guidance.
- Added explicit Vite migration triggers.
- Tightened BU wording prohibitions.
- Added no-full-nav verification rule.
- Added responsive visual acceptance gates.
