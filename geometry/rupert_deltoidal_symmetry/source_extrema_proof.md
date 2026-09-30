# Sharp source localization for two deltoidal area budgets

**six-rupert-1, researcher; 2026-09-30.** This is an author-checked intermediate
proof with exact finite computations. It is unformalized and independently
unreviewed. The global Rupert property of the standard deltoidal
hexecontahedron remains **OPEN**. Historical priority is unasserted.

The result replaces a subdivision-dependent source estimate by a complete
critical-point computation. It determines the optimal source radius about
the minimum-area axes at two useful physical-area budgets, including the
budget for the full prospective receiving wedge. No receiving exclusion
outside the previously proved whole `D_(2/3)` is asserted.

## Statement and normalization

Let `K` be the original centered 62-vertex solid in [verify.py](verify.py),
in its existing coordinate scale. For a unit vector `k`, write

```
A(k) = Area((I-kk^t)K),
s = sqrt(5) > 0,
M = ((3s-5)/6, (s-1)/6, 1),  m = M/||M||,
E = {g m : g in G},
R(T) = max {dist(k,E) : ||k||=1, A(k)<=T}.
```

Here `G` is the full group of 60 proper body rotations, `E` consists of
60 directed normals or 30 projective axes, and `-E=E`. Distance means
Euclidean chord distance between **unit** normals. The existing
[global area proof](global_area_proof.md) establishes the physical area
minimum

```
A0^2 = (3503950+1491850s)/31581,
{k : ||k||=1, A(k)=A0} = E.
```

Those facts are prerequisites, not new conclusions here. Put

```
T2 = 14803427/1000000,
T1 = 7409521/500000.
```

**Theorem.** The complete source sublevels have sharp radii satisfying

```
96537/1000000 < R(T2) < 96538/1000000,
105135/1000000 < R(T1) < 105136/1000000.
```

More precisely, for each `T` there is a unique maximizing direction
`k_T` in the original closed fundamental chamber. If
`f_T=M.k_T`, the exact radius is

```
R(T) = sqrt(2 - 2 f_T/sqrt((28-8s)/9)).                 (1)
```

All coefficients of `k_T=A+B sqrt(D)` and of `f_T` are supplied explicitly
in [expected_source_extrema.json](expected_source_extrema.json). The small
budget maximizer is the same point on cell1/edge0 and cell5/edge2. The larger
budget maximizer is the same point on cell8/edge1 and cell10/edge2. Edges
are zero-based and join successive corners in the pinned cyclic cell list.
The duplicates are boundary membership in adjacent **closed** cells,
not distinct maximizing directions. Both displayed directions have unit
norm, satisfy every cell inequality, and have physical area exactly `T`.

The extrema include all original unit source normals; no source-nearness,
roll, translation or small-angle hypothesis is assumed.

## A nearest minimum axis throughout the chamber

The verified body reflections have normals
`(1,0,0),(0,1,0),(-phi,-phi^2,1)`, with `phi=(1+s)/2`.
Their 120-element group `F` folds every direction into the cone over

```
H = conv{(0,0,1),(1/phi,0,1),(0,1/phi^2,1)}.
```

The prior proof gives a direct folding argument: maximize the third
coordinate over a finite orbit, change the first two signs to nonnegative,
and reflect across the third wall if it is violated. A violation would
increase the third coordinate, contradicting maximality. A nonzero folded
direction has positive third coordinate and can be scaled into `H`.

The new checker regenerates the 60 proper rotations, constructs
`F=G union S G` with `S` the third wall reflection, verifies that all three
wall reflections preserve this entire set, and checks `S M=M`.
Consequently `F M=G M`. Area and distance to `E` are invariant under `F`.

For every `v` in the 60-element raw orbit `G M` and every one of the three
corners `u` of `H`, the checker establishes

```
(M-v).u >= 0.                                       (2)
```

These 180 weak comparisons extend by linearity to the complete chamber
cone, including its boundaries. All `v` have norm `||M||`; thus (2) proves
that the nearest member of `E` to every folded unit direction `k` is `m`.
Therefore

```
dist(k,E)^2 = 2 - 2 (M.k)/||M||                      (3)
```

throughout that chamber. Minimizing `M.k` there is exactly the original
global source-radius problem after folding. In particular a displayed
feasible minimizer gives an **attained** sharp radius; it is not merely a
sufficient cap test.

## Complete finite critical-point reduction

The previously certified complete physical-area fan cuts `H` into twelve
closed convex polygons with fourteen distinct corners. Its area vectors
`C_i` satisfy `A(k)=C_i.k` on the unit spherical cone of cell `i`.
The checker replays the polygon construction and compares every cyclic
corner list with the pinned direct-area fixture. It verifies strict
convexity of consecutive corners and all inward edge sides. The separate
prerequisite entry point replays every physical-area check against all
original vertices, not just a generated surrogate body.

In one cell let its raw cyclic corners be `u_j`, its inward great-circle
edge normals `e_j=u_j cross u_(j+1)`, and its area vector `C`. Its feasible
set is

