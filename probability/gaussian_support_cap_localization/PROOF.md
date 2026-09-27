# Effective support-cap localization for eventual Gaussian majorisation

Author argument, 27 September 2026; independent review of this contribution
is pending. The spherical comparison and the all-threshold endpoint used
below have independent campaign acceptance. The unrestricted all-variance
dimension-three problem remains open.

## 1. Normalizations and accepted inputs

Let `mu` be a bounded probability law in R3, `T` a contraction on its
support, and `nu=T#mu`. Put

```
gamma_s(z) = (2 pi s)^(-3/2) exp(-|z|^2/(2s)),
H_f(h) = integral_R3 (f(z)-h)_+ dz,
S_mu(lambda) = integral_S2 log integral exp(lambda theta.x) dmu(x) dsigma(theta),
J(lambda) = S_mu(lambda)-S_nu(lambda),
D = E[|X-X'|^2-|T(X)-T(X')|^2].
```

Here `sigma` is probability area, and `X,X'` are independent. Separate
translations change neither `J`, `D`, nor Gaussian hinges. Assume that
both supports, after such translations, lie in radius-`R` balls, `R>0`.
Write `K=supp mu`, `L=supp nu`, and

```
delta = integral_S2 [h_K(theta)-h_L(theta)] dsigma(theta).
```

This is **half** the difference of the usual mean widths. All width gaps
in this directory use this convention. Compactness and continuity give
`L=T(K)`. The two imported results are:

1. R1, graph6494, independently accepted at6506 and6508:
   `J(lambda) >= lambda^2 D exp(-4 lambda R)/12`, for every `lambda>0`.
   If `D=0`, the contraction is an isometry on the support.
2. The endpoint criterion6032, independently accepted6048: if
   `J(lambda)>=eta>0` for all `lambda>=1/(2R)`, then
   `s>=R^2 max(8,44/eta)` gives
   `H_(nu*gamma_s)(h)>=H_(mu*gamma_s)(h)` for every `h>=0`.

The second statement combines the accepted small-threshold asymptotic
with the overlapping high-noise window. It is already an all-threshold
criterion, not merely pointwise convergence in `h`. If a map is specified
only on `K`, Kirszbraun extension permits its use in that criterion.
The source ball alone supplies the needed radius after recentering the
image at the image of its center. Translation invariance then restores
the independently centered notation here. [SOURCES.md](SOURCES.md) gives
exact dependencies and their review status.

## 2. A quantitative cap theorem

Suppose that numbers `delta_0>a>0`, `d>0`, and an integer `k>=0` satisfy

```
delta >= delta_0,       D >= d,
mu{x: theta.x >= h_K(theta)-a} >= 2^(-k)       for every theta in S2. (1)
```

Set

```
b = delta_0-a,
N = max(1, ceil(R(k+1)/b)),
s_* = (2112 R^4/d) 2^(8N).                                  (2)
```

**Theorem 1.** Every threshold is signed at every variance `s>=s_*`,
uniformly over all bounded contraction pairs satisfying (1).

Indeed the source cap and the target maximum give

```
log M_mu(lambda theta) >= lambda(h_K(theta)-a)-k log 2,
log M_nu(lambda theta) <= lambda h_L(theta),
J(lambda) >= lambda b-k,                                    (3)
```

using `log 2<1`. Hence `J>=1` for `lambda>=N/R`. On the complementary
interval `1/(2R)<=lambda<=N/R`, the accepted R1 comparison gives

```
J(lambda) >= d exp(-4N)/(48R^2)
          >= eta := d 2^(-8N)/(48R^2),                       (4)
```

where `e<4`. Since `d<=D<=4R^2`, we have `eta<=1/12`. Thus (3) and
(4) give `J>=eta` on the entire endpoint ray. Substitution into the
accepted endpoint yields `44R^2/eta=s_*`, which also dominates `8R^2`.
This proves the theorem. No limit in the threshold or uncovered middle
interval is left in this join.

**Corollary 2 (qualitative diffuse sector).** Every fixed bounded
contraction with `delta>0` has full Gaussian majorisation at all
sufficiently large variances.

To check the cap assumption, fix any `0<a<delta`. Choose a finite
`a/4`-net of `K` using sites in `K`. Every ball of radius `a/4` at such a
site has positive `mu`-mass by the definition of support. For any `theta`,
choose a net site within `a/4` of a maximizer of `theta.x`. Its whole
`a/4`-ball inside `K` lies in the `a`-cap. The minimum of the finitely many
positive masses exceeds some `2^(-k)`. Also `D>0`: otherwise the accepted
isometry conclusion would give `delta=0`. Apply Theorem 1.

The measure can be atomless and singular, and `T` can preserve nonzero
pairs. The required mass is aggregate mass in a positive-width cap,
not the mass of an individual atom. This corollary does **not** infer
`delta>0` from `D>0` for arbitrary infinite compact supports. Finite
strict mean-width comparison alone does not justify that inference.

