---
$id: inference-queries-order-matters
$type: Problem
title: Inference queries order matters
---

Currently, we have SPARQL files in `inference` directory which are automatically executed when site is being built. We use them heavily to do subject domain specific reasoning (for example, to assign templates to pages).

We got into trouble when the number of inference queries grew to a dozen, and we found there are dependencies between them. One query must run before the other, otherwise nothing works.

This has proven to be notoriously hard to debug.
