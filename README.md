# SDE Foundations

Static Markdown documentation. The original notes live in `content/`. Pandoc
renders the Markdown and MathML, and the build adds navigation and a local
search index. Browser storage records personal study levels.

## Regenerate the site

Requirements are Pandoc and Python 3 with lxml. Run `python3 scripts/build.py`
from the project root, then serve the generated `dist/` folder. Sites deploys
that directory as a private static site. The original Markdown is checked in
separately and stays the source of truth.
