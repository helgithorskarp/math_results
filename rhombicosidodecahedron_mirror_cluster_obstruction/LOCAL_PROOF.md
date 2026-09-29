# A uniform local exclusion for the rhombicosidodecahedron

Author: **six-rupert-3**, role **researcher**, 2026-09-29.

Let `K` be the standard rhombicosidodecahedron, whose sphere-inscribed vertex
set `V` is specified in [PROOF.md](PROOF.md). Put `phi=(1+sqrt(5))/2`.
The proof below combines the five-cell certificate in
[CELL_PROOF.md](CELL_PROOF.md) with new exact critical-direction identities.

**Theorem.** Set `theta0=1/10^16` radians. For every real 2-by-3 matrix `B`
with orthonormal rows, every proper rotation `Q` of angle at most `theta0`,
and every `t in R^2`,

\[
 BQK+t\not\subset\operatorname{int}(BK).                    \tag{1}
\]

Both projection orientations may vary independently. The angle is that of
the full relative three-dimensional rotation, including relative planar roll.
In particular, RID is **not locally Rupert in the varying-pair sense of
Steininger--Yurkevich, Definition 52**. The explicit angle is deliberately
conservative. This theorem does **not** settle global Rupertness: that paper's
Ruperthedron demonstrates that a body can be Rupert without being locally
Rupert. No exclusion of all nonlocal relative rotations is claimed here.

The finite hypotheses and every stated scalar error bound are verified by
[local_certificate.py](local_certificate.py), with expected output
[local_expected.json](local_expected.json). The analytic bridge below is
unformalized; the checker does not enumerate rotations or evaluate limits.

## 1. Reduction and scale of a hypothetical passage

Central symmetry removes translation by the midpoint argument in
[PROOF.md, Section 2](PROOF.md). Suppose for a contradiction that (1) fails,
and write `theta=angle(Q)`. Identical projections exclude `theta=0`, so
`0<theta<=theta0`.

The verified signed symmetry group reduces the target normal to the chamber
`x,y>=0, z>=phi*x+phi^2*y`. Conjugating `Q` by this body symmetry preserves
its properness and angle. Scale the target ray to `u_ray=(x,y,1)`.

Use the five closed triangles `ABD,AHE,HDE,AEF,FEC` and their exceptional
corners in [CELL_PROOF.md, Sections 2--4](CELL_PROOF.md). The polynomial
certificate excludes a passage when `theta<=q/100000`, with
`q=1-s_bad`, or `q=1` in the last triangle. Thus a passage in any triangle
would require

\[
 q<100000\theta.                                          \tag{2}
\]

In the three triangles exceptional at `A`, their diameter less than one
and the normalization estimate give target normal distance `<2q` from `A`.
By (2), this is `<200000 theta0<1/200`. Since `theta0<1/200`, the uniform
mirror-class neighborhood excludes these cases. Triangle `FEC` is excluded
by its fixed angle `1/100000`. Consequently the only remaining triangle is
`HDE`, a subset of the closed silhouette triangle `ADE`.

Write

\[
 u_*=(1,\phi,1+3\phi),\quad
 a=(1,\phi,1-\phi),\quad b=(-\phi,1,0),                    \tag{3}
\]
\[
 N=\|u_*\|^2=12+16\phi,\quad
 \|a\|^2=4,\quad \|b\|^2=\phi+2=:B_0.
\]

These three vectors are mutually orthogonal, and

\[
 u_*\times a=4\phi b.                                    \tag{4}
\]

The chamber ray `D` equals `u_* /(1+3phi)`. Put
`u=(1+3phi)u_ray`, so `u` has the actual target direction. The diameter
bound, (2), and `1+3phi<6` give

\[
 \|u-u_*\|<600000\theta.                                  \tag{5}
\]

Use the Cayley representation of `Q`, setting

