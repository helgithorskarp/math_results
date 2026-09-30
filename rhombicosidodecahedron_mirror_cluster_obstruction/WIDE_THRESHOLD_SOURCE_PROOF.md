# Threshold sources cannot enter the wider winning receiving band

**six-rupert-3 — researcher — 2026-09-30.** Complete written,
unformalized intermediate proof with exact finite certificates.
Global rhombicosidodecahedron Rupertness remains **OPEN**. No independent
review of this new result, formalization or historical priority is asserted.

## 1. Statement and exact dependencies

Let phi=(1+sqrt(5))/2. Let V be the sixty original signed even coordinate
permutations of (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).
These are the standard edge-two rhombicosidodecahedron vertices. Put

    K=conv(V)=-K, R^2=7+8phi, P_n=I-nn^t,
    f(n)=min_{v in V}|v.n|, beta=(19-8phi)/29, epsilon=1/150.

All normals in this proof are unit normals unless an unnormalized
reference is expressly displayed. The complete
[signed-region spectrum](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, graph
bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi at7256,
has 436 projective strict signed regions: ten **winning** regions
with maximum f^2=1/3, sixty **threshold** regions with maximum
f^2=beta, and 366 other regions with maximum at most 1/7.
Winning and threshold here name these precise original signed regions.

**Theorem (source-conditional closed exclusion).** Let n lie in a
winning signed region and satisfy f(n)^2>=beta-1/150. For every original
proper Q in SO(3) whose source normal k=Q^t n lies in a threshold signed
region, every planar translation t and every lambda>=1,

    lambda P_n(QK)+t is not a subset of P_nK.                 (1)

Both threshold families, every proper-body and antipodal image, all
original spatial rotations and planar rolls are included. The equality
height cutoff and every angular rank tie are covered.

**Corollary (source reduction).** Any closed containment with a winning
receiver in this band must have a winning source. In particular this
holds for any strict passage using such a receiver.

The substantive predecessor is the original-point injection in
[GLOBAL_SLACK_PROOF.md](GLOBAL_SLACK_PROOF.md), source
d68a00c27754ac1517aba99197334e5e19fabb8b, graph
bafkreie7fdnz7e7b3wlhu4o4d7dd5rzbzkodpnoplztzxqympafq2llvbq at7703.
The complete active receiving hexagon comes from
[WINNING_RECEIVER_PROOF.md](WINNING_RECEIVER_PROOF.md), source
a666fd496161000af9dcb9dd408f3ed3d2a00fcc, graph
bafkreiazq6m7zxvw26wrv6buovxbvnm3ltyyfaa63x2ehbl6b7k4ppm45m at7498.
Both full threshold tangent quadrilaterals and their proper reference
families come from [BETA_CAP_PROOF.md](BETA_CAP_PROOF.md), source
7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph
bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe at7659.
Their precise finite geometry is regenerated here and compared entry by
entry with hash-pinned public fixtures. The complete regional exhaustion
is inherited; its full computation is not claimed rerun.

The preceding [global receiving cutoff](EXPANDED_GLOBAL_SLACK_PROOF.md),
source 6afb6b9e4585a35561752b3ef34eccabaa0d7e3e, graph
bafkreihbc5jiplrfxcfepw4sf7xexzr6eob4ugaw36bpmukbhf4vkzakjm at7755,
requires f(n)^2<beta-1/450 for every strict passage. This new theorem
uses a band three times wider, but excludes only threshold sources for
winning receivers. It does **not** prove a global receiving gap 1/150
or by itself exclude winning-to-winning pairings. The companion
[all-source winning-band proof](WIDER_WINNING_BAND_PROOF.md) supplies that
separate rotation argument and classifies every closed containment in
the same winning receiving band.

The newly committed [independent global review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_global_slack_review2/REVIEW.md),
by six-reviewer-2, independent mathematical reviewer, source
e9b77dc0a403bd7093e03bb271db39a7f33e6401, graph
bafkreiahuxldhobwg2dajs7eqmpvjbcijnjdmh7ehxgxxd6n4ms4sga7ta at7792,
confirms both global predecessors and proves the stronger global
cutoff f(n)^2<beta-1/445. It independently checks all 720 height-order
permutations and proves the same sharp d3 square used below. The factor
29/20 is therefore already available in that reviewed rank geometry;
the new result here is its use with wider actual receiving localization
and source transport to prove (1). That review does not assess this
new source-conditional 1/150 theorem.

## 2. Centering, diameter and original signed-region gauges

Write S=P_n(QK), T=P_nK. Both are centrally symmetric convex polygons.
If lambda S+t is contained in T, symmetry gives lambda S-t contained
in T. Convex midpoints give lambda S contained in T, and lambda>=1
with 0 in S gives S contained in T. Thus it suffices to exclude closed
centered unit containment with exactly the original n and Q.

Every original vertex has norm R. Symmetry yields the exact identity

    diam(P_nK)^2=4(R^2-f(n)^2).

Hence S contained in T forces f(k)>=f(n), k=Q^t n. If k is threshold,
its regional maximum implies f(k)<=sqrt(beta), so necessarily

    F:=sqrt(beta-epsilon) <= f(n) <= f(k) <= sqrt(beta).     (2)

Exact field comparisons give F>q=449/1000 and F^2>1/7. Therefore every
source compatible with a receiver in the band is winning or threshold;
an original axial sign wall has f=0 and cannot occur. This proves the
source exhaustion needed for the corollary after (1) is established.

A winning center is a proper body image or antipode of
n0=B/||B||, B=(0,phi^-2,1). A threshold center is a proper body image
or antipode of one of the normalized references

    ell=(0,1,-3-3phi), h=(0,1,(3phi-1)/11).

The original signed-region classification supplies these whole families,
not just their optimizers. Proper body images preserve V, dot products,
projections and the exact finite certificates below. At the antipode
the positive active originals are negated, while P_n and absolute
heights are unchanged. We may consequently write the receiving argument
at n0 and the source argument at an actual threshold center n_*.
No improper original Q is introduced. In particular source and receiver
normal reversal need not be coupled: the source proof uses either sign
of its actual n_* and the receiving proof uses either sign of n0.

## 3. Wider receiving localization and actual original heights

The six positive active original vertices at n0 have common height
c0=1/sqrt(3). Their six actual tangents p_i=P_(n0)v_i have a centered
disk of sharp squared inradius 8/3+4phi>9. All six originals, tangents,
six facets and fifteen possible supporting pairs are regenerated.

For a winning normal write n=z n0+w, w perpendicular n0. Consistent
original signs in its region give

    f(n) <= min_i(c0 z+p_i.w) <= c0 z-rho6 ||w||,
    rho6>3.                                                (3)

Since f(n)>q>0, (3) first proves z>0. With c0<289/500 it gives

    ||w|| < ((289/500)-(449/1000))/3 = 43/1000,
    z > 499/500,
    ||n-n0|| = ||w|| sqrt(2/(1+z))
             < (101/100)||w|| < 1/20.                      (4)

The exact guards check 1-(43/1000)^2>(499/500)^2,
(101/100)^2(1+499/500)/2>1 and (101/100)(43/1000)<1/20.
Thus the larger receiver chord is derived from membership and the
actual height; it is not imported from the earlier 1/24 theorem.

All 48 nonactive original vertices have squared center height at least
5/3. Cauchy and R<9/2 imply their actual absolute heights exceed

    5/4-(9/2)(1/20)=41/40.                                 (5)

For every active positive original, the same chord estimate gives

    44/125=577/1000-9/40 < v_i.n
             < 289/500+9/40=803/1000 < 41/40.               (6)

Here 577/1000<c0<289/500 are verified by rational squares. Every active
sign is positive, every nonactive absolute height dominates the active
heights, and hence f(n)=min_i v_i.n. The first three positive original
height ranks are active. The checker lists all 48 actual nonactive
originals and their exact center heights; no presumed polygon order or
invented projected contact is used.

By (2), f(n)<=sqrt(beta)<23/50. Since ||p_i||<=R, also
f(n)>=c0 z-R||w||. With (4) and R<9/2 this implies

    ||w|| > [(577/1000)(499/500)-23/50]/(9/2)
           =57923/2250000.                                 (7)

In particular w is nonzero. This closes the otherwise exceptional
zero receiving-tilt branch for threshold sources.

## 4. Entire closed angular decomposition and the stronger rank gap

For the actual six tangents p_i, all fifteen pair-equality lines
(p_i-p_j).w=0 produce thirty signed candidates. Deduplication as
oriented rays gives eighteen directed walls, including every antipode.
Exact half-plane and determinant comparisons in coordinates
(w.(1,0,0), w.(B cross (1,0,0))) give their complete cyclic order.
All consecutive determinants are positive, so their eighteen closed
cones, each of angle strictly below pi, cover the full tangent plane.

On each adjacent cone [u,v], the interior ray u+v fixes a strict rank
permutation of all six originals. All five adjacent rank inequalities
are checked on BOTH closed endpoint rays. They extend linearly to every
a u+b v, a,b>=0. The exact full minimum endpoint square is

    d3^2=(60-12phi)/19 > (29/20)^2.                         (8)

For each cone the checker now directly verifies the stronger positive
endpoint inequalities g.u>(29/20)||u|| and g.v>(29/20)||v||, where
g=p_third-p_first for its full rank permutation. For every nonzero
w=a u+b v in that closed cone, linearity and the norm triangle
inequality give

    g.w > (29/20)(a||u||+b||v||) >= (29/20)||w||.           (9)

This is a whole-cone argument, including boundary ties and the cyclic
seam. It does not infer a continuum statement from sampled wall values.
All parent wall candidates, rays, ranks and endpoint values are
regenerated entry by entry before the stronger 36 endpoint checks.

The common c0 z cancels in original active height differences. Combining
(7)--(9), the actual third-smallest positive original height exceeds

    f(n)+tau, tau=(29/20)(57923/2250000)
                   =1679767/45000000.                     (10)

Thus at most two positive active originals and their antipodes, FOUR
originals in total, can have absolute height less than f(n)+tau.
For the support candidates below, the height is less than 1/2, so the
48 other originals are excluded separately by (5).

## 5. Every threshold source supplies eight separated actual points

Each actual threshold reference has four positive active original
tangents whose entire quadrilateral has centered disk squared radius
(39+37phi)/29>(9/5)^2. Its consistent signed-region signs and f(k)>=F
give the analogue of (3), with c_beta=sqrt(beta) and rho_*>9/5.
The scalar component along n_* is positive; the acute chord identity,
sqrt(2)<3/2 and c_beta+F>57/125+449/1000>9/10 yield

    ||k-n_*|| <= (sqrt(2)/rho_*)(c_beta-F)
                  < (25/27)epsilon = a=1/162.              (11)

The exact reference shadow has eight distinct projected original
vertices on its maximum circle, with unique original preimages v_i,
absolute height c_beta and radius r_beta=sqrt(R^2-beta)>4.
All 28 original pair distances at EACH reference are regenerated:

    min_{i<j}||P_(n_*)v_i-P_(n_*)v_j||^2
                          =(40+32phi)/29 > 1.              (12)

Both entire tangent quadrilaterals, their eight facets, all sixteen
original circle preimages and all 56 pair distances are compared with
the published exact finite records. Images and antipodes preserve
these statements.

Let A1 be the minimal proper rotation from n_* to the actual k. Its
angle is acute by (11). Choose ANY proper D mapping n_* to the ACTUAL
receiving n, and set W=Q A1 D^t. Then W fixes n and
Q=W D A1^t. For all eight actual source originals set

    p_i=P_n Qv_i, p_i0=W D P_(n_*)v_i.                     (13)

The p_i belong to the actual projected source. The p_i0 are an
isometric circle carrying every possible proper planar roll. For a
minimal normal transport of chord d, resolving the rotation plane gives

    ||P_(n_*)(A1^t-I)v|| <= |v.n_*|d+(R/2)d^2.

Indeed the transverse coefficient changes by -h sin(theta)
+x(cos(theta)-1), with |h|=|v.n_*|, |x|<=R,
|sin(theta)|<=d and 1-cos(theta)=d^2/2. Because
P_n W D=W D P_(n_*), (11)--(13) imply

    ||p_i-p_i0|| < eta=(23/50)a+(9/4)a^2
                         =853/291600 < 3/1000.             (14)

This retains the actual source preimages, both source families,
every proper orientation and full roll. It adds no receiving reference
transport cost. Source tilt zero is allowed; then A1=I and the same
strict upper error bound holds.

## 6. Support selection forces an impossible eight-into-four injection

Suppose S is contained in T. Set r_i=||p_i||>=r_beta-eta>0. The
support of T in direction p_i/r_i is attained by some ACTUAL projected
receiving original q_i=P_n v_i', and containment gives
q_i.p_i>=r_i^2. By (2), ||q_i||^2<=R^2-beta+epsilon. Consequently

    ||p_i-q_i||^2 <= ||q_i||^2-r_i^2
                       < L=epsilon+9eta=1069/32400<1/25.   (15)

Cauchy also gives ||q_i||>=r_i, so the absolute original height of v_i'
is less than H=sqrt(beta+9eta)<1/2. Since H+f(n)>9/10, (2) gives

    H-f(n) < (10/9)L=1069/29160 < tau,
    tau-(10/9)L=2436127/3645000000 > 0.                    (16)

These are exact rational and field guards. The candidate height is
below f(n)+tau, so Sections 3--4 leave at most FOUR actual original
receiving vertices that any support selection can choose. Support ties
cause no difficulty: every possible maximizing original satisfies
the same height bound.

Every source pair has distance greater than 1-2eta>2/5 by (12)--(14),
whereas (15) puts each source point within distance less than 1/5 of
its chosen receiving projection. Two distinct source points cannot
select the same receiving original; otherwise their distance would
be less than 2/5. Thus eight source originals inject into at most four
receiving originals, a contradiction. This excludes even closed
centered unit containment. Section 2 proves (1) and its corollary.

The old 1/24 receiving transport hypothesis, old rank factor 1, old
source-to-receiver distances and old nonwinning receiving cutoff are
not assumptions of this wider theorem. Every replacement bound needed
in the proof is derived above and checked exactly.

## 7. Reproduction, scope and remaining frontier

From a complete public repository checkout, use Python 3.11+ and the
standard library with one process and all numeric threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/wide_threshold_source_certificate.py --self-test
~~~

Every output byte must match
[wide_threshold_source_expected.json](wide_threshold_source_expected.json).
The checker regenerates the full original rank, circle, tangent and
height records and all new scalar gates. Its 26 malformed controls
reject unsupported height/chord/gap/injection parameters, missing or
duplicated originals, wrong ranks, omitted walls or cones, and invalid
circle preimages. Continuous centering, regional coercivity, whole-cone
extension, proper-frame transport and support selection remain the
written mathematical bridges. The old full spectrum, torque, global
and independent-review computations are inherited where cited, not
claimed rerun or as an independent review of this new theorem.

Trust boundary: the original RID model, inspected exact Q(phi)/Fraction
arithmetic and Python semantics, hash-pinned public prerequisites, and
the written bridges above. No floating-point predicate, solver,
sampled continuum, timeout or incomplete enumeration establishes
nonexistence. Native certificate checks are author validation.

This source reduction alone, combined with the independent global
1/445 cutoff, leaves the winning-to-winning receiving interval

    beta-1/150 <= f(n)^2 < beta-1/445

as a separate rotation obligation. Both its source and receiver are
winning, and their normals have chord less than 1/20 from their own
winning centers. The preceding torque certificate at q=909/2000 does
not cover this whole wider domain. The companion all-source proof now
closes that obligation with sharper 1/23 chords, new full840strata
torque geometry and exact closed equalities. Nonwinning receivers in
the wider band and lower-height receiving orientations remain
unresolved; a global 1/150 theorem is not asserted.

Current primary [2604.26531](https://arxiv.org/html/2604.26531) retains
RID non-Rupertness as a conjecture. [2508.18475](https://arxiv.org/abs/2508.18475)
proves non-Rupertness for a different constructed polyhedron. The
standard strict shadow-containment formulation follows
[2112.13754](https://arxiv.org/html/2112.13754). The named-solid table in
[2509.08190](https://arxiv.org/html/2509.08190), checked 2026-09-30,
still lists three unresolved Archimedean solids (snub cube, RID, snub
dodecahedron), two Catalan solids (deltoidal and pentagonal
hexecontahedra), and Johnson J72--J75 and J77. A bounded current
literature search is not an exhaustive absence or priority claim.

Complementary current work by six-rupert-1, researcher, gives the
[deltoidal half-wedge exclusion](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/selected_torque_wedge_proof.md),
source 062fb4ce6d5d471c92fc72a5821806ae16d5e120, graph7771.
Six-rupert-2, researcher, gives the
[J77 directional north-triangle proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_directional_north_triangle/PROOF.md),
source a2c00c148381a36cb840571ca5b82d98e274fc35, graph7735.
These are read as complementary structural work; no different-body
constant is used here. The orchestrator remains the management hub.
