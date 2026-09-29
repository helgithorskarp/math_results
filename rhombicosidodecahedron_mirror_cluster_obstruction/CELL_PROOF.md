# Five exact cells reduce the RID local frontier to one orbit

Author: **six-rupert-3**, role **researcher**, 2026-09-29.

Let `K` be the standard rhombicosidodecahedron (RID), with the 60 vertices
specified in [PROOF.md](PROOF.md). Put `phi=(1+sqrt(5))/2` and

\[
 d_*=(1,\phi,1+3\phi)/\sqrt{12+16\phi}.
\]

Let `G` be its 60-element proper rotation group, checked in [verify.py](verify.py),
and let `D_*={g d_*:g in G}`. The exact checker establishes that `D_*` consists
of **60 directed normals, or 30 unoriented axes**; it includes antipodes.

**Theorem (fixed-target rigidity and critical-orbit reduction).**

1. For every fixed orthonormal-row projection frame `B`, there is an
   `epsilon(B)>0` such that no `Q in SO(3)` with rotation angle at most
   `epsilon(B)` and no planar translation `t` satisfy
   `B Q K+t subset int(B K)`.
2. More quantitatively, if `0<rho<=1/200`, the unit normal of `B` has Euclidean
   distance at least `rho` from `D_*`, and the angle of `Q` is at most
   `rho/200000` radians, then the same strict containment is impossible.
3. Consequently, for any sequence of strict passage pairs
   `B_j Q_j K+t_j subset int(B_j K)` with `angle(Q_j)->0`, every accumulation
   point of the target normals belongs to `D_*`.

This cell theorem alone leaves a varying-target neighborhood of this one
orbit unresolved. Its quantifiers cannot be interchanged to obtain a uniform
statement. The subsequent [LOCAL_PROOF.md](LOCAL_PROOF.md) supplies the
additional quadratic argument and a uniform angle `1/10^16`. Neither theorem
proves that RID lacks global Rupert's property.

## 1. Supporting probes may have tied preimages

For a fixed target plane, choose `v_j in V` and nonzero `m_j` in that plane
with `m_j dot (v_j-w)>=0` for all vertices `w`. Unique support is unnecessary.
Put `T_j=v_j cross m_j`. Suppose `conv{T_j}` contains the closed radius-`r`
ball around zero, and `R max||m_j||<=M`, where `||v||<=R`.
Then strict containment is impossible for any rotation with

\[
 0\le\theta\le\theta_0,\qquad M\theta_0/2<r.             \tag{1}
\]

Indeed, central symmetry removes translation by the midpoint argument in
[PROOF.md](PROOF.md). At `theta=0` the two projections coincide. For
`theta>0`, let `a` be the unit rotation axis. Strict inclusion would imply
`m_j dot (Qv_j-v_j)<0` for every probe, even when the target support line has
multiple preimages. The exact analytic bound
`||Q-I-theta[a]_cross||_op<=theta^2/2`, proved in
[TORQUE_PROOF.md](TORQUE_PROOF.md), gives

\[
 a\cdot T_j<M\theta/2<r\quad\hbox{for every }j.
\]

This contradicts `max_j a dot T_j>=r`. This fixed-plane version differs from
transporting a fixed unique-support probe across a spherical cap: here the
probes will depend explicitly on the actual target normal.

## 2. A symmetry chamber and its five triangles

All target planes can be reduced to the cone

\[
 x\ge0,\qquad y\ge0,\qquad z\ge\phi x+\phi^2y.            \tag{2}
\]

Here is a finite proof of coverage that does not rely on a sphere plot.
The checker verifies that reflections with normals
`e_x`, `e_y`, and `h=(-phi,-phi^2,1)` belong to the signed symmetry group
`G union (-G)` and preserve every vertex. The vector `c=(1,1,5)` has positive
dot product with all three inward normals. Choose a signed symmetry image of
any normal maximizing its dot product with `c`. If one inequality in (2)
failed, reflection in that wall would increase the dot product, contradicting
maximality. Changing the sign of a normal does not change its projection plane.
Thus (2) covers all planes up to proper body symmetry and normal reversal.

Every nonzero ray in (2) has `z>0`. Scale it to `u=(x,y,1)`. The resulting
parameter triangle has vertices

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad C=(\phi^{-1},0,1).
\]

Define

\[
 D=(1/(\phi(\phi+2)),1/(\phi+2),1),\quad
 E=(\phi^{-2},\phi^{-4},1),\quad F=(\phi^{-2},0,1),
 \quad H=(A+D)/2.                                         \tag{3}
\]

The points `B,D,E,C` lie in that order on the outer side of the triangle;
`F` lies on the open side `AC`. Splitting first along `AD` and `AE`, then
along `EF` and `HE`, gives five closed triangles:

| cell | rays `U_0,U_1,U_2` | exceptional corner of this certificate |
| --- | --- | --- |
| 0 | `A,B,D` | `A` |
| 1 | `A,H,E` | `A` |
| 2 | `H,D,E` | `D` |
| 3 | `A,E,F` | `A` |
| 4 | `F,E,C` | none |

All incidences and orderings are exact checks in `Q(phi)`. The point `D` is
`(1,phi,1+3phi)/(1+3phi)`, so its normalized direction is precisely `d_*`.
Only three face-normal planes cross the chamber's interior, giving four
silhouette cells; dividing the middle cell at `H` gives the five triangles
above. That exploratory face arrangement is not required by the final proof:
support is checked directly against all vertices for each listed triangle.

## 3. Polynomial certificates on whole triangles

[cell_probes.json](cell_probes.json) specifies four exact pairs `(v_j,d_j)`
for each triangle. For the actual ray `u`, use

\[
 m_j(u)=d_j\times u,\qquad T_j(u)=v_j\times(d_j\times u).
\]

Every `d_j` has length two. The checker verifies, at each of the three rays,

\[
 (d_j\times U_k)\cdot(v_j-w)\ge0\quad(w\in V).             \tag{4}
\]

Since (4) is linear in `u`, these **3,600 exact comparisons** prove supporting
probe validity throughout each closed triangle, including tied support lines.
No sampled hull is assumed by this certificate.

Write `u=s_0U_0+s_1U_1+s_2U_2`, with nonnegative barycentric coordinates of
sum one. For each triangle the input supplies a sign `sigma=+1` or `-1`.
Define the four cofactor stresses

\[
 \lambda_j(s)=\sigma(-1)^j
 \det(T_0(u),\ldots,\widehat{T_j(u)},\ldots,T_3(u)).         \tag{5}
\]

Each is a homogeneous cubic. Determinant trilinearity gives its ten monomial
coefficients exactly. For all **200 coefficients**, the checker verifies:

* every coefficient is nonnegative;
* except for the cube of an exceptional barycentric coordinate, the coefficient
  of `s_0^i s_1^j s_2^k` is strictly greater than
  `binom(3;i,j,k)/10`;
* for cell 4 the strict condition applies to every coefficient.

The least normalized nonexceptional coefficient is
`(-1072+664phi)/15`, which is greater than `1/10`. These are coefficients of
the complete polynomials, not checks at a grid of parameter values.

Put `q=1-s_b` if the table's exceptional corner has index `b`, and `q=1`
for cell 4. The coefficient bounds imply

\[
 \lambda_j(s)\ge(1-s_b^3)/10\ge q/10\quad\hbox{or}\quad
 \lambda_j(s)>1/10\text{ in cell 4}.                       \tag{6}
\]

Thus every stress is positive when `q>0`. Cofactor algebra gives
`sum_j lambda_j T_j=0`; a nonzero minor gives rank three. Positive stresses
therefore place the origin in the interior of a nondegenerate torque
tetrahedron.

All triangle rays have norm less than `5/4`; this also holds for their convex
combinations. Since `R<5` and `||d_j||=2`,

\[
 \|T_j\|<25/2,\qquad R\|m_j\|<25/2=M.
\]

A facet normal `(T_j-T_i) cross (T_k-T_i)` has norm less than `625`. Its
dot product with any vertex of that facet is, in absolute value, the cofactor
stress for the omitted vertex. By (6), every facet has distance greater than

\[
 r=q/6250                                                  \tag{7}
\]

from zero. Hence its convex hull contains the closed radius-`r` ball.
Taking

\[
 \theta_0=q/100000
\]

satisfies (1), since `M theta_0/2=q/16000<q/6250`.
This proves a positive exclusion angle on every listed triangle away from its
exceptional corner. `D` itself is covered with `q=1` by cell 0; therefore all
normals in the chamber except `A` have a fixed-target exclusion angle.

## 4. The mirror direction and a uniform bound off the critical orbit

At `A`, apply the paired/singleton class lemma in [PROOF.md](PROOF.md).
After a common in-plane coordinate change the target frame is `P_xy`.
For a source rotation with angle at most `1/100`, its frame has distance at
most `1/100` from `P_xy`, giving the fixed-target assertion at `A`.

We also need the varying-target version near this axis. If the target normal
is within `1/200` of `A`, there is a common planar change of basis making its
row frame have operator norm distance at most `1/200` from `P_xy`. To see
this, use the minimal proper rotation taking `A` to the target normal: its
operator norm distance from identity equals the Euclidean normal distance.
A relative source rotation of angle at most `1/200` adds at most `1/200`
to the row-frame distance. Both frames then satisfy the class lemma's
`1/100` hypothesis. The same applies at all 15 mirror axes by symmetry.

For a cell with exceptional ray `U_b`, its diameter is less than one and all
its rays have norm at least one, because their third coordinate is one. Thus

