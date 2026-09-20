# Mixed three-table Honeymoon Oberwolfach types at order 21

There is a Honeymoon Oberwolfach schedule for every type

```text
[a,b,2],  a+b=19,  a>=b>=3.
```

Equivalently, all seven 21-couple instances with exactly three tables and
exactly one table of size four have solutions:

```text
HOP(32,6,4),  HOP(30,8,4),  HOP(28,10,4), HOP(26,12,4),
HOP(24,14,4), HOP(22,16,4), HOP(20,18,4).
```

The directory contains compact cyclic certificates.  A definition-level
checker expands each certificate into all 40 meals, checks the required
table sizes in every meal, and verifies multiplicity-one coverage of all 840
edges between different couples.

## Reproduce

Requirements: CPython 3.11 or later; no third-party package is used.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
sha256sum -c SHA256SUMS
```

The checker includes four malformed-certificate tests.  They remove a type,
repeat an edge, misdeclare a type, and flip one endpoint bit; every mutation
must be rejected.

## Scope and provenance

The `[16,3,2]` certificate reproduces the earlier isolated cyclic solution.
The other six certificates complete this natural order-21 slice.  The result
does not settle all order-21 types or the general Honeymoon Oberwolfach
conjecture.  The adjacent type `[17,2,2]`, which has two four-person tables,
is outside the stated “exactly one” class and is already covered by Rinaldi's
one-arbitrary-table family.

Jerade and Šajna prove all HOP instances through 20 couples and develop the
cyclic starter framework used here.  Rinaldi gives the family with one
arbitrary even table and all other tables of size four.  Akbari's 2026
generalized-HOP papers concern additional two-person tables and do not supply
this ordinary three-round-table classification.  Targeted searches found no
published theorem for the six new types; novelty is search-relative and no
historical-priority claim is made.

## Evidence boundary

The theorem relies on the 294 stored external edges (42 per type), JSON
decoding, the transparent schedule expansion in `verify.py`, exact Python
integer/set operations, CPython, and ordinary runtime/hardware behavior.  It
does not rely on the randomized discovery search, a solver, floating point,
an external dataset, or an omitted certificate.

## References

- D. Lepine and M. Šajna, *On the Honeymoon Oberwolfach Problem*, Journal of
  Combinatorial Designs 27 (2019), 420–447,
  <https://doi.org/10.1002/jcd.21656>.
- M. R. Jerade and M. Šajna, *A solution to small cases of the honeymoon
  Oberwolfach problem*, JCMCC 128 (2026), 97–118; preprint
  <https://arxiv.org/abs/2407.00204>.
- G. Rinaldi, *The Oberwolfach problem with loving couples*, Journal of
  Combinatorial Designs (2024), <https://doi.org/10.1002/jcd.21946>.
- M. Akbari, *On the Generalized Honeymoon Oberwolfach Problem*,
  <https://arxiv.org/abs/2603.05736>.
