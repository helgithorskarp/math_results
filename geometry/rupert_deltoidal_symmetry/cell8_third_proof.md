# All original closed passages on the deltoidal one-third collar are equality

**six-rupert-1, researcher; 2026-10-01.** Author-checked written
intermediate proof with exact finite certificates. The continuous
arguments are unformalized and independently unreviewed. Historical
priority and optimality are unasserted. The original deltoidal
hexecontahedron's global Rupert property remains **OPEN**.

The new step couples the source's necessary projection area to the
receiver's area. It sharpens both the actual spatial quaternion bound
near zero roll and the signed support bound at other rolls. The whole
closed receiving collar is covered, with every original source and
physical translation and scale, rather than one source-cell orbit.

## 1. Original body, domain and quantified conclusion

Let $K=-K$ be the original centered 62-vertex deltoidal hexecontahedron
in [verify.py](verify.py). Its actual proper rotation group $G$ has 60
elements; its full reflection group $F$ has 120. Use the actual twelve
area cells and their ordered corners from
[global_area_proof.md](global_area_proof.md). Put $s=\sqrt5>0$ and

$$
M=N_9=((3s-5)/6,(s-1)/6,1),\quad
M_2=(28-8s)/9,\quad L_0=\|M\|,\quad m=M/L_0.
$$

The original Cell8 has ordered corners $(N_6,N_{11},N_{10},N_8)$.
Define

$$
W=((75-17s)/114,(7+5s)/114,1),\qquad
U=(N_6+N_{11}+N_{10}+N_8)/4,\qquad Z=(2W+U)/3.
$$

The two closed receiving triangles are

$$
L=\operatorname{conv}(N_8,W,Z),\qquad
B=\operatorname{conv}(W,N_{10},Z).
$$

They partition the entire closed collar
$\mathcal C_{1/3}=\operatorname{conv}(N_8,N_{10},Z)$.
Indeed $W=(1-r)N_8+rN_{10}$ with $r=(17+4s)/57\in(0,1)$.
The verifier checks the partition, all Cell8 side inequalities, the
strict interior tip inequalities, and containment of the old
[one-quarter collar](cell8_quarter_proof.md).
Let $\mathcal R_{1/3}$ be the normalized rays of this collar and all
their actual proper-body and antipodal images. For unit $n$, put
$P_n=I-nn^t$ and $J_n=2nn^t-I\in SO(3)$.

**Theorem.** For every $n\in\mathcal R_{1/3}$, every original
$Q\in SO(3)$, every $t\in n^\perp$, and every $\lambda\ge1$,

$$
\lambda P_n(QK)+t\subseteq P_nK
\quad\Longleftrightarrow\quad
\lambda=1,\ t=0,\ Q\in G\cup J_nG.                 \tag{1}
$$

These are exactly 120 proper rotations in two disjoint **LEFT** cosets.
Every permitted placement has equal shadows. Thus strict Rupert passage
is excluded on this entire closed receiving domain. All triangle and
source-cell boundaries, shared edges and roll endpoints are included.
Whole Cell8 and the remaining global receiving complement stay open.

The earlier [Cell11 source exclusion](cell8_third_source_proof.md),
source74ad8c5d554c7c2e64527f7157e042adae519080, graph8352, handles its
entire full-symmetry source orbit on precisely these receivers and all
rolls. Its complete fixed checker is a required dependency below. The
present proof covers every other original source cell as well.

## 2. Exact area budgets and proper source gauges

For unit $k$, write $A(k)=\operatorname{Area}(P_kK)$. On each original
cell this is $C_i\cdot k$, where $C_i$ is its actual physical area vector.
Fresh complete corner, edge and interior stationary tests put both
receiving maxima at $Z$, with common squared value

$$
\frac{10491016792536550+4680162669608510s}{95123111726709}
<T^2,\qquad T=927669/62500.                         \tag{2}
$$

Suppose (1)'s containment holds. Reflection gives the negative
translation as well, and convex midpoints remove $t$. Contraction toward
zero removes $\lambda\ge1$ as a necessary condition. Therefore

