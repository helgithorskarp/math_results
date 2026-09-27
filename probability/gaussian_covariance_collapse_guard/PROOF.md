# A uniform Gaussian sign certificate across marginal covariance collapse

27 September 2026. Complete author proof; **independent acceptance pending**.
The unrestricted dimension-three majorisation problem remains open.

This signs a whole family near either marginal's rank-two boundary, with
a margin proportional to contraction loss. It addresses positive loss,
where the recently effective small-mean-loss guard does not apply. The
ingredients are the known rank-five lifting class, its quantitative hinge
margin, and a controlled projection of the original contraction. This is
not a new low-dimensional motion or a new Kneser--Poulsen theorem.

## 1. Statement

Let `X` have any bounded probability law in `R^3`, and let `Y=T(X)` for
a 1-Lipschitz map. At Gaussian covariance `s I_3`, put

\[
 C_s=(2\pi s)^{-3/2},\quad f=\operatorname{law}(X)*\gamma_s,
 \quad g=\operatorname{law}(Y)*\gamma_s,
\]
\[
 H(u)=\int(g-C_su)_+-\int(f-C_su)_+,
 \quad d=\frac{\mathbb E[|X-X'|^2-|Y-Y'|^2]}s,
 \quad \Sigma_X=\frac{\operatorname{Cov}(X)}s,
 \quad \Sigma_Y=\frac{\operatorname{Cov}(Y)}s.              \tag{1}
\]

Assume `|X-E X|<=sqrt(s)/2`. In particular `0<=d<=1/2`.

**Theorem.** If `d>0` and either marginal has a unit direction `e` with

\[
 e^T\Sigma_X e\le2^{-86}d^2
 \quad\hbox{or}\quad e^T\Sigma_Y e\le2^{-86}d^2,          \tag{2}
\]

then simultaneously

\[
 \boxed{H(u)\ge2^{-42}d\quad(1/64\le u\le1/2),
 \qquad H(u)\ge0\quad(u\ge1/64).}                       \tag{3}
\]

For `d=0` all hinges agree. Arbitrary priors, atom counts and diffuse laws
are included. The small quantity in (2) is a mean squared distance to a
plane; rare points need not be uniformly close to that plane. There is
no covariance lower bound, small maximum displacement, or small `Q/d`
assumption, where `Q=E(pair loss/s)^2`.

Equivalently, any **negative** hinge in `[1/64,1/2]` under the radius bound
must have `d>0` and both strict inequalities

\[
 \Sigma_X\succ2^{-86}d^2I_3,\qquad
 \Sigma_Y\succ2^{-86}d^2I_3.                             \tag{4}
\]

This provides an explicit covariance floor on every search restricted
to `d>=d0>0`: both matrices must exceed `2^-86 d0^2 I`.
It does not supply a uniform floor as d tends to zero, nor signs at
thresholds below `1/64` or outside (2). The numerical constants are
conservative and are not optimization claims.

## 2. Quantitative rank-five input, with its trust boundary explicit

The [paired-rank theorem](../gaussian_majorisation_rank_abel/PROOF.md)
supplies the following elementary construction: if the paired affine support,
including an anchor, has dimension at most five, its squared pair
distances can be interpolated linearly in `R^5`. If `v=(x-x0,y-y0)`
lies in its paired span and `A,B` are the projection Gram operators, take

\[
 Z_t(v)=((1-t)A+tB)^{1/2}v.                               \tag{5}
\]

The endpoint configurations are congruent to the original ones and
`|Z_t(v)-Z_t(v')|^2=(1-t)|x-x'|^2+t|y-y'|^2`.
All centers remain within distance `R` of a moving anchor if all source
centers are within `R` initially. An anchor of zero probability is allowed.

We need this quantitative special case:

**Core lemma.** If this motion has anchor radius at most `1/2`, at unit
variance its hinge gap is at least

\[
 2^{-40}d_0\qquad(1/64\le u\le1/2),                     \tag{6}
\]

where `d0` is its mean pair-distance loss. The general quantitative
[hinge-margin proof](../gaussian_axial_cone_rotations/HINGE_MARGIN.md)
is credited prior team work (graph6264, author proof pending review at
our entry snapshot). We give the needed uniform derivation here; its
constant is part of this author proof, not mislabeled prior acceptance.

Let `F_t` be the five-dimensional mixture along (5), after its moving
translation, and `C5=(2pi)^(-5/2)`. Gaussian product integration gives,
for every integer `k>=2`,

\[
 \int F_t^k=C_5^{k-1}k^{-5/2}
  \mathbb E\exp\!\left[-\frac1{2k}\sum_{i<j}
   \big((1-t)|X_i-X_j|^2+t|Y_i-Y_j|^2\big)\right].        \tag{7}
\]

These integrals are nondecreasing, so taking kth roots and then k to
infinity shows `max F_t>=max F_0>=C5 exp(-1/8)>=7C5/8`.
A mode lies in the convex hull of the centers, thus in the radius-1/2
ball. The global Gaussian gradient bound is
`|grad F_t|<=C5/sqrt(e)<5C5/8`, since `e>8/3>64/25`.

Fix `u in [1/64,1/2]`. On the ball of radius `r0=3/10` about a mode,
`F_t>=11C5/16`. On the sphere of radius `B=1/2+16/5=37/10`,

\[
 F_t\le C_5e^{-128/25}<C_5/128\le C_5u/2,              \tag{8}
\]

using `log 2<7/10`. Take a smooth increasing step `Q_eps` changing from
zero to one between `C5 u` and `C5 u+eps`, with
`0<eps<3C5/16`. Along every ray from the mode to that outer sphere it
changes by one. The gradient bound and radial integration give

\[
 \int_{B(0,37/10)}Q_\epsilon'(F_t(z))dz
 \ge\frac{|S^4|r_0^4}{5C_5/8}.                           \tag{9}
\]

Repeated level crossings cause no loss: bound the absolute derivative
by `(5C5/8)Q'_eps` and integrate. Throughout this ball, every product
of two center kernels is at least

\[
 C_5^2e^{-(21/5)^2}>C_5^2 3^{-18}.                       \tag{10}
\]

Write `Delta=|X-X'|^2-|Y-Y'|^2>=0` for the core contraction, so
`E Delta=d0`. The credited Gaussian pressure identity, in the form needed
here, is

\[
 \int F_1Q(F_1)-\int F_0Q(F_0)
 =\frac14\mathbb E\left[\Delta\int_0^1\int
 Q'(F_t(z))\gamma_5(z-Z_t(X))\gamma_5(z-Z_t(X'))dzdt\right].
 \tag{11}
\]

For a polynomial `Q`, (11) follows directly by differentiating (7) and
symmetrizing the replica pairs: for `Q(r)=r^(k-1)` the coefficient is
`(k-1)/4`. This differentiates affine squared distances, not possibly
nonsmooth square-root trajectories. Uniform approximation of `Q'` and
integration from zero extend the identity to `C^1` tests. The integrated
error is bounded by `||error||_infinity d0 C5/(4*2^(5/2))`.
This is the standard pressure argument of Aishwarya--Li and the credited
hinge-margin proof, specialized to the explicit Gram interpolation.

Insert (9)--(10) into (11). At the endpoints, the normalized density of
an independent two-dimensional Gaussian, sampled from itself, is uniform
on `[0,1]`. Thus `integral F_i 1_(F_i>C5u)` equals the corresponding
three-dimensional hinge at `C3u`. Let eps decrease to zero. The resulting
coefficient of d0 is at least

\[
 \frac25|S^4|C_5(3/10)^4 3^{-18}
 >\frac4{45}(3/10)^4 3^{-18}>2^{-40}.                    \tag{12}
\]

Here `|S^4|C5=2/(3 sqrt(2pi))>2/9`. The last inequality is checked
by integer arithmetic. This proves (6), including critical thresholds,
without a differentiability assumption on the trajectories or a finite
support assumption. The shell proof and constant are credited methods,
not the new result of this packet.

## 3. Approximation by an actual planar contraction

Translate and scale to `E X=0`, `s=1`, `|X|<=R=1/2`. If T is initially
given only on the support, use its classical Euclidean Kirszbraun extension.
Only existence is used; the certificate does not assume an extension
oracle or replace projected centers by incompatible target labels.

For a unit direction e, let `P=I-ee^T`. A Gaussian translation satisfies

\[
 \|\gamma(\cdot-a)-\gamma(\cdot-b)\|_1
 \le\sqrt{2/\pi}\,|a-b|<|a-b|.                           \tag{13}
\]

Integrate its directional derivative along the segment to prove (13).
Mixture averaging and Cauchy--Schwarz give the same bound using the
root-mean-square coupled displacement. Hinge integrals are 1-Lipschitz
in the density L1 norm.

### Source projection

Put `q=e^T Cov(X)e`, `X0=PX`, and **Y0=T(PX)**. In particular we do
not assign the old image T(X) to the projected point PX. The common map
T makes X0 to Y0 a contraction, and

\[
 \mathbb E|X-X_0|^2=q,\quad
 \mathbb E|Y-Y_0|^2\le q,\quad |H(u)-H_0(u)|\le2\sqrt q.
 \tag{14}
\]

Include the anchor `(0,T(0))`. The source lies in a plane and the target
in R3, so this paired affine span has dimension at most five. The source
anchor radius is at most R, and the core lemma applies.

The source squared-pair distance decreases on average by exactly `2q`.
For the target distances `b=|Y-Y'|`, `b0=|Y0-Y0'|`, both are at most
`2R`, and `|b-b0|<=|Y-Y0|+|Y'-Y0'|`. Consequently

\[
 d_0\ge d-2q-8R\sqrt q=d-2q-4\sqrt q.                   \tag{15}
\]

All these statements are coupling inequalities valid for nonatomic laws.
They do not require finding any finite support face.

### Target projection

