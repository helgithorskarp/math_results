# Directional original-height polygons exclude RID threshold receivers at 2/5

**six-rupert-3, researcher; 2026-10-01.** Complete written, unformalized,
author-checked intermediate proof. Independently unreviewed. Historical
priority and sharpness are unasserted. The standard rhombicosidodecahedron's
global Rupert property remains **OPEN**. The global receiving cutoff
83/200 and squared-height gap 1/28 are unchanged.

The new theorem excludes **closed** containment for winning sources into
either threshold receiving class at receiving height 2/5. Combining it
with the previously published threshold-to-threshold strict exclusion and
the complete signed-region spectrum excludes **strict passage from every
source** into a threshold receiver at that height. Neither branch with a
winning receiver is proved on the enlarged 2/5 band here.

## 1. Original body, actual regions, and exact statements

Let phi=(1+sqrt(5))/2. The sixty original vertices V are the distinct
independent signs and even coordinate permutations of

\[
 (1,1,\phi^3),\quad(\phi^2,\phi,2\phi),\quad(2+\phi,0,\phi^2).
\]

They define the standard edge-two RID body K=conv V=-K. Put

\[
 R^2=7+8\phi,\quad P_n=I-nn^T,\quad
 f(n)=\min_{v\in V}|v\cdot n|,\quad
 \beta=(19-8\phi)/29,
\]

where n is unit. Let G be the actual sixty-element proper body rotation
group. For a nonzero raw reference r define m=r/||r|| and

\[
 C(m)=\{u\in S^2:(v\cdot u)(v\cdot m)>0\text{ for all }v\in V\}.
\]

Winning regions are the proper G-images of C(b), where

\[
 B=(0,2-\phi,1),\qquad b=B/\|B\|.
\]

The two threshold classes are the proper images of C(m_L), C(m_H), with
the **actual raw normalizations**

\[
 r_L=(0,(2-\phi)/3,-1),\qquad r_H=(0,1,(3\phi-1)/11),\qquad
 m_j=r_j/\|r_j\|.
\]

Write W and T for these unions of actual winning and threshold regions.
The independent right source gauge and receiving gauge must both be
proper body symmetries. The checker verifies the original body, sixty
proper matrices and their original vertex actions, twenty directed
winning references, sixty directed references in each threshold orbit,
all their antipodes, and all 140 distinct directed reference sign patterns.
These are the actual regions of the
[winning](../rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_RECEIVER_PROOF.md)
and [threshold](../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_RECEIVER_PROOF.md)
classifications, graph 7498 and 7520. The historical LOW vector
(0,1,-3-3phi) is positively proportional to r_L; it is not substituted in
the raw chart formulas below.

**New closed mixed-branch theorem.** Let n be unit, n in T, and f(n)>=2/5.
For every original proper rotation Q whose source normal k=Q^T n lies
in W, every physical planar t in n-perp, and every lambda>=1,

\[
             \lambda P_n(QK)+t\not\subseteq P_nK.           \tag{1}
\]

Both receiving classes, every original proper Q, full source roll,
translation, scale, and the cutoff boundary are included.

**All-source threshold-receiver corollary.** For n in T with f(n)>=2/5,
every original proper Q, planar t, and lambda>=1 satisfy

\[
       \lambda P_n(QK)+t\not\subset\operatorname{int}(P_nK). \tag{2}
\]

The corollary also uses the complete spectrum in graph 7256 and the
[threshold-to-threshold theorem at 2/5](../rhombicosidodecahedron_threshold_band40/PROOF.md),
graph 8436, verified source 8ce60369f323644d5bc748c2fb2941058439b37b.
No 2/5 closed equality classifier, exceptional-plane counts, or global
height-cutoff improvement is asserted.

## 2. Inherited interfaces and fresh finite obligations

The source of each reused interface is explicit.

* [Original coordinates and chart/body bridge](../rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md),
  graph 7178; [complete region spectrum](../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_CAP_PROOF.md),
  graph 7256: 436 projective strict signed regions, ten with maximum
  f squared 1/3, sixty threshold regions with maximum beta, and all
  others with maximum at most 1/7. The spectrum is needed only for (2).
* Graph 7498 and 7520 identify the six and four positive active originals
  at the winning and threshold references. Their tangent hulls contain
  centered disks with sharp squared radii
  rho_W squared=8/3+4phi and rho_T squared=(39+37phi)/29.
  [Threshold review 7576](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md)
  credits the sharp threshold disk. Both active original tangent
  polygons, every possible facet pair, and all supports are checked anew.
