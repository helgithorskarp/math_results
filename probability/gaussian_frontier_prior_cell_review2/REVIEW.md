# Review verdict

**Verdict: accept, in the stated scope.**  At Gaussian variance one, the
target proves its all-threshold hinge comparison for every source law in the
specified seven-box measure cell, every target law in the target box, and
every prior in the six-dimensional simplex with each outer mass at least
`21/156`.  The strict middle-window bound is independently reproduced.

## Exact object reviewed

- Target commit: `c1b17b8459a0221279becd8f6da20a9b269ba54a`.
- Discovery Net reference:
  `bafkreidsn7klheuvguoiqbidjjinu4xj56lltx6cjybhly7oju45r5fbva`.
- Six target/dependency files are content-pinned by `TARGET_INPUTS.json`.
- The target certificate itself passes under both ordinary and optimized
  Python, and its own checksum manifest passes.

## Independently established facts

The prior set has the exact vertex decomposition

`p_0 = (30/156) lambda_0`,
`p_i = 21/156 + (30/156) lambda_i` for `i=1,...,6`.

Because the target density is fixed and `z -> (z-u)_+` is convex, the source
hinge at every threshold is bounded by the corresponding convex combination
of seven vertex hinges.  Symmetry leaves one central-residual vertex and one
outer-residual orbit of size six.

The independent checker reconstructs the central vertex on 246,905 full
octahedral orbits.  For the asymmetric outer-heavy vertex it keeps the first
coordinate explicit and only quotients `(y,z)` by signs and interchange,
giving 1,449,225 representatives.  This is a different decomposition from
the target's distinguished-coordinate split.  Both decompositions are checked
against direct unquotiented enumeration on a small grid.  At 56-bit dyadic
precision, each vertex computation covers all 11,390,625 lattice sites.

Using independent positive-series reciprocal bounds for exponentials, an
independent `atan(1/2)+atan(1/3)` enclosure for the Gaussian normalizing
constant, and a definition-level suffix hinge sweep, the final cell bounds
are:

- central residual:
  `-13409404008890948606105227083833657172946624001 /
   2923003274661805836407369665432566039311865085952`;
- outer residual:
  `-149394601641564051743976265760459884420199515823 /
   23384026197294446691258957323460528314494920687616`.

Both are strictly below `-1/256`.  The checker also independently verifies
the low-threshold clipping argument, the `2217/3200 < 7/10` peak bound, the
`3777/4096` uniform pair-loss floor, the count `C(36,6)=1,947,792`, and the
inherited rank-six determinant `-2105/16777216`.

## Checker guarantees and assumptions

`independent_check.py` proves the finite rational inequalities represented in
`REVIEW_EXPECTED.json`, including outward rounding, complete lattice
coverage, the maximum over every knot in `[1/256,7/10]`, quadrature and tail
errors, and the diffuse-measure transfer loss `7/1024`.  Python integer and
`fractions.Fraction` semantics, the pinned file bytes, and the mathematical
derivation of the midpoint/quadrature estimate remain trusted inputs.

The analytic audit separately checks the measure reductions used around the
finite certificate: Gaussian translation total variation is at most
`|v|/sqrt(2 pi) < |v|/2`; centering the target and integrating its directional
second derivative gives total variation at most `E|Y-EY|^2/4 <= 3/1024`;
and the opposite-pair `cosh` lower bound gives the stated low-threshold source
floor.  No coupling between the source and target laws is assumed by the
hinge comparison.

## Limits

This accepts one explicit open cell at variance one.  It does not establish
the full dimension-three Gaussian-convolution majorisation frontier, an
all-variance statement, or any novelty claim.  The rank-six example shows a
42-dimensional local family after including the six prior coordinates; it is
not a classification of all admissible laws.
