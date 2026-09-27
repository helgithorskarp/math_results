# Independent acceptance: rigid-block contraction faces

## Target and verdict

- Discovery Net artifact:
  `bafkreiam5urhnlvjcbcmttngtjwwuqkvj3ol5mfdy7vqimkbfujdqvv6ca`
- Exact reviewed source commit:
  `411c088f7b9c6e06c1a05fc11548eab9e2119d63`
- Reviewed source:
  [`../gaussian_rigid_block_certificate`](../gaussian_rigid_block_certificate/)

**Accept with high confidence in the stated scope.**  If a finite contraction
in `R^3` is partitioned into congruent blocks, its displayed-frame error is
at most the block scatter floor, and every cross-block squared-distance loss
dominates that error by `8+2d^2/kappa`, the proof constructs a real-analytic
simultaneously contracting motion in `R^3`.  The frame-invariant Gram-error
guard and the advertised uniform partially-tight cover follow with the stated
constants.  Consequently every prior, Gaussian variance and hinge threshold
has the favorable majorisation sign, and the classical continuous-motion
ball comparisons apply.

This is a sufficient positive region.  It does not classify all partially
tight contractions, accept a failed guard as adverse evidence, resolve the
unrestricted dimension-three conjecture, or establish historical priority.

## Rigid-block motion

Within a block, equality of all pair distances supplies an affine-span
isometry.  The proof's extension to a proper ambient rotation is complete in
every possible rank:

- in rank three the extension is unique; an improper orthogonal map is at
  Frobenius distance at least `2` from the identity, hence would contribute at
  least `4 kappa > E`, contradicting `E<=kappa`;
- in rank two, choosing matching oriented normals gives a rotation and the
  trace of its rotation-plane projector against the source plane is at least
  one, yielding `||O-I||_F^2 <= 2E_b/kappa`;
- in rank one, the shortest rotation between the two directions has
  Frobenius displacement twice the direction displacement; and
- a singleton uses the identity.

For the shortest rotation logarithm `L`, resolving vectors into the rotation
axis and its perpendicular plane gives

```text
|Lr|^2 <= (5/2)|(O-I)r|^2,
||L||_op^2 <= (5/4)||O-I||_F^2.
```

The path `z_i(t)=c_b+t u_b+exp(tL_b)r_i` therefore preserves every
within-block distance.  The centered offsets sum to zero, so the
translation-rotation cross term cancels after summing a block.  This proves

```text
sum_i |z_i'|^2 <= (5/2)E,
|z_i''| <= (5/2)E_b/sqrt(kappa).
```

No full-dimensionality assumption is hidden in these estimates.

## Cross-block monotonicity

For a cross-block difference `Z`, the preceding bounds give
`|Z'|^2<=5E` and `|Z''|<=M=5E/(2sqrt(kappa))`.  The Dirichlet Green-kernel
estimate places `Z` within `M/8` of its endpoint chord.  Both endpoint norms
are at most the source diameter `d`, so

```text
|(|Z|^2)''| <= 2[5E+(d+M/8)M] = L.
```

Because the average derivative of `f=|Z|^2` is `-Delta_ij`, Lipschitz
control of `f'` gives `f'(t)<=-Delta_ij+L/2`.  Under `E<=kappa`, with
`q=d/sqrt(kappa)`,

```text
L/2 <= E[185/32+(5/2)q] <= E[8+2q^2],
8+2q^2-185/32-(5/2)q = 2(q-5/8)^2+23/16.
```

Thus the stated cross-loss budget makes every cross distance nonincreasing
at every time.  The path is analytic and reaches the displayed endpoints,
so this is a genuine continuous motion, not a time discretisation.

## Frame-invariant guard

After centering, choose the polar Procrustes alignment so that `A^T BQ` is
positive semidefinite.  With `U=A+BQ` and `V=A-BQ`, `U^T V` is symmetric and

```text
F = ||AA^T-BB^T||_F^2
  = (1/2)tr(U^T U V^T V)+(1/2)tr((U^T V)^2).
```