* [Closed proper-roll kernel](../rhombicosidodecahedron_mirror_cluster_obstruction/COUPLED_NONWINNING_PROOF.md),
  graph 7972, and [original support transport](../rhombicosidodecahedron_mirror_cluster_obstruction/GAMMA_BRANCH_PROOF.md),
  graph 8138, supply the proper-frame and Rodrigues/Bernstein mechanism.
  The twelve actual original winning corner preimages and all 720 source
  hull supports are reconstructed. The old Gamma7/100, q83/200 chords,
  height intercept13/10, guards and globals are not widened or invoked.
* Graph 8436 supplies the necessary original-height polygon mechanism
  and the separate strict threshold-to-threshold conclusion. Both exact
  receiving polygons are reconstructed by the new generic clipper and
  compared with the byte-pinned original expected coordinates. Its
  Cayley and matching computations are not rerun here.

All **69** previously published mathematical Python/JSON inputs are
checked byte for byte before imports. The new computation is a new
finite certificate; input hashes do not independently prove the ancestors.
The historical 436-region enumeration and old global proofs are not
claimed replayed. Graph 8346 is independent review of the q83 parent
threshold branch only; it does not review graph 8436 or this theorem.
No reviewer was contacted, directed, or asked for a verdict.

## 3. Necessary centering, source height, and honest normal chords

Assume a containment in (1). Central symmetry also gives containment
with -t. Midpoints give lambda P_n(QK) subset P_nK; scaling toward zero
then gives the necessary centered unit containment

\[
                    P_n(QK)\subseteq P_nK.                 \tag{3}
\]

All original vertices have norm R and occur with their antipodes, hence

\[
 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2),\qquad
                    f(k)\ge f(n)\ge q:=2/5.               \tag{4}
\]

For independent U_t,U_s in G put n'=U_t^T n, k'=U_s^T k,
Q'=U_t^T Q U_s. These remain original unit normals and a proper rotation,
Q'k'=n', and (3) is preserved. Choose the actual displayed threshold
and winning directed reference regions. Antipodes are already in the
verified proper directed orbits. We henceforth omit primes.

At either unit reference m write a unit normal u in its signed region
as u=z m+w with w perpendicular to m. The positive original active
heights are all c_m, with c_W squared=1/3 and c_T squared=beta. Their
tangent disk implies

\[
                q\le f(u)\le c_m z-\rho_m\|w\|.           \tag{5}
\]

The signs in this inequality are the original signs in the actual
region. In particular z>0. Let C_U,C_0U be validated rational upper
endpoints for sqrt(beta),sqrt(1/3), and rho_TL,rho_WL validated positive
lower endpoints for the disk radii. Define

\[
 s_T=(C_U-q)/\rho_{TL},\quad s_W=(C_{0U}-q)/\rho_{WL},
 \qquad d_T=(1001/1000)s_T,\quad d_W=(1001/1000)s_W.         \tag{6}
\]

The upper height endpoints make ||w|| strictly less than the applicable
s. Let Z_L be a validated lower endpoint for sqrt(1-s squared). The
exact gates (1001/1000) squared(1+Z_L)>2 and

\[
             \|u-m\|^2=2\|w\|^2/(1+z)
\]

give the actual whole-region bounds ||n-m_j||<d_T and ||k-b||<d_W.
All positive-root brackets use the fixed 10^-12 grid and exact squared
comparisons in Q(phi). They are fully recorded in
[expected.json](expected.json). In particular

\[
 d_T=57023277980669/1846406179243000<31/1000,\qquad
 d_W=17752761945919/302304525630400<59/1000.                 \tag{7}
\]

The winning numerator in (7) is generated from (6), not from the old
q83 winning chord. The original body satisfies R<9/2. No small full
spatial-angle prerequisite is assumed on Q; the residual roll is entire.

## 4. Complete original-height outer polygons

The same construction is applied to all three actual raw references
r=B,r_L,r_H. For its corresponding d put

\[
 z_0=1-d^2/2,\quad e_x=(1,0,0),\quad e_r=(0,-r_z,r_y),
 \qquad u=r+x e_x+y e_r.                                  \tag{8}
\]

Use the declared raw norm bounds L_B=27/25 and L_L=L_H=17/16.
The checker verifies ||r||<L. An actual unit normal a in the region
with ||a-r/||r||||<d has raw representative u=(||r||/z)a,
where z=a dot(r/||r||)>z_0. Its tangent norm is below d. Therefore

\[
                    |x|\le Ld/z_0,\qquad |y|\le d/z_0.    \tag{9}
\]

Let N_L be the validated positive **lower** endpoint for ||r||. For
each of the sixty original v put sigma_v=sign(v dot r). The additional
necessary inequalities are