```
L = {k in S^2 : k is in the cell cone, C.k<=T}.
```

This set is compact. All cell rays have positive third coordinate, and
the cell is the bounded convex polygon at third coordinate one; hence its
closed spherical cone has third coordinate bounded away from zero. In that
hemisphere, `e_j.k>=0` is equivalent to membership in the polygon cone.
No antipodal cone is admitted by these inequalities.

If `L` is nonempty, `M.k` attains a minimum. Classify a minimizer by the
active polygon edges and the area constraint. The following list is complete:

1. A polygon corner gives its positive unit normalization.
2. With no active edge and inactive area constraint, a stationary point
   on the sphere is `+/- M/||M||`.
3. With one active edge and inactive area constraint, a stationary point
   on its great circle is `+/- P_e M/||P_e M||`, where
   `P_e x=x-e(e.x)/(e.e)`. Endpoints belong to case1.
4. With active area constraint and no active polygon edge, a stationary
   point on the area circle `C.k=T` is one of the two points in (4) below.
5. With active area constraint and an active edge, both intersections
   of the area circle and that edge's great circle are included, as in (5).

Two distinct active polygon edges meet at a polygon corner. Strict convexity
rules out an unlisted edge intersection in the spherical polygon.
For cases2--4 a minimizer in the relative interior of a smooth curve or
surface must have zero tangential derivative. If a feasible piece terminates,
an additional edge or the area constraint is active and the point enters
another case. This argument also covers an isolated feasible point: it must
be a corner, an area-edge intersection, or a collapsed area circle.

Here are the exact formulas, using base-field vectors and squared norms.
For the area circle, set

```
c2 = C.C,  A = (T/c2) C,
B = M - C(M.C)/c2,
r2 = 1-T^2/c2,
k = A +/- B sqrt(r2/(B.B)).                         (4)
```

For its intersection with edge plane `e.k=0`, set

```
c = P_e C,  c2 = c.c,
A = (T/c2) c,  B = e cross c,
r2 = 1-T^2/c2,
k = A +/- B sqrt(r2/(B.B)).                         (5)
```

If `r2<0` the corresponding intersection is empty. If `r2=0`, both formulas
give the same tangent or collapsed point `A`, and this point is still checked.
If `r2>0`, both square-root signs are generated. In case4, if `c2<T^2` the
area constraint is automatically inactive on the sphere and there is no area
circle. No strict area assumption drops a tied point.

All twelve actual cells have `C.C>0` and `B.B>0` in (4). All forty actual
edges have `e.e>0`, `||P_e M||^2>0` and `||P_e C||^2>0`; the checker asserts
these facts **before every division**. Thus the objective is nonconstant
on each actual great circle and each noncollapsed actual area circle.
No zero projected vector or constant-objective stratum is silently skipped.
These nondegeneracy conditions, which are verified for this solid, are part
of the finite reduction's hypotheses. The formulas are not claimed as a
general optimizer for degenerate input violating those hypotheses.

Every generated point is checked for exact unit norm and, where applicable,
its declared area and edge equalities. Feasibility uses positive third
coordinate, all **weak** inward cell inequalities and `C.k<=T`. It is
independent of which formula produced the point. Rejected candidates cannot
be minimizers in that cell. If a cell had any feasible point, compactness
and the complete classification would supply a feasible candidate; therefore
a cell with no feasible candidate really has empty area sublevel.

## Exact computation and sharpness

For `T2`, the complete list contains 230 entries:40 normalized corners,
24 sphere-stationary points,80 edge-stationary points,22 area-stationary
points and64 area-edge intersections. Exactly51 are feasible. For `T1`,
the corresponding numbers are226 total,40,24,80,22,60, and54 feasible.
Counts retain repeats at closed boundaries. The program regenerates the
full entries deterministically; only their exact SHA256 record digests,
per-cell counts and explicit maximizing witnesses are stored publicly.

It compares the objective of every feasible entry with the exact minimum.
There are49 strict larger comparisons and two equal ones at `T2`, and52
strict larger comparisons and two equal ones at `T1`. In either case the
two tied entries have exactly equal **three coordinates**, checked even
when their representations use different radicands. Thus every other
feasible candidate has strictly larger objective. The finite completeness
argument proves the unique chamber minimum and formula (1).

For each proposed upper radius `a`, the checker verifies `M.k>0` and

```
(M.k)^2 > (1-a^2/2)^2 (M.M)                         (6)
```

for every feasible candidate. On the checked positive branch, (6) is exactly
`||k-m||<a`. For the sharp witness it also checks the reversed squared
comparison at the claimed lower radius. These **exact** sign comparisons
prove both rational endpoints of the stated sharp windows. The rational
intervals stored for the sharp radius are supplementary diagnostics, not
a substituted floating-point decision.

## The full prospective receiving wedge

In the original unit-third-coordinate chart put