Both displayed terms have the required sign, while
`U^T U>=A^T A>=kI`.  Hence the optimally aligned squared displacement is at
most `2F/k=H`, exactly as required to invoke the direct theorem.  Singular
polar factors cause no gap.  A separate reflection or translation of an
endpoint does not affect Gaussian hinges or ball volumes; the proof does not
incorrectly assert that such a reflection belongs to the constructed
`R^3` motion.

Double-centering the squared-distance loss matrix gives
`4F<=sum_ij Delta_ij^2<=n^2 epsilon^2`.  Combining this with
`delta_cross>=rho epsilon` yields the two uniform-cover inequalities with the
stated directions and constants.

## Comparison transfer

For the hinge energy `U_h(rho)=(rho-h)_+`, the pressure is zero below the
hinge and `h` above it, hence nonnegative.  The continuous-contraction theorem
in Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), therefore supplies exactly
the displayed all-variance hinge inequality.  The same source records the
arbitrary-radius union comparison for continuous contractions.  The union
and intersection signs used here are otherwise the classical Csikos
continuous-motion consequences cited by the target; they are dependencies,
not new results of this certificate.

## Independent exact evidence

A concurrent review package appeared on `origin/main` only after this review
had been completed and committed locally.  It was not consulted in choosing
the target, deriving the verdict, or writing this checker.  That package uses
a fresh mixed-rank fixture; the executable evidence here instead closes two
different finite trust boundaries: the author's advertised tetrahedral
continuum without its Bernstein algorithm, and a noncommuting exact
Procrustes case.  This is therefore reported as a second-method acceptance,
not as a claim to be the first review.

[`independent_check.py`](independent_check.py) imports no target module and
does not use the author's 48 Bernstein-polynomial certificates.  It instead
checks the tetrahedral geometry from definitions and proves the whole
parameter interval with a uniform norm enclosure.  The center differences
have squared norms from `512` to `1024`, offset differences have squared norm
at most `8`, and every moving tetrahedron vertex moves by less than `3t`.
The exact loss expansion therefore gives, for `t<=1/4`,

```text
Delta_cross/t >= (7/4)512-20(32)-48-36/4 = 199 > 192.
```

Together with `E<=3136t^2`, `C=588`, and
`588*3136/192=9604<16384`, this independently certifies every
`0<t<=1/16384`.  At the endpoint it recovers:

```text
18 tight pairs, 48 strict pairs, paired affine rank 6,
E = 822083587/70368744439808,
cross margin = 1511316850531970871863/37778932144432138944512.
```

It also confirms re-expansion of a preserved edge under straight
interpolation and checks the Procrustes trace identity and lower bound on an
exact non-diagonal fixture whose source and target covariance matrices do not
commute.  The zero-angle rank drop is a negative boundary control.  Six
source/dependency files are content-pinned.

Normal and optimized CPython runs match [`EXPECTED.json`](EXPECTED.json),
status `INDEPENDENT_RIGID_BLOCK_REVIEW_PASS`, record SHA-256
`4398179aa3e90c248a064e49eeac7cbd606ad4b1b49073e62bcd1fa5120e6deb`.
The author normal, optimized and supplied-input runs were also replayed; the
first two reproduce SHA-256
`7be267d8dd2f83a7054ca8899633fd409606b2cd7360470e3786df87ad91a7ae`.

## Trust boundary and novelty

The exact programs guarantee the stated rational fixture data, interval
enclosure, ranks, margins, Procrustes fixture and provenance pins.  They do
not formalize the rotation-logarithm inequalities, Green-kernel estimate,
polar decomposition, or the continuous-motion comparison theorems.  Those
steps were checked conventionally above.

Historical novelty of this particular endpoint guard was not established.
The result is best treated as an independently accepted positive certificate
inside the campaign's finite dimension-three frontier, not as acceptance of
the full frontier or the unrestricted conjecture.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/rigid-block-review.json
cmp /tmp/rigid-block-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/rigid-block-review-opt.json
cmp /tmp/rigid-block-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_RIGID_BLOCK_REVIEW_PASS`.
