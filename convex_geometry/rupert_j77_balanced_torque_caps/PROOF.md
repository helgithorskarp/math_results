# Translation-balanced normalized torque and directional source errors for J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30.
Complete written intermediate proof with exact finite hypotheses, author
checked and unformalized. Independent review and historical priority are
not asserted. The global Rupert property of J77 remains **open**.

## 1. Statement and dependency boundary

Let K be the original-order 55-vertex paragyrate diminished
rhombicosidodecahedron J77 in the
[published coordinate model](../rupert_j77_projection_diameter/PROOF.md).
Write s=sqrt(5), z=(7+s)/2, D=(0,-1,z), N=(29+7s)/2 and n0=D/sqrt(N).
All original vertices have squared norm r²=(11+4s)/4. Fifty form a
three-dimensional antipodal core, so 0 is interior to K. Set
P_n=I-nn^T, M_n=I-2nn^T, X=diag(-1,1,1), and let R be the actual
72-degree proper body rotation about (0,(1+s)/2,1).

**Theorem.** For every unit receiver n in the entire closed union

    C = { n : ||n-e R^k n0|| <= 1/40 for some e=+1,-1, k=0,...,4 },

every original Q in SO(3), planar translation t and scale lambda>=1
satisfy

    lambda P_n(QK)+t subseteq P_nK

if and only if lambda=1, t=0 and

    Q=R^k or Q=M_n X R^k, k=0,...,4.

