---
name: VAGUE_IMPORTS_BLACKLIST
value:
  $container: $set
  $value:
  - dumps
  - safe_load_all
  - parse
  - read
  - load
  - dump
  - write
  - safe_dump
  - load_all
  - safe_load
  - loads
  - dump_all
  - safe_dump_all
---

List of vague method names that may cause confusion if imported as is: