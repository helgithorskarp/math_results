# Threefold receiver caps exclude every source orientation

Author: **six-rupert-3**, role **researcher**, 2026-09-30.

Let `K` be the standard rhombicosidodecahedron with edge length two,
`phi=(1+sqrt(5))/2`, and the 60 vertices in [verify.py](verify.py).
Every vertex has squared norm `R^2=7+8phi<25`, and `K=-K`.
Let `G` be the verified 60-element proper vertex rotation group. Put

\[
 d=(0,1,-\phi^2),\qquad
 \mathcal T=\{gd/\|d\|:g\in G\},\qquad \delta=1/2000000.       \tag{1}
\]

The set `T` contains twenty directed normals, including antipodes, hence
ten unoriented threefold axes.

**Theorem.** Let `B1,B2` be arbitrary real orthonormal-row `2 by 3`
projection frames. If the unit receiver normal `n2` has distance at most
`delta` from `T`, then for every planar translation `t` and every `lambda>=1`,

\[
             \lambda B_1K+t\not\subset\operatorname{int}(B_2K). \tag{2}
\]

There is **no restriction on the source orientation or its planar roll**.
These are receiver neighborhoods with an explicit chord radius, rather
than neighborhoods of a prescribed pair of frames. Their radius is
conservative. The global Rupert question remains open outside these caps.

In the argument below, translations are removed by central symmetry before
using centered shadow approximations. The last paragraph supplies that
reduction and the extension from unit scale to every `lambda>=1`.

Two additional exact conclusions used in the proof are

\[
 \min_{\|n\|=1}\operatorname{diam}(P_nK)^2=80/3+32\phi,       \tag{3}
\]

with equality exactly on `T`, and the following bound for *every* strict
passage, anywhere in the orientation space:

\[
                  \lambda^2<(87-6\phi)/76.                    \tag{4}
\]

The right side of (4) exceeds one. It does not establish non-Rupertness.
The Nieuwland supremum is at most the square root of this bound.

## 1. Exact shadow diameter and all axial sign regions

Choose thirty antipodal representatives `a_i` of the vertices and define

\[
                  f(n)=\min_i|a_i\cdot n|,\quad \|n\|=1.
\]

Central symmetry gives

\[
       \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2).             \tag{5}
\]

Indeed, a centered symmetric shadow has diameter twice its largest point
norm. Its largest squared norm is `max_v (R^2-(v dot n)^2)`.