Each displayed form gives equal shadows. All source orientations,
original relative angles, rolls and translations are quantified; no
small original-angle assumption is imposed. Consequently no strict
Rupert passage can have its receiving normal in C. We use the standard
strict proper-rotation projection formulation, as in
[Steininger--Yurkevich](https://arxiv.org/abs/2112.13754).

The ten directed caps are disjoint. Their unit-sphere area is pi/160,
or 1/640 of the sphere. This is **25 times** the spherical area of the
previous full 1/200 caps in the
[directional receiver theorem](../rupert_j77_directional_receiver_domains/PROOF.md).
This comparison concerns those explicit caps. The entire previous
[1/110 chart-area triangle](../rupert_j77_zero_height_supports/PROOF.md)
remains valid separately and is not wholly contained in C. We do not
assert dominance over every receiver in the previous analytic criterion.
Section 7 constructs a ray in C outside both explicit previous regions.

The direct parent is that zero-height proof, source
**afef1a458b006eb92866fb3d24c6bf99eee1590b**, graph
**bafkreiffa5re7uc5cksb4mtnxpnkudcaeigwl2qi75wwmk2w5xkgfhjbyy**,
actually committed at 7558. [dependencies.json](dependencies.json)
pins all seven parent files; its transitive boundary has 43 files,
so this checker verifies **50** pinned files. The mathematical
dependencies, with exact commits in that chain, are:

- The [sharp regional theorem](../rupert_j77_sharp_region_gap/PROOF.md),
  source 2def43a003a2a692571ae654c543517b1cb20e6b, graph 7438:
  all 301 projective/602 directed core sign regions, sharp nonwinning
  maximum f²=1/12, global maximum c0²=(65+10s)/596, and winning
  tangent-disk coercivity with rho²=(233-10s)/596.
- The [directional theorem](../rupert_j77_directional_receiver_domains/PROOF.md)
  and [translated local theorem](../rupert_j77_translated_local_exclusion/PROOF.md):
  actual minimal normal transports and the positive support/translation
  argument. Section 2 below replaces the six-coordinate torque bound.
- The [adaptive proper-frame and roll proof](../rupert_j77_adaptive_roll_domains/PROOF.md),
  source 94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b, graph 7514,
  and direct parent 7558: actual determinant-sensitive proper source/body
  gauges, zero-height convex difference witnesses, complete two signed
  roll covers, stable inverse quadratics and asymmetric half-turn stress.
- **six-rupert-3, researcher**'s
  [general perpendicular-axis composition lemma](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
  source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph 7414.
  Only the general axis result transfers; the actual J77 frames are
  provided by the adaptive parent. No RID centering or constant transfers.

The complete regional enumeration and complete parent outputs are not
replayed by this short checker. Their written theorems are explicit
dependencies. The new hull, active-contact constructions, entire-cap
hypotheses and all numerical gates are regenerated below.

## 2. Normalized torque with arbitrary translation

Regenerate the parent's 34 actual support pairs (v_l,p_l), with
p_l perpendicular to n0, from the entire original body. Thus
p_l.v_l=max_i p_l.V_i. Choose a positive rational outward enclosure

    b_l >= r ||p_l||.

Every radical is bounded on the fixed rational grid of denominator 10^12
by exact squared inequalities. Define a **balanced normalized stress** by

    w_l>=0, sum_l w_l=1, sum_l w_l p_l/b_l=0,

and its normalized torque

    T(w)=sum_l w_l (v_l cross p_l)/b_l.                    (1)

These are physical three-dimensional identities. The zero normal sum,
which is indispensable for arbitrary translation, is not inferred from
the centered case. For each of the 20 probe triples in the 454-byte
[fixture](certificates.json), the checker solves the three constraints
for coordinates x,y and total weight exactly in Q(sqrt(5)). It separately
checks all three normal coordinates, positivity and total weight, and
reconstructs (1). No approximate LP solution or external solver is a
proof input.

Let H be the convex hull of these 20 distinct stress torques. The
checker establishes rank three, enumerates all 1140 triples, and tests
all 22800 point-side inequalities. It finds all 36 actual facets; no
triple is degenerate. Each outward facet has **positive signed height**,
so 0 is inside H. Normalize its equation to A.x<=1. Every facet obeys

    1-||A||²/49 > 0.                                    (2)

Therefore the centered closed Euclidean ball of radius 1/7 lies
strictly inside H. We do not claim that these 20 points enumerate every
balanced stress or yield an optimal radius. Actual outward facets and
their signed heights are essential: a distance from the origin to a
plane alone would not prove a centered-ball inclusion.

Now let ||n-n0||<=delta, and put p'_l=P_n p_l. Section 4 establishes
that v_l remains an actual receiving support at every p'_l. Projection
preserves the zero normal sum. Also

    ||p'_l-p_l||<=||p_l||delta,
    ||T_n(w)-T(w)||<=delta,
    T_n(w)=sum_l w_l(v_l cross p'_l)/b_l.                 (3)

Thus in every unit-axis direction u one of the 20 stresses has
u.T_n(w)>=1/7-delta. This follows from the support function of H and
the matched point drift in (3); no moving-facet combinatorics is assumed.

Suppose a gauged proper source rotation Q' has principal angle theta>0
and unit axis u, and the stated closed containment holds. At each p'_l
test the source point Q'v_l. Dividing by lambda and using the positive
receiving support, lambda>=1 gives

    p'_l.(Q'v_l-v_l) + p'_l.t/lambda <= 0.

After summing with w_l/b_l the translation cancels. The exact
exponential formula and its integral remainder give

    Q'v_l=v_l+theta(u cross v_l)+e_l,
    ||e_l||<=r theta²/2.

Because ||p'_l||<=||p_l|| and sum w_l=1, the necessary summed
inequality is

    0 >= theta u.T_n(w)-theta²/2
      >= theta(1/7-delta-theta/2).                        (4)

Consequently

    delta+theta/2 < 1/7                                 (5)

excludes every nonzero gauged proper angle with arbitrary translation.
In particular delta<=1/40 and theta<=23/100 give the strict margin
1/7-1/40-23/200=1/350. This conditional local assertion is distinct
from the all-source theorem: Section 5 derives a sufficiently small
gauged angle from arbitrary original sources.

## 3. Active contacts couple the source error to the height deficit

The positive active core vertices at n0 are exactly V8,V12,V30,V32.
They have raw height h=(5+s)/4 and h²/N=c0². Write

    V_i=c0 n0+t_i,   B=conv(-t_8,-t_12,-t_30,-t_32).

B is a quadrilateral in n0-perpendicular with 0 inside. Enumerating
all six possible vertex pairs finds all four actual supporting edges,
with positive signed heights. For each of the parent's four actual
zero-height convex differences

    u±=(±(5/4+7s/20), 3/2+s, (1+s)/4),
    w±=(±(2+s), 1, (7-s)/22),

the edge gauges and eight explicit positive convex constructions give

    ±u±/L_u in B,   L_u=(99+65s)/38,
    ±w±/L_w in B,   L_w=(-115+75s)/22.                  (6)

Here each outer sign is checked separately. The checker reconstructs
every barycentric sum and all three physical coordinates. Membership
of u±,w± in the actual K-K, their original vertex indices and their
zero heights are regenerated from the pinned direct parent; they are
not arbitrary vectors of a supporting strip.

Let k be an actually gauged winning source normal, with f(k)>=F and
||k-n0||<=a<=1/10. The checker verifies c0_lower-r_upper/10>0;
therefore all four active contacts retain their positive signs and
V_i.k>=F. Consequently

    -t_i.k <= c0(n0.k)-F <= c0-F.

By (6), for any one of the four constructed differences v,

    |v.k| <= L_v(c0-F).                                 (7)

Let A1 be the minimal proper normal transport n0 to k, with chord a*
and tangent direction e1. At a*=0 the following identities hold by
continuity. Because v.n0=0, the exact Rodrigues formula gives

    P0(A1^T v-v)=-(a*²/2)(v.e1)e1,
    ||P0(A1^T v-v)||
       = a*/[2 sqrt(1-a*²/4)] |v.k|.                    (8)

Since a*<=a<=1/10 and (101/100)²(399/400)>1, (7)--(8) yield
the **directional** source-error bound

    ||P0(A1^T v-v)|| <= (101/200) a L_v(c0-F).           (9)

The generic zero-height bound r a² is also valid because ||v||<=2r.
Use the smaller of these two bounds. With outward enclosures, put
d=c0_upper-F and

    S_v=min{r_upper a², (101/200) a L_v d}.               (10)

This coupling uses the actual active-source geometry, not independence
of source chord and height deficit. It is decisive for the late witness
w±. On the new cap the former uncoupled late endpoint test is negative;
this is only failure of that sufficient estimate, never nonexistence.
For unchanged original difference witnesses use their parent's bound
|D.v|a/N_lower+r_upper a². A planar roll preserves each projected norm.

## 4. All receiving hypotheses on the entire closed cap

It suffices initially to consider ||n-n0||<=delta=1/40. All inequalities
here hold for **every** n in this cap and include its boundary; reference
tests or sampled rotations are not used as continuous coverage.

For an actual reference probe p=p_l and d_ij=v_l-V_j,

    (P_n p).d_ij
       >= p.d_ij-||p||delta(|D.d_ij|/sqrt(N)+||d_ij||delta).

The exact checker certifies this lower bound as positive for all
34*54=**1836** original receiving support comparisons, with outward
norms and radical denominators. Thus the hypotheses of (3)--(4)
persist uniformly on the whole cap.

For every nonantipodal original vertex pair d=V_i-V_j,

    ||P_n d||² <= ||d||²-
          max(0, |D.d|/sqrt(N)-||d||delta)².              (11)

All **1460** such original-pair upper bounds are strictly below
d0=4(r²-c0²). The global core theorem gives f(n)<=c0, so an antipodal
core pair attains squared diameter 4(r²-f(n)²)>=d0. Thus the **full
asymmetric body** has the exact receiving diameter

    diam(P_n K)²=4(r²-f(n)²).                            (12)

Centrality of K is not assumed. Its antipodal core supplies the lower
bound, and all original nonantipodal pairs are checked for the upper
bound. Absolute-height Lipschitz continuity yields uniformly

    f(n)>=F=c0_lower-r_upper/40>0.                       (13)

The squared comparison F²>1/12 is checked. Closed containment at
lambda>=1 and the source core diameter lower bound imply
f(source)>=f(receiver)>=F. The published regional classification
therefore puts **every source** in a winning source region. Its actual
body gauge and tangent-disk coercivity give the outward chord bound

    a=(101/100)(c0_upper-F)/rho_lower < 1/10.             (14)

Both source and receiver are now in the ranges needed above.

For receiving widths, retain the parent's complete signed one-sided
envelopes at probes 11,12,13. All 3025 ordered original pairs for each
probe and each sign are regenerated: **18150** comparisons, including
ties, and **6912** strict excess-height tests for delta<=1/20.
Unlike the old triangle, the entire cap can cross the sign walls; take
the larger of the two valid signed coefficients at each probe.
If eta>=||m|| and kappa is this coefficient, the common-plane bound is

    W_receiver(m)<=H+eta(kappa delta+r_upper delta²).    (15)

This is a maximum over two proved branches, not an assumption that
the small positive-branch coefficient persists everywhere. At the four
zero-height source witnesses the complete selected error becomes

    E_v=eta[kappa delta+r_upper delta²+S_v].             (16)

The remaining witnesses retain their original linear source height and
generic quadratic remainder. Original single-support bounds in the
asymmetric half-turn stress remain absolute envelopes; width bounds
are not substituted for those supports.

## 5. Complete full-roll reduction and the derived full angle

Retain the parent's actual proper gauges. A proper source body symmetry
S gives Q'=Q_original S; an improper one gives Q'=M_n Q_original S.
Both are proper and retain the original source shadow since P_n M_n=P_n.
The two-row frame's cross normal includes the determinant sign. The
actual common-plane decomposition is

    Q'=A2 C_alpha A1^T,

with both minimal transport axes perpendicular to n0 and roll axis n0.
No improper symmetry is treated as an allowed source rotation.

At a reference receiving probe m, with width H, and selected actual
difference v, write d_v=m.v, K_v<=sign(alpha)m.(D cross v)/sqrt(N) and
x=tan(|alpha|/2). The necessary width inequality is

    p_v(x)<=(1+x²) E_v,
    p_v(x)=(d_v-H)+2K_v x+(-d_v-H)x².                  (17)

Use (16) for the zero-height constructions and the retained errors for
the other original witnesses. Signed radical denominators are chosen
outward. For **each** sign, the five consecutive closed intervals are

    [57/400,53/200], [53/200,31/80], [31/80,51/100],
    [51/100,13/20], [13/20,1].

Their probes, original indices and endpoint adjacency are regenerated
from the direct parent. The last uses w± at probe 12. At each interval
the polynomial p_v-(1+x²)E_v is concave because H>=|d_v|. Both
endpoint values are strictly positive; therefore no point of that
closed interval survives. All thirty quadratic Bernstein coefficients
are also generated, with their power-basis reconstruction checked.
Ten signed intervals cover the entire remote reduced roll range.

For the residual range [0,b], b=57/400, use u+ at probe 11 and u-
at probe 13. Here p_v=Kx-Tx², K>0,T=2H>0. With the corresponding
nonnegative error E, let q(x)=(T+E)x²-Kx+E. The exact checks q(b)<0
and positive discriminant isolate the small branch. Every surviving
roll has

    x <= 2E/[K+sqrt(K²-4(T+E)E)],
    |alpha| <= epsilon=2 max(outward small roots).         (18)

Both root signs and the strict bracket below b are checked with the
stable displayed formula. Monotonicity of q in its nonnegative error
means that a uniform upper error bounds every actual point. Difference
body symmetry permits this roll reduction modulo pi, but does not
identify the full asymmetric shadow with its half-turn.

For the residual near-pi branch, retain the original positive stress
at probes 2,5,12 with weights

    (351-97s)/482, (351-97s)/482, (-110+97s)/241.

Their three-dimensional normal balance is zero. The unique original
minimum preimages V29,V31,V24 give weighted selected support
G cos(alpha), G=(90+74s)/241, with zero weighted sine term and receiving
support 1. All 165 original minimum comparisons are regenerated. The
original absolute receiving support envelopes and their 9075 pair
comparisons/5166 excess tests/165 single-support comparisons/120 excess
tests remain intact. Let E_pi be their positive weighted source and
receiving transport sum, with source/receiver quadratic costs
r_upper(a²+delta²)/2. The necessary translated full-shadow inequality
is contradicted by

    G-1-E_pi-(G/2)epsilon² > 0.                          (19)

This cancels arbitrary translation and rejects the exact half-turn as
well as its entire residual neighborhood. Only the near-zero full
roll remains. With a,delta,epsilon<=1/10, the published proper-axis
composition theorem yields

    theta <= Theta=min{epsilon+(101/100)(a+delta),
                 (101/100)sqrt((a+delta)²+epsilon²)}.      (20)

All roots are outward certified. In this check the derived bounds are
F>0.327, a<0.095, epsilon<0.046 and Theta<0.130; these decimal
inequalities are descriptive consequences of the exact rational/field
output, not proof inputs. The smallest remote interval margin exceeds
0.0078, (19) exceeds 0.0339, and

    1/7-delta-Theta/2 > 0.0530.                          (21)

The exact positive field expressions, rather than rounded versions,
are tested and recorded in [expected.json](expected.json). Equations
(4)--(5) and (21) now force Q'=I, with no original source-angle
restriction. This closes the all-source theorem on the whole cap.

## 6. Closed equalities and the complete body orbit

Undoing the proper/improper body gauges gives precisely
Q=R^k or Q=M_n X R^k. Conversely the body's C5v symmetries and
P_n M_n=P_n give equal shadows for every displayed form. The positive
equal-shadow diameter forces lambda=1. A bounded convex shadow cannot
contain a nonzero translate of itself, so t=0. This proves the claimed
closed classification including all boundaries.

Apply the actual body rotations R^j to the receiver and conjugate the
source rotations; they preserve the same displayed C5v forms. Reflection
images of the axial center are already in its fivefold orbit. Normal
reversal leaves P_n and M_n unchanged. These facts give the full ten
directed caps and their five projective axes, without constructing a
new source symmetry group.

The checker regenerates all five actual raw axes and their return
under R. For every distinct pair it certifies

    2-2|D_i.D_j|/N > 4(1/40)².

The opposite centers have distance 2, so all ten closed caps are
disjoint. On the unit sphere a chord-radius delta cap has cosine
threshold 1-delta²/2 and area 2pi(1-cosine)=pi delta². Hence the
area, fraction and ratio stated in Section 1 are exact spherical
quantities. They are not a measure of the union with the old triangle.

## 7. An exact new receiver outside the prior explicit union

Consider the normal ray through U=(0,-9/10,z). The checker proves
D.U>0 and

    (D.U)² > (1-(1/40)²/2)² N ||U||².

Thus its positive unit normal lies strictly inside the new cap. For
each of the five previous axial centers it proves

    (D_j.U)² < (1-(1/200)²/2)² N ||U||²,

excluding both directed old 1/200 caps on that axis. For every one of
the ten actual C5v images of the parent's entire triangle
conv(D,(0,-13/11,z),(1/10,-25/24,z)), it exactly solves for U as a
linear combination of the three image corners. In each solution at
least one coefficient is positive and one negative. Since the three
columns are independent, neither U nor -U is in the image cone.
Thus this ray is outside every old projective triangle image, even
including all normal reversals. This is a strict addition to that
explicit union, without asserting dominance over the old sufficient
criterion's other receivers.

## 8. Reproduction, literature and complementary work

From the repository root, with Python 3.11+ and only its standard library:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_balanced_torque_caps/verify.py --self-test > /tmp/j77-balanced-normal.json
python3 -B -O convex_geometry/rupert_j77_balanced_torque_caps/verify.py --self-test > /tmp/j77-balanced-optimized.json
cmp convex_geometry/rupert_j77_balanced_torque_caps/expected.json /tmp/j77-balanced-normal.json
cmp /tmp/j77-balanced-normal.json /tmp/j77-balanced-optimized.json
```

Run the two checks sequentially. They took 19.471 and 20.141 seconds
with peak child RSS 43200 and 44572 KiB respectively, inside separate
55-second deadlines with all numerical threads one. Every one of the
7228 expected bytes matched in both modes. Expected SHA256:
`de05a20afc1c881efc99f2d076f917429b86f45be23a1857f143c6d4d3489e11`.
Canonical fixture SHA256:
`c7777e6cbb45f9617fbece18cab4fc213d5105ff4ae83f85b7f33ac536ea5897`.

The checker uses explicit failures, so Python optimization does not
disable decisions. Ten malformed controls reject repeated/invalid probe
indices, negative and unbalanced stress weights, a duplicate hull point,
a false source gauge, an oversized receiving cap, an invalid source
range, a missing closed roll interval and a false radical enclosure.
The 73860 new sign records reduce to 10677 distinct independent rational
sign audits including nine field-kernel controls. Exact coefficient,
convex-identity and actual-facet checks supply the finite hypotheses;
the continuous cap inequalities, Rodrigues identity, integral remainder,
proper gauges and source/roll reductions are proved in this text or in
the explicitly pinned parents. Output agreement is author regression,
not independent review or proof-assistant checking.

The exploratory LP calculations are not imported. Their purpose was to
find the compact probe triples. Exact stresses and all selected-hull facets
are reconstructed by this checker. Six separate fixed-contact coordinate
LP optima and a private 30-direction hull search do not imply global
optimality. No private ledger, full search corpus, floating-point passage
scan or timeout is a mathematical input.

The live primary refresh on 2026-09-30 retains the located unresolved
Johnson list **J72,J73,J74,J75,J77** in
[Gosain--Grimmer Table 4](https://arxiv.org/html/2509.08190).
The required [2604.26531 seed](https://arxiv.org/html/2604.26531) retains
87 of 92 Johnson solids known Rupert and RID non-Rupertness as conjectural.
[2508.18475](https://arxiv.org/abs/2508.18475) constructs a different
non-Rupert body. No priority or absence theorem is inferred from bounded
searches. The assigned target is retained as a presently unresolved named
solid, not replaced with a known theorem.

Method credit: **six-rupert-1, researcher**'s
[normalized deltoidal cap proof](../../geometry/rupert_deltoidal_symmetry/normalized_cap_proof.md),
source 0b8097a272e4b134b88869e6bf1a395b898da6c3, graph
bafkreidbimtnphxte3m2xe2d7hev7c3lopnsvrxdzmbibfma232eyz2i74 at 7520,
suggested per-contact rotation remainders and a centered-hull rule.
Equations (1)--(5) add the necessary positive physical normal balance
for an asymmetric body and arbitrary translations. That author's new
[affine receiver-region proof](../../geometry/rupert_deltoidal_symmetry/normalized_receiver_piece_proof.md),
source 3263880e7e1613e04b648f7eabcd30184a9639ba, graph 7590, verifies
every possible moving facet and closed boundary stratum on two new
deltoidal regions. Its centered contacts/constants are not J77 hypotheses.

**six-rupert-3, researcher**'s
[balanced RID construction](../../rhombicosidodecahedron_mirror_cluster_obstruction/BALANCED_SUPPORT_PROOF.md),
graph 7468, uses equal signed heights and threefold covariance. Those
hypotheses do not hold merely from J77 mirror symmetry. The new
[RID contact-collar proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/CONTACT_COLLAR_PROOF.md),
source 0ac1d22eab1bc0cae62373d85a48d6a182a806aa, graph 7597, proves
existential positive receiving slack below its threshold. Its numerical
local caps concern sources near classified branches, and are not numerical
all-source cap radii. RID centrality and its nongauge 36-degree boundary
branch are not J77 premises.

The independent [RID threshold review](../../rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md)
by **six-reviewer-2, independent reviewer**, source
52d7829380a548c66fe716ca8155c2c22e6cd23f, actually at graph 7576,
confirms the full RID threshold classification and strengthens its roll
and tangent-disk certificates. That review and the later
[RID collar review](../../rhombicosidodecahedron_contact_collar_review2/REVIEW.md),
source c8e44ca98b50499e356396525444b92b0315345c, graph 7635, have RID
scope only. The latter independently confirms the existential slack and
enlarges source-near-branch caps, without certifying a numerical global
epsilon. None reviews this J77 result. The
[independent J77 review](../rupert_j77_all_source_review1/README.md),
by six-reviewer-1, source e78fafefba916f04dc61ec7e2f9556e1469776a1,
graph 7386, covers the 7360 predecessor and 1/1400 caps, not the later
7438/7514/7558 parents or the present theorem. No reviewer target or
verdict has been requested or influenced.

The J77 [uniform local phase](../rupert_j77_uniform_local_exclusion/PROOF.md)
at 7330 and the deltoidal
[uniform local phase](../../geometry/rupert_deltoidal_symmetry/README.md)
at 7322 remain closed qualitative results. An existential small-angle
gap is not a global numerical angle cover or a global non-Rupert proof.
The receiving complement of the new caps and previous regions remains
open, as does an exact strict passage or global exclusion for J77.

The next useful extension is a whole receiving piece using actual
original supports and translation-balanced stresses throughout the
piece, with both complete full-roll branches retained. The normalized
torque method alone supplies neither that support persistence nor
source coercivity beyond the winning gap. Any weaker source regime
requires a new exact source classification/reduction before global
claims can be made.
