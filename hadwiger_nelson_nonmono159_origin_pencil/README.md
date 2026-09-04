# All origin-centered double copies of the Parts 159 gadget are four-colorable

For the archived `v159e646` point set `A`, **every rotation or reflection `g`
fixing its published origin gives a four-colorable strict unit-distance graph
on `A union g(A)`**. This includes arbitrary angles and rotations outside
the previously four-colored complex field `E=Q(sqrt(-3),sqrt(-11))`.

This closes a fixed-origin family with at most 317 vertices. It does not
cover different shared vertices, arbitrary translations, or three copies,
and it produces no improvement to the 509-vertex record.

[PROOF.md](PROOF.md) gives the complete reduction. For a rotation multiplier
outside `E`, each new cross edge forces an irreducible quadratic over `E`.
Pairs with the same quadratic are exactly its complete cross-edge set.
The finite census contains 1,490 rotation classes and 1,377 reflection
classes, representing 5,734 labeled isometries. All are colored using a
640-byte library of four component colorings. Angles with no new cross edge
are settled by gluing at the origin; multipliers in `E` are settled by the
previous field-coloring theorem.

## Reproduce

From this directory, using Python 3.11 or later:

```bash
python3 census.py > /tmp/nonmono159-origin-census.json
cmp expected.json /tmp/nonmono159-origin-census.json
python3 audit.py > /tmp/nonmono159-origin-audit.json
cmp expected_audit.json /tmp/nonmono159-origin-audit.json
python3 check_example.py > /tmp/nonmono159-origin-example.json
cmp expected_example.json /tmp/nonmono159-origin-example.json
sha256sum -c SHA256SUMS
```

Only the Python standard library is required. Tested with CPython 3.11.2.
All entry points fail on invalid evidence. The main verifier reconstructs
the strict component graph and checks every class against the explicit
library. `audit.py` imports no main implementation and compares canonical
hashes of all pair classifications and edge partitions, using a different
field representation and normalization. `check_example.py` reconstructs
four actual radical-coordinate unions without the quadratic reduction.

Key results:

| Quantity | Verified value |
|---|---:|
| Component vertices / strict edges | 159 / 646 |
| Nonzero pairs examined per parity | 24,964 |
| Outside-field quadratic classes | 2,867 |
| Outside-field isometries with a new cross edge | 5,734 |
| Maximum new cross edges | 20 |
| Uncovered classes | 0 |

The canonical edge-partition SHA-256 is
`9c01c9e8419cce17660e32a3a683908b69900f8415c3df1be2e4a47d00fe8a70`.
Further hashes and the complete cross-edge histogram are in `expected.json`.

## Inputs and trust

The checker reuses hash-pinned `points159.tsv` from
`../hadwiger_nelson_nonmono159_214_lowden2/` and the small exact arithmetic
module `coloring.py` from `../hadwiger_nelson_nonmono_field_obstruction/`.
Both are included in `SHA256SUMS`. The latter directory's proved coloring
theorem is a mathematical dependency for multipliers in `E`.

All four coloring strings are published; no solver is required to verify
them. The universal quantifier over angles rests on the unformalized
completeness proof. Finite evidence uses exact rational or integer arithmetic,
not numerical geometry. No large generated artifact is required or omitted.

The method builds on the standard spindling/constrained-coloring approach
described in [Parts' paper](https://arxiv.org/abs/2010.12665). The specific
finite exclusion is the contribution; no priority claim is made for its
general algebraic or coloring mechanisms.