## 3. Uniform finite-cover consumer

The following form avoids paying twice for the support displacement.
Take a finite contracting reference `x_i -> y_i` with positive weights
`p_i`, sum one. After separate translations, assume both lists lie in
`B(0,R0)`. Define

```
D0 = sum_(i,j) p_i p_j (|x_i-x_j|^2-|y_i-y_j|^2),
delta_ref = integral_S2 [max_i theta.x_i-max_i theta.y_i] dsigma.
```

Let `delta_ref>=w>0` be certified. Actual bounded contraction pairs are
allowed to have an arbitrary finite labelled cloud decomposition with
common label probabilities `q_i`, such that

```
|q_i-p_i| <= rho p_i,  sum q_i=1,  0<=rho<=1/2,
|X-x_i|<=r,  |T(X)-y_i|<=r    almost surely conditional on label i. (5)
```

Labels may carry arbitrary diffuse conditional laws. Overlaps between
clouds are allowed. Actual contraction is a separate hypothesis; (5)
does not prove it. Set

```
R = R0+r,
d = (1-rho)^2 D0-16R0 r-8r^2,
b = w-2r,
k = smallest nonnegative integer with 2^(-k)<=(1-rho) min_i p_i. (6)
```

**Theorem 3.** If `d>0` and `b>0`, every pair satisfying (5) and actual
contraction has every Gaussian hinge signed for every

```
s >= (2112 R^4/d) 2^(8N),     N=max(1,ceil(R(k+1)/b)).         (7)
```

For the loss bound, write an actual source pair difference as `v+e`,
where `|v|<=2R0` and `|e|<=2r`. Then

```
||v+e|^2-|v|^2| <= 8R0 r+4r^2.
```

The same estimate holds for the target. The reference pair losses are
nonnegative, so their `q_iq_j` average is at least `(1-rho)^2 D0`.
Consequently actual `D>=d`. Both actual supports lie in radius `R` balls.
For the spherical tail choose a reference site maximizing `theta.x_i`.
Its entire source cloud has projection at least `theta.x_i-r` and mass
at least `2^(-k)`. The target cloud union has support function at most
`max_i theta.y_i+r`. Thus

```
J_actual(lambda) >= lambda(delta_ref-2r)-k >= lambda b-k.     (8)
```

Join (8) to (4), exactly as before. This proof of Theorem 3 does not
require an estimate of the actual support gap followed by a second cap
displacement. It uses the reference directly.

There is no covariance lower bound, atom-count bound, strict Lipschitz
constant, or martingale premise. This particular consumer uses **common
label weights**, unlike the independently reweighted two-endpoint
consumer in the earlier martingale handoff. Its cutoff is deliberately
conservative and may be enormous.

## 4. An exact rational width certificate

Normalize the centered reference lists by `R0`, so all point norms are
at most one, and put `g(v)=max_i v.x_i-max_i v.y_i` for these normalized
lists. Parameterize the sphere by the six cube faces
`v=(+/-1,u,v)` and coordinate permutations, `-1<=u,v<=1`. With
`q=1+u^2+v^2`, radial projection has area Jacobian `q^(-3/2)`.
Homogeneity of the support function supplies another `q^(-1/2)`. Hence

```
delta_ref/R0 = (1/(4 pi)) sum_faces integral_[-1,1]^2 g(v)/q^2 du dv. (9)
```

Face boundaries have area zero. The integrand `F=g/q^2` is Lipschitz
even at changes of maximizing site. Almost everywhere, each coordinate
partial is bounded in absolute value by

```
2/q^2 + 8|u|/q^(5/2) <= 10,                                 (10)
```

because `|g|<=2 sqrt(q)` and each coordinate partial of `g` is at most
two. These derivative bounds also give the Lipschitz bound along every
coordinate line, as the support functions are finite maxima of affine
functions. A square of side `2/M` differs from its midpoint by at most
`20/M` in `F`. Total area of the six faces is24. Therefore their summed
midpoint integral has absolute error at most `480/M`.

Let `H` be a common denominator of all normalized coordinates and write
the coordinates as integer vectors divided by `H`. A midpoint has integer
vector `z`, with one coordinate `+/-M` and the other two odd integers
`a,b` in `{1-M,3-M,...,M-1}`. Its weighted cell contribution is exactly

```
C = 4M [max_i X_i.z-max_i Y_i.z] / [H(M^2+a^2+b^2)^2].       (11)
```

For a positive integer precision `B`, sum `floor(2^B C)` over all `6M^2`
cells, including negative cells. Denote this integer by `Q`. Then

```
I_low = Q/2^B - 480/M
```

is a lower bound for the integral in (9), and the downward-rounding
error is less than or equal to `6M^2 2^(-B)`. If `I_low>0`, use `pi<4`
to certify

```
w = R0 I_low/16 > 0.                                       (12)
```

