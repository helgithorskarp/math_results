# Independent review: rigid blocks on partially tight faces

## Verdict

**Accepted, in the stated sufficient-criterion scope.** I independently
reviewed Discovery Net contribution
`bafkreiam5urhnlvjcbcmttngtjwwuqkvj3ol5mfdy7vqimkbfujdqvv6ca` at source
commit `411c088f7b9c6e06c1a05fc11548eab9e2119d63`. Its displayed-frame theorem,
frame-invariant corollary, uniform finite cover, and twelve-site calibration
are mathematically sound. The proof really constructs an analytic
simultaneous contraction in R3, including full-dimensional, planar,
collinear, and singleton rigid blocks.

This verdict does **not** accept the unrestricted dimension-three Gaussian
majorisation conjecture, classify all partially tight faces, or establish
historical novelty. A failed guard remains unresolved. The accepted statement
is a useful all-variance positive sector of the finite problem.

## Claim audited

For a finite contraction, partition the labels into at least two congruent
blocks, so all within-block squared-distance losses are zero. Let `kappa>0`
bound every positive eigenvalue of each nonsingleton block's unweighted
centered source scatter from below. With

```text
d^2 = maximum source squared distance,
E = sum_i |y_i-x_i|^2,
C = 8 + 2d^2/kappa,
delta_cross = minimum loss between different blocks,
```

the conditions `E<=kappa` and `delta_cross>=C E` imply an analytic
simultaneous contraction from the displayed source to target. The invariant
version replaces `E` by

```text
H = 2 ||AA^T-BB^T||_F^2 / k,
```

where the full centered source scatter obeys `A^T A >= k I`. The author then
deduces every probability-weight, variance, and threshold Gaussian hinge, as
well as the arbitrary-radius union and intersection signs. Finally, if
`epsilon` is the maximum loss and every cross loss is at least
`rho epsilon`, the two displayed uniform-cover inequalities imply the
invariant guard.

## Independent proof audit

### 1. Each block has a controlled proper rotation

Center a block and write its source offsets as `r_i`. Congruence gives a
linear isometry on their span. It admits an extension `O` in `SO(3)` with

```text
||O-I||_F^2 <= 2 E_b/kappa.
```

All affine dimensions are covered:

- In rank three the extension is unique. The scatter bound gives the sharper
  `kappa ||O-I||_F^2 <= E_b`. An improper orthogonal map in odd dimension has
  eigenvalue `-1`, hence squared Frobenius distance at least `4` from the
  identity. This contradicts `E_b<=E<=kappa`.
- In rank two, orient the normal to obtain a proper extension. If `P` projects
  to the source plane and the rotation angle is `theta`, then
  `||(O-I)P||_F^2 >= 4 sin^2(theta/2)`, half the full Frobenius displacement.
  Equivalently, two rank-two planes in R3 have projection-product trace at
  least one. This yields the factor two.
- In rank one, the shortest rotation taking the source line direction to its
  labelled target direction has full Frobenius displacement exactly twice
  the displacement of that unit direction. A singleton uses `O=I`.

There is therefore no hidden assumption that every block spans R3, and no
uncontrolled choice of an orthogonal extension.

### 2. The logarithmic and acceleration estimates close

Let `L` be the shortest skew logarithm of `O`. Concavity of sine gives
`theta/(2 sin(theta/2)) <= pi/2` on `[0,pi]`; the elementary bound
`pi<22/7` implies `pi^2<10`. Thus

```text
|Lr|^2 <= (5/2)|(O-I)r|^2,
||L||_op^2 <= (5/4)||O-I||_F^2 <= (5/2)E_b/kappa.
```

For `z_i(t)=c_b+t u_b+exp(tL_b)r_i`, every within-block distance is constant.
The offsets sum to zero, so translation-rotation cross terms cancel in the
total kinetic energy. Summing the preceding estimates gives

```text
sum_i |z_i'|^2 <= (5/2)E,
|z_i''| <= (5/2)E_b/sqrt(kappa).
```

For a cross-block difference `Z`, this implies
`|Z'|^2<=5E` and `|Z''|<=M=5E/(2sqrt(kappa))`. The second estimate uses both
factors in `|L^2r|<=||L||_op |Lr|`; its dependence is linear in the squared
endpoint error `E_b`, as required.

### 3. Every cross distance is nonincreasing

The Dirichlet Green kernel for the second derivative bounds the deviation
from the endpoint chord by `M t(1-t)/2<=M/8`. Endpoint contraction bounds
both endpoint norms of `Z` by `d`, hence `|Z(t)|<=d+M/8`. For
`f(t)=|Z(t)|^2`, therefore,

```text
|f''(t)| <= L := 2[5E+(d+M/8)M].
```

Since the mean of `f'` is `-Delta_ij`, comparison with that mean gives
`f'(t)<=-Delta_ij+L/2`; the kernel integral
`[t^2+(1-t)^2]/2` never exceeds `1/2`. When `E<=kappa`, putting
`q=d/sqrt(kappa)` yields

```text
L/2 <= E[185/32+(5/2)q] <= E[8+2q^2],
8+2q^2-185/32-(5/2)q = 2(q-5/8)^2+23/16.
```

The cross budget now gives `f'<=0`, including equality at the guard boundary.
This proves the claimed analytic simultaneous contraction; no sampled-time
argument is being substituted for the motion.

### 4. The invariant and uniform interfaces are valid

