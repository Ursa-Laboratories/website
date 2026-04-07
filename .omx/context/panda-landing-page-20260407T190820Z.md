# Deep Interview Context Snapshot: PANDA Landing Page

## Task statement
Create a simple one-page company landing page for a productized PANDA self-driving laboratory platform, geared toward professors.

## Desired outcome
A catchy landing page that explains the platform, shows video/images, describes functionality, and includes an embedded Airtable.

## Stated solution
One-page landing website with sections: hero/catchy positioning, video + pictures, written functionality section, and final embedded Airtable.

## Probable intent hypothesis
The user wants an academic/professor-facing marketing page that can introduce the company and convert interested research labs into inquiries/leads while establishing credibility around PANDA’s Boston University origins and autonomous materials discovery capabilities.

## Known facts/evidence
- PANDA is a self-driving laboratory platform developed at Boston University for autonomous materials discovery.
- It combines a CNC gantry robot with integrated fluid handling, electrochemistry, optical characterization, and AI orchestration.
- It runs hundreds of experiments in 96-well plates with no human intervention.
- It uses Bayesian optimization to select each next experiment based on prior results.
- The product goal is a turnkey modular/extensible self-driving lab for materials science and chemistry labs.
- Target audience: professors.
- Desired page content includes video/pics, functionality copy, and an embedded Airtable.

## Repository/codebase context
- `omx explore` was attempted first but failed because cargo / omx-explore harness is unavailable.
- Fallback filesystem inspection found no application source files, no `package.json`, and no `public`, `app`, `pages`, or `src` files at current depth; only `.omx` runtime files are present.
- Context type is therefore treated as greenfield in an empty landing-page workspace.

## Constraints
- Deep-interview mode must not implement directly.
- No new dependencies without explicit request if/when execution begins.
- Final execution should preserve a simple, one-page scope unless clarified otherwise.

## Unknowns/open questions
- Primary conversion action and Airtable purpose/content.
- Brand/company name, tone, and any required credibility/legal phrasing.
- Whether Boston University affiliation needs careful wording/disclaimer.
- Exact non-goals and what OMX may decide autonomously.
- Whether media assets already exist or placeholders should be used.

## Decision-boundary unknowns
- Can OMX choose the page framework/tooling from scratch?
- Can OMX write marketing copy and section names without approval?
- Can OMX use placeholders for video/images/Airtable if assets/embed URL are not yet available?
- Can OMX decide visual style/branding, or must it follow an existing identity?

## Likely touchpoints after handoff
- Create project scaffolding if no app exists.
- Add one-page landing content and styling.
- Add media placeholders or asset references.
- Add configurable Airtable embed placeholder or actual embed URL.