Instead take `q=e^T Cov(Y)e`, center Y, and put `Y0=P(Y-E Y)`, leaving
X unchanged. This is directly a contraction. Its target lies in a plane,
so the paired affine rank, with the corresponding anchor, is at most five.
Again the moving-anchor radius is at most R. Here the identities are sharper:

\[
 d_0=d+2q,\qquad |H(u)-H_0(u)|\le\sqrt q.                \tag{16}
\]

The independent centering of the target changes no hinge or pair loss.
Neither projection argument claims the original rank-six data possess
a motion in R5.

## 4. The exact uniform sign budget

Let `k=2^-40` and `eta=k/8=2^-43`. Assumption (2) means
`sqrt(q)<=eta d`. Since `d<=1/2`, the source-projection estimate gives

\[
 d_0\ge (1-4\eta-\eta^2)d\ge d/2.
\]

Equations (6) and (14) yield

\[
 H(u)\ge k d_0-2\sqrt q
       \ge(k/2-2\eta)d=2^{-42}d.                        \tag{17}
\]

For target projection, (6) and (16) give the stronger bound
`H(u)>=(k-eta)d`; (17) follows as well. Every u in the closed interval
`[1/64,1/2]` is covered by the same inequalities.

For `u>=1/2`, the separately accepted
[high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md)
applies: for epsilon=R^2/s<=1/4 its exponent
`L_epsilon=1/(2epsilon)-3/4+epsilon/(32(1-epsilon))`
is at least `5/4>log 2`. R=0 is trivial. This joins (17) without a gap
and proves (3). Only Theorem A's signed window is used, not its separate
quantitative interior theorem. The [review](../gaussian_small_radius_defect_review_frontier/REVIEW.md)
records the accepted scope.

If d=0, the nonnegative pair loss vanishes on the support; the prescribed
matching is an isometry of its affine span. Gaussian hinges then agree.
Taking the contrapositive of (2)--(3) gives (4). QED.

## 5. A complete rational spectral test

For rational finite data, d and both covariance matrices are rational.
Let `tau=2^-86 d^2`. The condition (2) holds exactly when at least one
of the rational symmetric matrices `Sigma_X-tau I`, `Sigma_Y-tau I`
is not positive definite. A rational nonzero witness v suffices:

\[
 v^T\Sigma v\le\tau v^Tv.                               \tag{18}
\]

[guard.py](guard.py) finds such a v by exact completion of squares.
Start with the coordinate basis. At each step evaluate the quadratic
form on its first remaining basis vector. If that pivot is nonpositive,
return that vector. Otherwise subtract its quadratic-form projection
from every remaining basis vector and continue. The basis changes are
invertible. Three positive pivots prove positive definiteness; a failed
pivot gives the required rational direction, including a singular equality
case. Clearing denominators gives a primitive integer witness. This is
not an approximate eigenvalue test or an incomplete search over directions.

The finite-input checker first validates rational probability weights,
all active pair contractions, and the centered radius. It removes
zero-weight labels. The certificate reports d, the selected side and
integer direction, q and the positive middle margin. Invalid probability
data or an expanding pair are rejected; a valid input outside the guard
returns **UNRESOLVED**, never an adverse sign. The d=0 branch returns
`ISOMETRIC_ZERO` without needing the radius restriction.

[verify.py](verify.py) checks signed records independently through ordered
pair sums for d and q, whereas the producer uses centered marginal moments.
It separately compares the spectral procedure with Sylvester's criterion,
checks equality and indefinite boundaries and rejects corrupted witnesses.
The analytic projection and Gaussian arguments remain written mathematics.

## 6. R2/R3/R8 handoff and limits

The independently accepted [small-mean-loss result](../gaussian_effective_mean_loss/PROOF.md)
works with a source covariance floor. The present result instead signs
small marginal covariance at positive loss, and yields an explicit floor
for any adverse point in a fixed positive-loss region. These are separate
guard hypotheses. For example, d bounded away from zero and target
thickness tending to zero eventually satisfies (2), even when the source
covariance stays nondegenerate and Q/d stays macroscopic.

Only the two means and covariance matrices are needed after contraction
and the radius are established. The accepted common-pair cubature at
coordinate degree two preserves this guard on at most 19 original pairs.
The usual degree-2q moment interface keeps its existing budget
`2 binom(2q+3,3)-1`, with no extra mixed features. No rational rounding,
uniform rule over a whole parameter cell or diffuse-law oracle is supplied.

Thus the positive-loss middle search can impose both matrix inequalities
(4) before using R3's loss cubature and R8's functional reconstruction.
No sign for that remaining nondegenerate region is inferred. If d tends
to zero together with covariance, (4)'s floor also tends to zero; the
joint boundary remains a separate obligation. Below u=1/64, an actual
uniform endpoint with checked overlap is still needed.

The rational controls include source-thin and target-thin contractions
with paired rank six and positive loss; they test the certificate's two
branches, not new example classes. Some are familiar compositions already
known positive. The result is the universal sufficient condition (2),
not the controls. No all-threshold theorem, new Kneser--Poulsen consequence,
new motion construction, optimized numerical constant or independent
acceptance is claimed.
