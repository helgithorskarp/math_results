# Independent acceptance: direction-dependent convex normal contractions

## Verdict

**Accept in the stated scope.** Let `C` be a nonempty closed convex subset of
Euclidean space, select any Borel family of its complete outward normal rays,
and fix `C`. On a selected ray write

```text
x=p+r u,       T(x)=p+r a(p,u)u,       a(p,u)>=0.
```

The target correctly proves that this map is nonexpansive on the resulting
domain if and only if every factor lies in `[0,1]` and every pair satisfies

```text
(u.v)(1-ab) <= sqrt((1-a^2)(1-b^2)).
```

Every such map has the claimed one-extra-coordinate contracting motion.
Through the two previously accepted transfer theorems, this gives all
Gaussian hinge comparisons at every positive variance for bounded Borel
laws, and both arbitrary-individual-radius ball union and intersection
inequalities for finite center lists.

The exact object reviewed is Discovery Net artifact
`bafkreidifxh4fbjb7cgjhs6p36ngsrlybpltu4axyiwdwkic7dsogtk574` at source
commit `656c9d7925e6cffa61384fd1cd9900239d721ed5`. Eight extension inputs are
content-pinned in `TARGET_INPUTS.json`. Both author-checker modes pass, both
extension and predecessor manifests pass, and the author expected-record
SHA-256 is `5dc4f8ef10972d90b3defc0dfd8c40ad34b4748e45298b3c6879fb231a96032f`.

This enlarges the accepted positive geometric class but does not settle
unrestricted dimension-three Gaussian majorisation, signed normal factors,
tangential motion, arbitrary angular remapping, or nonlinear
direction-dependent distance profiles. Historical novelty was not
exhaustively audited.

## Necessity and the complete-ray boundary

Comparison with the fixed projection point immediately forces `0<=a<=1`.
For two selected rays, compare `p+Lr u` and `q+Ls v`, divide their
squared-distance loss by `L^2`, and let `L` tend to infinity. Projection
offsets disappear, leaving

```text
(1-a^2)r^2+(1-b^2)s^2-2(u.v)(1-ab)rs >= 0
```

for all nonnegative `r,s`. Copositivity of this binary quadratic is exactly
the displayed angular condition, including zero diagonal coefficients. If
`u=v`, squaring its nonnegative sides gives `(a-b)^2<=0`; thus the factor is
constant across every collection of parallel normal rays and is genuinely a
function of the occurring direction.

The complete-ray hypothesis is essential. The independent checker builds
three inadmissible factor pairs whose leading quadratic loss is negative.
For two of them the unit-scale convex offset still leaves positive loss, but
the loss becomes negative at integer scales 10 and 3 respectively. This
directly verifies that a finite center sample cannot replace the asymptotic
whole-ray condition. A separate parallel-direction control detects unequal
factors through the square `1/4`.

## Sufficiency over an arbitrary convex core

For `d=p-q`, convex projection gives

```text
eta=d.u>=0,       zeta=-d.v>=0.
```

These inequalities require neither a smooth boundary nor a full-dimensional
core. Under the accepted angular raise, put

```text
A_theta(a)=(a+cos(theta))/(1+a cos(theta)),
B_theta(a)=sqrt(1-a^2)sin(theta)/(1+a cos(theta)).
```

Direct expansion separates every squared distance into

```text
|d|^2 + 2r A_theta(a) eta + 2s A_theta(b) zeta
      + |(r A_theta(a)u,r B_theta(a))
          -(s A_theta(b)v,s B_theta(b))|^2.
```

The last term decreases by the accepted point-core angular theorem. The two
new offset terms also decrease because `A_theta` is nonincreasing and their
coefficients are nonnegative. This proves simultaneous contraction between
different projection fibers and also handles a core point by setting its
normal radius to zero. At `theta=pi/2`, lowering the extra coordinate adds
only a decreasing nonnegative square to the target distance.

The independent checker does not import the author implementation. It uses
Pythagorean factors and angles so that all four-dimensional coordinates are
rational. On 25 cube-core sites it verifies 300 complete pair paths, 420
projection-offset signs, 1,500 raising inequalities, 900 lowering
inequalities, every stage join, and every endpoint. The fixture includes
multiple base points with the same normal direction, core points, zero and
unit-boundary behavior, faces, an edge, a vertex, and an opposite face.

