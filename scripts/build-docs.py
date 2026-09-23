#!/usr/bin/env python3
"""Render Cubware build guides (markdown) into styled landing-page HTML.

Usage: python3 scripts/build-docs.py [path/to/Cubware]
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CUBWARE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent.parent / "Cubware"
DOCS_SRC = CUBWARE / "documentation"
OUT = ROOT / "docs"
GITHUB = "https://github.com/Ursa-Laboratories/Cubware/tree/main"

GUIDES = [
    {
        "src": "vial-capper-decapper-build.md",
        "out": "vial-capper-decapper-build.html",
        "title": "Vial Capper / Decapper Build Guide",
        "eyebrow": "Build guide · CubXL+ / PANDA",
        "description": "Build the PANDA vial capper / decapper: BOM, magnetic cap fabrication, vial holder setup, Arduino wiring, and firmware notes.",
    },
    {
        "src": "opentrons-pipette-setup.md",
        "out": "opentrons-pipette-setup.html",
        "title": "Opentrons OT-2 Pipette Setup Guide",
        "eyebrow": "Build guide · CubXL+ / PANDA",
        "description": "Mount and wire an Opentrons OT-2 electronic pipette on a Cub gantry: BOM, printed parts, Arduino / TMC2209 control path, and commissioning steps.",
    },
]

TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{description}" />
    <title>{title} | Ursa Laboratories</title>
    <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg" />
    <link rel="stylesheet" href="../styles.css" />
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CFM3B0DT2P"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-CFM3B0DT2P');
    </script>
  </head>
  <body>

    <header class="site-header">
      <a class="brand" href="../index.html" aria-label="Ursa Laboratories — home">
        <img class="brand-mark" src="../assets/favicon.svg" alt="" aria-hidden="true" />
        <span>Ursa Labs</span>
      </a>
      <nav class="site-nav" aria-label="Primary">
        <a href="../index.html#instruments">Instruments</a>
        <a href="../index.html#compare">Hardware</a>
        <a href="../index.html#software">Software</a>
        <a href="../build.html" aria-current="page">Build It</a>
        <a href="https://github.com/Hydra-Laboratories/CubOS" target="_blank" rel="noopener">GitHub</a>
      </nav>
      <a class="btn btn-primary btn-nav" href="../index.html#airtable">Get in touch</a>
    </header>

    <main id="top">
      <article class="section build doc" aria-labelledby="doc-title">
        <nav class="doc-breadcrumb" aria-label="Breadcrumb">
          <a href="../build.html">Build It</a>
          <span aria-hidden="true">/</span>
          <span>Build guides</span>
        </nav>
        <div class="section-heading narrow">
          <p class="eyebrow">{eyebrow}</p>
          <h1 id="doc-title">{title}</h1>
          <p>{lede}</p>
          <p class="doc-source">
            Source: <a href="{source_url}" target="_blank" rel="noopener">{source_name}</a> in the Cubware repository.
          </p>
        </div>

        <div class="doc-layout">
          <aside class="doc-toc" aria-label="On this page">
            <p class="cad-group-label">On this page</p>
            <ol>
{toc}
            </ol>
          </aside>
          <div class="doc-body">
{body}
          </div>
        </div>
      </article>
    </main>

    <footer class="site-footer">
      <p>Ursa Laboratories — self-driving laboratories for autonomous materials discovery.</p>
      <nav class="site-footer-links" aria-label="Footer">
        <a href="https://github.com/Hydra-Laboratories/CubOS" target="_blank" rel="noopener">GitHub</a>
        <a href="../build.html">Build It</a>
        <a href="../index.html#airtable">Contact</a>
      </nav>
      <p class="site-footer-copyright">&copy; 2026 Ursa Labs. All rights reserved.</p>
    </footer>
  </body>
</html>
"""


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def rewrite_links(md_text):
    # Relative repo paths (../cubxl_plus/..., 3D-prints/...) -> GitHub URLs
    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith("../"):
            target = f"{GITHUB}/{target[3:]}"
        return f"[{label}]({target})"

    md_text = re.sub(r"\[([^\]]+)\]\((\.\./[^)]+)\)", repl, md_text)
    md_text = md_text.replace("](images/", "](../assets/docs/")
    return md_text


def render(guide):
    text = (DOCS_SRC / guide["src"]).read_text()
    # Drop the H1: the page template supplies it.
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = "\n".join(lines).strip()

    # First paragraph becomes the lede.
    lede_md, _, rest = text.partition("\n\n")
    lede_html = markdown.markdown(rewrite_links(lede_md))
    lede = re.sub(r"^<p>|</p>$", "", lede_html.strip())

    md = markdown.Markdown(extensions=["tables", "toc"], extension_configs={"toc": {"slugify": lambda v, s: slug(v), "toc_depth": "2-2"}})
    body = md.convert(rewrite_links(rest))
    # Wrap tables so wide BOMs scroll instead of breaking the layout.
    body = body.replace("<table>", '<div class="doc-table-wrap"><table>').replace("</table>", "</table></div>")
    body = body.replace("<a href=\"http", "<a target=\"_blank\" rel=\"noopener\" href=\"http")
    body = "\n".join("            " + l if l else l for l in body.splitlines())

    toc = "\n".join(
        f'              <li><a href="#{t["id"]}">{t["name"]}</a></li>' for t in md.toc_tokens
    )

    html = TEMPLATE.format(
        title=guide["title"],
        eyebrow=guide["eyebrow"],
        description=guide["description"],
        lede=lede,
        source_url=f"{GITHUB}/documentation/{guide['src']}".replace("/tree/", "/blob/"),
        source_name=f"documentation/{guide['src']}",
        toc=toc,
        body=body,
    )
    (OUT / guide["out"]).write_text(html)
    print(f"wrote docs/{guide['out']}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for g in GUIDES:
        render(g)
