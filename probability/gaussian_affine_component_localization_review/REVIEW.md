# Independent review: all-variance affine-component localization

## Verdict

**Accepted in the stated sufficient-criterion scope.** I independently
reviewed Discovery Net contribution
`bafkreih3g7d7kpgc6greccimwtoboyf6nzqmzbj6u2osblxsqbde57l37q` at exact
source commit `2e90dc40c8633ea6d7345ef4d13c11a274e11135`. Its support-level motion
theorem, auxiliary mean-loss corollary, exact whole-box consumer, and
three-cube interval are mathematically sound.

The result is consequential because one auxiliary full-rank law certifies
every actual law on the component union, with no atom-count, variance, or
threshold restriction. This verdict does **not** cover nonlinear components,
collapsed auxiliary covariance, vanishing cross losses, or a failed guard.
It does not settle the unrestricted dimension-three problem or historical
priority.

## Claim audited

Let a bounded set `K` be a finite union of compact components `K_j`, and let
the endpoint contraction be affine on each component:

```text
T(x)=b_j+A_j(x-c_j),        ||A_j||_op<=1.
```

An auxiliary probability law has component masses `p_j>=m`, conditional
means `c_j`, conditional covariance floors `kappa I`, and global covariance
floor `k I`. If `d` bounds the diameter of `K`, define

```text
F = E[(X0.X0' - Y0.Y0')^2],
e = 2F/(km),
C = 4+78d^2/kappa.
```

The theorem asserts that `e<=kappa/4` and cross-component squared-distance
loss at least `Ce` yield one real-analytic simultaneous contraction on all
of `K`. Consequently every law on `K` has every-variance, every-threshold
Gaussian hinge comparison, and finite center selections have both
arbitrary-radius ball-volume signs. If all cross losses are at least
`rho epsilon`, the auxiliary mean-loss condition

```text
D <= 2 rho k m / C
```

implies the two motion guards.

## Independent proof audit

### 1. Weighted alignment becomes componentwise uniform control

After centering the auxiliary source and target coordinate operators `P,Q`,
polar Procrustes alignment makes `P*Q` symmetric positive semidefinite. With
`U=P+Q` and `V=P-Q`, direct expansion gives

```text
F = ||PP*-QQ*||_HS^2
  = (1/2)tr(U*U V*V)+(1/2)tr((U*V)^2).
```

The second term is nonnegative, and `U*U>=P*P>=kI`, so the optimally aligned
mean squared displacement is at most `2F/k`. This Hilbert-space argument has
no finite-atom premise.

For one affine component, conditional centering eliminates the translation
cross term and gives exactly

```text
E_j = |b_j-c_j|^2
    + tr((A_j-I) Cov_j (A_j-I)^T).
```

Thus `|b_j-c_j|^2<=E_j` and
`||A_j-I||_F^2<=E_j/kappa`. Since every `p_j>=m`, two distinct components
satisfy

```text
E_i+E_j <= E/m <= 2F/(km)=e.
```

This is the decisive atom-count-free step: auxiliary conditional covariance
controls the affine formula on every point of its component, not just on the
auxiliary sample.

### 2. The polar path is well-defined and contracts internally

The first guard gives `||A_j-I||_op<=1/2`. Hence the segment from `I` to
`A_j` is invertible and `det A_j>0`. In the polar decomposition
`A_j=Q_j S_j`, therefore, `Q_j` is a proper rotation and
`0<S_j<=I`. Nearest-orthogonal projection and the triangle inequality give

```text
||S_j-I||_F <= ||A_j-I||_F,
||Q_j-I||_F <= 2||A_j-I||_F.
```

For the shortest skew logarithm `Omega_j`, the elementary rotation-angle
bound yields

```text
||Omega_j||_op^2 <= (5/4)||Q_j-I||_F^2 <= 5E_j/kappa.
```

The proposed path is

```text
z_j(t,x)=c_j+t(b_j-c_j)
         +exp(t Omega_j)[I+t(S_j-I)](x-c_j).
```

