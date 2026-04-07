# PANDA Landing Page

A pure static one-page landing page for PANDA, a BU-endorsed self-driving laboratory platform for autonomous materials discovery.

## Files

- `index.html` — page structure and professor-facing copy.
- `styles.css` — responsive styling and placeholder presentation.
- `README.md` — replacement notes and guardrails.

## Replace the Airtable placeholder

When the Airtable form is ready, replace the placeholder block inside `section#airtable` in `index.html` with the iframe Airtable provides, for example:

```html
<iframe src="https://airtable.com/embed/..." title="PANDA lab interest form"></iframe>
```

Keep the section id as `airtable` so the hero and footer CTAs continue to work.

## Replace media placeholders

Replace the video and image placeholder cards in `section#media` with approved PANDA product media:

- Demo/platform video.
- CNC gantry / deck image.
- 96-well workflow image.
- Characterization or optimization-results image.

Use descriptive `alt` text for real images and keep the media section from overwhelming the functionality section.

## Boston University wording and assets

Approved text-only wording for this first page:

- “BU-endorsed technology developed at Boston University.”
- “Developed at Boston University.”

Do **not** add BU logos, seals, or official visual brand assets unless approved assets are provided. Do **not** add stronger legal/affiliation language such as “official partnership,” “licensed by BU,” or “Boston University-backed” without explicit later approval.

## Static scope and migration triggers

Keep this version static. Reconsider a minimal Vite app if the site becomes multi-page, needs reusable components, adds analytics-heavy or interactive behavior, requires repeated media state management, or needs a formal build pipeline.

## Local verification

Serve locally:

```bash
python3 -m http.server 4173
```

Open `http://localhost:4173`, then verify against `.omx/plans/test-spec-panda-landing-page.md`.
