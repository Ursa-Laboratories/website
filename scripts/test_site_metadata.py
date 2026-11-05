import json
import re
import unittest
import xml.etree.ElementTree as ET
from site_metadata import BASE, ROOT, enhance_html, text_only


class SiteMetadataTests(unittest.TestCase):
    def test_sitemap_and_pages_agree(self):
        tree = ET.parse(ROOT / "sitemap.xml")
        urls = [node.text for node in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        pages = [ROOT / "index.html", ROOT / "build.html", ROOT / "cubware.html", *sorted((ROOT / "docs").glob("*.html"))]
        self.assertEqual(len(set(urls)), len(pages))
        for path in pages:
            relative = path.relative_to(ROOT).as_posix()
            html = path.read_text()
            canonical = BASE + ("/" if relative == "index.html" else "/" + relative)
            self.assertIn(canonical, urls)
            self.assertEqual(html.count('rel="canonical"'), 1)
            self.assertIn(f'href="{canonical}"', html)
            self.assertEqual(html.count('scripts/analytics.js?v=1'), 1)
            self.assertNotIn('googletagmanager.com', html)
            self.assertEqual(enhance_html(html, relative), html, relative)
            graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
            self.assertEqual(graph['@graph'][0]['url'], canonical)

    def test_faq_schema_matches_visible_answers(self):
        html = (ROOT / "index.html").read_text()
        graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])['@graph']
        questions = next(item for item in graph if item['@type'] == 'FAQPage')['mainEntity']
        visible = re.findall(r'<article class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.S)
        self.assertEqual(len(questions), 4)
        self.assertEqual([(item['name'], item['acceptedAnswer']['text']) for item in questions],
                         [(text_only(question), text_only(answer)) for question, answer in visible])

    def test_order_and_local_image(self):
        html = (ROOT / "index.html").read_text()
        sections = re.findall(r'<section id="([^"]+)"', html)
        self.assertEqual(sections[:3], ['liquid-handling', 'compare', 'instruments'])
        self.assertIn('Lab automation anyone can afford.', html)
        self.assertNotIn('Built by Ursa Laboratories', html)
        self.assertTrue((ROOT / 'assets/cub-xl-liquid-handling.png').is_file())


if __name__ == '__main__':
    unittest.main()
