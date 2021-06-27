---
$included:
    $id: pre-build-hook
    resolves: site-is-slow
---

One of the operations which takes too long is the second application of OWL RL after SPARQL queries. If that is not necessary (for example, because these queries do not add any triples that cause OWL RL to infer other triples) - then we can omit it. That can save us a few minutes of generation time.