## Regularity and collisions

Outside `C`, metric projection, normal distance, and normalized displacement
are continuous. The pair condition at unit radii makes
`u -> a(u)u` nonexpansive on the occurring direction set; taking norms makes
`a` continuous there. At the core, every horizontal and added displacement
is bounded by the normal distance, so the complete motion is jointly
continuous even when directions jump. A fixed point of `C` bounds projection
points, normal radii, and time derivatives on every bounded source support.
Each labeled trajectory is analytic on each of the two pieces.

For the ball-volume transfer, set

```text
a_epsilon=(1-epsilon)a+epsilon.
```

This is exactly `(1-epsilon)T+epsilon I`, hence remains nonexpansive. Every
regularized factor is positive. A noncore horizontal point therefore remains
strictly outside `C` with the same unique projection and direction, so the
projection coordinates recover the source label throughout the raising
stage. The regularized target is injective; the lowering stage retains that
target coordinate. Core and noncore points cannot collide. Repeated source
centers can first be merged by the largest union radius or smallest
intersection radius, and continuity handles epsilon tending to zero and
zero radii.

The independent checker verifies the regularized target on all 25 sites and
150 raised horizontal entries at `epsilon=1/7`, with 147 exact projection
recoveries. This finite audit supports the projection-fiber argument; it is
not its universal proof.

## Transfers and examples

Padding the motion by one zero coordinate puts it in the dimension required
by Aishwarya--Li Theorem 1.4(i)(a). The already-reviewed two-dimensional
Gaussian cancellation converts sampled-density order into every hinge
comparison. Reversing the piecewise-analytic motion and applying
Bezdek--Connelly Theorem 1 gives the stated arbitrary-radius ball-volume
directions. Those external results and their orientations were independently
checked in the predecessor reviews; this review verifies that the new motion
meets their hypotheses.

For a ball core the original radial factor becomes
`a(u)+(1-a(u))R/r`, so it genuinely depends on both radius and direction.
For the cube, coordinate clipping is the metric projection and

```text
T_C(x)=P_C(x)+|v_1v_2v_3|v/|v|^3,   v=x-P_C(x),
```

is exactly the accepted angular factor on each normal fiber. It fixes the
cube but contracts every exterior fiber because the factor is strictly less
than one. It cannot be a homogeneous ray map in independent endpoint frames:
agreement with an affine isometry on the open fixed cube forces that
isometry to be the identity, after which a homogeneous fixed set would be
conical rather than a bounded body.

The exclusion from common normal-distance profiles in the original
coordinates is also correct. Such a profile has fixed set `D+bB`. If this
were the cube with `b>0`, its putative support function
`h_D=h_cube-b|.|` would violate subadditivity on two nonparallel positive
coordinate vectors because `sqrt(2)<2`. Hence `b=0` and `D` is the cube.
At equal normal distance, however, the cube example has factor zero in
direction `e_1` and factor `4/27` in direction `(1,2,2)/3`, contradicting a
common profile. The source correctly does not claim exclusion from arbitrary
compositions or from independently framed common-profile maps.

## Evidence and trust boundary

`independent_check.py` uses only standard-library Python integers and
`fractions.Fraction`. It pins the eight target files, verifies the exact
motion and collision controls above, checks three whole-ray countercontrols,
exercises the cube separation data, and rejects three false normal inputs.
It uses no floating-point signs, solver, private data, or omitted certificate.

The universal metric-projection theorem, copositivity equivalence,
continuity across arbitrary nonsmooth cores, and transfer applications remain
reviewed written mathematics rather than proof-assistant formalization. The
Aishwarya--Li and Bezdek--Connelly results remain external dependencies.
The accepted point-core angular theorem and common-profile convex-core
theorem are credited dependencies rather than claims re-proved here.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_DIRECTIONAL_NORMAL_BUNDLE_REVIEW_PASS`.
Expected record SHA-256:
`02b780cbf89d23b45917947cd14c3dccba1d36fe221a48a0c5c86a3510d8b1e5`.
