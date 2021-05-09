---
name: MAGIC_METHODS_BLACKLIST
value:
  $container: $set
  $value:
  - __delattr__
  - __del__
  - __reduce__
  - __delete__
  - __reduce_ex__
  - __delitem__
  - __dir__
---

List of magic methods that are forbidden to use.