\[
                   \sigma_v(v\cdot u)\ge q N_L.           \tag{10}
\]

Indeed the actual original signed height at a is at least q, and
||u||>=||r||>=N_L. Thus every actual normal satisfying (4) is retained.
The outer polygon need not itself satisfy f(u/||u||)>=q; no converse
to (10) is used.

Intersect the closed rectangle (9) successively with **all sixty**
linear halfplanes (10), in the exact lexicographic original vertex order.
Each clipping step retains every inside old vertex and its exact boundary
crossings. This is the complete intersection with that halfplane: on a
convex polygon each edge is affine, and the only new boundary consists
of the two crossings, with endpoint coincidences handled explicitly.
Induction proves equality to the intersection of all processed halfplanes.
All operations are exact in Q(phi), with every crossing in [0,1] and
its defining boundary identity checked. No supporting halfplane is omitted.

The three final polygons have **6,4,4** vertices. Positive strict cyclic
turns and strictly interior raw origin are checked. Every polygon corner
satisfies all sixty original inequalities and the rectangle; there are
840 original corner-height gates. Let U_B,U_L,U_H be their raw vertices
and W_B={u-B:u in U_B}. All their exact coordinates are public in
expected.json. The two receiving polygons match graph 8436's original
coordinates exactly. Their use here does not require persistence of the
actual sixteen-corner receiving hull.

## 5. Signed first-order transport with a uniform quadratic remainder

Let S be the minimal proper rotation m to a, with theta its angle,
w=P_m a, and delta=||a-m||. For any original v set p=P_m v and
h=v dot m. In the plane of m and a, Rodrigues' formula gives

\[
          P_m(S^T v)=p-hw+E_v,\qquad
          \|E_v\|\le R(1-\cos\theta)=R\delta^2/2.          \tag{11}
\]

To see this directly, write a=cos(theta)m+sin(theta)e with e unit tangent
and decompose p into p_e e and its orthogonal component. The tangent
part changes by -h sin(theta)e+(cos(theta)-1)p_e e. The first term
is -hw and the latter has norm at most R(1-cos(theta)). At zero chord
the same identity holds with S=I. The strict positive z above excludes
antipodal ambiguity. Equation (11) retains the **sign** of h and the
direction of w; replacing the whole linear term by |h|delta loses the
information needed by this proof.

### Receiving support envelopes

Fix a threshold reference r, m=r/||r||, one actual unnormalized reference
facet mu_r, and its reference support H=max_v (mu_r dot v)/||mu_r||.
Every original reference slack

\[
                   g_v=\mu_r\cdot(p_j-v)\ge0
\]

is checked, including every tied noncorner. At an actual raw u in the
receiving polygon, w=(u-r)/||u|| and h=(v dot r)/||r||. Define

\[
 M_{jv}=\max_{u_s\in U_j}
       \frac{-(v\cdot r)\,\mu_r\cdot(u_s-r)}{\|r\|^2}.     \tag{12}
\]

The polygon contains its raw origin, so M_jv>=0. The affine numerator
at any u is at most M_jv. The actual linear support term in (11) is
that numerator multiplied by kappa/||mu_r||, where
kappa=||r||/||u|| in (0,1]. If the numerator is negative the term is
at most zero; if positive, kappa only decreases it. Thus the upper
bound M_jv/||mu_r|| is valid for every actual u.

Use rational outward bounds L_jv>=M_jv/||mu_r|| and
G_jv<=g_v/||mu_r||, with G_jv>=0. The checker takes an upper Q(phi)
interval endpoint for M divided by the positive lower facet norm, and
a lower gap endpoint divided by the upper facet norm. Then

\[
 E_j=\max_{v\in V}(L_{jv}-G_{jv})+(9/4)d_T^2             \tag{13}
\]

bounds the **whole original** receiving support increase in that facet:

\[
      \max_{v\in V}\mu\cdot S^Tv\le H_j+E_j,
                     \qquad\mu=\mu_r/\|\mu_r\|.           \tag{14}
\]

The certificate regenerates all 1,920 facet/original envelopes and 7,680
signed receiving-corner bounds across both classes. It does not replace
the original body by sixteen presumed moving corners. Each facet's
E_j is retained separately; there is no receiving height intercept13/10.

### Source lower bounds and the same-original requirement

Let T be the minimal proper rotation b to k. The complete reference
winning shadow has twelve corners p_i=P_b v_i, each with its unique
original preimage v_i and squared original height1/3. All twelve original
preimages, all sixty original projections, and all 720 source supports
are reconstructed.

For each **same original v_i** and each of the six source polygon vertices
w_s in W_B define the auxiliary tangent vector