\[
 \left\|\frac{u}{\|u\|}-\frac{U_b}{\|U_b\|}\right\|
 \le2\|u-U_b\|\le2(1-s_b)\max_k\|U_k-U_b\|<2q.            \tag{8}
\]

Now fix `0<rho<=1/200` and a target normal at distance at least `rho` from
`D_*`. Reduce it to the chamber. In cells 0,1,3, either its distance to `A`
is at most `1/200`, where the mirror lemma applies, or (8) gives
`q>1/400>=rho/2`. In cell 2, (8) and its distance to `d_*` give `q>rho/2`.
In cell 4, `q=1`. In every case, an angle at most `rho/200000` is excluded.
At `D` use cell 0, as above. This proves item 2, and compactness of the unit
sphere immediately proves the accumulation statement in item 3.

The relative rotation is the same one as in [TORQUE_PROOF.md](TORQUE_PROOF.md):
complete source and target row frames to proper matrices `S_1,S_2`, then
`Q=S_2^t S_1` and `B_1=B_2Q`. No arbitrary relative planar roll is removed
from its angle. All translations are allowed.

## 5. Why a uniform first-order argument still fails at D

[limit_silhouette.json](limit_silhouette.json) supplies the 16 cyclic
silhouette vertices in the open triangle `A,D,E`. The checker verifies its
entire silhouette: every edge supports all 60 vertices at all three parameter
rays, has only its two endpoints as supporting preimages in the open cell,
and every turn is strictly convex there. Vertex normal cones are generated
by their two incident edge normals, so the 32 endpoint-edge torques generate
the full contact cone on this open cell.

Every edge probe has a nonzero limit at `D`. For those 32 limiting torques,
the exact tangent vector

\[
 a_*=(1,\phi,1-\phi),\qquad a_*\cdot D=0,
\]

satisfies `a_* dot T<=0`: **16 dot products vanish and 16 are negative**.
The same signs hold after normalizing every edge probe to length one.
There is also a uniform bound for arbitrary unit support probes at a vertex:
if `m=alpha m_left+beta m_right` with the two edge normals normalized and
`alpha,beta>=0`, then `alpha+beta<5`. Indeed, the eight sign choices of
`(1,1,phi^3)` enclose the unit ball in `K`, so every unit edge normal has
support value at least one. Taking the dot product with the supporting vertex
gives `alpha+beta<=v dot m<5`. Thus no unbounded cancellation of incident
edge normals is hidden in this limit.

Consequently, the support of the convex hull of **all unit-probe contact
torques** in direction `a_*/||a_*||` tends to a value at most zero. A uniform
positive ball for bounded probes, or a uniform positive torque-to-probe-norm
ratio, is impossible along this cell as the target tends to `D`. This does
not describe all support preimages at `D` itself, where extra ties appear
and cell 0 supplies a positive torque tetrahedron. It does not establish a
passage or disprove a possible second-order exclusion. The explicit
`(D,a_*)` pair is the remaining structural frontier for this method.

## 6. Reproduction and dependencies

From the repository root, using Python 3.11+ and only its standard library:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/cell_certificate.py --self-test
```

Its exact output is [cell_expected.json](cell_expected.json). The checker
rejects reversed probes, reversed stress signs, a missing cell, and a reversed
silhouette. Cubic expansions are cross-checked against directly evaluated
determinants at two exact interior points. The prior mirror and four-probe
checkers remain dependencies and retain their previous outputs.

The hulls and candidate selection were discovered with floating-point
diagnostics. Final inputs are explicit algebraic vectors; the checker uses no
floating point, solver, incomplete enumeration, or sphere sampling. The
geometric proofs above remain an unformalized trust boundary; independent
review has not been claimed.

Primary literature: [Steininger--Yurkevich, 2023](https://arxiv.org/html/2112.13754)
for strict projection equivalence and standard coordinates;
[Steininger--Yurkevich, 2025, Section 9.1](https://arxiv.org/html/2508.18475)
for the RID local gap and their varying-target definition;
[Scott, 2022, Definition 1](https://arxiv.org/html/2208.12912) for the
fixed-oriented local formulation; and [Zeng, 2026](https://arxiv.org/html/2604.26531)
for the still-open RID non-Rupert conjecture. We state the quantifiers explicitly
and make no priority claim for the general contact-gradient mechanism.

Related team work: **six-rupert-1**, researcher,
[all-direction fixed-target deltoidal certificate](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md),
source commit `e254663421e086d03dbd8bf71486cbe06ac67c1b`, developed in parallel.
Both certificates use linear edge contacts, homogeneous cubic stresses, and
the same three-wall symmetry chamber for different named solids. The present
RID result additionally bounds the exclusion angle away from one critical
orbit and supplies an exact limiting separator there. It builds on
the author's [earlier support-probe and mirror lemmas](TORQUE_PROOF.md).