\[
 w=\varepsilon\alpha,\qquad \|\alpha\|=2,\qquad
 \varepsilon=\tfrac12\tan(\theta/2).
\]

For `0<theta<=1`, elementary trigonometric inequalities give
`theta<=4epsilon` and `epsilon<=theta`. Set `C=3000000` and write

\[
 u=u_*+\varepsilon r,\qquad \|r\|<C.                      \tag{6}
\]

Indeed, (5) gives `||r||<2400000<C`. The Cayley formula is

\[
 Qv= v+\frac{2\varepsilon\alpha\times v
             +2\varepsilon^2\alpha\times(\alpha\times v)}
                    {1+4\varepsilon^2}.                 \tag{7}
\]

Also `||u_*||<7`, `||u||<8`, and every vertex has norm `<5`.
The target norm bound follows from `||u_ray||<5/4` in the chamber and
`1+3phi<6`.

## 2. Five contacts force the relative rotation axis close to a

Let `L_0,...,L_15` be the cyclic vertices in
[limit_silhouette.json](limit_silhouette.json). Put

\[
 d_j=L_{j+1}-L_j,\qquad m_j(u)=d_j\times u,
 \qquad T_j(v)=v\times(d_j\times u_*),                     \tag{8}
\]

with cyclic subscripts. Each `d_j` has length two. All these probes support
`K` throughout the closed triangle `ADE`, including at extra ties. Supporting
endpoint contacts remain valid on its edges. The new checker separately
verifies **1080** corner support comparisons for the six edges used below;
linearity extends them over `ADE`.

The five endpoint contacts used are

\[
 t_0=T_1(L_1),\quad t_1=T_2(L_3),\quad
 t_-=T_3(L_4),\quad t_+=T_4(L_4),\quad t_n=T_0(L_1).
\]

Their exact identities are

\[
 \phi t_0+t_1=0,\qquad t_-=-2u_*,\qquad t_+=2u_*,          \tag{9}
\]
\[
 a\cdot t_0=0,\quad b\cdot t_0=-4,\quad
 u_*\cdot t_0=16+24\phi<56,\quad a\cdot t_n=-4.            \tag{10}
\]

For any of these contacts, strict containment and (7) give

\[
 \alpha\cdot(v\times m_j(u))
 +\varepsilon\big((\alpha\cdot v)(\alpha\cdot m_j(u))
                      -4v\cdot m_j(u)\big)<0.            \tag{11}
\]

Here `||m_j(u)||<16`. The quadratic expression in (11) has absolute value
less than `8*5*16=640`. Replacing `u` by `u_*` in its linear term costs
less than `2*5*2*C*epsilon=20C epsilon`. Therefore, with

\[
 E=21C\varepsilon<1/1000,
\]

all five contacts satisfy `alpha dot t<E`.
From (9), `|alpha dot u_*|<E/2` and `|alpha dot t_0|<E`.
Decompose `alpha=s a+p b+z u_*`. Since `N>30`,

\[
 |z|<E/60,\qquad
 |p|<\tfrac14(E+56E/60)<E/2.
\]

Using `||b||<2` and `||u_*||<7`, the orthogonal error
`e_perp=alpha-s a` has norm `<2E`. The equality `||alpha||=||a||=2`
implies `|s|>9/10`. If `s<0`, (10) and `||t_n||<70` would give

\[
 \alpha\cdot t_n>18/5-140E>E,
\]

contradicting (11). Thus `s>0`, and
`1-s=||e_perp||^2/(4(1+s))<E^2`. In particular,

\[
 \|\alpha-a\|<2E+2E^2<3E=63C\varepsilon.                 \tag{12}
\]

This replaces a qualitative limiting-axis assertion by a uniform error bound.

## 3. A hidden supporting vertex gives an upper bound on Y

Decompose `r=X a+Y b+Z u_*`. On edge 5, the outer supporting vertex is
`v=L_5=(-phi^2,2+phi,0)` and

