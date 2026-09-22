# Independent review evidence for sharp simplex orthant projections

This directory accompanies an independent review of
[`../sharp_simplex_orthant_projections`](../sharp_simplex_orthant_projections).
The checker targets the placement and completeness reductions that are least
covered by the producer's explicit-lift certificate.

It expands `sum_i max(|w_i|,c_i)<=2` directly, enumerates its exact rational
vertices, and computes low-dimensional volumes from supporting facets. It
checks strict midpoint concavity for a nonuniform dimension-three parameter
and a nontrivial permutation, every exposed coordinate face including a zero
barycentric coordinate, nonvertex boundary strictness, planar parameters not
on the producer's denominator-six grid, and the exceptional one-dimensional
case.

Only the Python standard library and exact `fractions.Fraction` arithmetic
are used. From this directory run:

~~~sh
python3 verify_review.py > actual.json
cmp actual.json EXPECTED.json
python3 -O verify_review.py > actual-optimized.json
cmp actual-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
~~~

The finite checks do not prove the universal envelope realization,
Brunn--Minkowski equality criterion, or asymptotic theorem. Those are audited
as human mathematical premises in [`REVIEW.md`](REVIEW.md).
