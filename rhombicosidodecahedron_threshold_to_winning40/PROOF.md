# Signed original threshold sources cannot enter winning RID receivers at 2/5

**six-rupert-3, researcher; 2026-10-01.** Complete written, unformalized,
author-checked intermediate proof; independently unreviewed. Historical
priority and sharpness are unasserted. The standard rhombicosidodecahedron
(RID) remains globally **OPEN**. Its proved global receiving cutoff
83/200 and squared-height gap 1/28 are unchanged.

This proof reverses the roles in the previous directional polygon result.
It uses the actual sixteen original threshold shadow corner preimages,
including eight noncircle originals with their different signed heights,
and all sixty originals in each of twelve winning receiving supports.
Each full-roll witness checks all four source polygon corners for the
**same original vertex**, with a positive physical margin 1/10000.

## 1. Original body, actual regions, and statement

Put phi=(1+sqrt(5))/2. Let V be the sixty distinct independent signs and
even coordinate permutations of

\[
 (1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2).
\]

The standard edge-two RID is K=conv V=-K. Every original v has common
squared radius R squared=7+8phi<81/4. For unit n set

\[
 P_n=I-nn^T,\qquad f(n)=\min_{v\in V}|v\cdot n|,
 \qquad\beta=(19-8\phi)/29.
\]

For any unit reference m, define its original strict signed region

\[
 C(m)=\{a\in S^2:(v\cdot a)(v\cdot m)>0\text{ for every }v\in V\}.
\]

Let G be the actual sixty proper body rotations. Let W be the union of
proper G-images of C(b), and T the union of proper G-images of C(m_L)
and C(m_H), using these **actual raw normalizations**:

\[
 B=(0,2-\phi,1),\quad b=B/\|B\|,\qquad
 r_L=(0,(2-\phi)/3,-1),\quad r_H=(0,1,(3\phi-1)/11),
 \quad m_j=r_j/\|r_j\|.
\]

The checker reconstructs all actual proper rotations and their original
vertex actions, twenty directed winning references, sixty in each
threshold class, all their antipodes, and 140 distinct original directed
sign patterns. These are the actual regions in graph 7498 and 7520.
A positive rescaling of a raw vector does not change the region, but
these precise raw vectors are retained in all chart denominators.

**Theorem (closed threshold-source exclusion).** If n is unit,
n in W, and f(n)>=2/5, then for every original Q in SO(3) with source
normal k=Q transpose n in T, every physical planar t in n-perp and
lambda>=1,

\[
                    \lambda P_n(QK)+t\not\subseteq P_nK.       \tag{1}
\]

Both threshold source classes, all original proper rotations, the entire
residual roll circle, translations, scales and the receiving boundary
f(n)=2/5 are included.

**Corollary (only the winning-to-winning branch remains at 2/5).** If
an original strict passage satisfies f(n)>=2/5, both its receiving normal
n and source normal k must belong to W. In particular all mixed W/T
branches are excluded for closed containment at this cutoff when (1)
is combined with graph 8487; all threshold receivers exclude strict
passage by that previous graph's all-source corollary. The remaining
winning-to-winning branch at 2/5 is unproved here.

## 2. Credited interfaces and fresh obligations

The graph references identify contributions, not independent review of
this new theorem. The source interfaces are:

* [Original body and chart bridge](../rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md),
  graph 7178. The complete original V and antipodal common radius are
  checked afresh.
* [Winning geometry](../rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_RECEIVER_PROOF.md),
  graph 7498, and [threshold geometry](../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_RECEIVER_PROOF.md),
  graph 7520: six and four positive original reference contacts of heights
  c_W squared=1/3 and c_T squared=beta. Their positive tangent hulls contain
  centered disks of sharp squared radii rho_W squared=8/3+4phi and
  rho_T squared=(39+37phi)/29. All possible active facet pairs and supports
  of both polygons are regenerated. The sharp threshold disk is also
  credited to [review 7576](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md).
* [Proper-frame transport and closed-roll kernel](../rhombicosidodecahedron_mirror_cluster_obstruction/COUPLED_NONWINNING_PROOF.md),
  graph 7972, and [directional original-height polygons](../rhombicosidodecahedron_winning_to_threshold40/PROOF.md),
  graph 8487, source 3d7955151dedbb83a37cee8faacaf8875491a37c. Its exact
  2/5 scalar bridge and complete polygon clipper are reused without
  modifying their guards. Each necessary polygon is regenerated and
  compared entry by entry with its pinned previous coordinates. Its
  previously proved roles are reversed here; the new original source
  preimages, receiving envelopes, physical coefficients and closed
  covers are rebuilt for those roles.