$$
P_n(QK)\subseteq P_nK,\qquad A(Q^tn)\le A(n)<T.     \tag{3}
$$

The complete [source-critical proof](source_extrema_proof.md) supplies
the compactness and active-stratum classification on all twelve closed
fan cells. At this fresh budget the verifier generates 212 entries:
40 corners,24 sphere stationary points,18 area-circle stationary points,
80 edge stationary points,50 area-edge intersections. Exactly65 are
feasible. Unit norms, declared active constraints, all weak cone signs
and the unsquared area inequality are checked for every entry, retaining
both radical branches. The verifier compares objectives separately in
every cell and regenerates every sharp direction and chord window.

In the fundamental chamber the nearest minimum-area axis is $m$.
The original nearest-axis proof and 180 comparisons are replayed.
Every feasible source in cells

$$
\mathcal I=\{0,1,2,3,4,5,6,7,9\}
$$

has $\|k-m\|<a_c=113081/10^6$; Cell0 is empty at this budget.
Cells8,10,11 have the valid common bound
$\|k-m\|<a_w=13441/50000$. The sharp global maximum is on Cell11/edge0,
strictly between268819/$10^6$ and $a_w$. In particular an area-only
source cap $1/5$ is false here; it is never assumed.

Proper gauges require both source copies. Let $S$ be the third original
wall reflection. It permutes all62 vertices and fixes $M$. Choose
$f\in F$ such that $f^tQ^tn\in H$ for the original source direction.
For $\det f=1$ use the actual right body factor $h=f\in G$; for
$\det f=-1$ use $h=fS\in G$. The gauged source $k=h^tQ^tn$ is in
$H$ or $SH$. Both copies of every closed cell are retained, with
physical area vectors $C_i$ and $SC_i$ respectively. The verifier
checks all three original reflection permutations, central symmetry
and $SM=M$. No improper moving rotation is admitted.

Let $R_1,R_2$ be the actual proper minimal transports $m\mapsto k$ and
$m\mapsto n$. Since $Qh\,k=n$, it differs from $R_2R_1^t$ by a proper
roll about $m$. The actual left half-turn $J_n$ preserves the centered
source shadow because $P_nJ_n=-P_n$ and $QK=-QK$. Thus, for some
$\epsilon\in\{0,1\}$,

$$
Q'=J_n^\epsilon Qh=R_2C_\alpha R_1^t,\quad
-\pi/2\le\alpha\le\pi/2.                              \tag{4}
$$

Put $x=\tan(|\alpha|/2)\in[0,1]$ and retain both signs $\sigma$.
For each sign, all eight closed intervals $[i/8,(i+1)/8]$ are covered.

## 3. Complete closed source and roll forests

Represent a gauged source by $q=M+w$, $M\cdot w=0$, $k=q/\|q\|$,
using $w=y_1(1,0,-M_x)+y_2(0,1,-M_y)$.
For the appropriate $a=a_c$ or $a_w$, set

$$
c_0=1-a^2/2>17/18,\qquad
U_0=M_2(c_0^{-2}-1),\qquad \|w\|^2<U_0.               \tag{5}
$$

The exact inverse-Gram rectangle and16 Cauchy halfplanes enclose this
cap. Intersect with every actual cell's inward cone sides and the
necessary area halfplane $C_i\cdot q\le TM_H/c_0$, where

$$
M_L=21199/20000<L_0<1059951/10^6=M_H.                 \tag{6}
$$

Both squared root signs are checked. Reflect the complete polygons for
$SH$, rather than assuming their enclosing cap polygon is invariant.
At each node apply two further necessary area cuts using
$\|q\|\le\operatorname{upper\_sqrt}(M_2+
\min(U_0,\max_P\|w\|^2))$. Every actual feasible source is retained.

The fixed table has352 roots: two signs,eight roll bins,two proper
source copies,eleven cells0 through10. The required Cell11 dependency
supplies the other32 roots. A roll step bisects the closed interval;
a source step bisects the longer coordinate range at its exact midpoint,
with both closed halves retained. Each depth is at most3. Source splits
occur only after the three roll steps. Each node repeats the two
necessary area cuts. Fixed replay reconstructs exactly this sequence.

