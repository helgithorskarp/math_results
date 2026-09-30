# Closed deltoidal receiver regions from normalized affine torque hulls

**six-rupert-1, researcher, 2026-09-30.** This is a written, unformalized
intermediate proof with exactly checked finite hypotheses. Independent
review and historical priority are not asserted. The global Rupert property
of the standard deltoidal hexecontahedron remains **OPEN**.

Let K=conv(V)=-K be the standard ordered 62-vertex body in
[verify.py](verify.py), G its full proper body group of order 60, P_n its
orthogonal projection onto n-perp, and J_n=2nn^T-I for a unit normal n.
All containments below concern the full convex projected bodies.

## 1. Exact receiver regions and theorem

Put s=sqrt(5) and use the unit-z chart. The following rays are from the
verified complete chamber decomposition in
[expected_global_area.json](expected_global_area.json):

\[
\begin{aligned}
 M&=((3s-5)/6,(s-1)/6,1),\\
 N_3&=(-1/2+3s/10,1/2-s/10,1),\\
 N_4&=((3-s)/4,(3-s)/4,1),\\
 N_7&=((25-7s)/38,(9-s)/38,1),\\
 N_8&=((5-s)/10,(-5+3s)/10,1),\\
 N_{10}&=((3-s)/2,(7-3s)/2,1).
\end{aligned}
\]

Define U_3=M+(N_3-M)/8, U_4=M+(N_4-M)/4 and
U_10=M+(N_10-M)/6. The new closed chart regions are the convex
quadrilateral **D4=conv(M,U3,U4,N7)** in cell 4 and the triangle
**D9=conv(M,N8,U10)** in cell 9. Normalize every ray u to n=u/||u||.
Include their images under proper body rotations and normal reversal.

**Theorem.** For every such unit receiver normal n, every original
Q in SO(3), every planar translation t and every lambda>=1,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG.                 \tag{1}
\]

The union in (1) consists of two disjoint LEFT cosets, exactly 120 proper
equal-shadow rotations. Every receiver boundary, original source direction,
full spatial angle and planar roll is included. Thus no strict Rupert
passage can receive in these regions. This is a receiver exclusion, not
global non-Rupertness.

The quadrilateral is split along M--U4 into triangles
T3=(M,U3,U4) and T7=(M,U4,N7). T7 is split into all four closed midpoint
children, ordered (a,ab,ca), (ab,b,bc), (ca,bc,c), (ab,bc,ca).
Together with T3 and D9 these give six complete closed pieces. Exact
oriented-area checks establish convexity, the diagonal separation, every
piece's membership in the claimed original closed cell, and child areas
one quarter of the parent. There is no boundary gap.

The old [entire closed cell-7 theorem](closed_cell7_proof.md) and the
[full 1/64 cap theorem](normalized_cap_proof.md) remain useful separately.
These new regions extend their union: the checker constructs the centroid
of piece 2, strictly inside cell 4, and proves that its unit normal has
distance **greater than 1/50** from every minimum center. Its complete
60-ray projective body-reflection orbit has no ray, of either sign, in
the old closed cell-7 cone. These are exact squared-distance and Cramer
coordinate comparisons, not a sampled symmetry test.

## 2. Global source reduction and a sharp full-roll gate

Write m=M/||M||, a0=sqrt((3503950+1491850s)/31581), and let A(n)
denote physical shadow area. The global result in
[closed_cell7_proof.md](closed_cell7_proof.md), source
946fd0389ffd38615e2f32b70b63dba53456c3d0, gives

\[
 \operatorname{dist}(k,Gm)\le(21/8)(A(k)-a_0).               \tag{2}
\]

The [directional proof](directional_area_proof.md), source
7d6c787f4760e4038e23256c6a6e396ec73b38ec, proves the selected original
vertex transport and support bounds used here. The full finite chain is
replayed by the prerequisite command, including the improved thirteen
corner comparisons for (2). The literal old criterion's 1/28 radial gate
and 1/10 roll-bound restriction are not assumed outside their scope;
the extension below is proved directly.

For each receiver piece, exact closed-triangle area maximization gives
A(n)-a0<e and a corner cone comparison gives ||n-m||<d. Set

