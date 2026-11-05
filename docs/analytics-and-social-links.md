# Website analytics and campaign links

Use these URLs in your social profiles, posts, newsletters, and messages. They all open the Ursa homepage. GA4 records the source, medium, campaign, and placement. Existing measurement ID: `G-CFM3B0DT2P`.

## Copyable links

| Placement | URL |
| --- | --- |
| LinkedIn | [https://www.ursalabs.ai/?utm_source=linkedin&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=linkedin&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| Substack newsletter | [https://www.ursalabs.ai/?utm_source=substack&utm_medium=email&utm_campaign=always_on&utm_content=newsletter](https://www.ursalabs.ai/?utm_source=substack&utm_medium=email&utm_campaign=always_on&utm_content=newsletter) |
| Substack website | [https://www.ursalabs.ai/?utm_source=substack&utm_medium=referral&utm_campaign=always_on&utm_content=article](https://www.ursalabs.ai/?utm_source=substack&utm_medium=referral&utm_campaign=always_on&utm_content=article) |
| Substack Notes | [https://www.ursalabs.ai/?utm_source=substack&utm_medium=social&utm_campaign=always_on&utm_content=notes](https://www.ursalabs.ai/?utm_source=substack&utm_medium=social&utm_campaign=always_on&utm_content=notes) |
| Instagram | [https://www.ursalabs.ai/?utm_source=instagram&utm_medium=social&utm_campaign=always_on&utm_content=bio](https://www.ursalabs.ai/?utm_source=instagram&utm_medium=social&utm_campaign=always_on&utm_content=bio) |
| Facebook | [https://www.ursalabs.ai/?utm_source=facebook&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=facebook&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| X / Twitter | [https://www.ursalabs.ai/?utm_source=twitter&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=twitter&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| Threads | [https://www.ursalabs.ai/?utm_source=threads&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=threads&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| Bluesky | [https://www.ursalabs.ai/?utm_source=bluesky&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=bluesky&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| YouTube | [https://www.ursalabs.ai/?utm_source=youtube&utm_medium=video&utm_campaign=always_on&utm_content=description](https://www.ursalabs.ai/?utm_source=youtube&utm_medium=video&utm_campaign=always_on&utm_content=description) |
| TikTok | [https://www.ursalabs.ai/?utm_source=tiktok&utm_medium=social&utm_campaign=always_on&utm_content=bio](https://www.ursalabs.ai/?utm_source=tiktok&utm_medium=social&utm_campaign=always_on&utm_content=bio) |
| Reddit | [https://www.ursalabs.ai/?utm_source=reddit&utm_medium=social&utm_campaign=always_on&utm_content=post](https://www.ursalabs.ai/?utm_source=reddit&utm_medium=social&utm_campaign=always_on&utm_content=post) |
| Mastodon | [https://www.ursalabs.ai/?utm_source=mastodon&utm_medium=social&utm_campaign=always_on&utm_content=profile](https://www.ursalabs.ai/?utm_source=mastodon&utm_medium=social&utm_campaign=always_on&utm_content=profile) |
| Pinterest | [https://www.ursalabs.ai/?utm_source=pinterest&utm_medium=social&utm_campaign=always_on&utm_content=pin](https://www.ursalabs.ai/?utm_source=pinterest&utm_medium=social&utm_campaign=always_on&utm_content=pin) |
| GitHub | [https://www.ursalabs.ai/?utm_source=github&utm_medium=referral&utm_campaign=always_on&utm_content=readme](https://www.ursalabs.ai/?utm_source=github&utm_medium=referral&utm_campaign=always_on&utm_content=readme) |
| Medium | [https://www.ursalabs.ai/?utm_source=medium&utm_medium=referral&utm_campaign=always_on&utm_content=article](https://www.ursalabs.ai/?utm_source=medium&utm_medium=referral&utm_campaign=always_on&utm_content=article) |
| Discord | [https://www.ursalabs.ai/?utm_source=discord&utm_medium=referral&utm_campaign=always_on&utm_content=community](https://www.ursalabs.ai/?utm_source=discord&utm_medium=referral&utm_campaign=always_on&utm_content=community) |
| Slack | [https://www.ursalabs.ai/?utm_source=slack&utm_medium=referral&utm_campaign=always_on&utm_content=community](https://www.ursalabs.ai/?utm_source=slack&utm_medium=referral&utm_campaign=always_on&utm_content=community) |
| Email signature | [https://www.ursalabs.ai/?utm_source=email_signature&utm_medium=email&utm_campaign=always_on&utm_content=signature](https://www.ursalabs.ai/?utm_source=email_signature&utm_medium=email&utm_campaign=always_on&utm_content=signature) |

## Name a specific campaign or post

Keep sources lowercase and consistent. Use `utm_campaign=always_on` for permanent profile links. For a launch or outreach campaign, replace it with a stable name such as `cub_demo_2026_11`. Replace `utm_content` with a placement or post ID, such as `founder_post_20261105`, `company_profile`, `newsletter_header`, or `newsletter_footer`. Use letters, numbers, underscores, hyphens, and dots. Never put names, emails, or other personal information in campaign tags.

Use `utm_medium=email` for the emailed Substack newsletter, `referral` for an article on its website, and `social` for Notes. Paid social ads should use `paid_social` and their own campaign name. Do not put UTM tags on links between pages of this website: GA4 handles navigation attribution.

## Where to read results

In GA4, open **Reports → Acquisition → Traffic acquisition**, then select **Session source / medium** and add **Session campaign**. This answers which sites and campaigns brought visits. In Explorations, combine those session dimensions with **Event name** to compare contact intent and engagement by source. `Session manual ad content` distinguishes the `utm_content` placements.

Custom events added by this site:

| Event | Meaning |
| --- | --- |
| `contact_cta_click` | Click to the Get in touch section, with the CTA's `section_id`. |
| `contact_form_start` | First edit to the contact form per page load. |
| `contact_email_draft_open` | A valid form attempts to open an email draft. It is not proof that an email was sent or received. |
| `email_click` | Direct click on an email link. |
| `section_view` | At least half of a section heading enters the viewport, once per page load. |
| `resource_click` | Click on a web resource or navigation link, with destination domain/path and section. |
| `demo_video_start` | Pipetting demo plays while at least half visible and the page is active. Includes autoplay. |
| `demo_video_progress` | Visible playback reaches 25%, 50%, and 75% of the video duration, once each per page load. |
| `demo_video_complete` | Visible playback accumulates one full video duration; looping playback can contribute. Not a unique full watch or a deliberate play click. |

The background hero video is excluded. Custom event payloads do not include contact names, email addresses, organizations, message text, or mailto bodies. Resource URLs omit query strings. Local previews queue events for inspection but do not load Google's collector.

## GA4 account setup and verification

The website code is configured; account settings are separate. In **Admin → Custom definitions**, create event-scoped custom dimensions for `section_id`, `link_path`, and `playback_type` if you want those breakdowns in reports. UTM source, medium, and campaign already have built-in dimensions. Consider marking `contact_email_draft_open` as a key event to measure contact intent; keep it distinct from a confirmed lead. None of these account changes has been applied by this code update.

Once the site is published, visit a tagged URL with `&analytics_debug=1` and check **Admin → DebugView**, or use Realtime. Confirm the correct source/campaign and trigger a contact CTA. The extra events require publication; the UTM links can work with the existing live GA4 tag. Do not include the debug parameter in shared links. Ad blockers and browser privacy settings can prevent collection.

## Search and answer engines

The site has factual HTML answers, Organization/WebSite/WebPage/FAQPage structured data, canonical URLs, social previews, and a sitemap covering public pages and guides. The metadata script derives FAQ schema from visible answers. These improve access and clarity; indexing, rankings, rich results, and AI citations are not guaranteed. No prices or unsupported product offers are encoded.

After publication, submit `https://www.ursalabs.ai/sitemap.xml` in Google Search Console and Bing Webmaster Tools, then inspect the homepage and a build guide. Those account submissions are not part of this code update.

After changing page titles, descriptions, FAQ copy, or adding a page, run:

```sh
python3 scripts/site_metadata.py
node --test scripts/analytics.test.cjs
python3 scripts/test_site_metadata.py
```

Both existing documentation generators refresh shared metadata and the sitemap automatically after rendering.

References: [Google campaign URLs](https://support.google.com/analytics/answer/10917952), [GA4 events](https://developers.google.com/analytics/devguides/collection/ga4/events), [enhanced measurement](https://support.google.com/analytics/answer/9216061), [Google AI search guidance](https://developers.google.com/search/docs/appearance/ai-features), [canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls).
