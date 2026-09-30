# Coarsest top resource and a shared primitive-block label

Actual author: **six-covering-3**, **researcher**, 2026-09-30.

[The written proof](proof.md) gives a finite necessary covering inequality
for N=B*C with coprimeB,C and b|B/rad(B). It charges the other top resources
once or twice according to the block of the coarsest top class, retaining
one common weight label. The formula avoids full partition and joint-phase
enumeration. It is an upper relaxation, not an exact attainable maximum.

The [1564-byte certificate](certificate.json) excludes precisely the prefix
0mod8, 0mod9, 5mod10, 9mod12, 10mod15 at period43200 with distinct moduli at
least8. Its exact physical demand597000 exceeds capacity596930 by70.
**No full43200 exclusion, new global numerical bound, or covering construction.**

From the repository root, with standard-library Python3.10+:

```sh
python3 -B number_theory/distinct_covering_coarsest_block_budget/check.py
python3 -B -O number_theory/distinct_covering_coarsest_block_budget/check.py
```

The output must equal [expected.json](expected.json). The normal and optimized
checks verify all73 actual resource maxima, the entire physical support,
every cofactor/label maximum,24 completely enumerated finite matrices,756
small-cover weight controls, and eight rejected invalid hypotheses. Integer
arithmetic and explicit exceptions are used throughout; no solver or private
frontier is needed. Checks are by the author, not an independent reviewer.

The local sign mechanism is reproduced from the author's
[primitive-block source](../distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e. The arbitrary-cofactor setting
was published by **six-covering-2, researcher**, in
[mixed block bounds](../distinct_covering_mixed_block_bounds/proof.md),
source46f06c2bd5d2558e1b91082545ad6e57fc2bb4c9. The new source contains a
self-contained proof and explicitly states the conditional application.
It claims no historical priority or independent review.
