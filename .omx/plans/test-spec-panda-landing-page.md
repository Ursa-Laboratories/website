---
slug: panda-landing-page
created_utc: 20260407T192201Z
source_spec: .omx/specs/deep-interview-panda-landing-page.md
context_snapshot: .omx/context/panda-landing-page-20260407T190820Z.md
interview: .omx/interviews/panda-landing-page-20260407T191553Z.md
consensus_mode: RALPLAN-DR short
consensus_status: approved_with_improvements_applied
---

# Test Spec: PANDA Professor-Facing Landing Page

## Verification Strategy
Because the consensus-favored implementation is pure static HTML/CSS, verification should use local static serving plus a manual content, layout, and constraint checklist. If an execution agent intentionally chooses a framework instead, it must run that framework’s build/lint/typecheck commands and document the reason for deviating from the static plan.

## Static File Verification
- Confirm only minimal landing-page files are added, expected:
  - `index.html`
  - `styles.css`
  - `README.md` (optional/likely for replacement notes and guardrails)
- Confirm no package/dependency scaffold is added unless explicitly justified.

## Local Render Verification
Run:
```bash
python3 -m http.server 4173
```
Open:
```text
http://localhost:4173
```

## Functional Checks
1. Hero CTA links to `#airtable` or the final Airtable section id.
2. Bottom/repeated CTA links to the same Airtable section.
3. Airtable placeholder renders as an intentional styled integration block if no real embed URL is present.
4. No booking calendar exists.
5. No full/multi-link company navigation exists. A minimal text brand + CTA header is acceptable; multi-link company nav is not.

## Content Checks
Confirm page copy mentions:
- BU-endorsed technology developed at Boston University.
- Self-driving laboratory platform.
- Autonomous materials discovery.
- CNC gantry robot.
- Integrated fluid handling.
- Electrochemistry.
- Optical characterization.
- AI orchestration.
- Bayesian optimization.
- Hundreds of experiments / 96-well plates.
- No-human-intervention / overnight operation.
- Clean structured data.
- Optimal synthesis conditions.
- Modular/extensible support for potentiostats, pipetting systems, and characterization tools.

## Prohibited Content Checks
Confirm absent:
- BU logo/seal/official brand assets.
- “Official partnership.”
- “Licensed by BU.”
- “Boston University-backed.”
- Pricing section.
- Booking calendar.
- Airtable field/content design.
- Deep technical whitepaper structure.

## Visual / Responsive Checks
Check desktop, tablet, and mobile widths:
1. Hero CTA remains visible above the fold on desktop.
2. CTA still reaches Airtable section on mobile.
3. Media placeholders do not dominate the page before the functionality section.
4. Text remains readable and spacing remains coherent.
5. Placeholder video/images look intentional, not broken.
6. Color contrast is acceptable for body text and CTAs.
7. Focus states and links are keyboard-visible enough for a simple static page.

## README / Replacement Note Checks
If `README.md` is added, confirm it documents:
- How to replace the Airtable placeholder with a real embed iframe.
- How to replace media placeholders with approved product video/images.
- Do not add BU logos/seals unless approved assets are provided.
- Migration triggers for Vite if the site grows beyond static scope.
