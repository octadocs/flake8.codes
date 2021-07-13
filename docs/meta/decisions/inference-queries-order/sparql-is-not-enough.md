---
$id: sparql-is-not-enough-for-inference
$type: Problem
title: SPARQL is not enough for inference queries
---

Inference is not always easy to do with raw SPARQL. I am currently struggling to express a very simple transformation of data in SPARQL — it either doesn't work at all or has to be a very complex query with a few nesting levels. This is not what we'd want to see.

To the contrary, if I could run a SPARQL query, preprocess results in Python and then do another SPARQL query, this would have been simple, readable and easy to debug.