Before mathematical imports, the verifier checks every original root,
the distinct complete binary roll cover and, at each roll terminal,
the distinct complete binary source cover. Missing roots, prefix gaps,
duplicate or ancestor leaves and incorrect source-before-roll paths are
rejected. Boundary overlap is allowed and ensures closed coverage.
The table has839 leaves:32 empty-cap,89 empty-area,58 local-Cayley,
650 ordinary strict-support and10 correlated strict-support leaves.
The Cell11 certificate separately has32 strict original-vertex patches.

The polygon norm maximum occurs at a corner. Its minimum is obtained
from all corners, admitted edge stationary points, and zero if zero
belongs to the polygon. Points, segments and both polygon orientations
are included. If the minimum exceeds $U_0$, the cap branch is empty.
Otherwise this gives exact bounds on every actual source norm and
on the positive increasing transport factors
$l(c)=c/M_2$, $b(c)=c^2/(M_2(1+c))$, with $c=L_0/\|q\|$.
The [Cell11 checker](cell8_third_source_certificate.py) also supplies
six exact norm-extrema degeneracy regressions.

## 4. Source area constrains the actual receiver

Map a receiving raw ray $u$ to

$$
v=M_2u/(M\cdot u)-M.                                  \tag{7}
$$

All original receiving corners have $M\cdot u>0$. This projective map
sends their convex triangle precisely to the convex hull of its tangent
corner images: the weights are proportional to $M\cdot u$, and the
inverse weights are positive. Thus no receiver is lost.

For a closed source polygon, choose outward corner norms
$r_j\ge\|M+w_j\|$ and
$a\le\min_j C_i\cdot(M+w_j)/r_j$, with $a>0$.
The reflected copy uses $SC_i$. The millionth-grid value $a$ is rounded
**down**, with both bounding comparisons checked. For convex weights,

$$
C_i\cdot\sum_jt_j(M+w_j)
\ge a\sum_jt_j\|M+w_j\|
\ge a\left\|\sum_jt_j(M+w_j)\right\|.                 \tag{8}
$$

Consequently $A(k)\ge a$ throughout the whole polygon. If $a>T$, (3)
is impossible. Otherwise every compatible receiver has $A(n)\ge a$.
For ANY tangent anchor $z$ and outward $r_z\ge\|M+z\|$, Cauchy gives
the necessary **closed affine cut**

$$
\left[C_8-(a/r_z)(M+z)\right]\cdot(M+v)\ge0.          \tag{9}
$$

Indeed $\|M+v\|\ge(M+z)\cdot(M+v)/r_z$; when the latter dot product
is negative the inequality is immediate. Combine this with
$C_8\cdot(M+v)\ge a\|M+v\|$. Any number of these cuts is valid.
The fixed algorithm takes two rounds of current polygon corners and
their average as anchors. It records every norm, anchor, cut and
retained polygon. An empty receiver polygon eliminates that branch.

For an ordinary signed-support leaf use the whole original receivers.
For a correlated leaf use both retained receiver polygons from (9).
Mapping their corners back to $M+v$ gives their exact positive ray cones.
An acute chord cap is a convex cone, so outward corner chord tests bound
the entire retained receiver domain, including segments and points.

For each original reference facet $\mu,H$, put
$\eta\ge\|\mu\|$, $r_p\ge\|P_mp\|$ and
$\chi=\mu\cdot n/L_0$. The
[rank-one transport proof](rank_transport_wedge_proof.md) gives

$$
\mu\cdot R_2^tp
\le\mu\cdot p-(M\cdot p)\chi
+(d^2/4)(\eta r_p-\mu\cdot p).                       \tag{10}
$$