\[
 d=d_5=(1-\phi,-1,\phi).
\]

The distinct vertex `h=(-2phi,phi^2,-phi)` ties at the critical ray:
`(d cross u_*) dot (h-v)=0`. It need not be a supporting endpoint for the
actual target; strict inclusion must place its rotated image below this
outer supporting line. Exact arithmetic gives

\[
 (d\times r)\cdot(h-v)=2B_0Y,\qquad
 2a\cdot(h\times(d\times u_*))=16+24\phi.                 \tag{13}
\]

Apply (7) to this vertex and multiply its support inequality by
`1+4epsilon^2`. After division by `epsilon`, its numerator is

\[
 (1+4\varepsilon^2)\,2B_0Y
 +2\alpha\cdot(h\times(d\times u_*))
 +2\varepsilon\alpha\cdot(h\times(d\times r))
 +2\varepsilon q,
\]

where `q=(alpha dot h)(alpha dot m_5(u))-4 h dot m_5(u)` has absolute
value `<640`. By (12), replacing `alpha` by `a` costs `<8820C epsilon`.
The last two terms cost `<40C epsilon+1280 epsilon`, and the extra
`4epsilon^2` term costs `<80C epsilon^2`. Thus (13) implies

\[
 2B_0Y+16+24\phi<10000C\varepsilon.
\]

Since `B_0>3` and
`(16+24phi)/(2B_0)=(12+16phi)/5`,

\[
 Y<-(12+16\phi)/5+2000C\varepsilon.                      \tag{14}
\]

Keeping this hidden preimage is essential. Using only the open-cell
endpoint contacts would miss (14).

## 4. Two zero-height vertices give the incompatible lower bound

The four vertices `+/-v_+,+/-v_-`, where

\[
 v_+=\phi(a+b)=(-1,1+2\phi,-1),\quad
 v_-=\phi(a-b)=(1+2\phi,1,-1),                            \tag{15}
\]

have zero dot product with `u_*`. Each is uniquely radially exposed in
that projection:

\[
 v\cdot(v-h)\ge2\quad(h\in V,\ h\ne v).                  \tag{16}
\]

All **236** comparisons are checked exactly; the minimum is two.
Choose any fixed orthonormal frame `P` for the plane perpendicular to `u_*`.
After one common planar orthogonal change, the target frame is within
`2C epsilon` of `P`: normal normalization is Lipschitz with constant at
most two here, and the minimal normal-aligning rotation has operator
norm distance equal to the normal chord distance. The source frame `BQ`
is within `(2C+4)epsilon<3C epsilon` of `P`.

The radial-class lemma in [PROOF.md, Section 1](PROOF.md) is coordinate
independent. At frame radius `eta=3C epsilon`, its support error is

\[
 4R^2\eta+2R^2\eta^2<100\eta+50\eta^2<2.
\]

By (16), strict containment consequently requires

\[
 \|BQv_\pm\|<\|Bv_\pm\|,
 \quad\text{equivalently}\quad
 |v_\pm\cdot Q^tu|>|v_\pm\cdot u|.                       \tag{17}
\]

From the transpose of (7), (4), (6), and (12), write

\[
 Q^tu=u_*+\varepsilon(r+8\phi b+e),\qquad
 \|e\|<1000C\varepsilon.                                 \tag{18}
\]

For completeness, subtract the first-order term explicitly. The error
numerator is

\[
 -2(\alpha-a)\times u_*
 -2\varepsilon\alpha\times r
 +2\varepsilon\alpha\times(\alpha\times u)
 +8\varepsilon^2 a\times u_*.
\]

After division by `1+4epsilon^2`, the corresponding bounds are
`882C epsilon`, `4C epsilon`, `64 epsilon`, and `112 epsilon^2`.
Their sum is less than the bound in (18).

Since `v_+ dot u_*=v_- dot u_*=0`, (17) implies that the sum of the two
squared axial differences is positive. The exact ideal sum is

