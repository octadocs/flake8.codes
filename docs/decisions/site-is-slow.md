---
$id: site-is-slow
$type: Problem
title: flake8.codes is slow to build
---

`mkdocs build` or `mkdocs serve` command takes more than 15 minutes to complete building the site. This happens when we generate all available versions for `wemake-python-styleguide` and `flake8-bugbear` packages. That means the `docs` directory has almost 6900 Markdown files.

The MkDocs build process itself (if to turn off `octadocs` and `mkdocs-macros` plugins) takes about 5 minutes. Obviously, the remaining 10 minutes are occupied by Octadocs to load the graph and execute queries, and by Jinja2 to render macros in pages.