On each positive ray cone, $\mu\cdot u/(M\cdot u)$ is a weighted
corner average, and $\chi$ is that ratio times $m\cdot n\in(0,1]$.
Include zero with its corner endpoints. All16 facets,62 original
vertices and both ratio endpoints give1984 exact comparisons for each
receiver polygon. Their maximum with zero supplies $B_\mu\ge0$ such
that $\max_K\mu\cdot R_2^tp\le H+B_\mu$.
Taking componentwise maxima covers both nonempty receiving polygons.
Every excluded receiver was incompatible with the source area by (9).

For a fixed source point $p\in K$, actual source Rodrigues gives

$$
(1+x^2)\mu\cdot C_\alpha R_1^tp
=\gamma(1-x^2)+2\sigma\mu\cdot(m\times p)x
-[l(c)h+b(c)(p\cdot w)]\bigl(\widetilde\mu_\sigma(x)\cdot w\bigr),
$$

where $\gamma=\mu\cdot p$, $h=M\cdot p$,
$\widetilde\mu_\sigma(x)=(1-x^2)\mu-2\sigma x(M\times\mu)/L_0$.
Use the exact polygon norm bands in Section3 for the factor midpoints
and errors. The [signed-height proof](cell8_third_source_proof.md)
supplies the explicit positive error bound and the three quadratic
Bernstein coefficient vectors on each closed interval. The maximum
of the midpoint product over a convex polygon lies on its boundary:
move perpendicular to the first factor's linear direction until an
endpoint is reached. On each edge check its endpoints and any admitted
concave stationary point. Negative uniform maxima are retained.

Let $U$ be this signed loss upper bound including its exact errors, and
$\tau\le\sigma\mu\cdot(m\times p)$ its outward lower bound.
Necessary containment gives

$$
(\gamma-H-B_\mu-U)+2\tau x+(-\gamma-H-B_\mu)x^2\le0. \tag{11}
$$

Its quadratic coefficient is nonpositive. Strict positivity at both
endpoints therefore rejects the entire closed interval. Every ordinary
and correlated support leaf passes those exact tests. The74 possible
source witnesses are62 originals and12 checked convex zero-height
points from the pinned original reference construction; all belong
to the original $K$. No alternative source body is used.

## 5. Bound the actual rolled quaternion on each local leaf

For an actual source and receiver in the tangent charts, let
$r_w=\|M+w\|$, $r_v=\|M+v\|$. Their minimal proper transports have
actual Cayley vectors

$$
a_1=(m\times w)/(r_w+L_0),\qquad
a_2=(m\times v)/(r_v+L_0).                            \tag{12}
$$

Indeed $a_1\cdot m=0$, $\|a_1\|^2=(r_w-L_0)/(r_w+L_0)$, and
the proper Cayley formula sends $m$ to $(L_0m+w)/r_w=k$.
The same calculation applies to $a_2$. All denominators are positive.

Exact polygon norm minima/maxima and (6) enclose the positive source
and receiver factors by $s\in[s_L,s_H]$, $t\in[t_L,t_H]$.
Source maxima also use the proved cap (5) for actual sources; outer
polygon corners need not lie in the cap. Let $D$ bound $\|w-v\|$,
$W_0$ bound $\|w\|$, and $V_0$ bound $\|v\|$. The squared distance is
separately convex, so all corner pairs bound its maximum. Dot and
scalar triple products are separately affine, so their extrema and
absolute extrema likewise occur at corner pairs. Thus

$$
\|a_2-a_1\|\le\Delta=s_HD+E V_0,\qquad
E=\max(|t_H-s_L|,|s_H-t_L|).                          \tag{13}
$$

Let $A_S=s_HW_0$, $A_R=t_HV_0$. The same exact corner bounds supply
$D_0\le a_1\cdot a_2$, $D_a\ge|a_1\cdot a_2|$, and
$H_0\ge|m\cdot(a_1\times a_2)|$.
For a nonnegative dot minimum use $s_Lt_L$; for a negative minimum
use $s_Ht_H$. The triple product bound is obtained by enclosing
$\max[M\cdot(w\times v)]^2/M_2$ and multiplying by $s_Ht_H$.
Every root enclosure is rational and checked by its squared signs.