After polar alignment, `A^T B` is symmetric positive semidefinite. Set
`U=A+B` and `V=A-B`. Direct expansion gives

```text
F = ||AA^T-BB^T||_F^2
  = (1/2)tr(U^T U V^T V) + (1/2)tr((U^T V)^2).
```

Here `U^T V=A^T A-B^T B` is symmetric and
`U^T U>=A^T A>=kI`, so `F>=(k/2)||A-B||_F^2`. Consequently the optimally
aligned displayed error is at most `H=2F/k`; the two invariant guards imply
the direct guards. Separate endpoint translations and an orthogonal target
frame do not alter either endpoint comparison quantity. When `F=0`, equality
of centered Gram matrices gives congruence directly.

Double-centering the loss matrix gives
`AA^T-BB^T=-(1/2)J Delta J`. Therefore
`4F<=sum_ij Delta_ij^2<=n^2 epsilon^2`. The two uniform-cover inequalities
are exactly what is needed for `H<=kappa` and `C H<=rho epsilon`; there is no
missing factor of two or ordered-pair convention.

### 5. The packaged family is nonvacuous

For the three tetrahedral blocks, each source scatter is `4I`, the diameter
is `d^2=1160`, and hence `C=588`. The translation and two rational rotations
give

```text
E = 3072t^2 + 64t^2/(1+t^2) <= 3136t^2.
```

Writing a cross source difference as `D+w`, the rotated-offset perturbation
has norm at most `6t`. With `512<=|D|^2<=1024`, `|D|<=32`, and `|w|<=4`, the
author's expansion gives a loss at least `199t`, hence at least `192t`, for
`t<=1/4`. Since `588*3136/192=9604<16384`, both guards hold throughout the
stated interval `0<t<=1/16384`.

The paired affine rank argument is also correct. Each block's paired edge
span is the graph of its rotation. A functional annihilating the graphs of
`I`, `R_z`, and `R_x` would give a vector fixed by both nontrivial rotations,
so it vanishes. The span is all of R6. A global alignment making straight
interpolation contract would have to identify every preserved tetrahedral
edge at both endpoints and hence make all three rotations equal, which they
are not.

## Independent exact reproduction

The review checker pins all eight author-artifact files plus the cited
Procrustes proof at the exact target commit. It does not import the author's
checker. It constructs a new 11-site input with four blocks:

```text
rank 3: tetrahedron centered at (-24,0,0), rotated about z;
rank 2: square centered at (24,0,0), rotated about x;
rank 1: two points centered at (0,24,0), rotated about y;
rank 0: singleton centered at (0,-24,0).
```

All block centers contract by the factor `1-t`; the rotations use the exact
rational tangent parametrization. At `t=2^-20`, exact arithmetic finds 11
sites, 55 pairs, 13 tight within-block pairs, 42 strictly contracting cross
pairs, `kappa=2`, `d^2=2505`, and `C=2513`. It proves `E<10^-8`, the least
cross loss exceeds `1/600`, and the guard margin exceeds `1/600`.

At `t=2^-30`, the checker applies a determinant `-1` global target reflection
and a translation. Pair losses and the centered target Gram matrix are
frame-invariant, while the displayed error now exceeds `kappa`. Nevertheless
the source scatter has floor `k=4`; exact double-centering proves
`F<10^-10`, `H<1/(2*10^10)`, and invariant cross margin greater than
`1/600000`. The same input satisfies both uniform-cover conditions with
margins greater than `15` and `1`. This separately exercises the invariant
corollary and the uniform cover.

As a structural control, straight interpolation of one preserved rotated
edge has positive terminal squared-distance derivative
`16/1099511627777`; it shortens and then re-expands, whereas the reviewed
rigid motion keeps it fixed. The checker also exercises sharp rank-two,
rank-one, and improper-orthogonal constants, and rejects a changed
within-block distance, a nonorthogonal matrix, and an oversized scatter
floor.

I also ran the author's exact checker from the target source, normally and
with `python3 -O`; both ended in
`RIGID_BLOCK_ALL_VARIANCE_CONTROLS_PASSED`. Its packaged `INPUT.json` was
certified and its byte manifest passed.

## Transfer boundary and remaining uncertainty

The implication from a continuous contraction to all Gaussian internal
energy comparisons is supplied by Aishwarya--Li, Theorem 1.4; their paper
also explains why a lift with at most two auxiliary coordinates suffices for
the full convex-energy conclusion. The arbitrary-radius ball consequences
use the classical continuous-motion/lifting results credited by
Bezdek--Connelly and Csikos. I checked the current primary sources, but did
not reprove those external comparison theorems here.

Accordingly, the evidence establishes:

- the endpoint hypotheses and all rational algebra for the fresh fixtures;
- the universal rotation, speed, acceleration, Green-kernel, and budget
  argument in the written proof;
- the Procrustes upper bound, double-centering constants, and uniform cover;
- the stated author family and its obstruction to straight interpolation.

It does not establish:

- a converse to either guard or any conclusion when a guard fails;
- approximate rigidity when within-block losses are nonzero;
- contractions whose zero-loss graph is not a union of congruent cliques;
- the complete dimension-three Gaussian-convolution frontier;
- historical priority or non-overlap with every construction in the
  literature.

Primary references inspected: [Aishwarya--Li,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2) and
[Bezdek--Connelly, arXiv:math/0108098](https://arxiv.org/abs/math/0108098).