The sign guard is essential: division by16 would not give a valid lower
bound from a negative numerator. In that case the implementation returns
`UNRESOLVED`, which is not a negative mathematical answer.

The default `B=max(32,4 bit_length(M))` makes both error terms tend to
zero as `M` tends to infinity. The calculation takes `O(n M^2)` arithmetic
operations and `O(n)` working storage; bit complexity additionally
depends on the rational input and `B`. It evaluates no trigonometric or
transcendental function. Integer floor division has the required downward
direction even for negative summands. Huge powers in (7) are retained as
`prefactor * 2^exponent`, rather than expanded into large output files.

## 5. Completeness and the localization boundary

For every fixed noncongruent **finite** contracting reference, the strict
mean-width theorem of Gorbovickis gives `delta_ref>0`, and positive weights
give `D0>0`. For rational reference data, increasing `M` in (9)--(12)
therefore eventually yields a positive `w`. Sufficiently small positive
`r,rho` then make both reserves in (6) positive. Thus this is an effective
uniform diffuse neighborhood of every such rational finite reference,
not a test of one selected geometric box.

For an original bounded measure, a radius-`r` cover using original source
sites `x_i`, their true images `T(x_i)`, and the original cell masses has
(5) with `rho=0`. Contraction gives the same target-cover radius. The
cover consumer then signs the **original** measure whenever its reserves
are positive. A moment cubature or a weak approximation by itself supplies
none of these uniform displacement or cell-mass guarantees.

There is also an existence-level completeness statement for this consumer
in the strict-width sector. Suppose a fixed bounded pair has `delta>0`.
Choose successively finer finite nets from the original compact support
and Voronoi cells. Distinct net sites have positive-mass cells: a small
ball at each site lies in its own cell and has positive mass. The source
and target reference hulls approximate the actual hulls in Hausdorff
distance at most `r`, so their width gap tends to `delta`. The preceding
pair-distance estimates show that `D0` tends to `D>0`. Radii of the
separately centered reference lists stay bounded. Taking the cover fine
enough and then the width mesh fine enough makes both reserves positive.
The minimum cell mass can tend to zero, but at each fixed cover it is
positive and gives a finite `k`.

If rational input is required, a fixed such finite reference can be
approximated by a rational contracting one while slightly enlarging the
cloud radius: first contract its target uniformly by a factor below one
arbitrarily close to one. All distances between distinct source sites
then have strict contraction slack. Rationally approximate both lists
within that finite slack, and approximate the positive cell weights by
rational probabilities. The true weights satisfy the relative error
condition for an arbitrarily small positive `rho`. Continuity preserves
the already strict width/loss reserves. Choose a rational enclosing
radius and refine the width mesh. This proves existence of a finite
rational certificate for every strict-width bounded pair, provided the
required cover and mass inequalities are supplied and verified.

The uniform diffuse neighborhoods of a finite reference are nonempty:
Kirszbraun extends its contraction to R3, and any source law concentrated
in the radius-`r` site balls has image within the corresponding target
balls. Positive-volume source clouds and varying common priors are
therefore possible whenever `r>0`.

This is **not** an algorithm for extracting exact mass bounds from an
arbitrary unspecified measure, and no measure-independent atom, mesh,
or variance bound is asserted. There is no justified inference here from
finite strictness to strictness for every infinite support. Non-isometric
zero-width pairs, if any, and the smaller-variance range remain outside
this theorem. Rescaling preserves `s/R^2`, so it does not remove that
variance restriction. No new Kneser--Poulsen union/intersection theorem
is claimed.

## 6. Reproducible control and trust boundary

[INPUT.json](INPUT.json) uses the already published thin-source control
from the earlier localization work: uniform signs `u,v,w` with source
`(u,v,2^-24 w)` and target `(u/2,v/2,2^-12 uv+2^-24 w)`.
It is a contraction with a preserved nonzero pair, hence Lipschitz
constant exactly one. Its source least covariance eigenvalue is `2^-48`,
while the target least eigenvalue is `2^-24+2^-48`. Conditional Jensen
therefore forbids a martingale coupling between these two center laws
even after separate rotations, also for dilation at least one. This
removes an unnecessary premise from the **consumer**, not a historical
class-separation claim: the calibration already has a contracting straight
motion and is known positive at all variances.

The mesh256, precision36 calculation signs a whole cloud/prior family,
not just the reference. [CERTIFICATE.json](CERTIFICATE.json) records
`N=64` and a cutoff with exponent512. Its size makes the conservatism
explicit. [verify.py](verify.py) reconstructs the record separately,
checks exact coarse quadrature against direct rational evaluation,
negative-cell rounding, malformed hypotheses, symmetries, and boundary
cases. This is author validation, not independent peer review. The
continuum arguments, sphere charts, derivative estimate, and accepted
analytic dependencies remain conventional mathematics, not a formal
proof-assistant certificate.
