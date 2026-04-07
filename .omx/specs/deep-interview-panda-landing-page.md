# Deep Interview Spec: PANDA Landing Page

## Metadata
- Profile: standard
- Context type: greenfield
- Rounds: 6
- Final ambiguity: 14.8%
- Threshold: 20%
- Context snapshot: `.omx/context/panda-landing-page-20260407T190820Z.md`
- Interview transcript: `.omx/interviews/panda-landing-page-20260407T191553Z.md`

## Context
The repository at `/Users/alexchan/Documents/hephaestus/landing-page` is an empty greenfield workspace except for `.omx` runtime files. `omx explore` was attempted first but failed because the local cargo / omx-explore harness is unavailable; fallback filesystem inspection found no app source, `package.json`, `src`, `app`, `pages`, or `public` directory.

## Intent
Create a simple, professor-facing company landing page that introduces and commercializes PANDA as a BU-endorsed self-driving laboratory platform for autonomous materials discovery.

The page should make professors understand that PANDA can compress materials discovery workflows from manual weeks/months into autonomous days by combining a CNC gantry robot, integrated fluid handling, electrochemistry, optical characterization, and AI/Bayesian optimization in 96-well plate experimentation.

## Desired Outcome
A catchy one-page landing page that persuades professors and research labs to fill out the embedded Airtable form.

## Audience
- Primary: professors / principal investigators in materials science, chemistry, electrochemistry, polymer synthesis, and adjacent autonomous experimentation domains.
- Secondary: research lab decision-makers evaluating self-driving lab infrastructure.

## In Scope
- One-page landing page only.
- A strong hero section with a professor-facing value proposition and Airtable-focused call-to-action.
- A video-and-pictures section using placeholders if real media assets are absent.
- A written functionality section describing the system’s core capabilities:
  - CNC gantry robot
  - integrated fluid handling
  - electrochemistry
  - optical characterization
  - AI orchestration
  - Bayesian optimization for next-experiment selection
  - 96-well plate experimentation
  - overnight/no-human-intervention autonomous operation
  - structured data generation
  - modular/extensible hardware integrations (potentiostats, pipetting systems, characterization tools)
- An Airtable embed section or clearly marked placeholder; Airtable field/content design is out of scope.
- Text-only BU-forward credibility wording such as “BU-endorsed technology developed at Boston University.”
- Clean, polished, academic/technical visual style chosen autonomously by the implementation agent.

## Out of Scope / Non-goals
- No full company navigation or multi-page company site.
- No booking calendar or scheduling integration.
- No Airtable form field/content design; the user will handle the Airtable itself.
- No BU logos, seals, or trademarked visual assets unless the user provides approved assets later.
- No pricing section unless explicitly requested later.
- No deep technical whitepaper or exhaustive scientific validation page unless explicitly requested later.

## Decision Boundaries
The implementation agent may decide without further confirmation:
- Framework/tooling for this greenfield landing page, while avoiding unnecessary dependencies.
- Visual style and layout.
- Section headings and marketing copy.
- CTA wording and placement.
- Placeholder treatment for video/images and Airtable embed.
- Text-only BU endorsement/developed-at-BU language.

The implementation agent should not decide without later user input:
- Real Airtable embed URL or Airtable form fields/content.
- Use of BU logos/seals/official brand assets.
- Formal legal/licensing claims beyond the user-stated “BU endorsed” and “developed at Boston University” wording.

## Constraints
- Keep the first version simple and one-page.
- No new dependencies unless clearly justified by the chosen framework or already inherent to scaffolding.
- Prefer editable static content and straightforward structure.
- Use placeholders for missing video/images/Airtable URL rather than blocking.
- Tone should be professor-facing: credible, technical, concise, and benefit-oriented rather than consumer-flashy.

## Acceptance Criteria
1. The landing page is a single-page website.
2. The primary CTA points users toward the Airtable section/form.
3. The page includes the required content sequence:
   - catchy hero/value proposition
   - video + picture/media area
   - written functionality/capability section
   - Airtable embed/placeholder section
4. Copy accurately reflects the provided PANDA summary:
   - BU-endorsed / developed at Boston University
   - self-driving laboratory for autonomous materials discovery
   - CNC gantry robot + fluid handling + electrochemistry + optical characterization + AI orchestration
   - 96-well plates and hundreds of experiments
   - Bayesian optimization for next-experiment selection
   - productized turnkey platform for materials science/chemistry labs
   - modular/extensible support for different lab hardware
5. The page avoids out-of-scope elements: full nav, booking calendar, Airtable field design, BU logos/seals.
6. Missing media or Airtable embed URL is handled with tasteful placeholders and replacement notes.
7. The result is professor-facing, readable, responsive, and visually polished enough for a simple first landing page.
8. Verification includes at minimum build/lint/typecheck appropriate to the chosen stack plus a manual content checklist against this spec.

## Assumptions Exposed + Resolutions
- Assumption: Airtable conversion requires deciding form fields. Resolution: form fields/content are out of scope; user will handle Airtable.
- Assumption: BU wording should be conservative. Resolution: user says the platform is BU endorsed, but approved boundary is text-only wording and no BU logos/seals unless assets are provided.
- Assumption: implementation may choose copy/style. Resolution: user grants autonomy over all landing-page design/copy decisions.

## Pressure-pass Findings
The initial conversion goal was “fill out Airtable.” The pressure pass asked what Airtable should collect. The user clarified not to worry about Airtable and that they will handle it. Therefore, downstream planning should treat the Airtable as an embed/placeholder target, not a form-design task.

## Brownfield Evidence vs Inference Notes
- Evidence: workspace contains only `.omx` runtime files; no application files were found by fallback filesystem inspection.
- Evidence: `omx explore` failed because cargo / harness was unavailable.
- Inference: this is a greenfield landing-page project and can be scaffolded if execution proceeds.