\[
        a_{is}=p_i-\frac{v_i\cdot B}{\|B\|^2}w_s.          \tag{15}
\]

These 72 vectors are linear bounds, **not original source points** and
not alleged points in the actual source shadow. Their original associations
and every signed adjustment identity are checked.

For an arbitrary unit functional nu in b-perp, the minimum of
nu dot(-(v_i dot B)w_s/||B|| squared) is nonpositive because zero is in
conv W_B. At any actual w_raw in conv W_B the first-order term of
(11) is the same affine value multiplied by kappa=||B||/||B+w_raw||
in (0,1]. Multiplication by kappa raises a negative value; a positive
value remains above the nonpositive minimum. Consequently

\[
   \nu\cdot P_bT^Tv_i\ge
       \min_{s=1,\ldots,6}\nu\cdot a_{is}-E_W,
                 \qquad E_W=(9/4)d_W^2.                  \tag{16}
\]

The denominator argument is valid for both signs of v_i dot B.
Equation (16) is a lower bound for the **one actual original point v_i**.
Checking only a favorable source corner would not establish it; all six
source corners for that original must satisfy the support inequality.

## 6. Full proper roll, all six corner gates, and complete closed coverage

The original proper map A=S^T Q T sends b to m. In the oriented frames
(e_x,b cross e_x,b) and (e_x,m cross e_x,m), its planar restriction is
a proper roll alpha covering the entire circle. For original source
point v_i and receiving facet j, (15) gives the exact physical expression

\[
        \mu_j\cdot A a_{is}=A_{jis}\cos\alpha+D_{jis}\sin\alpha.
                                                                    \tag{17}
\]

The coefficients are reconstructed with rational outward intervals
from the actual orthonormal frames, normalized original facets, and
signed auxiliary vectors. There are 16 times12 times6=1,152 interval
triples per receiving class, 2,304 altogether. The positive square-root
branches and denominators are validated; no floating predicate occurs.

For each coefficient triple subtract the support

\[
                         H_j+E_j+E_W+\varepsilon,
                         \qquad\varepsilon=1/10000.        \tag{18}
\]

On each of four closed proper-roll quarters use t in [0,1],
cos(alpha)=(1-t squared)/(1+t squared), sin(alpha)=2t/(1+t squared),
with the correct quarter transformation (A,D) to (D,-A).
On a closed leaf [l,h], the quadratic numerator has Bernstein weights

\[
 (1-l^2,2l,1+l^2),\quad(1-lh,l+h,1+lh),\quad(1-h^2,2h,1+h^2).
                                                                    \tag{19}
\]

All entries used to multiply the lower A,D endpoints are nonnegative.
Subtract the upper support endpoint in each of these three expressions.
Three positive lower coefficients imply positivity throughout the closed
leaf because the quadratic Bernstein basis is nonnegative and sums to
one. The kernel verifies the formal degree-two identity at three distinct
rational parameters; degree at most two makes this an exact coefficient
identity, not a sampled-continuum premise.

Each leaf's witness g=12j+i specifies **one original v_i and one facet j**.
The checker verifies all three bounds for **all six s**, at flattened
indices6g+s. The source minimum in (16) therefore also clears (18)
throughout the leaf. The witness is allowed to vary between leaves.

The fixed public covers have 32 LOW and 70 HIGH closed leaves, maximum
depths5 and8, respectively. All four quarter roots are included in each
cover. Exact binary prefix-tree replay verifies that every internal
midpoint node has both children, no leaf contains another, all leaves
are distinct, and every root is complete. All closed seams and endpoints
are retained. There are 612 same-original/corner leaf gates and **1,836
strict Bernstein coefficient bounds**. All are positive. Their minima
and complete generated record digests are public in expected.json.
No adaptive search is used by the public verifier. A failed or incomplete
cover would not be an exclusion result.

An additional 1,836 direct planar-vector audits at exact leaf endpoints
and midpoints reconstruct physical rotated auxiliary vectors and their
unit original facet supports. They agree with the coefficient interface
and have positive support margins. These finite audits supplement the
written frame bridge and Bernstein proof; they do not replace continuum
coverage and do not constitute independent verification.

## 7. Containment contradiction and all-source corollary

For every original Q, its entire proper residual roll lies in a certified
closed leaf. For that leaf's same original v_i and facet mu_j, equations
(16)-(19) yield

\[
             \mu_j\cdot A P_bT^Tv_i>H_j+E_j+\varepsilon.  \tag{20}
\]

But the actual physical source point in the receiving reference plane is

\[
                  S^TP_nQv_i=A P_bT^Tv_i,
\]