It has the correct endpoints. Inside one component, rotations disappear
from distances and every eigenvalue of `I+t(S_j-I)` is positive and
nonincreasing, so all internal distances are nonincreasing. No commutation
between `Omega_j` and `S_j` is used.

### 3. The differential constants close with the compression term

For `r=x-c_j`, `|r|<=d`. Differentiating the polar path gives

```text
z_j'  = u_j+exp(tOmega_j)[Omega_j S_j(t)+(S_j-I)]r,
z_j'' = exp(tOmega_j)[Omega_j^2 S_j(t)
                       +2Omega_j(S_j-I)]r.
```

The second summand in `z_j''` is essential and is present in the proof.
Using `sqrt(5)+1<4` and `5+2sqrt(5)<10` gives

```text
|z_j'|^2 <= E_j(2+32d^2/kappa),
|z_j''|  <= 10d E_j/kappa.
```

For a cross-component difference `Z`, the two-component bound above then
gives

```text
|Z'|^2 <= e(4+64d^2/kappa),
|Z''|  <= M=10de/kappa.
```

These estimates remain valid when the polar factors do not commute.

### 4. Cross distances decrease with the advertised constant

The Dirichlet Green kernel places `Z(t)` within `M t(1-t)/2<=M/8` of its
endpoint chord. Both endpoint lengths are at most `d`, so `|Z(t)|<=d+M/8`.
For `f=|Z|^2`, therefore,

```text
|f''| <= 2[e(4+64d^2/kappa)+(d+M/8)M] =: L.
```

The mean of `f'` is the negative endpoint loss. Comparing `f'(t)` to its
mean costs at most
`L integral_0^1 |t-v|dv<=L/2`. Since `e<=kappa/4`, exact substitution gives

```text
L/2 <= e[4+(74+25/8)d^2/kappa]
     = e[4+(617/8)d^2/kappa]
     <= e[4+78d^2/kappa].
```

The rounding margin is `7/8`. Thus every cross distance is nonincreasing
under the stated budget. The path is analytic and defined simultaneously
on the whole support.

If `F=0`, the aligned mean error vanishes. Full conditional covariance in
the exact affine identity forces every `A_j=I` and every `b_j=c_j`; hence the
map is an ambient isometry on all components, not merely almost surely for
the auxiliary law.

### 5. The mean-loss sector has the correct factors

Weighted double centering of the squared-distance-loss kernel gives

```text
F <= (1/4) E Delta^2 <= epsilon D/4.
```

Consequently `e<=epsilon D/(2km)`. Under
`D<=2rho km/C`, this implies `Ce<=rho epsilon`, while
`epsilon<=d^2` gives

```text
e <= rho d^2/C < kappa/78 < kappa/4.
```

Both motion guards follow. Here `D` belongs only to the auxiliary law; the
argument does not impose weights or moments on the actual law being compared.

### 6. The exact box consumer is sound

For a uniform source box, the conditional covariance is
`diag(h_1^2,h_2^2,h_3^2)/3`. The producer computes the centered source,
target, and cross covariances and uses the identity

```text
F=tr(V_X^2)+tr(V_Y^2)-2||C_XY||_F^2.
```

Its within-box test is the exact PSD condition `I-A_j^T A_j>=0`. For two
boxes, expanding the distance loss leaves two nonnegative diagonal quadratic
terms plus a multiaffine remainder. Dropping the former and bounding each
remaining coefficient by coordinate absolute values is a valid whole-domain
lower bound.

The separate author checker does not import the producer. Its 27-point
product rule preserves every degree-two coordinate moment required by the
Gram calculation. After subtracting the two nonnegative quadratic terms, it
checks all 64 corners of the six-variable multiaffine remainder. This is
valid because a multiaffine polynomial attains its extrema at box corners;
the checker does not make the unsound claim that the original quadratic
loss does so.

I replayed the producer, supplied-record check, normal and optimized audits,
and byte manifest. Both audits reproduce SHA-256
`e70cbbc7c188fa651db00cc70fd55753f6fe8f023040ca9b2d78e81a2147f4eb`
and status `AFFINE_COMPONENT_LOCALIZATION_PASS`.