\[
 \sum_{\sigma\in\{+,-\}}
 \big[(v_\sigma\cdot(r+8\phi b))^2-(v_\sigma\cdot r)^2\big]
 =32\phi^3B_0^2(Y+4\phi).                                \tag{19}
\]

For each term, `|v dot(r+8phi b)|<5(C+32)<6C` and
`|v dot e|<5000C epsilon`. Thus the total error introduced by (18) is less
than

\[
 120000C^2\varepsilon+50000000C^2\varepsilon^2
 <121000C^2\varepsilon.
\]

The coefficient `32phi^3B_0^2` is greater than 1000. Equations (17)--(19)
therefore imply the weaker convenient bound

\[
 Y>-4\phi-200C^2\varepsilon.                             \tag{20}
\]

But the exact gap between (14) and (20) is

\[
 (12+16\phi)/5-4\phi=(12-4\phi)/5>4/5,
\]

whereas their combined error is at most

\[
 (200C^2+2000C)\theta_0=900003/5000000<4/5.               \tag{21}
\]

This is a contradiction. It excludes the last triangle, including all
boundary cases, and proves the theorem.

## 5. Definitions, literature, and what remains

[Steininger--Yurkevich, Definition 52](https://arxiv.org/html/2508.18475#S8)
allow both projections to vary while their two angular parameter differences
and planar roll tend to zero. These differences force the completed proper
projection frames' relative rotation to tend to identity, even at polar
coordinate singularities; thus the uniform theorem implies failure of their
local property. It also implies failure of Scott's fixed-outer local property.

[Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1)
identify the RID local gap, acknowledge polynomial exclusion of the top view,
and leave harder regions untreated. Their global theorem is a method,
not a published full RID global exclusion certificate. The contribution here
is the whole-chamber certificate plus the explicit critical-ray obstruction
(9)--(21). No literature priority claim is made.
[Zeng](https://arxiv.org/html/2604.26531) retains the global RID conjecture.
Both primary seeds were refreshed on 2026-09-29.

Complementary all-direction fixed-target contact certificates by
**six-rupert-1**, for a different solid, are acknowledged in
[the deltoidal proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md).
They are not mathematical assumptions in the critical-direction argument.
The earlier RID five-cell and mirror proofs are actual dependencies, and
their finite hypotheses are rechecked by the reproduction command below.

Next: use the explicit local exclusion to organize a rigorous nonlocal
containment obstruction, preferably structural, or produce a certified finite
cover of the remaining relative rotations. Improving the very conservative
angle is useful for a practical global cover, but global nonexistence cannot
be inferred from a positive local gap.

## Reproduce and trust boundary

From the repository root, with Python 3.11+ and its standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/local_certificate.py --self-test
```

The checker rechecks the complete prior cell certificate and mirror criterion,
adds 1080 support and 236 radial comparisons, the exact axis and hidden-vertex
identities, the quadratic stress identity, and 15 rational error audits.
Self-tests reject a reversed axis or silhouette, a wrong hidden vertex, missing
radial directions and an unsupported angle; they also check exact Cayley
orthogonality, determinant and support-numerator identities. No numerical
solver, sampled directions, external database, or large certificate is needed.

Recorded complete self-test run: Python 3.11.2, 3.291 seconds, peak child
resident memory 19,872 KiB, one process. Expected output SHA256:
`5ba10067e5e707810cdf08b3a41d117e619e866d2c97032ddb914544e6379f84`.
The inherited cell output remains byte-identical, with SHA256
`a1840fc9ca6f501ad0a2ad5a4b56cf0069636ddf224162b5e3a3d1b7754c30d9`.
The trust boundary is the Q(phi)/Fraction kernel, the standard coordinate
model, and the inspected unformalized analytic arguments above and in the
dependency proofs. Independent review or formal verification is not asserted.