* [Complete signed-region spectrum](../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_CAP_PROOF.md),
  graph 7256, is needed only for the corollary: 436 projective regions,
  ten winning with maximum f squared 1/3, sixty threshold with maximum
  beta, and all others with maximum at most 1/7. Its old enumeration is
  not rerun. Graph 8487's all-source strict threshold-receiver corollary
  also uses [the threshold-to-threshold 2/5 proof](../rhombicosidodecahedron_threshold_band40/PROOF.md),
  graph 8436, source 8ce60369f323644d5bc748c2fb2941058439b37b.

The earlier [axial-majorization theorem](../rhombicosidodecahedron_mirror_cluster_obstruction/AXIAL_MAJORIZATION_PROOF.md),
graph 8110, excludes this same ordered mixed branch at 21/50. The new
proof extends it to 2/5 using directional supports. Its old scalar guard
is retained; its scalar is not called at 2/5. A private four-height-sum
estimate at 2/5 had a negative sufficient gap and is not a premise here.
The [global 83/200 proof](../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph 8330, and [closed exceptional-plane classifier](../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CLOSED_BAND_PROOF.md),
graph 8390, retain their original cutoff and counts. Review 8346 applies
to the earlier 83/200 threshold branch, not this new theorem.

All **73** previously published mathematical Python/JSON files are
byte-pinned before imports. This verifies provenance, not independent
proof of the ancestors. Old region enumeration, global moment and
Cayley computations are not recursively replayed. No reviewer was
contacted or directed. This proof is author-checked and unformalized.

## 3. Necessary centering and localization of actual original normals

Suppose containment in (1) holds. By central symmetry the same holds
with -t. Midpoints give lambda P_n(QK) subset P_nK. Since zero belongs
to P_n(QK) and lambda>=1, scaling toward zero gives necessary centered
unit containment

\[
                         P_n(QK)\subseteq P_nK.               \tag{2}
\]

Because all originals are antipodal and have equal radius, a farthest
projected original and its negative attain the diameter. Thus

\[
 \operatorname{diam}(P_nK)^2=4(R^2-f(n)^2),\qquad
                       f(k)\ge f(n)\ge q:=2/5.               \tag{3}
\]

Independent actual proper receiving and source body gauges U_t,U_s
replace n,k,Q by U_t transpose n, U_s transpose k, U_t transpose Q U_s.
They preserve (2), original vertices, physical orientation, scale and
translation. Choose the displayed winning receiver reference b and
either threshold source reference m_j. Directed reversal is already
covered by the actual proper orbits. No small initial angle on Q is
assumed.

For a unit normal a=z m+w in the actual signed region of a reference m,
the original positive active heights and their centered tangent disk give

\[
                    q\le f(a)\le c_m z-\rho_m\|w\|.           \tag{4}
\]

The retained original signs imply z>0. With validated rational upper
height endpoints C_U>=sqrt(beta), C_0U>=sqrt(1/3) and positive lower
disk endpoints rho_TL,rho_WL, put

\[
 s_T=(C_U-q)/\rho_{TL},\quad s_W=(C_{0U}-q)/\rho_{WL},
 \quad d_T=(1001/1000)s_T,\quad d_W=(1001/1000)s_W.            \tag{5}
\]

The endpoints are outward, hence actual tangent norms are strictly
smaller than s_T or s_W. Validated lower roots Z_L for sqrt(1-s squared)
satisfy (1001/1000) squared(1+Z_L)>2. The exact unit chord identity
||a-m|| squared=2||w|| squared/(1+z) therefore gives

\[
 \|k-m_j\|<d_T=57023277980669/1846406179243000<31/1000,
 \quad\|n-b\|<d_W=17752761945919/302304525630400<59/1000.      \tag{6}
\]

These are bounds on the two actual normals; the residual proper roll is
still entire. All root brackets use the fixed positive 10^-12 grid and
exact squared comparisons in Q(phi). Every used positive denominator
is checked. The original-body radius bound R<9/2 will give uniform
quadratic remainder bounds.

## 4. Necessary original-height polygons and exact source preimages

For each actual raw reference r=B,r_L,r_H and its appropriate d, use

\[
 e_x=(1,0,0),\quad e_r=(0,-r_z,r_y),\quad
 z_0=1-d^2/2,\qquad u=r+x e_x+y e_r.                        \tag{7}
\]

Then r dot u=||r|| squared. For every actual normal a with the chord
bound in (6), its unique raw representative u=||r|| a/(a dot m) has

\[
 |x|\le L_r d/z_0,\qquad |y|\le d/z_0,
 \quad L_B=27/25>\|B\|,\quad L_{r_j}=17/16>\|r_j\|.         \tag{8}
\]

Indeed a dot m>=z_0 and the tangent coordinates have norm at most d;
||e_r||=||r|| gives the y bound. The actual height constraints and
original signs imply, for all sixty originals,

\[
 \sigma_v(v\cdot u)\ge q\|u\|\ge qN_L,
 \quad\sigma_v=\operatorname{sign}(v\cdot r),
 \quad 0<N_L\le\|r\|.                                    \tag{9}
\]

Here ||u||>=||r|| follows from orthogonality. Thus the closed chart
rectangle in (8), intersected with every one of the sixty exact affine
halfplanes in (9), retains every actual normal required by (3).
The fixed positive lower raw norm N_L is validated by squaring.

The reused exact clipper intersects all sixty halfplanes in original
lexicographic order. For a convex polygon, each retained side endpoint
and each exact crossing is the complete polygon-halfplane intersection;
induction proves complete clipping of the rectangle. It does not infer
an actual normalized height bound from a merely necessary halfplane.
The resulting outer polygons have six winning vertices U_B and four
vertices U_L,U_H. Exact tests verify distinct cyclic vertices, strict
positive turns, the raw reference strictly inside, chart rectangle
bounds and all 840 original/corner height gates. Their full exact
coordinates are in [expected.json](expected.json). They match the
previous graph 8487 polygons, regenerated for the new roles.

For each threshold source reference, the sixty original projections
are all distinct. The complete exact monotone-chain hull has sixteen
corners p_i=P_m v_i, each with a unique **original** v_i. All 960 source
facet/original supports are checked per class. Eight preimages have
squared unit reference height beta; the other eight do not. Their actual
squared heights, including multiplicities, are:

| Source class | Eight circle originals | Four noncircle originals | Four other noncircle originals |
| --- | --- | --- | --- |
| LOW | beta | (31+48phi)/145 | (119+72phi)/145 |
| HIGH | beta | (31+48phi)/145 | (171-72phi)/145 |

Every **signed raw** height v_i dot r, projected point and original
association is recorded and checked. None of the noncircle heights is
replaced by sqrt(beta). The twelve winning receiving facets are freshly
reconstructed from the complete original reference hull. Receiving
transport below includes all sixty originals, including tied noncorners;
no moving hull combinatorics is assumed.

## 5. Signed transport of original source points and receiving supports

For the minimal proper rotation S from m to a, write w=P_m a and
h=v dot m. Resolving Rodrigues' formula in the plane of m,a gives

\[
 P_mS^Tv=P_mv-hw+E_v,\qquad
                  \|E_v\|\le R\|a-m\|^2/2.                \tag{10}
\]

Specifically a=cos(theta)m+sin(theta)e, and the tangent component of
v along e changes by -h sin(theta)e+(cos(theta)-1)(v dot e)e.
The first term is -hw; the remaining norm is at most
R(1-cos(theta))=R||a-m|| squared/2. At a=m, S=I. Positive z excludes
antipodal ambiguity. This retains both the sign and direction of the
original axial contribution.

Let S now denote the minimal rotation b to the winning receiver n.
For receiving facet j let mu_j_raw be its nonzero outward original
normal, p_j its reference endpoint, mu_j=mu_j_raw/||mu_j_raw|| and
H_j=mu_j dot p_j>0. Every original reference slack

\[
                   g_{jv}=\mu_{j,raw}\cdot(p_j-v)\ge0       \tag{11}
\]

is checked. On the six-corner receiving polygon U_B define

\[
 M_{jv}=\max_{u_s\in U_B}
       \frac{-(v\cdot B)\mu_{j,raw}\cdot(u_s-B)}{\|B\|^2}.
                                                                    \tag{12}
\]

Because the raw reference is inside the polygon, M_jv>=0. At any
actual raw u in that polygon, the linear support term in (10) is the
same affine numerator multiplied by kappa/||mu_j_raw||, with
kappa=||B||/||u|| in (0,1]. A negative affine value is bounded above
by zero; a positive value decreases after multiplication by kappa.
Thus M_jv/||mu_j_raw|| is a valid uniform upper bound.

The checker uses outward rational L_jv>=M_jv/||mu_j_raw|| and
0<=G_jv<=g_jv/||mu_j_raw||. Set

\[
 E_j=\max_{v\in V}(L_{jv}-G_{jv})+(9/4)d_W^2.              \tag{13}
\]

It follows from (10)-(13), R<9/2 and every original slack that

\[
                \max_{v\in V}\mu_j\cdot S^Tv\le H_j+E_j.  \tag{14}
\]

All twelve facets, all 720 facet/original envelopes and 4,320 signed
receiving-corner bounds are regenerated. A separate E_j is retained
for each facet. The maximization is over all originals, rather than
presumed corner labels of the actual receiving shadow.

For either threshold source put r=r_j, m=r/||r|| and let T be the
minimal proper rotation m to k. For every original preimage v_i and
every one of its four source polygon corners define the auxiliary vector

\[
 a_{is}=p_i-\frac{v_i\cdot r}{\|r\|^2}(u_s-r),
                 \qquad p_i=P_m v_i.                     \tag{15}
\]

These are bounds, not substituted original vertices or asserted actual
source points. All signed adjustment identities for all sixteen
originals are checked, retaining each actual v_i dot r.

For any unit functional nu in m-perp the minimum of the affine linear
adjustments at all four corners is nonpositive, because the raw reference
is in their convex hull. At an actual raw u in that polygon the linear
term in (10) is the corresponding affine adjustment multiplied by
kappa=||r||/||u|| in (0,1]. This increases a negative value; a positive
value remains above the nonpositive corner minimum. For the **same**
original v_i it follows that

\[
 \nu\cdot P_mT^Tv_i\ge\min_{s=1,\ldots,4}\nu\cdot a_{is}-E_T,
                       \qquad E_T=(9/4)d_T^2.             \tag{16}
\]

This denominator argument is valid for every signed original height,
including all eight noncircle originals in each class. It does not
select a favorable source corner. All four corners for a common v_i
must satisfy the next support test.

## 6. Entire proper roll with fixed closed covers

The proper original map A=S transpose Q T sends m to b. Its planar
restriction in the oriented orthonormal frames
(e_x,m cross e_x,m) and (e_x,b cross e_x,b) has arbitrary proper roll
alpha. The whole circle must be covered. For source corner vector a_is,

\[
              \mu_j\cdot A a_{is}
                      =A_{jis}\cos\alpha+D_{jis}\sin\alpha. \tag{17}
\]

Normalized actual original facets and those frames generate outward
interval coefficients, with checked positive root denominators. There
are 12 times16 times4=768 interval triples for each source class.
Subtract H_j+E_j+E_T+epsilon, where epsilon=1/10000.

On each of four closed proper quarters parameterize by t in [0,1],
cos=(1-t squared)/(1+t squared) and sin=2t/(1+t squared). Successive
quarter coefficients transform (A,D) to (D,-A). On any closed leaf
[l,h] the numerator's three quadratic Bernstein coefficients have
weights

\[
 (1-l^2,2l,1+l^2),\quad(1-lh,l+h,1+lh),\quad(1-h^2,2h,1+h^2).
                                                                    \tag{18}
\]

All multipliers of the A,D lower endpoints are nonnegative; the upper
support endpoint is subtracted. Three strictly positive rational lower
bounds imply positivity throughout the closed interval, since the
Bernstein basis is nonnegative and sums to one. The kernel checks the
identity between these two degree-at-most-two polynomials at three
distinct rational points, which proves an exact polynomial identity.
Those identity checks are not a sampled-continuum premise.

Each fixed leaf witness g=16j+i chooses **one facet and one original**.
At all four flattened indices 4g+s the checker verifies all three
Bernstein lower bounds. Consequently the source minimum in (16) also
exceeds H_j+E_j+E_T+epsilon on that entire leaf.

Each source class has a fixed complete 26-leaf cover, maximum binary
depth three. Both have all four closed quarter roots, exact dyadic
endpoints, both children at every internal node, no missing leaves,
no repeated leaves and no leaf overlapping its child. Prefix-tree
replay proves complete coverage including all quarter seams. The input
leaf lists coincide for the two classes, but their distinct original
geometry, coefficients, signed heights and every numerical gate are
reconstructed separately; equality of leaf labels does not substitute
for either replay. In total, 52 closed leaves give 208 same-original
corner gates and **624 positive Bernstein lower bounds**.

An additional 624 direct planar-vector audits reconstruct rotated
auxiliary vectors at leaf endpoints and midpoints, check their agreement
with the physical coefficient interface, and verify their positive
support margins. These finite checks supplement the frame derivation
and continuum proof; they are not independent review or a substitute
for the Bernstein cover. No adaptive search is used by the public
checker. An incomplete cover, timeout or failed bound would not prove
nonexistence.

## 7. Original containment contradiction and remaining branch

For any original Q its actual full proper residual roll belongs to a
certified closed leaf. By (16)-(18), that leaf's **same original v_i**
satisfies

\[
                 \mu_j\cdot A P_mT^Tv_i>H_j+E_j+\varepsilon.\tag{19}
\]

But its physical source point in the receiving reference plane is
S transpose P_n Q v_i=A P_m T transpose v_i, while (14) bounds every
actual original receiving point, and hence its convex hull, by H_j+E_j.
This contradicts (2). The centering reduction retained the original
n,Q,physical t and lambda, proving (1) for all of them, including the
closed height boundary. No full-Q small-angle assumption was used.

For a strict passage with f(n)>=q, (3) still applies. Since
q squared=4/25>1/7, neither n nor k lies on an original zero-height
boundary or in any of the other regions of the inherited 436 spectrum.
Thus each lies in W or T. If n is threshold, the all-source corollary
of graph 8487 excludes strict passage. If n is winning and k is
threshold, (1) excludes even closed containment. Therefore any remaining
strict passage on the 2/5 receiving band has n,k in W. This establishes
the stated corollary, leaving that specific winning-to-winning branch
open. It does not lower the global cutoff.

The enlarged winning receiving domain is nonempty below the old
83/200 band. The actual raw normal

\[
                           u_*=(21/500,2-\phi,1)
\]

has all sixty original strict winning signs and its exactly computed
minimum squared original height lies in [4/25,(83/200) squared).
The certificate checks these inequalities in Q(phi) and records the
exact value. This is an actual receiver in the new domain, not a
passage witness or a non-Rupert conclusion.

## 8. Reproduction, finite evidence, and trust boundary

From the repository root, Python3.11+ standard library, with numerical
threads one, run these separately:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_threshold_to_winning40/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_threshold_to_winning40/verify.py
```

Every byte of [expected.json](expected.json) is regenerated and compared.
The fixed [certificate](certificates.json), all [dependency pins](dependencies.json),
and [verifier](verify.py) provide compact reproducible source. The exact
counts are 60 original vertices, 60 proper body rotations, 140 directed
sign regions, 32 threshold source preimages with 1,920 source support
tests, twelve winning receiving facets with 720 reference supports,
180 original clipping halfplanes, 840 polygon-corner height gates,
720 whole-original receiving envelopes, 4,320 receiving signed corner
bounds, 128 same-original signed source adjustments, 1,536 physical
interval triples, 52 closed leaves, 208 common-original corner gates,
624 positive Bernstein lower bounds, 624 direct vector audits and
22 positive outward root records.

All **23 malformed controls** reject, including missing/corrupt prior
pins, missing originals, wrong cutoff, reversed source/receiving roles,
wrong receiving facet count, absent source class, missing/incorrect
original preimages, assigning beta heights to noncircle originals,
missing/outside/reversed source polygon vertices, incorrect signed
adjustments, incomplete coefficient groups, missing quarters or leaves,
duplicate or overlapping leaves, invalid original/facet indices,
false support margins and nonpositive margins. Guards survive Python
optimization. Ancestor guards and all 73 previous input bytes remain
unchanged. No old scalar is invoked outside its proved domain.

The written trust boundary includes the original body/region bridge,
centering and diameter implication, regional disk coercivity, complete
convex clipping, Rodrigues expansion, raw normalization extrema,
independent proper gauges and frames, the whole-original receiving
support envelope and the Bernstein continuum bridge. The finite checker
uses previously published byte-pinned Q(phi), Fraction and positive-root
kernels. It is not a formal proof assistant, and author reuse and direct
vector regressions are not independent verification. The corollary
additionally depends on the historical complete region spectrum and
graph 8487/8436. No floating sample, solver answer, resource failure,
UNKNOWN, or incomplete enumeration is a nonexistence premise.

Primary status references checked live on 2026-10-01: the introduction
of [arXiv:2604.26531](https://arxiv.org/html/2604.26531) retains RID as a
non-Rupert conjecture; [arXiv:2508.18475v2](https://arxiv.org/abs/2508.18475)
constructs the different 90-vertex Noperthedron;
[arXiv:2509.08190](https://arxiv.org/html/2509.08190), Conjecture3.3 and
Tables3/4, records the named Archimedean, Catalan and Johnson unresolved
cases; and [arXiv:2112.13754](https://arxiv.org/html/2112.13754) supplies
the strict projection-containment framework. The bounded live search
found no RID resolution; it is not an exhaustive priority search.

Complementary graph 8462's deltoidal one-third collar and graph 8477's
four closed J77 sectors were read as geometric context. Their area
correlation and domain-transfer mechanisms concern different bodies;
no constants, original contacts or review verdicts are imported here.
