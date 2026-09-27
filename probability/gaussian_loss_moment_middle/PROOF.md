# A loss-moment guard for a uniform Gaussian middle interval

Complete author proof, 27 September 2026. Independent review pending.
The unrestricted three-dimensional conjecture remains open.

The first-variation and Procrustes estimates used here are **already proved
and independently accepted** in R1's
[near-isometry packet](../gaussian_contact_near_isometries/PROOF.md).
We retain its second loss moment instead of replacing it by a worst-case
displacement. The additions are a rational fixed-threshold guard, a uniform
family with arbitrarily small loss and rare macroscopic motions, and ten
extra cubature features that preserve the guard. This is not a new proof of
the underlying rigidity estimate or another quadrature box.

## 1. A moment-defined family, including diffuse laws

Let X have an arbitrary bounded probability law in R^3, T be 1-Lipschitz
on its support, and s>0. Put Y=T(X), let primes denote independent copies,
and define

```
C_s=(2 pi s)^(-3/2), f=law(X)*gamma_s, g=law(Y)*gamma_s,
H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
Delta=(|X-X'|^2-|Y-Y'|^2)/s >=0,
d=E Delta,                         Q=E Delta^2.
```

H has the favorable sign convention. The letter Q here is a scalar loss
moment, not a density or an orthogonal matrix.

**Theorem 1 (uniform rational guard).** Suppose

```
|X-E X| <= sqrt(s)/2 almost surely,
Cov(X)/s >= 2^(-15) I_3,
Q <= 2^(-48) d.                                      (1)
```

Then

```
H(u) >= 2^(-40) d        for 1/64 <= u <= 1/2,         (2)
H(u) >= 0               for u >= 1/64.                (3)
```

There is no lower bound on d, positive atom masses, or the probability of
a large displacement. There is no atom-count restriction; the law can be
nonatomic. If d=0, H is identically zero. When d>0, (2) is a strict sign on
the entire closed interval, not an interpolation of sampled signs.

The source covariance floor and the small second-loss-to-first-loss ratio
are substantial restrictions. Thresholds below 1/64 remain unsigned.
No full majorisation or Kneser--Poulsen conclusion is asserted. Conditions
(1) are dimensionless: the same statement applies at every variance at
which that input satisfies them, not at all variances for one fixed input.

## 2. Keep the accepted loss-moment remainder

Scale by sqrt(s), so s=1, and center the two clouds independently. Align
the target orthogonally by Procrustes. Write h=Y-X and M=E|h|^2. The
accepted estimate is

```
M <= Q/(2 kappa),           Cov(X) >= kappa I_3.       (4)
```

For clarity, double centering of the pair-loss kernel gives
`||AA*-BB*||_HS^2 <= Q/4`, where A,B are the centered coordinate maps
into L2(mu). Procrustes makes A*B symmetric positive semidefinite.
Writing U=A+B, V=A-B gives

```
||AA*-BB*||_HS^2
 = (1/2)tr(U*U V*V)+(1/2)tr((U*V)^2)
 >= (kappa/2) M.
```

This proves (4), without a bound on ess sup |h|. The earlier theorem
subsequently used `Q <= 8 R delta d`; **we do not use that relaxation**.

Let `|X|<=R`, `0<u<1`, `ell=-log u`, `C=(2pi)^(-3/2)`, and
`E={f>Cu}`. Its boundary can be critical; the regular-value approximation
in the accepted proof applies because positive Gaussian-mixture level
sets are null and nearby superlevels lie in a common compact ball.
For `f_theta=law(X+theta h)*gamma_1`, that proof gives exactly

```
integral_E dot f_0
 = (Cu/4) integral_E E_(pi_z x pi_z)
                       [Delta+|h-h'|^2] dz.             (5)
```

No contracting path is assumed. Only the derivative at theta=0 is used.
Gaussian envelopes put E inside `B(0,R+sqrt(2ell))`. Since f<=C, every
posterior density relative to mu on E is at least
`exp(-(2R+sqrt(2ell))^2/2)`. Applying this to both labels in (5), and
discarding the nonnegative displacement term, proves

