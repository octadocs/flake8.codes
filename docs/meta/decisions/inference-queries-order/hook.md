---
$id: pre-build-hook
title: Create a Python hook to run before site is going to build
resolves:
    - sparql-is-not-enough-for-inference
---

This should be another hook in `mkdocs-macros-plugin`.

In a pluglet, we will create a `def on_before_build()` function which will then be able to run arbitrary Python code, including calls to SPARQL.
