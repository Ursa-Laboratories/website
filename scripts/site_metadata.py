"""Keep static page metadata, shared analytics, and crawl discovery in sync.

Run: python3 scripts/site_metadata.py
Documentation generators also call this after rendering their pages.
"""
import json
import re
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.ursalabs.ai"
START = "<!-- Ursa site metadata -->"
END = "<!-- /Ursa site metadata -->"


class PageInfo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def text_only(markup):
    return " ".join(unescape(re.sub(r"<[^>]+>", "", markup)).split())


def enhance_html(html, relative_path):
    html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    # Replace the existing inline GA snippet, rather than configuring it twice.
    html = re.sub(r"[ \t]*<!-- Google tag \(gtag\.js\) -->\s*<script\b[^>]*>.*?</script>\s*<script\b[^>]*>.*?</script>\s*", "", html, flags=re.S)
    info = PageInfo()
    info.feed(html)
    if not info.title or not info.description:
        raise ValueError(f"Missing title or description: {relative_path}")
    home = relative_path == "index.html"
    url = BASE + ("/" if home else "/" + relative_path)
    prefix = "../" if relative_path.startswith("docs/") else ""
    image = BASE + "/assets/cub-xl-liquid-handling.png"
    page = {
        "@type": "WebPage", "@id": url + "#webpage", "url": url,
        "name": info.title, "description": info.description, "inLanguage": "en",
        "isPartOf": {"@id": BASE + "/#website"},
        "publisher": {"@id": BASE + "/#organization"},
    }
    graph = [page]
    if home:
        graph.extend([
            {"@type": "Organization", "@id": BASE + "/#organization", "name": "Ursa Labs",
             "alternateName": "Ursa Laboratories", "url": BASE + "/",
             "logo": BASE + "/assets/ursa-wordmark.svg", "email": "alex@ursalabs.ai",
             "description": "Affordable lab automation, automated pipetting, and custom instrumentation."},
            {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
             "name": "Ursa Labs", "publisher": {"@id": BASE + "/#organization"}},
        ])
        # Derive answers from visible copy so structured data cannot silently drift.
        questions = []
        for question, answer in re.findall(r'<article class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</article>', html, flags=re.S):
            questions.append({"@type": "Question", "name": text_only(question),
                              "acceptedAnswer": {"@type": "Answer", "text": text_only(answer)}})
        if questions:
            graph.append({"@type": "FAQPage", "@id": BASE + "/#faq", "isPartOf": {"@id": url + "#webpage"}, "mainEntity": questions})
    elif relative_path.startswith("docs/"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ursa Labs", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Build guides", "item": BASE + "/build.html"},
            {"@type": "ListItem", "position": 3, "name": info.title.split(" | ")[0], "item": url},
        ]})
    title = escape(info.title, quote=True)
    description = escape(info.description, quote=True)
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    block = f'''{START}
    <link rel="canonical" href="{url}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Ursa Labs" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{image}" />
    <meta property="og:image:width" content="1774" />
    <meta property="og:image:height" content="887" />
    <meta property="og:image:alt" content="Cub XL liquid handler with a mounted pipette and labware deck" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image}" />
    <meta name="twitter:image:alt" content="Cub XL liquid handler with a mounted pipette and labware deck" />
    <script type="application/ld+json">{schema}</script>
    <script defer src="{prefix}scripts/analytics.js?v=1"></script>
{END}
'''
    return html.replace("</head>", block + "</head>", 1)


def update_site(root=ROOT):
    pages = [root / "index.html", root / "build.html", root / "cubware.html", *sorted((root / "docs").glob("*.html"))]
    urls = []
    for path in pages:
        relative = path.relative_to(root).as_posix()
        original = path.read_text()
        updated = enhance_html(original, relative)
        if updated != original:
            path.write_text(updated)
        urls.append(BASE + ("/" if relative == "index.html" else "/" + relative))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{escape(url)}</loc></url>\n" for url in urls)
    (root / "sitemap.xml").write_text(sitemap + "</urlset>\n")
    (root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    return len(pages)


if __name__ == "__main__":
    print(f"Updated metadata and sitemap for {update_site()} pages.")