We use the **general equal-radius active-set reduction** from
[six-rupert-2's J77 diameter proof, Section 3](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md),
source `fce6fd20899e14d0e65c564f410e98518df76977`, graph
`bafkreifyedsqxvx6zpxnj2jpg6bjzladxq3ufn7ef4ekjs6a42nvgfvxaa`.
That reduction is a dependency, rather than a new result asserted here.
The RID calculation and the quantitative uses below are provided here.

For completeness, at a positive local maximum, replace active `a_i` by
signed vectors `b_i` with `b_i dot n=f(n)>0`. The tangent gradients
`b_i-f(n)n` contain zero in their convex hull. Otherwise a separating tangent
direction increases every active contact, hence the minimum, a contradiction.
Caratheodory in the two-dimensional tangent plane uses at most three vectors.
One vector makes `n` parallel to `a_i`. Two nonzero tangent gradients have
equal norms, because the original vertices have equal norms; opposite
gradients therefore have equal weights. This makes `n` parallel to
`a_i +/- a_j`. Three signed contacts give

\[
             n\parallel(a_i-ea_j)\times(a_i-ha_k),\quad e,h=\pm1.
\]

Three distinct points on one sphere cannot be affinely collinear, so this
cross product is nonzero. Cases with fewer gradients have already been
included. The argument captures **every** positive local maximum.

It also applies separately to each nonempty open axial sign region. Such a
region is the intersection of strict hemispheres with specified signs of all
thirty dot products. Its closure is compact, its boundary has `f=0`, and it
contains a point with `f>0`. Its maximum is thus positive and interior.
Antipodal regions are identified throughout.

[global_cap_certificate.py](global_cap_certificate.py) generates all
`30+2 binom(30,2)+4 binom(30,3)=17,140` raw directions, finds no zero,
and canonically deduplicates them to **4,681** projective directions.
It evaluates all **140,430** candidate dot products, recording every sign
pattern and its exact maximum. There are 495 boundary candidates and
**436 antipodal open sign regions**. As a separate coverage check, thirty
great circles can form at most `2+30*29=872` spherical regions, or 436
antipodal pairs; the checked patterns already attain that upper bound.

The exact region maxima have eleven distinct values. Only ten regions
attain `f^2=1/3`, and all their optimizing directions form exactly the
projective orbit of `d`. Every other region has maximum at most

\[
          \beta=(19-8\phi)/29<1/3,\qquad 1/3-\beta>1/1000.   \tag{6}
\]

The compact expected output records the score multiplicities and a digest
of every candidate evaluation. No stored list of candidate directions or
region maxima is required as a proof input. Equations (5)-(6) prove (3).
Diameter monotonicity under strict containment proves (4), since an outer
shadow has squared diameter at most `4R^2` and an inner one at least
`4(R^2-1/3)`. This use of diameter follows the invariant obstruction in
[Steininger--Yurkevich, Lemma 1](https://arxiv.org/html/2112.13754).

## 2. A nearly minimal source normal is quantitatively close to T

Write `n0=d/||d||`, `c0=1/sqrt(3)`, and
`rho^2=R^2-1/3=20/3+8phi`. Thus `4<rho<5`.
The checker selects three vertices with positive `v dot n0=c0` forming
an orbit under the order-three directed stabilizer of `d`. Their tangent
projections `p_j` have sum zero, squared norm `rho^2`, and pairwise inner
product `-rho^2/2`. They form an equilateral triangle of inradius `rho/2>2`.
Hence for every tangent vector `w`,

\[
                 \min_j p_j\cdot w\le-2\|w\|.              \tag{7}
\]

In the winning sign region of `n0`, these three signed vertex dot products
are positive. If `c=n dot n0` and `s=||P_n0 n||`, (7) gives

\[
                    f(n)\le c_0c-2s.                        \tag{8}
\]

This inequality also proves uniqueness of the region's optimizer: equality
`f=c0` forces `s=0` and `c=1`. Proper body symmetries and reversal give the
same assertion at every directed member of `T`.

Each `(v dot n)^2` is Lipschitz with constant less than fifty on the unit
sphere: its difference is bounded by `R^2 ||n-n0|| ||n+n0||<50||n-n0||`.
The same bound holds for their minimum. Suppose a unit-scale closed
containment has a receiver normal within `delta` of a member of `T`.
By (5), its source normal `n1` satisfies

\[
                    f(n_1)^2\ge1/3-50\delta.                \tag{9}
\]

The gap (6) places `n1` in a winning region; boundary normals have `f=0`.
Choose its directed optimizer `n10`. Here `f(n1)>1/2` and `c0>1/2`, so

\[
 c_0-f(n_1)=\frac{c_0^2-f(n_1)^2}{c_0+f(n_1)}<50\delta.
\]

Equation (8) implies `c>0`, `s<25delta`, and therefore

\[
              \|n_1-n_{10}\|\le\sqrt2s<36\delta.          \tag{10}
\]

The proper group is transitive on all twenty directed optimizers. Changing
the source frame by a body rotation thus makes its normal within `36delta`
of the *receiver's* chosen directed threefold normal `n0`, without changing
its projected set. This includes the case of opposite normal signs.

## 3. Near containment forces the planar roll near C6

Choose minimal proper rotations `A_i` taking `n0` to the source and receiver
normals. Their operator norm distances from identity equal the corresponding
normal chord distances. Set `B0=B2 A2`. There is `U in SO(2)` such that

\[
           B_2=B_0A_2^t,\qquad B_1=UB_0A_1^t.
\]

Write `S0=B0 K`. Equation (10) bounds the source set's Hausdorff distance
from `U S0` by `5*36delta`; the receiver's distance from `S0` is less than
`5delta`. Any unit-scale containment consequently implies

\[
                 US_0\subset S_0+\eta\mathbb D,
                 \qquad\eta=190\delta,                      \tag{11}
\]

where `D` is the planar unit disk. Only this one-sided approximation is used.

The exact ambient projector `I-dd^t/||d||^2` gives **twelve distinct**
projected vertices on the radius-`rho` circle. Every other projected vertex
has squared radius at most `rho^2-4/3`. Denote the circle point set by `C`.
For `x=Up`, `p in C`, (11) gives a point `y in S0` with `||x-y||<=eta`.
Some projected vertex `q` therefore satisfies

\[
       x\cdot q\ge\rho^2-\rho\eta,\qquad
       \|x-q\|^2\le2\rho\eta<10\eta.                       \tag{12}
\]

Cauchy also gives `rho^2-||q||^2<=2rho eta`. Since `10eta<1/10`, the
squared radius gap forces `q in C`. Thus every `Up` is within

\[
              e=\sqrt{1900\delta}<1/32                     \tag{13}
\]

of the circle set.

Fix one `p in C`, and let `Uq` be the rotation sending `p` to the chosen
nearby `q in C`. Then `||U-Uq||_op=||Up-q||/rho<e/4`. The twelve possible
rotations `Uq` are checked exactly, using

\[
 c=(p\cdot q)/\rho^2,\quad
 t=d\cdot(p\times q)/(\|d\|^2\rho^2),\quad
 U_qx=cx+t(d\times x).
\]

Exactly six preserve `C`, and they also preserve the entire projected point
set. They form `C6`: the cosines are `+/-1,+/-1/2` and the nonzero cross
coefficients are `+/- (phi-1)/2`. Each of the other six rotations has some
circle point whose squared distance from `C` is strictly greater than
`1/100` (the smallest defect is `(176-96phi)/57`). Such a rotation is
impossible, since all `Uq p_j` are within `2e<1/10` of `C` by (12)-(13).
Therefore the nearby roll `Uq` belongs to `C6`.

The whole shadow's rotation group is exactly `C6`: the body stabilizer
provides `C3` and central symmetry provides the planar half-turn; any shadow
rotation must preserve its maximum-radius points, which permit only `C6`.

## 4. Remove the roll and bound the full relative rotation

Choose a body rotation `h` fixing `n0` and a sign `sigma=+/-1` so that
`sigma Uq B0 h=B0`. The three axial body rotations and the planar half-turn
generate all six possibilities. Change the source frame to
`B1'=sigma B1 h`. It gives exactly the same source shadow, since `hK=K=-K`.
Its normal remains within `36delta` of `n0`. Moreover,

\[
 \|B_1'-B_2\|_{op}<37\delta+e/4,\qquad
 \|n_1'-n_2\|<37\delta.
\]

Complete both row frames with their cross-product unit normals to proper
orthogonal matrices `S1,S2`. Summing the top-block and bottom-row operator
norm bounds gives

\[
 \|S_1-S_2\|_{op}<74\delta+e/4.
\]

The full relative rotation `Q=S2^t S1` satisfies `B1'=B2 Q`. For a rotation
of angle `theta in [0,pi]`, `theta<2||Q-I||_op` when `theta>0`. Hence

\[
              \theta<148\delta+1/64=15699/1000000.           \tag{14}
\]

This bound includes the planar roll; it is not merely a normal-angle bound.
The harmless source half-turn is essential when the limiting roll has an
odd multiple of sixty degrees.

## 5. An effective local bound throughout the threefold receiver cap

We use the actual torque-ball estimates from the prior
[five-cell proof](CELL_PROOF.md), graph
`bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq`,
source `fa77703cccae7cf90a5e5ca519bded273de776f3`.
Its chamber is `x,y>=0, z>=phi x+phi^2 y`. The threefold ray in this
chamber is `B=(0,phi^-2,1)`, a body symmetry image of `d`.

Here is a quantitative reason that a cap at `B/||B||` stays in cell `ABD`
after chamber reduction. In the complete signed orbit of `B`, every point
other than `B` violates some inward wall by a negative unit-normal dot
product of magnitude greater than `1/100`. This is checked exactly; the
minimum of the best squared negative-wall margin is `(2-phi)/3`.
Consequently a symmetry taking a normal within `delta<1/100` of `B/||B||`
into the chamber must fix `B/||B||`. It cannot move the center to a different
orbit point and repair that negative wall with a perturbation of size `delta`.

For the resulting unit normal `n`, scale to the chart `u=n/n_z`. Since
`||B||<5/4`, `n_z>79/100`, and

\[
       \|u-B\|\le\frac{(1+\|B\|)\delta}{n_z}<3\delta.     \tag{15}
\]

All vertices of the four other cells have `y<=D_y=1/(phi+2)`, whereas
`B_y-D_y=(7-4phi)/5>1/10`. Equation (15) therefore puts `u` in `ABD`.
If `u=s_A A+s_B B+s_D D`, then `y<=q B_y`, where `q=1-s_A`. Since
`B_y>3/10`, (15) gives

\[
                      q>1-10\delta>999/1000.                 \tag{16}
\]

The inherited weak contacts are valid throughout `ABD`, including all
boundary targets. We now use their **actual center facet distances**, rather
than the coarse uniform cofactor lower bound. At `B`, all four signed
cofactors are positive, their weighted torque sum is zero, and the four
squared distances from zero to the tetrahedron's facets are
`r_a^2,r_b^2,r_b^2,r_a^2`, where

\[
 r_a^2=\frac{18272-11056\phi}{37561}>\frac1{100},\qquad
 r_b^2=\frac{24160-14640\phi}{2449}>\frac1{100}.              \tag{17}
\]

Thus the center torque tetrahedron contains the ball of radius greater than
`1/10`. Each column has the form `T_j(u)=v_j cross(e_j cross u)`, with
`||v_j||<5` and `||e_j||=2`. By (15), every torque column moves by less than
`30delta`. A convex hull's support function changes by at most the largest
column displacement. The perturbed torque tetrahedron therefore contains
the centered ball of radius

\[
                r>1/10-30\delta=19997/200000.               \tag{18}
\]

The inherited remainder factor is `M=R max||m_i||<25/2`. For a nonzero
rotation with angle at most `1/63`, some torque has axis dot product at
least `r`, while its rotation remainder factor obeys

\[
         M\theta/2<25/252<19997/200000<r.                   \tag{19}
\]

That supporting inequality is violated. At zero angle the shadows
coincide. Finally (14) is strictly less than `1/63`. This contradicts the
hypothetical strict containment, using the full relative rotation angle.
Covariance under the signed body symmetries preserves properness and the full
rotation angle, so the argument applies to every member of `T`.

Central symmetry removes arbitrary translations by reflecting the containment
and taking midpoints in the convex open receiver shadow. For `lambda>=1`,
division by `lambda` reduces a strict scaled containment to a strict
unit-scale containment; the receiver contains the origin in its interior.
This proves all quantifiers in (2).

## Reproduction, prior work and scope

From the repository root, with Python 3.11 or later:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/global_cap_certificate.py --self-test
```

The deterministic output is [global_cap_expected.json](global_cap_expected.json).
Its SHA-256 is
`69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8`.
The Python 3.11.2 replay with all controls took 26.773 seconds and 24,380 KiB
peak child RSS, using one process and one thread.
The checker regenerates all candidates and sign regions, the optimizer orbit,
the active equilateral stress, the complete circle roll classification, every
needed chamber orbit separation, four exact center torque facet distances,
and twelve rational error inequalities.
It also rechecks the full inherited five-cell certificate and compares every
output field with `cell_expected.json`. Malformed controls reject a missing
vertex, missing raw or distinct candidate, missing circle point, an invalid
roll classified as valid, and a larger unsupported cap radius. No large
generated corpus, floating-point calculation, solver or external data is used.

The trust boundary comprises the inspected `Q(phi)`/`Fraction` kernel and
coordinate model, finite generator/checker completeness, and the unformalized
active-set, compactness, convexity, frame and torque arguments above. This is
an analytic theorem with exact finite hypotheses, not a proof-assistant
formalization or independent review. A separate private fixed-threshold
execution checked all 17,140 raw candidates without deduplication and obtained
the same `1/3` optimum and ten-axis optimizer set; it is a cross-check rather
than an additional trust assumption.

The named-solid status was refreshed in primary sources on 2026-09-29:
[Zeng](https://arxiv.org/html/2604.26531) explicitly leaves RID non-Rupert as
a conjecture; [Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1)
describes their remaining RID local difficulties. Their diameter invariant
is prior work. The general active-set reduction is credited to the published
J77 artifact above. Bounded targeted searches found no source for this
RID-specific exact optimizer classification or cap radius, and no priority
claim is made. The recent J77 and deltoidal local theorems remain complementary
context rather than assumptions transferred to RID.

The next global frontier is the complementary receiver directions and
relative rotations away from the excluded local neighborhoods. The global
uniform local theorem in [LOCAL_PROOF.md](LOCAL_PROOF.md) remains available;
its much smaller angle is not used in the cap proof. These explicit caps and
the quantitative sign-region gap reduce the global search domain, but they
do not complete that search or prove global mathematical nonexistence.