```
integral_E dot f_0 >= (C |E|/4) q_R(u) d,
q_R(u)=u exp(-(2R+sqrt(2 log(1/u)))^2).                 (6)
```

The global Gaussian directional-Hessian bound is
`||partial_ee gamma_1||_infinity <= C`. Taylor's theorem, integrated on
the SAME source set, loses at most `C |E| M/2`. Using E as an admissible
competitor for the target hinge, (4)--(6) yield

```
H(u) >= (C |E|/4) [q_R(u)d-Q/kappa].                  (7)
```

This is a direct fixed-threshold use of R1's accepted argument. No
difference-of-convex-functions shortcut, reference top set, level-gradient
lower bound, or differentiability of the optimizing threshold is assumed.

## 3. Exact constants for the whole interval

For `R<=1/2` and `1/64<=u<=1/2`, elementary bounds give

```
sqrt(2 log(1/u)) <= sqrt(12 log 2) < 3,
q_R(u) > (1/64) exp(-16) > 2^(-32).                  (8)
```

Indeed `log 2<3/4`, `e<3`, and `3^16<2^26`. The first logarithm bound
follows from `exp(3/4)>1+3/4+(3/4)^2/2>2`.
Conversely `log 2>1/2`, since `e<3<4`. The lower Gaussian envelope
`f(z)>=C exp(-(|z|+R)^2/2)` therefore shows

```
B(0,1/2) subset E,        |E|>1/2,        C>1/16.     (9)
```

Here `pi>3` gives the volume bound and `pi<22/7` gives
`(2pi)^3<(44/7)^3<256`, hence the bound on C.
With kappa=2^(-15), (1) gives `Q/kappa<=2^(-33)d`.
Thus (7)--(9) give `H(u)>=2^(-40)d`, proving (2).
All constants hold simultaneously over the full interval and all parameters
in (1). If d=0, (4) gives M=0, so the two densities are isometric.

For (3), R8's accepted
[high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md)
applies with epsilon=R^2/s<=1/4. Its logarithmic window is

```
L_epsilon=(4-5epsilon)^2/[32epsilon(1-epsilon)].
```

For `0<epsilon<=1/4`, the numerator is at least 121/16 and the
denominator is at most 6, so `L_epsilon>=121/96>1>log 2`.
Its signed interval therefore contains `[1/2,1]`, and both hinges vanish
above 1. This joins (2) with no gap. No low-endpoint overlap is inferred.
If T is initially defined only on the source support, its standard
Euclidean 1-Lipschitz extension supplies the global map used in that
window theorem, with exactly the same pushforward law.

## 4. Ten extra features preserve the sign guard exactly