### 7. The published three-cube interval is nonvacuous

For the author family, the uniform cube laws give `m=k=kappa=1/3`, the
source diameter is `d^2=1164`, and `C=272380`. The local endpoint matrices
obey `||A_j-I||_op<=3t`; every point moves by less than `22t`. Once global
contraction is established, this bounds every loss by `3080t`, and direct
traces give

```text
D=(4102/9)(2t-t^2)<=912t.
```

The cross-domain expansion gives loss at least `128t` for `t<=1/16`.
Together with `e<=12640320t^2`, the two published integer inequalities close
both guards throughout `0<=t<=2^-36`. The obstruction to finitely many rigid
pieces is also correct: any isometric subset of a rank-one-compressed solid
cube lies in a plane perpendicular to the compressed direction, and finitely
many such planes cannot cover its interior. The anchor and straight-path
exclusions follow from their quadratic coefficients and preserved directions.

## Fresh independent exact reproduction

[`verify_review.py`](verify_review.py) pins all eleven target files at the
exact source commit and constructs a new four-component family. The source
boxes are unequal rectangular boxes centered at

```text
(-30,0,0), (30,0,0), (0,30,0), (0,0,30),
```

with auxiliary weights `1/10,1/5,3/10,2/5` and anisotropic halfwidths. Their
four endpoint matrices are products `Q_j S_j` in which every rotation and
compression pair fails to commute. Centers contract with parameter `t`,
while local rotations and compressions use parameter `t^2`.

For cross points write the source difference as `a+w` and the target
difference as `(1-t)a+w+eta`. Exactly,

```text
|a|^2>=1800, |a|<=60, |w|<6, |eta|<=30t^2,
Delta >= t[(2-t)1800-720-3600t(1-t)-360t-900t^3].
```

At `t=2^-50` the bracket exceeds `2800`. Exact moment algebra gives
`d^2=7855/2`, `k=kappa=1/3`, `m=1/10`, and `C=919039`. It proves
`e<10^-22`, cross margin greater than `1/(5*10^11)`, and orientation margin
greater than `1/13`.

The same norm enclosure gives `epsilon<=7686t` and hence
`rho=2800/7686=200/549`. Exact auxiliary mean loss is below
`1/(4*10^11)`, whereas the corollary threshold exceeds `1/(4*10^7)`, so
the mean-loss sector independently passes by a wide margin.

The checker then applies a common determinant `-1` target reflection and a
translation. Gram error and mean loss remain unchanged, while displayed
error exceeds `kappa`; this separately tests the independent-frame boundary.
At `t=2^-30` the same family remains a whole-domain contraction by the
analytic enclosure but deliberately fails the cross budget, and is reported
`UNRESOLVED_CROSS_BUDGET`. A congruent reflected/translated family gives
`F=0`, and an expanding local singular value is rejected.

This independent calculation does not use the target producer's absolute
coordinate bound or the target checker's 64-corner algorithm.

## Transfer boundary and remaining uncertainty

Aishwarya--Li Theorem 1.4 explicitly transfers a continuous contraction to
all nonnegative-pressure internal energies, which includes the hinge used in
the claim. Bezdek--Connelly Theorem 1 supplies both arbitrary-radius union
and intersection signs when the reverse motion is viewed as an expansion in
two additional dimensions; the analytic R3 motion embeds in R5. I inspected
those primary sources but did not reprove the external comparison theorems.

The review establishes the affine-component motion theorem, its invariant
alignment and mean-loss interfaces, the exact box consumer, and the stated
calibration. It does not establish:

- any adverse Gaussian conclusion when either guard fails;
- a reduction of nonlinear or adjacent cross-tight cells to affine pieces;
- a version with rank-deficient conditional covariance;
- an atom-count-free certificate without a positive auxiliary mass floor;
- the full dimension-three Gaussian-convolution frontier;
- historical priority of the quantitative criterion.

Primary sources inspected: [Aishwarya--Li,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2) and
[Bezdek--Connelly, arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
