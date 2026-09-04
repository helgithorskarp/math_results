# Independent review of the Parts-159 fixed-origin pencil

Verdict: **accepted and verified**.  For the archived Parts `v159e646` point
set `A`, every rotation or reflection fixing its published vertex-0 origin
gives a four-colorable strict unit-distance graph on `A union g(A)`.

This is a universal exclusion of one continuous family, with at most 317
vertices.  It does not cover a different shared vertex, a translated second
copy, or three copies, and it produces no sub-509 five-chromatic graph.

Reviewed Discovery Net artifact:
`bafkreidwmyhtgkd37doecn6dx7b4nj5cdhnaqr3clkrdxic5zhcg25ztta`, source commit
`faab6a8027555c2a842c1f051e314867a2e3f32f`.

## Completeness audit

Write `R=Q(sqrt(33))` and `E=R(alpha)` with `alpha^2=-3`.  Every
origin-fixing isometry has one of the forms `g(z)=uz` and
`g(z)=u conjugate(z)`, with `|u|=1`; the latter is handled by replacing the
second labeled point set with `conjugate(A)`.

The three-way split is exhaustive.  If `u` lies in `E`, both copies lie in
`E` and the previously verified four-coloring of the whole field applies.  If
`u` lies outside `E`, a nonzero overlap `a=ub` would put `u=a/b` in `E`, so
the origin is the sole overlap.  With no new cross edge, any two component
colorings can be permuted to agree there.

For the remaining branch, a new cross edge from `a` to `ub` gives

```text
c = conjugate(a)b,
S = |a|^2 + |b|^2 - 1,
Delta = 4|a|^2|b|^2 - S^2,
c u^2 - S u + conjugate(c) = 0.
```

This follows by expanding the distance equation and using
`u conjugate(u)=1`.  A unit solution requires `Delta>=0`; when this holds the
two roots `(S +/- sqrt(-Delta))/(2c)` have unit modulus.  The double-root case
lies in `E`.  For positive `Delta`, `sqrt(-Delta)` lies in `E` exactly when
`Delta/3` is a square in `R`: a square root of a negative real element must be
`alpha*y`, with `y` in `R`.

When that square test fails, the monic quadratic over `E` is irreducible.
Two pair-derived quadratics sharing an outside-`E` root must be identical by
uniqueness of the monic minimal polynomial.  Hence all labeled pairs with the
same quadratic are exactly the full new cross-edge set for either of its two
distinct unit roots.  Conversely every pair in the class is an edge at both
roots.  This proves that the finite classes cover the continuous angular
family, rather than sampling it.

The exact sign and square tests are correct.  For `x+y sqrt(33)`, sign reduces
to rational signs and comparison of `x^2` with `33y^2`.  Squareness follows
from the rational square norm `(p^2-33q^2)^2` and reconstruction from
`p^2=(x +/- sqrt(x^2-33y^2))/2`; the zero second coefficient is handled by
the two pure cases.

## Finite reproduction

The target checksum audit, main census, separately represented arithmetic
audit, and four direct radical-coordinate examples all reproduce exactly.
The main verifier checks the four published component colorings on all 646
strict internal edges and checks an explicit color-permutation witness for
every outside-field class.  Thus the SAT solver used to discover two library
rows is not a proof dependency.

`independent_census.py` imports no target implementation module.  It rebuilds
`E` as nested pairs in `Q(sqrt(33))[alpha]/(alpha^2+3)`, parses the hash-pinned
coordinates, reconstructs the strict graph and component coloring library,
and independently derives the monic polynomial of every nonzero labeled pair.
It agrees on all 24,964 pairs in each parity:

```text
negative Delta       2,937
roots in E          12,906
outside-E pairs      9,121
```

It recovers 1,490 rotation classes and 1,377 reflection classes, representing
5,734 isometries, with 2,866 distinct labeled cross-edge sets across the two
parities.  Every separate histogram bin and both canonical stream hashes
match the target.  A direct search through the four rows and six
origin-fixing color permutations finds a positive witness for every class;
the independent witness stream is hash-pinned in `EXPECTED_OUTPUT.txt`.

The previously published independent field-coloring audit was rerun and also
passed, covering the essential `u in E` branch.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_nonmono159_origin_pencil_review3/independent_census.py \
  | cmp - hadwiger_nelson_nonmono159_origin_pencil_review3/EXPECTED_OUTPUT.txt
cd hadwiger_nelson_nonmono159_origin_pencil_review3
sha256sum -c SHA256SUMS
```

Python 3.11 or later and the standard library suffice.

## Trust boundaries

The in-field branch imports the separately reviewed 2-adic four-coloring of
`E`.  The finite branch trusts the hash-pinned Parts coordinates, the four
explicit coloring strings, exact CPython integer/fraction semantics, and the
reviewed and independent implementations.  The passage from all angles to
the finite quadratic census is an ordinary unformalized algebraic proof, not
a proof-assistant development.  No approximate geometry, solver verdict, or
omitted large certificate is used.  The theorem says nothing about other
shared vertices or arbitrary translations.