The accepted [paired cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
preserves both marginal moments through degree 2q with at most
`M_q=2 binom(2q+3,3)-1` original source--target pairs. It already preserves
the two means, covariance matrices, and d for q>=1. It does not in general
preserve Q, which is a quantity of the specified pairing.

Use dimensionless centered coordinates
`x=(X-E X)/sqrt(s)`, `y=(Y-E Y)/sqrt(s)`. Add these TEN scalar features:

```
x_i y_j   (1<=i,j<=3),          |x|^2 |y|^2.           (10)
```

**Theorem 2 (guard-preserving cubature).** For every q>=2 there is a
probability law on at most `M_q+10` original pairs that preserves the
marginal moments through degree 2q, d, Q, both covariance matrices, and
the centered source radius bound. In particular **79 pairs suffice at
q=2**. Every inequality (1) is retained exactly, including equality and
arbitrarily small d.

To prove Q preservation, write Z=(x,y), J=diag(1,1,1,-1,-1),
`h(Z)=Z^T J Z`, `A=E xx^T`, `B=E yy^T`, `Cxy=E xy^T`. Since E Z=0,
expanding `Delta=h(Z)+h(Z')-2Z^T J Z'` gives

```
Q = 2 E h(Z)^2 + 2(E h(Z))^2
       + 4[tr(A^2)+tr(B^2)-2||Cxy||_F^2],
E h(Z)^2=E|x|^4+E|y|^4-2E(|x|^2|y|^2).               (11)
```

The cross term involving `(h(Z)+h(Z')) Z^T J Z'` vanishes because E Z=0.
All quantities in (11) are preserved by degree-four marginal moments and
(10). The original marginal first moments fix the centering constants;
the sparse law uses the SAME centered coordinates. The finite-function
Caratheodory argument adds at most ten atoms to the old bound. The source
sites are unchanged and its mean is unchanged, so the centered support
radius stays valid. Continuity on compact support permits diffuse input.

For finite rational input this is a rational feature problem and ordinary
exact affine-dependence elimination produces rational weights on existing
sites. No denominator bound, lower weight bound, or effective diffuse-law
oracle is asserted. **Independent rounding does not preserve (1).**

The ten centered features use the original input's two means; a single
cubature rule simultaneously valid at all parameter values is not asserted.
If a consumer needs a fixed feature list before the prior is specified,
use the nine raw `X_i Y_j`, the raw `|X|^2|Y|^2`, and the SIX additional
raw mixed cubics `X_i|Y|^2,Y_i|X|^2`. The bound becomes `M_q+16`, or 85
pairs at q=2. To check this without centering, write Z=(X,Y)/sqrt(s),
`m=E Z`, `M0=E ZZ^T`, `v=E[(Z^T J Z)Z]`, and `h=Z^T J Z`. Then

```
Q=2 E h^2+2(E h)^2+4 tr(J M0 J M0)-8 v^T J m.         (11a)
```

Exactly those sixteen cross features and the degree-four marginal moments
preserve (11a). The checker compares (11), (11a), and direct pair sums on
the same translated, nonuniform inputs. This fixed-list option does not
claim a denominator bound either.

Adding features leaves all hypotheses of the accepted
[loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md)
intact. Its beta error `d B_(N,q)(epsilon)` is unchanged. In the range
epsilon<=1/2, R8's accepted
[loss modulus](../gaussian_loss_normalized_hinges/PROOF.md) therefore still
gives

```
||H_mu-H_nu||_infinity
 <= d [2 K_epsilon (N+2)^(-1/4)+B_(N,q)(epsilon)].       (12)
```

The atom bound is now `M_q+10`, with the SAME degree schedule. On (1) the
new exact guard signs the middle directly, avoiding a large modulus-based
mesh altogether. Outside (1), (12) remains only an approximation estimate;
it does not manufacture a normalized positive margin or an endpoint sign.

The concurrently published [Jackson reconstruction](../gaussian_jackson_certification/PROOF.md)
improves this approximation schedule using the SAME marginal moments and
loss. Its author proof therefore also accommodates the ten features without
altering its errors: replace M_q by M_q+10. Its acceptance is a separate
obligation; neither Theorem 1 nor Theorem 2 depends on that newer result.
We do not claim the older fourth-power degree as the current best schedule.

## 5. A parameter family with rare large motions and loss tending to zero

This is a checkable use of the general guard, not the definition of its
scope. It uses R6's [eight-site templates](../gaussian_open_eight_site_obstruction/PROOF.md),
whose geometric obstruction remains an author result unless separately
reviewed. The Gaussian proof below does not depend on that obstruction.

Let v_i be `(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)`. Put

```
a_i=v_i/80,          b_i=-20v_i/80,
Ta_i=(1-t)v_i/80,    Tb_i=(1-t)(58/3)v_i/80,
0<t<=2^(-40),        0<=alpha<=2^(-65)t.             (13)
```

Give the four cores arbitrary masses p_i, and the four outer sites
arbitrary masses r_i, subject only to

```
sum p_i=1-alpha,    p_i>=(1-alpha)/8,
sum r_i=alpha,      r_i>=0.                            (14)
```

This is a full three-dimensional conditional core-prior simplex and a
full three-dimensional outer-prior simplex, together with t and alpha.
It includes all their boundary faces; no positive outer mass floor is
used. Every member satisfies (1), hence (2)--(3), uniformly as t and the
loss tend to zero.

The template distance table gives a contraction: before division by 80,
the source/target squared distances are respectively

| Type | Source | Target before multiplying by (1-t)^2 |
| --- | ---: | ---: |
| distinct cores | 8 | 8 |
| outer/core with different indices | 1163 | 1163 |
| outer/core with the same index | 1323 | 3025/3 |
| distinct outer sites | 3200 | 26912/9 |

All distinct pair losses are positive for t>0 and at most 1/2 after
scaling. Since alpha<=1/19, the source mean has norm at most sqrt(3)/40.
Its centered support radius is at most `11sqrt(3)/40<1/2`.
Using `sum v_i v_i^T=4I` and `sum v_i=0`, for the ACTUAL source mean m,

```
Cov(X) >= ((1-alpha)/8) sum_i (a_i-m)(a_i-m)^T
       >= (1-alpha) I/12800 >= I/25600 > 2^(-15) I.     (15)
```

Let d_cc and Q_cc be the contributions of the ordered distinct core
pairs. Their loss is `(2t-t^2)/800<=t/400`. There are twelve such pairs,
each with weight at least `(1-alpha)^2/64`. Thus

```
d >= d_cc >= 3t/51200,
Q_cc <= (t/400)d,
Q-Q_cc <= Pr{at least one outer label} <=2alpha.       (16)
```

Consequently, for the ENTIRE family (13)--(14),

```
Q/d <= t/400 + 102400 alpha/(3t)
     <= 2^(-40)/400 + 102400/(3*2^65)
      = (2161/2400) 2^(-48) < 2^(-48).             (17)
```

The guard retains the relative slack 239/2400 even as t tends to zero;
alpha is allowed to be linear in t, not just quadratic. This proves the
guard analytically for all intermediate parameter values
and priors; sample controls are not a substitute for (15)--(17).

For balanced weights within each group, both endpoint means are zero and
their cross moment is the positive scalar
`(1-t)(1-1163alpha/3)/6400` times I. The Procrustes alignment is the
identity. If alpha>0, the outer displacement has norm
`[20+(58/3)(1-t)]sqrt(3)/80>3/4`. The actual covariance is less than
`I/6000` here, so even the weaker necessary bound
`delta<=kappa/(16R)` from the old worst-displacement criterion fails.
The new loss-moment guard still holds, including as d tends to zero.

The balanced-prior member is already covered, more strongly and at all
variances, by the concurrent [parity-alignment theorem](../gaussian_parity_alignment/PROOF.md).
It is a control for the displacement comparison, not a newly signed example.
The full family (14) permits independent, unbalanced weights within both
orbits; the parity theorem explicitly requires uniform orbit weights.
The main statement (1) is still broader: it is a moment condition on arbitrary
bounded laws, with no tetrahedral or orbit hypothesis.

When all eight masses are positive, the prescribed labelled contraction
also retains R6's no-R5-motion obstruction: in its unscaled template
coordinates every target squared distance changes by at most
`6400t<=6400*2^(-40)<1/100`. Its metric-interval theorem applies. This
claim concerns the specified labelling; alternative rematchings are not
excluded. The sign theorem itself needs only the exact distance table.
At t=0 the allowed outer mass is zero and the actual four-site law is
unchanged. We make no eight-site support claim at that degenerate endpoint.

## 6. Consumer and evidence boundaries

[HANDOFF.md](HANDOFF.md) gives the exact finite consumer contract. It uses
the covariance and quartic loss guard before any threshold quadrature,
maintains the loss factor without a division at d=0, and adds only ten
features to the existing approximation spine. A failed guard is
**UNRESOLVED**, not a negative hinge. Covariance collapse and unrestricted
loss ratios remain outside this result.

[verify.py](verify.py) checks rational constant chains, complete finite
pair tables, the guard over explicit family parameters and nonuniform
priors, two independent formulas for Q, exact feature-preserving cubature,
and deliberately invalid inputs. The universal bounds (7), (11),
(15)--(17), and finite-function existence are written mathematics, not
formalization. No quadrature, solver, private corpus, or omitted large
certificate is a premise. Replays do not constitute independent review.

The [source list](SOURCES.md) credits R1's accepted analytic mechanism,
R8's accepted sign window and loss modulus, R3's accepted paired cubature
and loss error, R2's exact-certificate context, and R6's geometric template.
The contribution is parameter/loss uniformity and a moment-preserving sign
handoff. There is no historical priority claim for first variation,
Procrustes rigidity, or Caratheodory cubature.
