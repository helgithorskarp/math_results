# Sharp symbolic-power bands for residual cycle arrangements

Take `n>=7` projective lines with no three concurrent. Keep their pairwise
intersections except those corresponding to a disjoint union of cycles
on all line labels. Let `I` be the ideal of the kept points, `F` the product
of all line equations, and `c` the number of missing cycles.

The first nonzero degrees of the symbolic powers are

    alpha(I^(2k))=kn,       alpha(I^(2k+1))=kn+n-3.

More strongly, for `0<=r<n-6`,

    (I^(2k))_(kn+r)       = F^k S_r,
    (I^(2k+1))_(kn+n-3+r) = F^k I_(n-3+r).

The width is sharp: powers of an adjoint give counterexamples at the
next offset `r=n-6`. The odd minimum space has dimension `c`, with one
explicit component-adjoint basis element per missing cycle. For the
side lines of a convex polygon, `c=1`; the minimum forms are unique up
to scale. The Waldschmidt constant is `n/2`.

[PROOF.md](PROOF.md) gives the complete proof, scope and sharp boundary
examples. [SOURCES.md](SOURCES.md) credits the classical Wachspress adjoint
and Kohn--Ranestad's multiplicity-two rigidity. Our contribution is the
sharp all-multiplicity range and disjoint-cycle description, with
search-relative novelty only. This is a special-configuration result,
not a resolution of Nagata's conjecture.

## Reproduce

From this directory, with CPython 3.11+ and its standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands must emit exactly [expected.json](expected.json),
ending in `"status": "VERIFIED"`. Runtime is about 15 seconds per run
on the development machine, using under 30 MiB of reported process RSS.

The checker builds projective Hasse-jet interpolation matrices directly
from the point sets. It certifies 94 vector spaces over `Q` on eight
fixtures, checks all 16 first-failure forms, and exercises the `n=5,6`
boundaries. Fixtures include disconnected missing cycles and points at
infinity. Negative controls reject triple concurrency, malformed cycles,
a removed vanishing condition, and confusion between simple and double
zeros. A digest records the exact component adjoints, and another the
space audit. No exhaustive classification of coordinate arrangements is
claimed or needed.

The dimension certification combines integer matrix rank modulo the
verified prime `1000003` with rational independent kernel vectors whose
membership is checked over the integers. Rank modulo a prime alone
would not suffice: the matching rational witness supplies the other
inequality. The checker does not use the Bezout recursion to determine
the full higher-multiplicity kernel dimension. It uses no solver,
floating point, randomness, external dataset or algebra-system package.

The universal result rests on the written proof. Ordinary unformalized
proof and interpreter trust remain; independent review is pending.