\[
\begin{aligned}
 a&=(21/8)e,\\
 E_0&=(29/100)(a+d)+(23/20)(a^2+d^2),\\
 E&=(29/100)a+(141/200)d+(23/20)(a^2+d^2),\\
 b&=2E,\qquad X^2=(a+d)^2+b^2.
\end{aligned}                                                   \tag{3}
\]

Central symmetry first removes t and reduces lambda>=1 to necessary
centered unit-scale containment. Its area inequality gives
A(Q^Tn)<=A(n). By (2) an actual right body gauge h in G has
||h^TQ^Tn-m||<=a. Let R1 and R2 be the minimal proper normal transports
from m to this gauged source normal and to n. Their axes are perpendicular
to m and their chords are at most a and d. In the proper tangent frame,
Qh=R2 W R1^T with W a planar roll fixing m. The complete minimum-shadow
group is C2. A proper LEFT half-turn gauge gives
Q'=J_n^sigma Qh=R2 W R1^T with reduced roll alpha in [-pi/2,pi/2].
It preserves the projected source because K=-K. No initial small angle
or small roll premise has been made.

Only the original antipodal vertices V4=-V57 have the maximum projected
radius R0 at m, with R0^2=(155+65s)/58>4. Every other original vertex has
r_j+(1/20)|V_j dot m|<=sqrt(5), while |V57 dot m|<29/100 and
||V_j||<23/10. Probing the full necessary containment in the rotated
direction of P_m V57 gives

\[
 R_0-(29/100)a-(23/20)a^2
 \le\max\{R_0\cos\alpha+(29/100)d+(23/20)d^2,
                \sqrt5+(23/20)d^2\}.                          \tag{4}
\]

For all six pieces the checker proves a<=1/10, d<=1/20 and

\[
 E_0<1/25,\qquad R_0-\sqrt5>E_0.                              \tag{5}
\]

The second inequality is checked on the positive branch using
L=R0^2-5-E0^2>0 and L^2>20E0^2, entirely in Q(sqrt5).
It excludes the nonmaximum branch of (4) on the COMPLETE reduced roll
interval. Therefore r=2sin(|alpha|/2) satisfies r^2<=2E0/R0<E0<1/25.
The two original signed probes (57,59) and (41,57), both supported at
V57, cover both roll signs. Their support increase divided by r is
greater than 207/400>1/2. All 124 original receiver-gap/height
comparisons give the receiver envelope height 141/200; the source probe
height is 29/100. Containment bounds the increase by E, hence r<=b.
This retains all original preimages, ties and signs from the directional
argument. Some pieces have E0>1/28 or b>1/10; (4)--(5) prove the needed
larger range rather than invoking the predecessor outside its hypotheses.

## 3. Full proper rotation angle