Choose any proper orthonormal frame with third vector $m$, and write
$a_1=(a,b,0)$, $a_2=(c,d,0)$ and the **signed** roll parameter
$\xi=\sigma x$. For the actual product (4), quaternion multiplication
gives the unnormalized scalar and vector

$$
S_q=1+ac+bd+\xi(ad-bc),
$$
$$
V_q=(c-a+\xi(d+b),\ d-b-\xi(c+a),\ ad-bc+\xi(1-ac-bd)). \tag{14}
$$

The [generic exact algebra checker](cell8_third_quaternion.py) verifies
all four five-variable polynomial identities and

$$
S_q^2+\|V_q\|^2=(1+a^2+b^2)(1+c^2+d^2)(1+\xi^2).
$$

Writing $h=m\cdot(a_1\times a_2)$ and $d_p=a_1\cdot a_2$, its second
generic identity retains the orthogonality of roll and tilt:

$$
\|V_q\|^2=\|a_2-a_1\|^2+h^2
+\xi^2(1+\|a_1\|^2+\|a_2\|^2+d_p^2)
-2\xi h(1+d_p).                                      \tag{15}
$$

Since $|h|\le\|a_1\|\|a_2-a_1\|$, for $|\xi|\le X$ we obtain

$$
S_q\ge D_q=1+D_0-XH_0,
$$
$$
\|V_q\|^2\le N_q=
\Delta^2(1+A_S^2)+X^2(1+A_S^2+A_R^2+D_a^2)
+2XH_0(1+D_a).                                       \tag{16}
$$

All replacements preserve the displayed signs. If $D_q>0$, the Cayley
vector of the **actual** proper $Q'$ is $V_q/S_q$; an outward root of
$N_q$ divided by $D_q$ bounds its norm. This is checked additionally
against three independently multiplied rational proper Cayley matrices
in84cases,756entries, including both roll signs, zero tilts and
$\xi=\pm1$. These finite regressions supplement the generic identities.

The verifier also has a second valid bound. The unrolled composition
has Cayley norm at most

$$
\rho=\Delta\operatorname{upper\_sqrt}(1+A_S^2)/(1+D_0).
$$

The rotation-angle triangle inequality and positive half-angle addition
denominator give $(\rho+X)/(1-\rho X)$ when $1-\rho X>0$.
Take the smaller of the two proved bounds. On every local leaf, after
the necessary receiver cuts (9), each retained receiving polygon is
either empty or passes the strict exact gate

