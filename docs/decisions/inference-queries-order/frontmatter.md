---
resolves: inference-queries-order-matters
title: Use YAML front matter section for SPARQL files
---

For example:

```yaml
depends-on: some_other_query.sparql
```

By these dependencies, the system would deduce the proper order of the queries; then, it would run the queries in the specified order.