```
N10 = ((3-s)/2,(7-3s)/2,1),
W = ((75-17s)/114,(7+5s)/114,1),
D_t = conv{M, M+t(W-M), M+t(N10-M)}.
```

Receiving normals here mean positive unit normalizations of points in
`D_t`; also allow all proper-body and antipodal images. The checker verifies
that `D_(2/3)` and `D_1` lie wholly in closed cell9. It computes the exact
area maximum on each entire triangle, including every possible edge and
interior stationary point. Both maxima occur at corner2 and have squares

```
max_(D_(2/3)) A^2 = (1208294350+539801050s)/11021769,
max_(D_1) A^2 = (119575+53475s)/1089.
```

The two strict rational upper bounds are exactly `T2,T1` above. Their
predecessors on the `10^-6` grid fail the strict squared upper test.

Let `n` be a unit receiving normal in `D_1` or its stated images. For every
original `Q in SO(3)`, every planar translation `t` and every `lambda>=1`,
the closed containment

```
lambda (I-nn^t)(QK) + t  subseteq  (I-nn^t)K
```

implies by physical area monotonicity
`lambda^2 A(Q^t n)<=A(n)<T1`. Consequently

```
dist(Q^t n,E) < 105136/1000000 < 11/100,
lambda^2 < 1007/1000.                               (7)
```

The scale comparison is the exact positive inequality
`T1^2 < (1007/1000)^2 A0^2`. For `D_(2/3)`, the sharper source upper radius
in (7) is `96538/1000000`; the same scale bound holds. Translation is arbitrary
because it preserves planar area. Proper rotation carries the source shadow
isometrically to the projection along `Q^t n`.

These necessary bounds are uniform over the **whole** larger receiving
triangle and every original source rotation. They do not bound the remaining
planar roll or the full spatial angle. A larger receiving exclusion still
requires freshly verified signed roll and torque conditions. The separate
[two-thirds wedge proof](two_thirds_wedge_proof.md) retains its existing
120 closed equality orientations and its exact receiving scope.

## Reproduction, arithmetic and trust boundary

Use Python3.11+ and the standard library. From the repository root run
sequentially with all numerical threads one:

```
python3 -B geometry/rupert_deltoidal_symmetry/source_extrema_certificate.py --prerequisites
python3 -B geometry/rupert_deltoidal_symmetry/source_extrema_certificate.py
```

The prerequisite entry point pins eight prior files and freshly compares
all mathematical fields of the direct physical-area parent. It replays
45,632 original vertex support comparisons,736 turns and52 physical
shoelace/Jacobian checks. The old parent negative-control report is excluded
from that mathematical comparison; no geometric or numeric field is excluded.
The new standard entry point compares **every** field with the compact
expected JSON. Optimized Python is refused before computation.

Each candidate coordinate and objective has the form `a+b sqrt(D)`, with
`a,b,D in Q(sqrt(5))` and `D>=0`. The sign kernel handles zero coefficients
and zero radicands first. When both nonzero terms have the same sign it uses
that sign. On opposite-sign branches, it uses
`sign(a) sign(a^2-b^2D)`. This remains valid for reducible radicands and exact
cancellation; no irreducible extension-field assumption is made.

For two different radicands, write their difference as
`x-y=L-c sqrt(E)`, where `L=p+b sqrt(D)`. Check both summand signs first;
only if they oppose compare `L^2-c^2E`, again an expression with one radical.
This compares all candidate objectives and tied coordinates exactly without
rounding, incompatible-field multiplication, or omitted equality branches.

Independent audits use integer square-root rational enclosures of `sqrt(5)`
and of each nonnegative radicand to separate every nonzero sign. A zero
radical sign is checked by its exact squared identity and opposing signs.
All executed base-field and radical sign decisions, including the different-
radicand comparison reductions, are audited. The temporary audit wrappers
leave the deciding kernels, geometric inputs and existing resource caps
unchanged, and restore methods on exit. Declared precision ceilings cause
failure, never acceptance by tolerance. Additional tests cover zero and
reducible radicands, cross-radical equality and both comparison directions.
Eight malformed controls reject, including both falsely sharpened radii
at the lower ends of the sharp windows.

The trust boundary consists of the pinned original coordinates and freshly
replayed physical-area fan, the written compactness and critical-stratum
argument, the chamber and nearest-axis argument, exact Python/Fraction
semantics, and the continuous physical-area implication of containment.
It includes no solver status, floating passage search or assertion that a
missing construction proves global nonexistence. This is author validation,
not independent review or formal proof.

The [area polar proof](area_polar_proof.md) motivated replacing a coarse
large-budget polar cover by direct exact optimization. Its five low facet
families at `T2` remain correct. The narrower small-excess linear bounds
in that proof have different hypotheses and are not extended to these larger
budgets. The current Catalan status was checked against the primary papers
of [Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531) and
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475) on 2026-09-30.
The deltoidal hexecontahedron is still listed as unresolved; the last paper's
constructed Noperthedron is a different body. This targeted literature check
does not establish an exhaustive priority search.
