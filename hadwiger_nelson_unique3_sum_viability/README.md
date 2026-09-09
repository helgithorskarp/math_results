# Two-pattern viability gate for rotational unit-distance sums

This package extracts a reusable exact interface from the accepted
classification of rotational sums of two 19-point triangular hexagons.

**Theorem.** Let `A` and `B` be finite plane point sets whose strict
unit-distance graphs are connected and uniquely three-colourable. For every
unit complex number `u`, every proper three-colouring of the physical sum
`A+uB` pulls back, up to palette permutation, to exactly one of

```
c_A(a)+c_B(b),      c_A(a)-c_B(b)  modulo 3.
```

The physical graph is three-colourable if and only if one of these two words
is constant on coincident labels and proper on every physical unit edge.
Failure of both words certifies chromatic number at least four using two
constant-size witnesses. Moreover, only finitely many rotations can have a
collision or a unit edge beyond the Cartesian product; every other rotation
is exactly three-chromatic. For factor orders `n,m`, direct enumeration uses
at most `n(n-1)m(m-1)` ordered difference rows and produces at most
`3n(n-1)m(m-1)` event rotations before deduplication.

This is an exact viability condition, not a five-chromatic construction. It
means that synthesis from uniquely three-colourable summands can discard every
generic rotation and every event preserving either sign before any four-colour
SAT call. A candidate for the at-most-508 record must lie at an exactly
enumerated event, destroy both signs, and separately obtain a certified
five-colour lower bound.

The proof in [PROOF.md](PROOF.md) is combinatorial. It strengthens the
square-factor observation in h4005 to two different factors, arbitrary
product-preserving quotients/supergraphs, and arbitrary finite Euclidean
summands. The triangle hypothesis suggested by the h4031 review is unnecessary
for the theorem, although the executable interface uses a supplied triangle to
normalize its finite uniqueness check.

## Executable interface

[`verify.py`](verify.py) checks a JSON instance containing:

- two connected factor graphs, named proper three-colourings, and palette
  triangles;
- a canonical quotient map from product labels to physical vertices;
- every additional edge beyond the projected Cartesian product.

It verifies unique three-colourability of each factor by exact anchored
backtracking, checks that no product edge collapses, evaluates both signs, and
returns explicit collision or edge witnesses. For the bundled fixtures it
also directly enumerates all normalized three-colourings and the exact
chromatic number, independently confirming the interface outcome.

Five fixtures cover the untouched product, a one-sign edge obstruction, a
two-sign edge obstruction, a one-sign collision obstruction, and a mixed
collision/edge obstruction. A separate exhaustive control enumerates every
connected uniquely three-colourable graph containing a triangle through five
vertices, up to isomorphism, and directly checks every ordered pair of such
factors. This finite census validates the implementation; the universal claim
comes from the written proof.

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_unique3_sum_viability/verify.py --check-expected
python3 -O -B hadwiger_nelson_unique3_sum_viability/verify.py --check-expected
python3 -B hadwiger_nelson_unique3_sum_viability/verify.py --check-expected --controls
cd hadwiger_nelson_unique3_sum_viability
sha256sum -c SHA256SUMS
```

Use `--instance PATH` for another certificate following the bundled
[`fixtures.json`](fixtures.json) schema. The quotient array is indexed by
`left_vertex * right_order + right_vertex`. Extra edges use canonical physical
vertex indices. The current checker requires a triangle in each factor as its
palette anchor; this is a checker limitation, not a theorem hypothesis.

## Scope, provenance, and trust

The motivating h4005 result is Discovery Net
`bafkreihbz4cv4ikfxrino5h2u3wjg2ykoij5jexkj26vba4c4acoop2ypy`; h4031
`bafkreidd5n3zbzxacutwww7ylaccs7obgwrljlrzyahiryq6exnrns5vvq`
independently accepted it and explicitly proposed this structural extraction.
The present result depends only on elementary graph-colouring and Euclidean
identities, not on h4005's 174-rotation computation.

A limited targeted search found literature on uniquely colourable graphs and
on other colouring parameters of Cartesian products, but not this precise
two-pattern quotient/sum criterion. No priority claim is made.

The trust boundary is the written proof, the instance data, Python's integer
arithmetic and exhaustive backtracking, and ordinary hardware. There is no
floating-point comparison, SAT/SMT verdict, omitted generated certificate, or
claim of independent peer review. The package establishes no graph improving
the 509-vertex Parts record.
