---
slug: panda-landing-page
created_utc: 20260407T192201Z
source_spec: .omx/specs/deep-interview-panda-landing-page.md
context_snapshot: .omx/context/panda-landing-page-20260407T190820Z.md
interview: .omx/interviews/panda-landing-page-20260407T191553Z.md
consensus_mode: RALPLAN-DR short
consensus_status: approved_with_improvements_applied
---

# PRD: PANDA Professor-Facing Landing Page

## 1. Problem / Opportunity
Professors and research labs need a fast way to understand why PANDA matters and how to express interest. PANDA is a BU-endorsed self-driving laboratory platform for autonomous materials discovery; the first landing page should communicate the value proposition clearly and route interested professors to an Airtable form without becoming a full company website.

## 2. Goal
Create a simple one-page landing page that persuades professors / principal investigators to fill out the Airtable form.

## 3. Primary Audience
- Professors and principal investigators in materials science, chemistry, electrochemistry, polymer synthesis, and adjacent autonomous-experimentation fields.
- Research lab decision-makers evaluating self-driving laboratory infrastructure.

## 4. Messaging Requirements
The page must communicate:
- PANDA is a BU-endorsed technology developed at Boston University.
- PANDA is a self-driving laboratory platform for autonomous materials discovery.
- PANDA combines a CNC gantry robot, integrated fluid handling, electrochemistry, optical characterization, and AI orchestration.
- PANDA runs hundreds of experiments in 96-well plates without human intervention.
- Bayesian optimization selects next experiments from prior results, compressing months of lab work into days.
- The productized version should be turnkey, modular, extensible, and useful beyond conductive polymer synthesis.
- Supported extension targets include different potentiostats, pipetting systems, and characterization tools.
- The system should help labs run overnight, generate clean structured data, and surface optimal synthesis conditions automatically.

## 5. Page Structure
1. **Hero / value proposition**
   - Text-only credibility line: “BU-endorsed technology developed at Boston University.”
   - Catchy professor-facing headline.
   - Concise technical subheadline.
   - Primary CTA to `#airtable`.
2. **Video and picture/media section**
   - One polished video placeholder.
   - Two or three image placeholders for platform, 96-well workflow, and results/characterization.
3. **Functionality / capabilities section**
   - Capability grid or cards for robotics, measurement, AI optimization, throughput, data, and modular integrations.
4. **Airtable section**
   - Airtable embed placeholder if no real URL exists.
   - CTA copy that invites professors to share lab interest through the form.

## 6. In Scope
- Greenfield static one-page landing page.
- Likely files: `index.html`, `styles.css`, and `README.md` for replacement notes/guardrails.
- Responsive visual polish for mobile/tablet/desktop.
- Placeholder treatment for missing media and Airtable URL.
- Text-only BU endorsement/developed-at-BU wording.

## 7. Out of Scope / Non-goals
- Full company navigation or multi-page website.
- Booking calendar or scheduling integration.
- Airtable form fields/content design; the user will handle Airtable.
- BU logos, seals, or official visual assets unless approved assets are provided later.
- Pricing section.
- Deep whitepaper-level scientific validation.

## 8. BU Wording Guardrails
Allowed text-only wording:
- “BU-endorsed technology developed at Boston University.”
- “Developed at Boston University.”

Do not add without later explicit approval:
- BU logos or seals.
- “Official partnership.”
- “Licensed by BU.”
- “Boston University-backed.”
- Any legal/licensing/trademark claim beyond the user-stated endorsement/origin.

## 9. Acceptance Criteria
1. A single `index.html` page renders the landing page.
2. `styles.css` provides responsive, polished styling.
3. Optional/likely `README.md` documents media replacement, Airtable embed replacement, BU asset restrictions, and static-to-Vite migration triggers.
4. Hero CTA links to the Airtable section anchor.
5. A repeated CTA near the bottom also routes to Airtable.
6. Required sections appear in order: hero, media, functionality, Airtable.
7. Required technical terms/capabilities are present in page copy.
8. Page uses text-only BU endorsement wording and no BU logos/seals.
9. Page does not include full company nav, booking calendar, pricing, or Airtable field design.
10. Missing media/Airtable URL appears as intentional placeholders, not broken embeds.
11. Hero CTA is visible above the fold on desktop.
12. Airtable section is reachable from CTA on mobile.
13. Media placeholders do not overwhelm or bury the functionality section.

## 10. Migration Triggers
Stay static for this version. Reconsider a minimal Vite app if any of these become true:
- The landing page becomes a multi-page site.
- Reusable components or repeated sections become necessary.
- Analytics-heavy or interactive behavior becomes central.
- Asset/media state management becomes repeated or complex.
- Formal build pipeline requirements outweigh the current dependency-free simplicity.