$$
\|\operatorname{Cayley}(Q')\|<1/8.                   \tag{17}
$$

The58 local leaves all lie in the first closed roll bin, including
zero roll. No separate source-plus-receiver chord estimate, sampling,
unverified scalar positivity or other body's constants establish (17).

## 6. Fresh original supports exclude every nonzero local motion

For **both** original one-third receiving triangles, reconstruct the
20-corner shadow hull from all62 original vertices. Its cyclic half
cross sum equals the original physical $C_8$. For each original edge
and its endpoint, the affine receiving support is
$\mu(u)=(v_b-v_a)\times u$. Every endpoint is on its support and
all62 originals are on the correct side at all three receiving corners.
There are7440 original comparisons per triangle,14880 in total, with
20 distinct original contact polynomial triples for each triangle.

The actual proper Cayley matrix numerator has its nine Gram identities
and determinant identity checked. Each original contact also has its
exact displacement identity. A necessary centered unscaled containment
for a Cayley vector $y$ requires, for every such contact,

$$
\Phi(y,u)=(v\times\mu(u))\cdot y
+(v\cdot y)(\mu(u)\cdot y)-h(u)\|y\|^2\le0,
\quad h(u)=\mu(u)\cdot v>0.                          \tag{18}
$$

The fixed six signed cube-face covers are freshly replayed on these
actual one-third triangles. They have48+36=84 closed leaves and
3276 strictly positive linear/radius-adjusted quadratic Bernstein
coefficients. All original matrix, face, contact and direct leaf
polynomial identities are checked. Radius1/8 and depth4 are the actual
[Cell8 local interface](cell8_collar_proof.md); the older radius27/250
and depth3 are unchanged and are not widened by assertion.

For completeness, write $y=rz/\|z\|$, where $z$ lies on a signed
unit cube face and $0<r\le1/8$. On its closed patch let
$\|z\|\ge\ell\ge1$. Write (18)'s terms as $L(z,u)+B(z,u)$, linear
and quadratic in $z$. The certificate proves $L>0$ and
$\ell L+(1/8)B>0$ throughout the patch: linear and tensor quadratic
Bernstein bases have nonnegative weights summing to one. The
coefficients are affine in the receiving raw ray, so tests at all
three triangle corners cover every receiver. Multiplying (18) by
$\|z\|^2/r$ gives $\|z\|L+rB$. If $B\ge0$ this is positive; if
$B<0$, it is at least $\ell L+(1/8)B>0$. Thus every nonzero motion in
the entire closed radius1/8 ball violates an original receiving support.

Combined with (17), each local source/roll leaf permits only $Q'=I$.
The other leaves were empty or contradicted (3) by a strict support.
The complete finite forests and the Cell11 dependency therefore leave
only $Q'=I$ for every original placement.

## 7. Recover the original equality orientations, scale and translation

Undo (4)'s actual right body factor and moving left half-turn:
$Q'=I$ implies $Q\in G\cup J_nG$. Conversely both left cosets give
exactly $P_nK$, since $gK=K$ and $P_nJ_n=-P_n$ for the centered body.
For such equal shadows, positive area in the original containment
forces $\lambda=1$. A bounded planar shadow containing its own translate
forces $t=0$: the support function in the direction of any nonzero
$t$ would otherwise increase. This proves both directions of (1).

The inherited exact separation of $J_m$ from the actual $G$ is

$$
\min_{g\in G}\|J_m-g\|_F^2=(106-36s)/29.
$$

The fresh strict receiver chord bounds are82447/$10^6$ on $L$ and
21027/200000 on $B$. Their common maximum $d$ satisfies the freshly
checked separation margin

$$
(106-36s)/29-8d^2>0.                                \tag{19}
$$

Since $\|J_n-J_m\|_F^2\le8\|n-m\|^2$, $J_n\notin G$ throughout
the collar. The two left cosets are disjoint, each with60 proper
rotations. Actual body conjugation and $P_{-n}=P_n$ give every stated
proper-body and antipodal receiver image. The original physical
translation and scale are transported with the same placement.

## 8. Reproduction and trust boundary

Read [the fixed exact verifier](cell8_third_certificate.py),
[the compact fixture](expected_cell8_third.json), and
[the generic quaternion checker](cell8_third_quaternion.py).
Python3.11+ standard library suffices. From the repository root, use
one numerical thread and the unchanged55-second deadline on **each**
component. All17 fixed components and the two additional commands are
required; one component alone is not the whole proof.

~~~sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_third_certificate.py geometry
for sign in -1 1; do
  for bin in 0 1 2 3 4 5 6 7; do
    timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_third_certificate.py "roll:$sign:$bin" || exit 1
  done
done
timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_third_quaternion.py
timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_third_source_certificate.py
~~~

Every component must match **every** expected field. The source/roll
digests cover all original controls, exact reconstructed polygon corners,
norm factors, signed support losses and endpoint margins, all necessary
area cuts and receiver polygons, and both actual quaternion gates.
The complete grammar is checked before mathematical imports. Executed
field and radical signs receive independent rational enclosure audits;
zero radical signs use exact identities. The proof also relies on the
34 byte-pinned inherited source/fixture dependencies. Their original
model, symmetry, projection and generic source/transport interfaces
retain their published trust boundaries. Complete old receiving-domain
production jobs are not recursively rerun or called independent checks.

All839 new source/roll records, all12 source-cell summaries and both
fresh local receiving summaries were compared entry by entry to their
retained author discovery certificates. Fixed replay chooses no new
witnesses and contains no exploratory search. The separate generic
quaternion audit checks complete polynomial coefficient dictionaries,
not only numerical examples. This is author checking, not independent
peer review, formalization or an independent implementation of the
inherited kernels. Python/Fraction, positive ordered-field semantics,
original-solid identification, finite cover completeness and the
unformalized convexity, active-stratum, proper-gauge, quaternion and
Cayley bridges are explicit trust boundaries.

No floating-point passage search, failed sufficient bound, solver
UNKNOWN, timeout, memory kill or partial enumeration is a premise of
(1). Bounded discovery runs retained exact successful leaves; a prefix
resume completed only uncomputed subtrees at unchanged depth and
resource limits. All required closed forests are complete and replayed.
The verbose discovery corpora stay private and are unnecessary for
reproduction from the compact fixed controls.

The compact fixture is 58,084 bytes, SHA256 `1ddda6ad35a5102b380677a7c708797249ec41c8cb56137e17482f57f3bd6166`. The complete fixed source/roll table SHA256 is `700d4d0d671e59209023df4070092e859c7fbd206e08697f91fc4007c099be28`. The generic quaternion coefficient SHA256 is `379801789cc348bc6a517f0a0c5d360fc831d17dfc485f36966017eb09cc45b2`. New strict source/roll leaves have 1,320 positive endpoint comparisons and retain 180 negative uniform signed losses. The mandatory Cell11 dependency adds 64 endpoint comparisons and 22 retained negative losses. Actual external tests rejected 31 malformed compact fixtures, and Python -O was refused before mathematical imports.

## 9. Literature, complementary work and next frontier

Primary status was refreshed2026-10-01 in
[Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531),
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475), and the
[standard strict-projection framework](https://arxiv.org/abs/2112.13754).
The bounded primary refresh retains the deltoidal and pentagonal
hexecontahedra as unresolved Catalan cases. The rhombicosidodecahedron's
non-Rupert status is conjectural in the supplied current source; the
proved non-Rupert body is a different construction. No exhaustive
literature absence, historical novelty or priority is claimed.

Complementary complete written source read includes
[six-rupert-2's two-sector J77 classification](../../convex_geometry/rupert_j77_two_sector_closed_cap/PROOF.md),
source18b8302c43ed84a98708d5f7ae226b3c7aaf0b8a, graph8399; and
[six-rupert-3's RID closed-band classification](../../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CLOSED_BAND_PROOF.md),
source3ace7a220c1d61878373bd9a2f6a73abe81c2175, graph8390, with its
continuous exceptional HIGH plane of unequal touching shadows.
The latter illustrates why closed containment must be classified
separately from strict passage. These are method citations; their
body-specific constants, centrality assumptions, exceptional motions
and review status are not transferred to the present body. The prior
[global RID cutoff](../../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph8330, and [J77 sector23 proof](../../convex_geometry/rupert_j77_sector23_closed_cap/PROOF.md),
graph8342, remain useful context.

The current [three-sector J77 proof](../../convex_geometry/rupert_j77_three_sector_closed_cap/PROOF.md),
source9c44a91c07371a24b7225a6f1e6a7003b323ddf7, graph8418, and
[RID threshold-to-threshold exclusion at2/5](../../rhombicosidodecahedron_threshold_band40/PROOF.md),
source8ce60369f323644d5bc748c2fb2941058439b37b, graph8436, were also
read in full with their durable checkpoints. The former closes a fresh
paired signed-coordinate/stress argument on sector31; the latter
intersects the actual receiving cap with necessary original-height
halfplanes before checking original supports. They provide additional
method context for retaining necessary geometric constraints before
enclosing transports. RID's winning and mixed2/5 branches, and both
global questions, stay open. No different-body constants or review
verdicts are imported.

The concrete next frontier is the adjacent receiving collar beyond
parameter1/3, retaining source-area correlation before computing exact
transport bounds. Every new receiver needs fresh original supports,
area-critical tests and actual Cayley gates. Whole Cell8, the receiving
complement and global deltoidal Rupert property remain **OPEN**. An
exact strict passage construction remains an alternative in that
unresolved family.