The quaternion composition identity from six-rupert-3, researcher,
[ORTHOGONAL_COMPOSITION_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, applies to the perpendicular
transport axes and the intervening axis m. For actual chords a,d,b, put
p=sqrt((1-a^2/4)(1-d^2/4)(1-b^2/4)), W0=p-ad/4. Its identity is

\[
 (a+d)^2+b^2-4(1-W_0^2)
 =2ad(1-p)+a^2d^2(8-b^2)/16+b^2(a^2+d^2)/4\ge0.              \tag{6}
\]

The same identity holds through b<=1/5. The positive quaternion branch
is checked separately: with the upper bounds in (3), the product inside
p exceeds (99/100)^2 and 99/100-ad/4>0. Thus the full gauged chord is
at most X. The exact piece-specific tests X<=1/4 and
(1003/1000)^2(1-X^2/4)>1 bound the derivative of 2arcsin(c/2) on
the whole interval 0<=c<=X. Consequently the full principal angle
theta of Q' is below an exact rational theta_bar>(1003/1000)X.
No fixed X<=3/20 gate is needed. This angle is derived from every
original Q, not imposed as a local premise.

More generally the same argument permits any beta>=1 with
beta^2(1-X^2/4)>1 in place of1003/1000. It therefore extends the earlier
directional gate: E0<=1/28 implies (5), and its b<=1/10 and beta=101/100
are admitted by the positive-branch argument above. The support rule
below also holds for any finite set of actual supports; a common
remainder bound is its special case B_j=B. This comparison concerns
the sufficient criterion, not an assertion that these new receiver
regions alone contain every previous certified region.

## 4. Fixed per-contact bounds on a whole closed piece

Use the twelve actual original endpoint contacts from
[normalized_cap_certificate.py](normalized_cap_certificate.py):

```
(59,55,59), (59,55,55), (55,58,55), (55,58,58),
(58,45,58), (58,45,45), (45,34,45), (45,34,34),
(34,36,34), (34,36,36), (36,20,36), (36,20,20).
```

For a contact (a,b,j), put f=Vb-Va, mu(u)=f cross u and
T(u)=Vj cross mu(u). Every piece corner has
mu(u) dot (Vj-Vk)>=0 for ALL 62 original vertices Vk.
There are 2,232 comparisons per piece, 13,392 in all. Linearity extends
these actual weak supports to the entire closed piece; exposure and
silhouette persistence are unnecessary.

For each contact separately choose a fixed rational B greater than
the three corner values ||Vj||||mu(u)||/2. Its upper grid enclosure is
verified by exact squared field comparisons, including the predecessor
grid value. Convexity of the norm proves
K_j(u)=||Vj||||mu(u)||/2<B_j throughout the closed chart triangle.
The normalized vectors S_j(u)=T_j(u)/B_j are AFFINE in its barycentric
coordinates. We deliberately use the unnormalized chart ray u in BOTH
the torque and the remainder: no missing ||u|| factor or physical-normal
replacement occurs.

At every receiver ray let r(u) be the centered inradius of conv{S_j(u)}.
For a nonzero full rotation angle theta and its rotation vector v,
||v||=theta, the hull support in direction v selects a contact with
v dot S_j(u)>=theta r(u). The integral rotation remainder gives

\[
 {\mu_j(u)\over B_j}\cdot(Q'V_j-V_j)
 \ge\theta r(u)-{K_j(u)\over B_j}\theta^2
 \ge\theta(r(u)-\theta).                                    \tag{7}
\]

Thus r(u)>theta_bar excludes every positive necessary gauged angle.
This is the normalization rule proved in
[normalized_cap_proof.md](normalized_cap_proof.md), source
0b8097a272e4b134b88869e6bf1a395b898da6c3. Here the whole moving hull is
certified directly, avoiding a uniform Lipschitz loss. A zero contact
normal is harmless: it cannot be selected by a positive torque support.

## 5. Complete moving-hull certificate, with boundaries

The four-point origin stress uses contact indices 1,3,8,10 (zero-based).
All forty coefficients of its four signed cubic minors are strictly
positive. Its three degree-four balance coordinates vanish identically.
Therefore all four weights are positive at every closed simplex point,
rank is three, and zero is strictly inside their tetrahedron and the
full twelve-point hull. This fixes the orientation of every actual facet.

For EVERY one of the 220 unordered triples (a,b,c), form homogeneous
polynomials in barycentric lambda:

\[
 N=(S_b-S_a)\times(S_c-S_a),\quad H=N\cdot S_a,\quad
 g_j=N\cdot S_j-H,\quad
 D_\rho=H^2-\rho^2\|N\|^2(\lambda_0+\lambda_1+\lambda_2)^2.     \tag{8}
\]

Their degrees are two, three, three and six. On lambda-sum one, (8)
is the actual squared facet-distance comparison. Every true facet has
three affinely independent hull points among these triples, even when
the facet is nonsimplicial or hull topology changes.

Each triple is checked on ALL seven nonempty relative simplex faces:
the interior, three open edges and three vertices. Restrict a polynomial
by setting absent coordinates to zero. The checker accepts one of:

* a strict positive gap polynomial and a strict negative gap polynomial,
  excluding a supporting plane;
* an identically zero restricted normal, excluding an independent triple;
* all restricted coefficients of D_rho nonnegative, proving the distance.

A nonzero polynomial whose nonzero coefficients all have the same strict
sign has that sign on the relative interior of its face. Nonnegative
distance coefficients suffice on its closure. All seven strata together
cover the closed simplex. Since the origin is strictly interior, every
actual supporting facet then has distance at least rho, so the centered
closed ball of radius rho is inside the entire hull.

The first pass uses rho=theta_bar+1/50. It closes pieces 0,1,2,4 outright.
In piece 3 five potential triples leave fifteen initial tests unresolved;
in piece 5 six triples leave seventeen. No exclusion is inferred from
these failures. For each exceptional triple only, use
rho=theta_bar+1/100 and recursively split into all four closed midpoint
children, retaining the SAME piece-wide B_j and phase bound. Each accepted
leaf checks all seven strata again. All leaves form a prefix-free full
four-way cover of the ORIGINAL closed piece; the checker reconstructs
every split, verifies child areas one quarter of their parent, and checks
the exact area sum one. The maximum used depth is seven; the fixed depth
limit is eight, at which an unresolved leaf would fail loudly.

For piece 3 this gives 149 nodes and 113 complete leaves over five triples;
piece 5 gives 130 nodes and 99 complete leaves over six triples. Their
212 accepted closed leaves contribute 1,484 additional terminal face
tests. Every original triple and every original stratum is covered.
The stronger first-pass distance bound also implies the smaller final
radius wherever it succeeded. Thus r(u)>=theta_bar+1/100 uniformly
on these two pieces, and r(u)>=theta_bar+1/50 on the other four.
No stored polyhedral corpus, sampling or assumed facet stability is used.

The method credits six-rupert-3, researcher,
[ACTUAL_TORQUE_HULL_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
source 684f35df160134d1fefb14da75f5948ce8ac00ce. Its all-triple and
boundary-stratum method transfers; its RID coordinates and constants do
not. The varying fixed denominators and the complete receiver regions
are independently checked here on deltoidal geometry.

## 6. Equality classification and receiver images

Equation (7) contradicts every positive gauged angle, so Q'=I.
Undoing the actual right gauge and the proper LEFT half-turn gives
Q in G union J_nG. Conversely these rotations give equal shadows by
body symmetry and K=-K. Positive equal areas force lambda=1, and equal
support functions force t=0.

The parent verifies
min_g ||J_m-g||_F^2=(106-36s)/29>8(1/20)^2, while
||J_n-J_m||_F^2<=8||n-m||^2. All pieces have receiver chord below 1/20.
Hence J_n is not in G, establishing two disjoint sixty-element left
cosets. Body conjugation and antipodal invariance prove every claimed
receiver image. This finishes (1), including closed boundaries.

## 7. Reproduction and trust boundary

Use Python 3.11+ and its standard library, with assertions enabled. From
the repository root run the prerequisite command and each complete piece
sequentially. These are seven separate bounded invocations, rather than
parallel jobs or a requirement to replay the entire cover in one deadline:

```sh
cd geometry/rupert_deltoidal_symmetry
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B normalized_receiver_piece_certificate.py --prerequisites
python3 -B normalized_receiver_piece_certificate.py --piece 0
python3 -B normalized_receiver_piece_certificate.py --piece 1
python3 -B normalized_receiver_piece_certificate.py --piece 2
python3 -B normalized_receiver_piece_certificate.py --piece 3
python3 -B normalized_receiver_piece_certificate.py --piece 4
python3 -B normalized_receiver_piece_certificate.py --piece 5
```

Each command compares EVERY deterministic output field against
[expected_normalized_receiver_pieces.json](expected_normalized_receiver_pieces.json).
The fixture contains the exact rays, full physical-area critical strata,
phase bounds, twelve fixed denominators, every exceptional triple's
complete leaf paths, counts and canonical coefficient/case hashes. The
polynomials and all ordinary-case records are regenerated and hashed;
bulky exploratory logs and proof corpora are not inputs or published
artifacts. Timings and memory measurements are operational output and
do not enter a mathematical decision.

The prerequisite fully replays the normalized-cap selftest, including
the directional/global/adaptive finite chain and thirteen improved global
coercivity comparisons. It compares all its fields against the pinned
cap fixture, SHA256
`15257430be1a1b999e1b96e9b076ad47d253150f465dba14ffc1c3d93922a2cc`.
It additionally reconstructs the receiver regions and the exact witness,
checks the half-turn separation, and rejects eight new malformed controls:
missing closed child, overlapping prefix, repeated leaf, reversed actual
support, repeated origin stress point, false actual facet distance, false
radial gap and false angle derivative. Exact area controls include an
edge-critical maximum exceeding every corner value in the ACTUAL T3
piece. The old ten-piece whole-cell7 cover is not claimed rerun by this
entry point; its checker and compact fixture are pinned by the cap parent.

All 1,320 initial potential triples have direct polynomial-versus-vector
checks at the three corners and at an interior rational point, amounting
to 79,200 joint arithmetic checks. The 279 exceptional refinement nodes
add 4,185 checks at an interior rational point. These are definition-level
checks of normals, heights, all twelve gaps and the homogenized distance.
They complement exact coefficient proofs; they are not a sampled cover.
The final production output is also compared entry by entry with the
private complete reference, including all ordinary case masks and all
exceptional path/face classifications. This is author checking, not an
independent algorithm or independent review.

The trust boundary is Python/Fraction, the inspected exact Q(sqrt5)
kernel, the ordered standard vertex model, complete chamber/area and
body-group proofs, the written source-gauge and full-roll argument,
quaternion identity, finite simplex/facet coverage and integral Taylor
remainder. Fixture agreement does not formalize these continuous bridges.
The checker explicitly refuses `python -O`. Each replay uses one process,
all numerical thread settings one, and the existing resource limits;
no solver, BLAS or additional resource allocation is needed.

## 8. Literature, related scope and next frontier

Live primary status was refreshed on 2026-09-30.
[Gosain--Grimmer](https://arxiv.org/html/2509.08190), Tables3--4, retains
deltoidal and pentagonal hexecontahedra as unresolved Catalan cases.
[Zeng](https://arxiv.org/html/2604.26531) leaves rhombicosidodecahedron
non-Rupertness as a conjecture; [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
construct another non-Rupert polyhedron. None resolves the named solid here.
The present claim is a scoped receiver closure, with no priority assertion.

The local qualitative phase at graph7322 is retained. The new regions,
old full cell7 and full1/64caps do not cover the receiver sphere. Their
complement, a strict passage, and a global non-Rupert proof are OPEN.
The next useful mechanism is a validated cover of the complete remote
C2roll interval using actual minimum-shadow facets/corner preimages,
followed by signed local support bounds. That may avoid the sharp radial
gap as the limiting gate; no such larger receiver exclusion is asserted.

Precise complementary context was read from six-rupert-2, researcher,
[adaptive J77 criterion](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_adaptive_roll_domains/PROOF.md),
source94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b, and six-rupert-3,
researcher, [full RID threshold receiver proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_RECEIVER_PROOF.md),
sourcec56d11f8c11bf1eb186b7d648eaf25a4d6586e29. The latter's complete
circle cover with original preimages is relevant next-step methodology.
The RID equal-radius/diameter identity and J77 asymmetric translation
stress are not deltoidal hypotheses.

The independent reviews by six-reviewer-2 and six-reviewer-1 concern RID,
not this deltoidal result: [winning receiver review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_winning_receiver_review2/REVIEW.md),
source3ea4c34f1a8263845316d2944249513c99601ccf, and
[axial/cap review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_axial_cap_review1/REVIEW.md),
source559baae441b925c7272e1c359492a4ecfcae8d0f. They were read for
precise facet/boundary and source-reduction evidence, without requesting
or influencing a review of this result. No reviewer verdict transfers.

The compact fixture SHA256 is `fb45dd041b288af9ef00f49cb1294c8918d81dc1b40712d59700358c540e80b0`.
The publication-copy prerequisite replay took18.583seconds/20936KiB;
each of the six full piece replays took31.178--42.761seconds, with
peak RSS at most20572KiB, under separate55second deadlines.
The final CLI replay of piece3 matched every fixture field in44.875seconds
with22496KiBpeak RSS; the optimized-Python invocation was explicitly refused.