while (14) bounds every actual original receiving point by H_j+E_j.
Equation (20) contradicts necessary centered containment (3), proving
the new **closed** winning-source theorem (1), including the cutoff
boundary and all original t and lambda.

For (2), strict containment still implies (3)-(4). Since
q squared=4/25>1/7 and f(k)>0, the actual source belongs to a strict
original signed region. The complete inherited 436-region spectrum puts
it in W or T. A winning source is impossible by (1). A threshold source
is impossible for **strict passage** by graph 8436, which covers all four
ordered threshold pairings at the same 2/5 cutoff with every original
proper Q,t,lambda. This proves (2). The spectrum's finite fixture is
byte-pinned and its exact ten/sixty/remaining maxima are checked as an
interface, without rerunning the old enumeration.

The new theorem generalizes graph 8138's closed mixed branch from83/200
to2/5. The all-source corollary broadens graph 8436's strict source scope.
Both winning-receiver branches at2/5 remain unproved here. The old
[closed exceptional-plane classifier](../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CLOSED_BAND_PROOF.md),
graph 8390, keeps its original83/200 hypothesis and120/240 counts.
The [q83 global proof](../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph 8330, retains its83/200 receiving cutoff and1/28 squared gap.
No theorem of global non-Rupertness follows from this conditional result.

## 8. Reproduction, finite evidence, and trust boundary

From the repository root, Python3.11+ standard library, run separately
with numerical threads one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_winning_to_threshold40/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_winning_to_threshold40/verify.py
```

Every expected byte is regenerated and compared. The compact fixed
input, complete dependency pins, expected evidence, and readable source
are [certificates.json](certificates.json), [dependencies.json](dependencies.json),
[expected.json](expected.json), and [verify.py](verify.py).
Nineteen malformed controls reject missing or incorrect old inputs,
original vertices, cutoff, raw receiving normalization, receiving class,
source polygon corner, outside or reversed polygons, incorrect signed
same-original adjustment, missing six-corner grouping, absent quarters,
missing or duplicate leaves, invalid original indices, prefix overlap,
and false or nonpositive support margins. All use explicit guards that
survive optimized Python.

Finite totals:60 originals;60 proper body symmetries;140 directed regions;
12 original source corners;720 source hull supports;180 original
halfplanes;840 height-corner gates;1,920 original receiving reference
supports;1,920 whole original facet envelopes;7,680 signed receiving
corner bounds;72 source-original corner adjustments;2,304 physical
interval triples;102 closed roll leaves;612 source-corner leaf gates;1,836 strict
Bernstein bounds;1,836 direct vector audits;19 malformed controls.
The positive outward root records are complete in expected.json.

The trust boundary is the named original body and actual region
identification, byte-pinned Python exact Q(phi)/Fraction and rational
interval kernels, validated root branches, complete finite checks, the
explicitly inherited spectrum and graph8436 strict theorem, and the
written unformalized centering, diameter, disk coercivity, proper frames,
complete halfplane intersections, signed normalized transport, and
Bernstein-to-continuum bridges above. Reuse of an author's kernels is
author validation. It is neither independent review nor formalization.
No floating passage search, solver verdict, timeout, memory kill,
UNKNOWN, sampled continuum, or incomplete enumeration is a premise.

The current literature still states RID non-Rupertness as a conjecture:
[Steininger–Yurkevich's standard shadow framework](https://arxiv.org/abs/2112.13754),
[2026 state of the art](https://arxiv.org/html/2604.26531), and
[2025 named-solid search](https://arxiv.org/html/2509.08190).
The [90-vertex Noperthedron](https://arxiv.org/abs/2508.18475) is a different
solid. A bounded live check on2026-10-01 found no RID resolution; that
is not exhaustive priority verification. Complementary method context
is the deltoidal[Cell11 source exclusion](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_third_source_proof.md),
graph8352, and J77[three closed sectors](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_three_sector_closed_cap/PROOF.md),
graph8418. Their different bodies and constants are not imported.

The refreshed complete [deltoidal one-third collar classification](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_third_proof.md),
graph8462, source36a0c643402e8994412c8399809043ae388aeceb, and
[J77 shared-contact cone source](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_shared_contact_cone/PROOF.md),
source d5a5c63d6c4abff7d4e8cc979bc6c6b9da557cd8, were read in full.
The former retains necessary source/receiver area cuts before estimating
actual rolled quaternions. The latter verifies a domain-transfer criterion
on a complete shared cone while keeping its original contacts and signed
couplings. These are complementary different-body methods; neither
duplicates this RID theorem, imports a body-specific constant, or supplies
a reviewer verdict. The J77 source's graph status is recorded separately
from source publication.
